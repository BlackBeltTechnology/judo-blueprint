---
id: "actor-resolution-variable-resolver"
title: "Actor Resolution via VariableResolver Pattern"
domain: "backend"
category: "auth"
score: 147.7
usage_count: 9
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - alba
  - mlszksz-platform
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
  - reserve-app
  - doors-model
---
## Description

A standard pattern for resolving the current authenticated user in custom operations. The `VariableResolver` service is injected via `@Reference` and used to extract the actor's email from the security context. The email is then used to query the user entity from the database. This pattern appears as a boilerplate block at the start of virtually every custom operation, providing the "current user" context for authorization checks, ownership assignment, and audit trail recording.

## Structure

```java
@Reference VariableResolver variableResolver;
@Reference UserDao userDao;

// Resolve current user (appears at the start of every operation)
User user = userDao.query()
    .filterByEmail(StringFilter.equalTo(
        variableResolver.resolve(String.class, "ACTOR", "email")
    ))
    .selectOne()
    .stream()
    .findAny()
    .orElse(null);
```

Key elements:
- `VariableResolver.resolve(String.class, "ACTOR", "email")` extracts email from security context
- The email is used with `StringFilter.equalTo()` to find the user entity
- `.selectOne().stream().findAny().orElse(null)` handles the case where user might not exist
- This block is copy-pasted across ALL custom operations that need the current user

## Examples

### ALBA
All 9 custom operations use identical actor resolution code. The resolved user is used for: product ownership (`withAuthor(user)`), event attribution (`withPerformedBy(user)`), task creation (`withCreatedBy(user)`), impersonation tracking (`withImpersonatingAuthor(user)`), and role-based validation (`user.getRole().orElse(UserRole.GUEST)`). The `LogAuthenticationInterceptor` ensures the user entity exists before operations run.

### mlszksz-platform
Encapsulated in a dedicated `ActorServiceImpl` that wraps the VariableResolver + UserDao lookup into a reusable `getCurrentUser()` method. All operations inject `ActorService` instead of repeating the boilerplate. Throws `BusinessErrorException("USER_NOT_FOUND")` if user not found. Used for authorization, audit logging (auto-resolves user+organization), and as author for created content.

### judo-demo-miniworkflow
Actor resolution via model script expression: `User!filter(u | u.email == types::Email!getVariable('ACTOR', 'email'))!any()`. Used in all state transition operations to identify who performed Accept, Reject, Close, or RequestReview. The resolved user is stored on each `DocumentHistoryEntry` for audit. Also used in `CreateDocument` to assign the document owner.

### Ubives
Encapsulated in a `Variables` wrapper class that injects `VariableResolver` with target filter `(judo.model.name=Ubives)`. Provides `getActorUserName()`, `getActorEmailName()`, and `getCurrentOrganizationId()`. Services (AccountService, OrganizationService) inject `Variables` to resolve the current authenticated account for organization ownership and leave operations.

### ParkHere
Encapsulated in `ActorServiceImpl` which wraps VariableResolver + UserDao lookup into `getCurrentUser()` and `validateCurrentUserHasPermissionTo(user, message)`. Permission check allows same-user or admin access. All custom operations inject `ActorService` for user context. Used for: permission validation, audit trail (createdBy/modifiedBy), reservation ownership, and admin-only feature gating (exclusive parking slots).

### Indamedia-AdTrack
Encapsulated in `ActorServiceImpl` which wraps VariableResolver + UserDao lookup into `getCurrentUser()`. Uses `VariableResolver` to resolve `ACTOR.email` from security context, then queries User entity by email. Throws `BusinessErrorException(USER_NOT_FOUND)` with i18n message if user not found. Injected with `ThreadLocalLocaleSupplier` for locale-aware error messages. Used for audit trails throughout the application.

### judo-partner
Used directly in custom operations and interceptors (not encapsulated in a service). `CreatePartnerCustomImplementation` and `DeleteCustomImplementation` both resolve the current user via `variableResolver.resolve(String.class, "ACTOR", "email")` then `userDao.query().filterByEmail(StringFilter.equalTo(email)).selectOne().orElseThrow()` to create `PartnerLog` audit entries. `PartnerInterceptor` uses the same pattern to check `user.getIsPartnerAdmin()` for role-based access control.

### ReserveApp
Used in `PartnerActorInterceptor` to resolve the authenticated partner user's email via `variableResolver.resolve(String.class, "ACTOR", "email")`, then queries User by email and navigates to the associated Partner entity. Demonstrates the pattern in an interceptor context (not a custom operation) for automatic ownership assignment on reservation creation.

### doors-model
Model-level actor resolution using JUDO expression language: `doors::types::Email!getVariable('ACTOR', 'email')`. Used in approval workflow operations to identify the current employee initiating approval, approving, or rejecting stages. Position-based authorization checks match the resolved employee against workflow stage requirements for division and role matching.

## Trade-offs

- Pros: Standard approach across all JUDO projects, decouples security context from business logic, works with any authentication provider (Keycloak, custom)
- Cons: Boilerplate code duplicated across every operation, extra DB query per operation, null result not always handled safely, `.orElse(null)` can lead to NPE
- Alternative: Centralized actor service that caches the resolved user per request, or framework-level actor injection (not currently available)

## Related Patterns

- keycloak-jit-user-provisioning
- custom-operation-osgi-component
- dao-fluent-query-filter
