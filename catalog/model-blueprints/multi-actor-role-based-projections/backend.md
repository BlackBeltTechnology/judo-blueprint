## Overview

The multi-actor role-based projections pattern manifests in backend code through role-based authorization checks in custom operations, an `ActorService` that resolves the current user's role from JUDO security context, and interceptors that compute derived fields differently per actor context.

## Implementation Pattern

- `ActorService` (OSGi `@Component`) provides `getCurrentUser()` which resolves the logged-in user's email from `VariableResolver.resolve("ACTOR", "email")` and queries the User entity
- Custom operations use `actorService.getCurrentUser().getRole()` to enforce role-based authorization: PLATFORM_ADMIN can manage all organizations, COMPANY_ADMIN only their own, COMPANY_READER is read-only
- The `LogAuthenticationInterceptor` (implementing `AuthenticationInterceptor`) runs on every `_principal` operation to update `lastLogin` and log authentication for all actors
- The `StatisticsActiveUsersInterceptor` (implementing `OperationCallInterceptor`) intercepts Statistics-related operations on the AdminDashboard to compute derived fields (activeUsers, recentNews, etc.) that cannot be expressed in JUEL
- The `ProfilePanelKeycloakSyncInterceptor` runs for CompanyReader actor operations to sync profile data with Keycloak
- Operations in the `companyadmin` package validate organization scope: the current user's organization must match the target entity's organization
- Operations in the `feed` package are consumer-facing and typically do not require role checks (all authenticated users can view feed)
- In simpler projects, interceptors use `VariableResolver` to resolve the current actor's identity and auto-assign role-specific relations on entity creation (e.g., auto-linking a partner to a newly created reservation)

## Examples

### mlszksz-platform
- Key files: `common/services/ActorService.java`, `common/services/impl/ActorServiceImpl.java`, `interceptors/StatisticsActiveUsersInterceptor.java`, `interceptors/LogAuthenticationInterceptor.java`, `interceptors/ProfilePanelKeycloakSyncInterceptor.java`
- Pattern: `ActorService.getCurrentUser()` resolves user from JUDO security context; custom operations check `user.getRole()` for authorization; interceptors compute derived fields per-actor
- Notable: 6 service sub-packages (admin, companyadmin, companyreader, feed, registration, technical) each have separate custom operation sets; authorization is enforced in service methods, not in the custom operation classes

### reserve-app
- Key files: `interceptors/services/PartnerActorInterceptor.java`, `interceptors/InterceptorOperationLogger.java`
- Pattern: `PartnerActorInterceptor` intercepts the PartnerActor's `_createInstanceReservationsForPartner` operation to auto-assign the logged-in partner's association to newly created FreightReservation entities; resolves the current user via `VariableResolver.resolve("ACTOR", "email")` and queries `UserDao` + `PartnerMask`
- Notable: Lighter-weight approach than mlszksz-platform -- no shared `ActorService` abstraction; instead, each actor-specific interceptor directly injects `UserDao` and `FreightReservationDao` via OSGi `@Reference` to perform role-specific post-creation wiring. The `InterceptorOperationLogger` provides cross-cutting operation logging for all actors.
