## Overview

Implements an `AuthenticationInterceptor` that hooks into the JUDO authentication pipeline to perform side effects on login -- updating timestamps, creating audit log entries, or auto-provisioning User entities from JWT claims. Intercepts the `_principal` resolution operation.

## Implementation Pattern

**Interceptor structure:**
- `@Component(property = { "judo.model.name=<ModelName>" })` implementing `AuthenticationInterceptor` (not `OperationCallInterceptor`)
- `isSuitableForOperation()` returns `true` for all operations (the filtering happens inside `authenticate()`)
- `authenticate()` checks if `operationFQName.endsWith("#_principal")` to only trigger on principal resolution (login)

**Common authentication behaviors:**
1. **Login tracking:** Extract `email` from JWT `attributes`, query User by email, update `lastLogin` timestamp
2. **Audit logging:** Log `USER_LOGIN` event via an `AuditLogService` with the user's entity ID and email
3. **Auto-provisioning:** If the user does not exist in the local database, create a new User entity from JWT claims (`email`, `given_name`, `family_name`), optionally assigning roles based on configuration (e.g., admin email list)

**Key design decisions:**
- Uses `AuthenticationInterceptor` (not `OperationCallInterceptor`) because login tracking must happen during authentication, before the operation dispatches
- The `_principal` filter ensures the interceptor only fires once per request (on session establishment), not on every operation call
- Failures are caught and logged (never propagated) to avoid blocking the user's login

## Examples

### mlszksz-platform
- Key files: `interceptors/LogAuthenticationInterceptor.java`
- Pattern: Implements `AuthenticationInterceptor`, filters for `#_principal` operations in `authenticate()`. Queries User by email, updates `lastLogin` timestamp, and logs `USER_LOGIN` via `AuditLogService`.
- Notable: Uses `UserMask.userMask().withEmail()` for minimal data projection. Wraps all logic in try-catch to prevent login failures from authentication side effects.
- DI wiring: `@Reference UserDao`, `@Reference AuditLogService`

### indamedia-adtrack
- Key files: `interceptors/LogAuthenticationInterceptor.java`
- Pattern: Implements `AuthenticationInterceptor`, filters for `#_principal` operations. Extracts `email`, `given_name`, `family_name` from JWT attributes. If no User exists with that email, auto-provisions one via `userDao.create(UserForCreate)` with name and admin flag.
- Notable: Auto-provisioning variant -- creates users on first login rather than just tracking existing users. Admin role assignment is config-driven: `@Activate` reads an `admins` comma-separated email list from component properties. Uses `synchronized (createLock)` to prevent duplicate user creation under concurrent login. Name assembly logic handles missing first/last name fields gracefully.
- DI wiring: `@Reference UserDao`. No `AuditLogService` in this variant -- focused purely on user provisioning.
