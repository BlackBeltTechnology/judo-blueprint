---
id: "dao-fluent-query-filter"
title: "Fluent DAO Query with Type-Safe Filters"
domain: "backend"
category: "data-access"
score: 79.5
usage_count: 10
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - alba
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

The standard JUDO data access pattern using generated SDK DAOs with fluent, chainable query builders and type-safe filter classes. Filters are AND-combined when chained. Supports `selectOne()` (Optional), `selectList()` (List), and `count()` (long) terminal operations.

## Structure

Filter types from `hu.blackbelt.judo.sdk.query`:
- `StringFilter.equalTo(value)` -- exact string match
- `BooleanFilter.isTrue()` / `isFalse()` -- boolean filtering
- `EnumerationFilter.equalTo(enumValue)` -- enum match
- `NumberFilter.equalTo(number)` -- numeric match
- `TimestampFilter.greaterOrEqualThan(threshold)` -- timestamp comparison
- `DateFilter.greaterOrEqualThan(date)` / `lessOrEqualThan(date)` -- date range
- `TimeFilter.lessThan(time)` / `greaterThan(time)` -- time comparison

```java
// Multi-filter query returning Optional
Optional<User> user = userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .filterByCode(StringFilter.equalTo(code))
    .filterByActive(BooleanFilter.isTrue())
    .selectOne();

// Relation-based query with enum filter
List<Test> tests = contestDao.queryTests(contest)
    .filterByStatus(EnumerationFilter.equalTo(TestStatus.STARTED))
    .filterByPlayerEmail(StringFilter.equalTo(email))
    .selectList();

// Count query
long correctCount = testDao.queryPrompts(_this)
    .filterByCorrect(BooleanFilter.isTrue())
    .count();
```

## Examples

### Trivia
Uses all four filter types extensively: `StringFilter` for email/code lookups, `BooleanFilter.isTrue()` for active users and correct answers, `EnumerationFilter` for TestStatus/QuestionStatus filtering, `NumberFilter.equalTo()` for prompt number matching. 15+ distinct query patterns across 8 operations.

### RackInspect
Adds `StringFilter.notEqualTo()`, `DateFilter.equalTo()`, and `maskedBy()` for field projection. Example: `currencyDao.query().filterByCode(StringFilter.equalTo("HUF")).selectOne()`. Also uses paginated queries with `selectList(limit, lastItem, isReverse)` and `orderBy(Attribute, Order.ASC)`.

### ALBA
Uses `StringFilter.equalTo()` for user lookup by email, `EnumerationFilter.equalTo(ProductState.APPROVED)` for finding approved versions across a container. Also uses `findAllById()` for bulk-fetching related entities (audiences, curriculums, result types) by extracted UUIDs from input.

### mlszksz-platform
Extensive use of `TimestampFilter.greaterOrEqualThan()` for active-user counting (lastLogin within 30 days) and date-filtered queries. Relation queries via `organizationDao.queryUsers(orgId)` for per-org user counts. `EnumerationFilter.equalTo(UserStatus.ACTIVE)` and `EnumerationFilter.equalTo(PostStatus.PUBLISHED)` for status filtering. Count queries for statistics aggregation.

### Ubives
`StringFilter.equalTo()` used extensively for username lookups: `accountDao.query().filterByUserName(StringFilter.equalTo("admin")).maskedBy(mask).count()` for existence checks, `.selectOne()` for user retrieval. `count() > 0` pattern for duplicate detection before creation (organizations, applications). All queries consistently use `maskedBy()` for field projection.

### ParkHere
Extensive use of `DateFilter` for date range queries (reservation lookups), `TimeFilter` for time overlap detection (parking slot availability), `EnumerationFilter` for status/type filtering (ACTIVE reservations, non-GUEST types), and `BooleanFilter` for archived/favorite filtering. Complex availability queries combine 4+ filters: `.filterByDate(DateFilter.equalTo(date)).filterByReservationStatus(EnumerationFilter.equalTo(ACTIVE)).filterByStartTime(TimeFilter.lessThan(endTime)).filterByEndTime(TimeFilter.greaterThan(startTime))`.

### Indamedia-AdTrack
Uses `StringFilter.equalTo()` for user lookup by email in interceptor and ActorService. `EnumerationFilter.equalTo(Status.ONGOING)` for filtering active campaigns in scheduled jobs. `DateFilter.lessOrEqualThan(today)` and `DateFilter.greaterOrEqualThan(today)` for campaign date range checks. Relation queries: `trackedCampaignTransferDao.queryAggregatedCampaign()` for parent navigation, `aggregatedCampaignDao.queryTrackedCampaigns()` for children.

### judo-partner
Heavy use of `StringFilter.equalTo()` for tax identifier, email, country code, and alpha2/alpha3 lookups. `BooleanFilter.isTrue()`/`isFalse()` for primary flag and archive filtering. Paginated batch processing with `selectList(i, i += 100)` for bulk validate/migrate operations. Combined mask + filter: `partnerDao.query().maskedBy(PartnerMask.partnerMask().withNormalizedName().withIsArchived()).filterByNormalizedName(...)`.

### workflow-poc
Uses `StringFilter.equalTo()` for name-based lookups across workflow entities: `contextTypeDao.query().filterByName(StringFilter.equalTo(input.getContextType())).selectOne()`, `tokenDao.query().filterByTokenID(StringFilter.equalTo(input.getTokenID())).selectOne()`. Multi-filter with ordering: `eventDao.query().filterByCorrelationID(StringFilter.equalTo(correlationID)).filterByProcessed(BooleanFilter.isFalse()).orderBy(EventAttribute.SEQUENCE).selectOne()`. `EnumerationFilter.equalTo(LogEntryType.COMPLETION)` for log queries. `BooleanFilter.isTrue()/isFalse()` for generic context type and event-less transition filtering.

### ReserveApp
`PartnerActorInterceptor` uses `userDao.query().filterByEmail(StringFilter.equalTo(email)).selectOne().stream().findAny().orElse(null)` to find the current user by email. Also uses relation query `userDao.queryPartner(user, PartnerMask.partnerMask())` to navigate from User to Partner with mask projection. Minimal but demonstrates both entity query and relation navigation patterns.

## Trade-offs

- Pros: Type-safe, compile-time checked, fluent API, supports all common filter types
- Cons: Filters are AND-only when chained (OR requires `filterBy(String)` with JQL), no built-in pagination in trivia usage, no mask usage observed in trivia
- Alternative: Raw JQL expressions via `filterBy(String)` for OR logic or complex conditions

## Related Patterns

- builder-pattern-entity-creation
- relation-based-entity-creation
- mask-field-projection
