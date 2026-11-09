## Overview

The User entity lifecycle is managed through a `UserService` OSGi service that handles user creation (with Keycloak provisioning), status transitions (activate/suspend/deactivate), visibility toggling, and user invitation workflows. An `AuthenticationInterceptor` updates the user's `lastLogin` timestamp on every authentication event.

## Implementation Pattern

- `UserServiceImpl` is an OSGi `@Component` injecting `UserDao`, `CompanyUserDao`, `KeycloakUserService`, `OrganizationDao`, `PlatformEmailService`, and `ConfigurationTemplateService`
- `createUser()` creates the User entity with ACTIVE status, the specified UserRole, and organization association, then provisions a Keycloak account via `KeycloakUserService.createUser()` with Hungarian name convention (first word = lastName, rest = firstName)
- Status transitions: `suspend()` validates ACTIVE status and not-last-platform-admin, `activate()` validates SUSPENDED status, `deactivate()` validates not-last-admin-in-organization
- `changeVisibility()` toggles the `isVisible` flag for user profile visibility
- `inviteUser()` creates a `UserInvitationRequest` with hashed token and expiry, sends verification email
- `verifyUserInvitation()` validates the hashed token, checks expiry, transitions from PENDING to VERIFIED
- `LogAuthenticationInterceptor` implements `AuthenticationInterceptor`: on `_principal` operations, resolves user by email, updates `lastLogin` timestamp, and logs `USER_LOGIN` audit entry
- Custom operations: `ActivateCustomImplementation`, `DeactivateCustomImplementation`, `SuspendCustomImplementation`, `ChangeVisibilityCustomImplementation` (companyadmin/companyuser), `CreateUserCustomImplementation`, `InviteUserCustomImplementation` (organizationadminpanel)

## Examples

### mlszksz-platform
- Key files: `common/services/UserService.java`, `common/services/impl/UserServiceImpl.java`, `interceptors/LogAuthenticationInterceptor.java`, `custom/.../companyadmin/companyuser/SuspendCustomImplementation.java`
- Pattern: User creation combines JUDO entity creation + Keycloak provisioning; status transitions enforce state machine rules with last-admin guards; authentication interceptor updates lastLogin + logs audit
- Notable: `validateNotLastPlatformAdmin()` prevents suspending/deactivating the last PLATFORM_ADMIN; `validateNotLastAdmin()` prevents deactivating the last COMPANY_ADMIN in an organization; both count active users by role via `CompanyUserDao` queries
