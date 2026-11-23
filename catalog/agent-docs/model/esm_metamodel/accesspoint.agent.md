# accesspoint.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/esm_metamodel/accesspoint.md.

## Element Reference

- `ActorType`: role (e.g. Administrator, Customer). Attributes: `name` [1]; `principal` TransferObjectType [0..1] (the TO holding identity); `claims` Claim [0..*]; `accesses` Access [0..*]; `menuItems` MenuItem [0..*] (nav root); `kind` ActorKind [1] (`HUMAN`/`SYSTEM`); `anonymous` Boolean [1] (unauthenticated guest); `managed` Boolean [1].
- `managed=true`: framework syncs the principal row from the IdP token on `#_principal`. Requires `principal` to be a MAPPED TO (projecting an EntityType) and ≥1 `claims`.
- Gotcha (dispatcher 1.0.6.20241030 / 1.0.6.20251205): only lookup is implemented, NOT first-login insert. `getActorByClaims` throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. Pair with an `AuthenticationInterceptor` doing the insert (see authentication-guide Just-in-Time User Provisioning).
- `Access`: data-permission grant. `name` [1]; `target` TransferObjectType [1] (query entry point); `getterExpression` ReferenceExpression [0..1] (filter; omitted = all instances); `createable`, `updateable`, `deleteable` Boolean [1].
- Write-side membership invariant: UPDATE rejected if post-update state no longer satisfies the predicate; filter attributes are read-only through the filtered path. See `../../../best-practices/model/derived-relation-membership-invariant.md`.
- Pairing rule: an `Access` creates NO navigation. Every UI-reachable Access needs a `MenuItemAccess` under the same `ActorType.menuItems` (directly or in a `MenuItemGroup`) whose `access` points back. Otherwise it is API-only. See `./ui.md` and `../ui-authoring-guide.md`.
- `Claim`: maps a principal DataMember to a claim type. Attributes: `attribute` DataMember [1] (must be MAPPED when `managed=true`); `claimType` ClaimType [1] (`EMAIL` → `email` claim, `USERNAME` → `preferred_username`).
- Claim has NO `name`. FQN is `<actor fqn>::<attribute name>::<claimType>`. Selecting `name` on claims fails: `Field 'name' in type 'ESM_Claim' is undefined`. `claimType` values: `EMAIL`, `USERNAME`, `UNDEFINED`.
- Create a claim: `judo create -t Claim --ns <Model>::<Actor> --set claimType=EMAIL --set attribute=<Model>::<PrincipalTO>.<attribute>`; check with `judo query esm Claim -s fqn,claimType`.
- Authoring chain (all four must link, or `managed` and `ACTOR.*` silently degrade to transient principal):
  - `ActorType`: `principal` = mapped principal TO; `managed = true`.
  - `ActorType.claims`: one per claim type; `attribute` = DataMember on that TO; `claimType`.
  - Principal TO: `actorType` = the ActorType (back-link); outer `createable/updateable/deleteable = false` (no public CRUD).
  - Principal TO identity DataMember: `memberType = MAPPED`; `binding` = attribute on backing EntityType.
- Runtime: first login `#_principal` inserts row (claim columns populated; others default). Later logins look up by claims (EMAIL, USERNAME, or both) and refresh changed values. JQL reads persisted attrs via `!getVariable("ACTOR", "<member name>")`.
- Claim type choice is an IdP/deployment decision: `USERNAME` for stable unique `preferred_username`; `EMAIL` when email is canonical; both when filtering needs either.
- Principal back-link exclusivity: `TransferObjectType.actorType` and `ActorType.principal` are eOpposite, single-valued. Only ONE TO per actor holds `actorType`. Setting it moves the principal and clears the previous link. Other TOs on the same entity stay plain mapped TOs.
- Observed: pointing a wider TO at the actor moved the principal; the build then failed in `esm2ui/claim.etl` (`Could not find attribute: userName`).
- Managed-realm sync: when `managed=true`, CUD on principal TO syncs to Keycloak managed realm. Trigger is `UserManagedWrappedDao` (`judo-runtime-core-security`) via `KeycloakUserManager.getManagedActorOfPrincipal(clazz)`: sync follows TO metadata, not entity.
- Other TOs mapping the same entity (e.g. admin `UserTO`, `UserListTO`) do NOT sync to Keycloak; the row updates, the realm user does not.
- Pattern: admin mutations needing realm sync go through a custom operation that calls the principal TO's DAO. Design rule: one lean principal TO owns `actorType` and managed sync; other mapped TOs serve admin/list projections.
- Three actor shapes (`principal`/`managed`/`claims` decide shape; no `claimPrincipal` flag):
  - Token-only: no principal, `managed=false`, no claims. Persists nothing. JQL `USER.*`.
  - Transient principal: unmapped TO, `managed=false`, claims optional. Persists nothing. JQL `PRINCIPAL.*`.
  - Managed mapped principal: mapped TO, `managed=true`, ≥1 claim on a MAPPED DataMember. Persists row. JWT via `USER.*`; persisted attrs via `ACTOR.*`.
  - See `../advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables`.
