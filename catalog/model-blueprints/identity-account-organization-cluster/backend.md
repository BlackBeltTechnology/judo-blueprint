## Overview

The Identity-Account-Organization entity cluster is backed by a set of OSGi service layer classes that encapsulate multi-tenant account management, organization access control, and user lifecycle operations. Custom operation classes delegate to these services, and authentication interceptors ensure accounts are auto-provisioned on first login.

## Implementation Pattern

- A **service layer** of OSGi `@Component` classes encapsulates business logic for each entity in the cluster: `AccountService`, `OrganizationService`, `AccessService`, `UserService`
- Each service injects the relevant entity DAOs (`AccountEntityDao`, `OrganizationEntityDao`, `OrganizationAccessEntityDao`, `UserEntityDao`) and peer services via `@Reference`
- A `Variables` service wraps `VariableResolver` (with `target = "(judo.model.name=...)"`) to resolve the current actor's `userName`, `email`, and request-scoped `organization` header
- **Custom operation classes** (OSGi `@Component`) are thin delegates: they extract the entity identifier from `_this.identifier().getIdentifier()`, cast to `UUID`, and call the corresponding service method
- Multiple transfer object projections (e.g., Account, DashboardOrganization, Organization, PartnerDashboard, Profile) each have their own custom operation classes for the same business action (e.g., `InviteUserCustomImplementation` appears under `services/invitation/`, `services/organization/`, `services/dashboardorganization/`, `services/partnerdashboard/`, and `services/user/`) -- all delegating to the same shared service
- **OrganizationAccess operations** (changeAccessToAdmin, changeAccessToOwner, enableAccess, disableAccess, cancelAccess) modify the junction entity's `type` enum or `enabled` flag via `organizationAccessEntityDao.update()`
- **Authentication interceptors** implement `AuthenticationInterceptor` to auto-create Account entities on first OIDC login by checking if a user with the `preferred_username` claim exists and creating one if not
- All service methods declare `throws BusinessErrorException` and use `ErrorCode` enum values for structured error reporting

## Examples

### ubives
- Key files: `services/AccountService.java`, `services/AccessService.java`, `services/OrganizationService.java`, `services/UserService.java`, `services/Variables.java`
- Key custom ops: `services/account/CreateOrganizationCustomImplementation.java`, `services/organizationaccount/ChangeAccessToAdminCustomImplementation.java`, `services/organizationaccount/CancelAccessCustomImplementation.java`, `services/user/DisableUserCustomImplementation.java`
- Pattern: Service layer classes are OSGi `@Component` beans injecting entity DAOs and peer services. `AccountService.getCurrentAccount()` resolves the authenticated user via `Variables.getActorUserName()` and queries `AccountEntityDao`. `AccountService.createAccount()` creates an `IdentityEntity` (if not existing), an `AccountEntity`, and a Keycloak user in the organization's realm via `RealmManager`
- Notable: `AccessService.changeAccessTo(UUID, OrganizationAccessType)` loads the `OrganizationAccessEntity` by ID, sets the new type, and calls `update()`. Custom ops like `ChangeAccessToAdminCustomImplementation` are one-liners delegating to `accessService.changeAccessTo(id, OrganizationAccessType.ADMIN)`
- Interceptors: `CreateAuthenticatedUserAuthenticationInterceptor` and `LogAuthenticationInterceptor` in the `interceptors` module implement `AuthenticationInterceptor`; the former auto-creates Account records from OIDC claims on first login
