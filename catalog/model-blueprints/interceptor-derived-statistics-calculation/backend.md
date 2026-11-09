## Overview

Uses `OperationCallInterceptor.postCall()` to compute derived statistics fields that require date arithmetic (e.g., "active users in last 30 days"), which cannot be expressed in JUEL. The interceptor runs after list/refresh operations on statistics transfer objects and injects computed values into the response payload.

## Implementation Pattern

**Interceptor structure:**
- `@Component(property = { "judo.model.name=<ModelName>" })` implementing `OperationCallInterceptor`
- `getOperations()` returns the specific `_list*` and `_refreshInstance*` operations to intercept (resolved via `AsmUtils.resolveOperation()`)
- `postCall()` receives the return payload, executes DAO count queries, and puts computed values into the `Payload` map

**Calculation pattern:**
1. Define a threshold: `LocalDateTime.now(Clock.systemUTC()).minusDays(ACTIVE_DAYS_THRESHOLD)`
2. Query DAOs with combined filters: `dao.query().filterByStatus(equalTo(ACTIVE)).filterByLastLogin(greaterOrEqualThan(threshold)).count()`
3. Put the result into the payload: `payload.put("activeUsers", (int) count)`
4. Handle both single-payload (`Payload`) and collection-payload (`Collection<Payload>`) return types

**When to use this pattern:**
- Model-level derived attributes need date arithmetic that JUEL cannot express
- Statistics/dashboard fields need counts with relative date filters ("last N days")
- Per-entity statistics need navigated count queries (e.g., active users per organization via `organizationDao.queryUsers(orgId).filterByLastLogin(...)`)

**Alternatives:**
- If the expression can be written in JUEL, prefer a model-level derived attribute
- If the calculation is expensive and does not need real-time accuracy, consider a scheduled job that pre-computes and stores the values

## Examples

### mlszksz-platform
- Key files: `interceptors/StatisticsActiveUsersInterceptor.java`
- Pattern: Intercepts `_listStatistics`, `_refreshInstanceStatistics`, `_listOrganizationStatistics`, and `_refreshInstanceOrganizationStatistic` operations. In `postCall()`, queries `UserDao`, `NewsDao`, `OfferDao`, `RequestDao`, `AnnouncementDao` with `TimestampFilter.greaterOrEqualThan(now - 30 days)` and puts computed counts (`activeUsers`, `recentNews`, `recentOffers`, `recentRequests`, `recentAnnouncements`) into the response payload.
- Notable: For per-organization statistics, extracts `__identifier` from the payload and uses `organizationDao.queryUsers(orgId)` with the timestamp filter. Handles both `Collection<Payload>` and single `Payload` return types. Uses `Clock.systemUTC()` for testability.
- DI wiring: `@Reference` to `UserDao`, `OrganizationDao`, `NewsDao`, `OfferDao`, `RequestDao`, `AnnouncementDao` -- all generated SDK DAOs
