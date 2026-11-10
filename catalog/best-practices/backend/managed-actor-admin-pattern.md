---
id: "managed-actor-admin-pattern"
title: "Managed-Actor Admin Surface: Read-Only Relation + Custom-Op Delegation"
domain: "backend"
category: "auth"
score: 0.0
usage_count: 0
alternative_count: 0
first_seen: "2026-05-11"
last_updated: "2026-05-11"
projects:
  - compsych-letter-demo
---
## Purpose

Admin user-management surface on a managed actor. Read-only relation + custom ops + principal-DAO routing for Keycloak realm sync. Canonical specialization combining principal back-link exclusivity, managed-realm sync trigger, path-agnostic outer CRUD, and capability ladder.

## §1 When

- `ActorType.managed=true` (Keycloak-synced principal). See [accesspoint.md — Managed-realm sync trigger](../../agent-docs/model/esm_metamodel/accesspoint.md#managed-realm-sync-trigger).
- Admin surface needed for user-management: invite / role-edit / deactivate / reactivate.
- Mutations from admin surface must propagate to Keycloak realm user (create / update / disable).

## §2 Shape

Read-only access on the actor + view-model TO + relation to principal-entity TO + custom ops for each CUD verb.

```
AdminDashboard  // mapped <PrincipalEntity>, getterExpression = self
  outer createable=false  updateable=false  deleteable=false
  // access carries enabledBy on parent = "self.isAdmin"

  .users : <PrincipalEntity>TO[0..*]
    // R only + row-click → detail. No relation C/U/D flags.

  .inviteUser(input: UserInvitationInput) : <PrincipalEntity>TO
  .updateUserRole(target: <PrincipalEntity>TO, isAdmin: Boolean) : <PrincipalEntity>TO
  .deactivateUser(target: <PrincipalEntity>TO) : <PrincipalEntity>TO
  .reactivateUser(target: <PrincipalEntity>TO) : <PrincipalEntity>TO

  // Each op: enabledBy = "self.isAdmin"
  // Each op body: delegate write through <PrincipalTO>'s DAO → Keycloak realm sync.
  // OperationFlowManager redirects each result to admin.users[id].
```

`UserInvitationInput` = **unmapped** TO with `{ email, givenName, familyName, isAdmin }`. Shape diverges from `<PrincipalEntity>TO` mapped attributes (e.g. no `userName` field — Keycloak derives `preferred_username` from `email`). See [relation-driven-crud-with-custom-input.md — §2](../model/relation-driven-crud-with-custom-input.md#2-custom-operations-for-shape-divergent-mutations).

`<PrincipalEntity>TO` = the **principal TO** (the one holding `actorType = <Actor>` back-link). Same TO is the relation row, the row detail, the custom-op result, and the redirect target. **One representation per concept.**

## §3 Rationale

- **Custom ops bypass capability ladder rungs 1–6.** Single `enabledBy="self.isAdmin"` gate per op. Ladder applies only to direct relation CUD. See [relation-driven-crud-with-custom-input.md — §4](../model/relation-driven-crud-with-custom-input.md#4-capability-ladder).
- **Principal-DAO routing triggers Keycloak realm sync.** Op body invokes `<PrincipalEntity>TO`'s DAO (e.g. `userPrincipalDao.create(...)`, `.update(...)`, `.delete(...)`). Dispatcher injects Keycloak sync because DAO call carries principal TO metadata. Direct CUD on `<PrincipalEntity>TO` via relation would skip Keycloak (relation rooted under different TO context; sync trigger is TO-metadata-bound).
- **Read-only relation avoids opening `AdminDashboard.updateable=true`.** Setting `updateable=true` on the view-model TO opens `_updateInstance<AdminDashboard>` endpoint. Admin editing own row via `~admin` PUT = self-elevation risk. Read-only relation + `enabledBy`-gated ops = single security surface.
- **`OperationFlowManager` redirects to canonical view.** Default mapped-TO output navigates to standalone `<PrincipalEntity>TO>View` route. Redirect to `admin.users[id]` = access-context detail. Same row, one canonical URL, breadcrumbs preserved. See [operation-flow-manager-redirect.md](../../best-practices/frontend/operation-flow-manager-redirect.md).
- **Result row's `__updateable` / `__deletable` computed in admin access-context.** Parent `AdminDashboard.updateable=false` but per-instance `<PrincipalEntity>TO.__updateable` evaluated against the admin's access — not the caller's ladder gate, because redirect lands in access-context detail. Layer-2 navigation breaks the ladder coupling.

## §4 Op body skeleton

```java
@Service(classes = AdminDashboardInviteUserExchangeFunctions.class)
public class AdminDashboardInviteUserCustomImpl
    implements AdminDashboardInviteUserExchangeFunctions {

  @Reference volatile UserPrincipalDao userPrincipalDao;  // principal TO's DAO

  @Override
  public UserTO inviteUser(UserInvitationInput input) {
    UserPrincipalForCreate payload = UserPrincipalForCreate.builder()
        .withEmail(input.getEmail())
        .withGivenName(input.getGivenName())
        .withFamilyName(input.getFamilyName())
        .withIsAdmin(input.getIsAdmin())
        .withIsActive(Boolean.TRUE)
        .build();

    // Principal-TO DAO create → triggers Keycloak realm-user create.
    UserPrincipal created = userPrincipalDao.create(payload);

    // Return UserTO (admin projection) — same row, different mapped TO.
    return userTODao.getByIdentifier(created.getIdentifier()).orElseThrow();
  }
}
```

DAO call shape: `userPrincipalDao.create / update / delete`. NOT `userEntityDao.*` (skips Keycloak). NOT `userTODao.*` directly (admin TO does NOT carry the sync trigger). See [accesspoint.md — Managed-realm sync trigger](../../agent-docs/model/esm_metamodel/accesspoint.md#managed-realm-sync-trigger).

## §5 Anti-patterns

| Anti-pattern | Consequence | Correct shape |
|---|---|---|
| Framework auto-generates "Add user" button on `users` relation (`<PrincipalEntity>TO.createable=true` + relation C-flag) | Auto-form uses `<PrincipalEntity>TO`'s mapped shape. Admin can set `userName`. Framework cannot enforce Keycloak `preferred_username` derivation constraint. | `<PrincipalEntity>TO.createable=false` outer (path-agnostic). Custom op `inviteUser` with unmapped `UserInvitationInput`. |
| `<PrincipalEntity>TO.actorType = <Actor>` (admin TO holds principal back-link) | Lean principal TO loses back-link (cleared to null). Build breaks (e.g. `esm2ui/claim.etl` "Could not find attribute: userName"). See [accesspoint.md — Principal back-link exclusivity](../../agent-docs/model/esm_metamodel/accesspoint.md#principal-back-link-exclusivity). | Keep `<Principal>TO.actorType = <Actor>` on the lean principal TO. Admin TO maps same entity without `actorType`. |
| Op body mutates `<PrincipalEntity>` via entity DAO directly | Skips Keycloak realm sync. Entity row updates; realm user does not. | Route through `<PrincipalEntity>TO`'s DAO (the TO with `actorType` back-link). |
| Open `AdminDashboard.updateable=true` to enable inline edits in admin table | Admin editing AdminDashboard view = editing own User row via `~admin` PUT. Self-elevation: admin sets `isAdmin=true` on a peer through the same endpoint. | Outer `updateable=false`. Each U operation a separate `enabledBy`-gated custom op (e.g. `updateUserRole`). |

## §6 Related operations

| Op | Output shape | Layer-1 nav | OperationFlowManager redirect |
|---|---|---|---|
| `resetPassword(target: ...) : ResetPasswordResultTO` | Unmapped (`{ temporaryPassword, expiresAt }`) | Inline view-mode form. No re-fetch. | Typically null (stay inline). |
| Bulk ops returning `void` | n/a | Stay + refresh caller list. | n/a (default behaviour). |
| `assignRoles(target: ..., roles: ...) : <PrincipalEntity>TO` | Mapped | Standalone `<TO>View`. | `{ actor, access: 'users', id }` to canonical detail. |

## See also

- [relation-driven-crud-with-custom-input.md](../model/relation-driven-crud-with-custom-input.md) — spine: relation auto-wiring, custom-op pattern, return-type matrix, capability ladder
- [operation-flow-manager-redirect.md](../frontend/operation-flow-manager-redirect.md) — redirect recipes + registration boilerplate
- [accesspoint.md — Principal back-link exclusivity](../../agent-docs/model/esm_metamodel/accesspoint.md#principal-back-link-exclusivity)
- [accesspoint.md — Managed-realm sync trigger](../../agent-docs/model/esm_metamodel/accesspoint.md#managed-realm-sync-trigger)
- authentication-guide.md `Keycloak managed-realm sync — trigger surface` in `judo-backend-docs` skill
- [actor-based-transfer-projection.md](../model/actor-based-transfer-projection.md) — multi-TO same-entity projection rules
- [keycloak-jit-user-provisioning.md](keycloak-jit-user-provisioning.md) — first-login `AuthenticationInterceptor` companion
