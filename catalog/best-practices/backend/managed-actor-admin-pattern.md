---
id: managed-actor-admin-pattern
title: "Managed-Actor Admin Surface: Read-Only Relation + Custom-Op Delegation"
description: "Admin user management on a managed actor uses a read-only users relation plus gated custom operations that write through the principal TO's DAO, so Keycloak realm sync fires."
aliases: [admin user management, managed actor admin, invite user operation, Keycloak sync admin]
keywords: [managed actor, Keycloak, realm sync, principal DAO, custom operation, enabledBy, read-only relation, invite user, OperationFlowManager]
tags: ["domain:backend", "layer:backend", "project:compsych-letter-demo", "status:single-project"]
category: auth
status: single-project
projects: [compsych-letter-demo]
evidence: ["compsych-letter-demo:unrecorded"]
alternatives: []
first_seen: 2026-05-11
last_updated: 2026-11-10
---
## Intent

Give an admin a user-management surface on an actor with `managed=true` (principals synced to a Keycloak realm): list users, invite, change role, deactivate, reactivate. Every mutation must reach the Keycloak realm user. The surface is a read-only relation plus one custom operation per write verb, each writing through the principal TO's DAO.

## Practice

### Platform base

- With `ActorType.managed=true`, the framework delegates create/update/delete on the principal TO to the managed Keycloak realm. The sync is bound to the **principal TO's DAO metadata**, not to the entity: other TOs mapping the same entity (an admin `UserTO`, a list TO) do not sync, the entity row changes and the realm user does not ([managed-realm sync trigger](../../agent-docs/model/esm_metamodel/accesspoint.md), [authentication guide](../../agent-docs/backend/authentication-guide.md)).
- Multiple TOs may map the same principal entity; only the `actorType` back-link is exclusive. Setting it on a second TO clears it from the previously linked one ([principal back-link exclusivity](../../agent-docs/model/esm_metamodel/accesspoint.md)).
- Docs' design rule: one lean principal TO owns `actorType` and the framework-managed sync; other mapped TOs serve admin and list projections; admin mutations needing realm sync go through a custom operation that calls the principal TO's DAO.
- A custom operation is an OSGi component implementing the generated interface; it is not intercepted ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern), [which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). The relation access flags and `enabledBy` chain (the relation-CUD capability ladder, [access CRUD rules](../../agent-docs/model/esm_metamodel/accesspoint.md)) apply to direct relation create/update/delete only.
- An actor's access targets must be mapped transfer objects, hence the admin view-model is a mapped TO (a self-mapped entity access).

### Practice notes: shape

Practice notes (one example), not platform API:

- An admin dashboard access, mapped to the principal entity (self getter), with outer `createable`, `updateable` and `deleteable` all false, shown only when `self.isAdmin`.
- A `users` relation of the principal entity TO (0..*) with no relation create/update/delete flags: read-only list with row click to detail.
- Operations on the dashboard, each `enabledBy` the admin flag: `inviteUser(UserInvitationInput)`, `updateUserRole(target, isAdmin)`, `deactivateUser(target)`, `reactivateUser(target)`, each returning the principal entity TO.
- `UserInvitationInput` is an **unmapped** TO (email, given name, family name, admin flag). Its shape differs from the mapped attributes: no user name, because Keycloak derives the preferred username from the e-mail ([[relation-driven-crud-with-custom-input]]).
- The principal TO (the one holding the `actorType` back-link) is the single representation: relation row, row detail, operation result and redirect target.
- Each operation body writes through the principal TO's DAO. The frontend redirects the result to the access-context detail (`admin.users[id]`) with an OperationFlowManager hook ([[operation-flow-manager-redirect]]).

```java
// Example code: UserPrincipalDao / UserTODao are generated DAOs
@Component(service = AdminDashboardInviteUser.class, immediate = true)   // generated interface name varies, verify
public class AdminDashboardInviteUserCustomImpl implements AdminDashboardInviteUser {

  @Reference UserPrincipalDao userPrincipalDao;   // principal TO's DAO
  @Reference UserTODao userTODao;                 // admin projection DAO

  @Override
  public UserTO inviteUser(UserInvitationInput input) {
    UserPrincipalForCreate payload = UserPrincipalForCreate.builder()
        .withEmail(input.getEmail())
        .withGivenName(input.getGivenName())
        .withFamilyName(input.getFamilyName())
        .withIsAdmin(input.getIsAdmin())
        .withIsActive(Boolean.TRUE)
        .build();
    UserPrincipal created = userPrincipalDao.create(payload);   // triggers realm-user create
    return userTODao.getByIdentifier(created.getIdentifier()).orElseThrow();
  }
}
```

The DAO to call is the principal TO's one (`create`, `update`, `delete`): not the plain entity DAO (skips Keycloak) and not the admin TO's DAO (carries no sync trigger).

### Variation: separate identity-server client module

A second variant provisions users through an identity-server user service with invitations. Instead of writing through the principal TO's DAO, it calls a separate client module that talks to the identity server. Whether realm sync fires on this path is not confirmed by the agent-docs: *verify*.

## Rationale

- Custom operations are outside the capability ladder, so one `enabledBy` gate per operation is the whole check.
- Principal-DAO routing is what triggers realm sync; a direct create/update on the admin TO through the relation would not.
- Read-only relation avoids `updateable=true` on the dashboard. That would open the generated update endpoint for the admin's own row (the actor's own access), a self-elevation risk. One security surface: read-only relation plus gated operations.
- Redirecting to the access-context detail gives one canonical URL per row with breadcrumbs, instead of the standalone mapped-TO view. The per-instance updatable/deletable flags of the result row are evaluated in the admin access context (observed in practice, *verify*).

## Example

Anti-patterns seen or predicted in one example:

| Anti-pattern | Consequence | Instead |
|---|---|---|
| Enable create on the users relation so the framework generates an "Add user" button | The auto-form uses the mapped shape, so the admin can set a user name and the Keycloak username derivation cannot be enforced | Outer createable false; custom `inviteUser` with the unmapped input |
| Put `actorType` on the admin TO | The lean principal TO loses its back-link and a later generator step fails with a missing-attribute error (one example saw "Could not find attribute: userName") | Keep `actorType` on the lean principal TO; map the admin TO without it |
| Mutate through the entity DAO | Row updates, Keycloak does not | Use the principal TO's DAO |
| `updateable=true` on the dashboard for inline edits | Admin can change an arbitrary user, including the admin flag, through the generated update endpoint | `updateable=false`; one gated operation per update |

Related operations by output shape:

| Operation | Output | Redirect |
|---|---|---|
| `resetPassword(target)` returning `{ temporaryPassword, expiresAt }` | Unmapped; shown inline in the view-mode form | Usually none |
| Bulk operations returning void | n/a | Stay and refresh the caller list |
| `assignRoles(target, roles)` | Mapped principal TO | Redirect to the canonical detail (`access: users`, id) |

## When to avoid

- The actor is not managed: there is no realm sync to route, a plain generated CRUD relation may do.
- The user needs no admin UI at all: JIT provisioning covers first login ([[keycloak-jit-user-provisioning]]).

## Related

- [[relation-driven-crud-with-custom-input]] — relation auto-wiring, custom-operation pattern, capability ladder
- [[operation-flow-manager-redirect]] — redirect recipes and registration
- [[actor-based-transfer-projection]] — several TOs over one entity
- [[keycloak-jit-user-provisioning]] — first-login companion
