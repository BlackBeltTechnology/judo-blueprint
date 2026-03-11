## Overview

The Invitation entity's operations (inviteUser, inviteAccount, acceptInvitation, cancelInvitation) are implemented as custom Java classes that delegate to a central `InviteService` OSGi service. The accept flow branches on `InvitationType` (USER vs ACCOUNT) to either create a new organization-scoped user or grant an existing platform account access to the organization, provisioning the user in Keycloak in both cases. A `MailServices` component sends invitation emails via SendGrid with Handlebars-templated HTML.

## Implementation Pattern

- An `InviteService` OSGi `@Component` centralizes all invitation logic: `invite()`, `accept()`, `cancel()`, and lookup helpers
- `invite(organizationId, email, invitationType)` creates an `InvitationEntity` with a generated `inviteId` (32-char random string via `ApiKeyGenerator`), a 1-month expiration, and default feature flags set to false. It calls `organizationEntityDao.createInvitations()` to compose the invitation under the organization, then triggers `mailServices.sendInvitation()`
- `accept(invitationId, userName, password, firstName, lastName)` loads the invitation with its type and email, resolves the parent organization with its realm name, checks for Keycloak username conflicts, then branches:
  - **ACCOUNT type**: calls `accountService.createAccount()` (creates Identity + Account + Keycloak user in platform realm), then creates an `OrganizationAccessEntity` with ADMIN type linking the account to the organization, and creates a second Keycloak user in the organization's realm
  - **USER type**: finds or creates an `IdentityEntity` by email, creates a `UserEntity` under the organization via `organizationEntityDao.createUsers()`, and creates a Keycloak user in the organization's realm
  - In both cases, the invitation is deleted after successful acceptance
- `cancel(invitationId)` simply deletes the invitation entity
- Custom operation classes are thin delegates: `AcceptInvitationCustomImplementation` validates password match, then calls `inviteService.accept()`. `InviteUserCustomImplementation` and `InviteAccountCustomImplementation` resolve the current organization and call `inviteService.invite()` with the appropriate `InvitationType` enum value
- The same invitation operations appear under multiple transfer object packages (`services/invitation/`, `services/invitelink/`, `services/organization/`, `services/dashboardorganization/`, `services/partnerdashboard/`, `services/user/`) because multiple actor projections expose the same business action -- all delegate to the shared `InviteService`
- `MailServices` is an OSGi `@Component` with `ConfigurationPolicy.REQUIRE` and `@Designate` for baseUrl, fromAddress, and SendGrid API key. It renders a Handlebars HTML template (`email-inline-template.html.hbs`) with the invitation action link and sends via SendGrid API
- `ApiKeyGenerator` produces 32-character alphanumeric random strings using `SecureRandom` for invitation IDs

## Examples

### ubives
- Key files: `services/InviteService.java`, `services/MailServices.java`, `services/ApiKeyGenerator.java`, `custom/.../invitelink/AcceptInvitationCustomImplementation.java`, `custom/.../invitation/InviteUserCustomImplementation.java`, `custom/.../invitation/InviteAccountCustomImplementation.java`, `custom/.../invitation/CancelInvitationCustomImplementation.java`
- Pattern: Central `InviteService` OSGi `@Component` injecting `OrganizationEntityDao`, `InvitationEntityDao`, `AccountService`, `UserService`, `RealmManager`, and `MailServices`. Custom ops are one-liner delegates
- Notable: `AcceptInvitationCustomImplementation` is the only custom op with inline business logic -- it validates `password == passwordAgain` before delegating. The accept flow demonstrates dual-provisioning: entity creation in the database followed by `realmManager.createUser()` in the organization's Keycloak realm
- Email: `MailServices` uses SendGrid REST API with Handlebars templates; the invitation link includes the `inviteId` as a query parameter (`?invitationKey=...`) pointing to the anonymous frontend for acceptance
- Multiple projections: `InviteUserCustomImplementation` exists in 5 packages (invitation, organization, dashboardorganization, partnerdashboard, user) -- each actor's view of the same invite operation, all calling `inviteService.invite(orgId, email, InvitationType.USER)`