- Enums: `ActorKind` HUMAN (interactive UI) / SYSTEM (automated, external). `ClaimType` EMAIL / USERNAME. `AccessType` ALL (all instances, subject to getter) / DERIVED (from another source).

## Behaviour Rules

- ActorType page visibility: Actor always; Realm always (groups vary by anonymous state); Theme only when `kind = HUMAN`.
- ActorType attributes: `principal` read-only; `anonymous` enabled when principal null or unmapped; `realm` enabled when NOT effectively anonymous; `managed` enabled when principal non-null AND mapped; `claims` enabled when NOT effectively anonymous; `isActiveExpression` always.
- Theme attributes (HUMAN only): `defaultLanguage` (LDML, e.g. `en-US`), `applicationLogo`, `applicationIcon`, `applicationTitle`, `applicationBackgroundImage`, `primaryColor`, `secondaryColor`, `textPrimaryColor`, `textSecondaryColor`, `backgroundColor`, `subtitleColor`, `paperBackgroundColor` (colours as `#rrggbbaa`), `menuOrientation` (`VERTICAL`/`HORIZONTAL`).
- ActorKind: HUMAN generates UI and shows Theme page; SYSTEM generates no UI and hides Theme.
- Access page visibility: Access and CRUD always visible.
- Access attributes: `name` always; `target` read-only; `accessType` always (ALL/DERIVED); `cardinality` only when DERIVED (`0..1` or `0..*`); `getterExpression` only when DERIVED.
- AccessType: ALL fixes cardinality to `0..*` (lower=0, upper=-1) and disables getter; choosing ALL sets those values. DERIVED makes cardinality editable and enables getter.
- Access CRUD: `createable` enabled only when target NOT abstract; `updateable`, `deleteable`, `exportable` always enabled.
- Access CRUD flags are rung 2 of the relation-CUD capability ladder (rungs 1–6 in `../../../best-practices/model/relation-driven-crud-with-custom-input.md#capability-ladder`).
- Claim attributes: `attribute` required, chosen from `principal.getAllAttributes()`; OK disabled while null. `claimType`: EMAIL, USERNAME, UNDEFINED.
- Anonymous vs authenticated: effectively anonymous → AnonymousGroup shown, claims and managed hidden. Not anonymous → RealmGroup, claims and managed visible.
- `isEffectiveAnonymous()` true when `anonymous = true` AND principal is null or not mapped. A mapped principal is never effectively anonymous, even with `anonymous = true`.
- `anonymous` defaults `true` on every actor, also with a mapped principal (harmless there; matters only if the principal mapping is later removed). CLI: `anonymous` is read-only once a principal is mapped (`update -s anonymous=false` / `-u anonymous` → `does not apply to this ActorType (applies when effectively anonymous)`). To store `false` with a mapped principal pass it in the same `create` as the principal (option order is irrelevant): `create -t ActorType ... -s anonymous=false -s principal=<TO>`; on an existing actor only while no principal is mapped.
- Exposing an operation without login: put it on an effectively anonymous actor. No `realm` → `asm2keycloak` makes no realm or client, and REST does not verify a bearer token: calls run with no principal and no `ACTOR`. Everything reachable is public; keep minimal; guard in an interceptor or the operation. Verify: access control on calls without principal outside the Keycloak interceptor is not checked.
- `isActiveExpression`: JQL on principal entity (e.g. `self.active`), copied into the mapped actor TO filter. Runtime: token `azp` selects actor type; actor found by claim (USERNAME, then EMAIL, then identifier attribute). Expression false → `AUTHENTICATED_ENTITY_NOT_FOUND`; no matching entity → same error. Only mapped-principal actors are looked up. Verify the filter applies inside `dao.search`.
- Visual indicators: `kind = SYSTEM` → system style; `Access.target` not mapped → warning style.
- Context checks: Effectively anonymous (see above); Principal mapped = principal non-null AND `principal.mapping` non-null; Target abstract = `Access.target.abstract = true`.
- UI requirement on target TO: list access (`upper = -1`: every ALL grant, DERIVED with `0..*`) renders a table page, so target TO needs `<table>` with ≥1 `<columns>`; else transformation fails with `Columns are not defined for the viewable table of <TO>`. Single access (`upper = 1`) needs `<form>`. The same applies to TOs reached via `TabularReferenceField.dataFeature`. One TO table is shared by all actors.
- Column rules: skip `BinaryType` and large-text members; skip expensive derived aggregates (put in detail view); `visible="false"` for technical columns (hashes, ids, durations) — kept for filters/export; lead with human-readable keys (name, code, status, date).
- `<columns>` typed abstract `ui:Column`; each child needs `xsi:type="ui:DataColumn"`; root model element must declare `xmlns:ui`. See `./ui.md` (DataColumn).

## Related Documentation

- [Structure Package](./structure.md) — TransferObjectType and EntityType.
- [UI Package](./ui.md) — MenuItem and navigation.
- [Operation Package](./operation.md) — operation access control.
