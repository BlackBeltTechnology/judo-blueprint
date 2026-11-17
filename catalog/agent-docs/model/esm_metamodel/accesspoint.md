---
title: accesspoint Package Reference
description: Reference of the ESM accesspoint package: actors, claims, principals, accesses and security behaviour rules.
aliases: [actor roles, security model, managed principal, claims mapping, access grants, who can do what]
keywords: [ActorType, Access, Claim, ActorKind, ClaimType, AccessType, principal, managed, getterExpression, MenuItemAccess]
tags: [domain:model, layer:model, status:platform]
---

# `accesspoint` Package Reference

**[◄ Back to Index](./README.md)**

This package defines the security model for the application, including user roles (actors), permissions, and access control mechanisms. It specifies *who* can do *what*.

---

## Element Reference

### `ActorType`
Defines a role or type of user/system that can interact with the application (e.g., `Administrator`, `SalesAgent`, `Customer`). It aggregates all security-related definitions for that role.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the actor role. |
| `principal` | `TransferObjectType` | `[0..1]` | A reference to the TO that holds the identifying information for this actor (e.g., a `UserAccount` TO). |
| `claims` | `Claim` | `[0..*]` | A list that defines which attributes of the `principal` are used for identity purposes (e.g., mapping the `email` attribute to the `EMAIL` claim type). |
| `accesses` | `Access` | `[0..*]` | The list of data access permissions granted to this actor. This defines what data the actor can see. |
| `menuItems` | `MenuItem` | `[0..*]` | The root of the navigation menu structure that will be visible to this actor. |
| `kind` | `ActorKind` Enum | `[1]` | The type of actor: `HUMAN` (an interactive user) or `SYSTEM` (an automated process or external system). |
| `anonymous` | Boolean | `[1]` | If `true`, this actor represents an unauthenticated guest user. |
| `managed` | Boolean | `[1]` | If `true`, the framework is *intended* to synchronise the `principal` row in the DB from the IdP token during the `#_principal` operation. Requires `principal` to be a **mapped** `TransferObjectType` (projecting an `EntityType`) and at least one `<claims>` element that marks which `DataMember` is the identity key. **Empirical caveat:** in `judo-runtime-core-dispatcher` 1.0.6.20241030 / 1.0.6.20251205 only the *lookup* side is implemented — the first-login *insert* is not, and `DefaultActorResolver.getActorByClaims` throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. Pair `managed=true` with an `AuthenticationInterceptor` that performs the insert (see [Just-in-Time User Provisioning](../../backend/authentication-guide.md#example-just-in-time-user-provisioning)). See *Three actor shapes* below and [Mapped Managed Principal with Claim Mapping](../advanced-modeling-patterns.md#pattern-mapped-managed-principal-with-claim-mapping). |

### `Access`
A grant of permission for an `ActorType` to access a collection of data objects. It links a role to a data set, with an optional filter.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the access grant (e.g., "AccessMyCustomers"). |
| `target` | `TransferObjectType` | `[1]` | A reference to the TO that this rule grants access to. This is the entry point for a query. |
| `getterExpression` | `ReferenceExpression` | `[0..1]` | An optional expression to filter the data this actor is allowed to see (e.g., `self.customers` to only see customers directly related to the actor). If omitted, the actor can see all instances. Write-side membership invariant: UPDATE rejected when post-update state no longer satisfies the predicate — filter attributes are read-only through the filtered access path. See [derived-relation-membership-invariant.md](../../../best-practices/model/derived-relation-membership-invariant.md). |
| `createable` | Boolean | `[1]` | If `true`, the actor can create new instances of the `target`. |
| `updateable` | Boolean | `[1]` | If `true`, the actor can update instances. |
| `deleteable` | Boolean | `[1]` | If `true`, the actor can delete instances. |

**Pairing rule (`Access` ↔ `MenuItemAccess`).** An `Access` is a *data-permission* grant only; it does **not** create any navigation entry. Every `Access` on an `ActorType` that should be reachable from the UI **must** be paired with a `MenuItemAccess` placed under that same `ActorType.<menuItems>` (directly or inside a `MenuItemGroup`), with its `access` reference pointing back to this `Access`. Without the paired `MenuItemAccess` the target is exposed through the access point API but never appears in the actor's menu. See [ui.md — MenuItemAccess](./ui.md) and [UI Authoring Guide](../ui-authoring-guide.md).

### `Claim`
A declaration that maps a specific attribute on the `principal` TO to a standard security claim type. This tells the JUDO runtime which `DataMember` on the `principal` TO corresponds to which JWT claim, so it can (a) look up the existing principal row on each call, and (b) — when `ActorType.managed = true` — auto-provision or synchronise the row on `#_principal`.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `attribute` | `DataMember` | `[1]` | A reference to the `DataMember` on the `principal` TO that holds the claim value. For `managed = true` actors, this `DataMember` MUST be `MAPPED` (have a `binding` to an `EntityType` attribute) so the value persists. |
| `claimType` | `ClaimType` Enum | `[1]` | Which standard claim of the IdP token this attribute carries: `EMAIL` or `USERNAME`. The framework pulls the matching OIDC claim from the JWT (`email` for `EMAIL`, `preferred_username` for `USERNAME`) and writes it through the binding. An `ActorType` may declare one claim or both — whichever the principal entity needs to be keyed and synchronised by. |

A `Claim` has no `name`. It is identified by the FQN `<actor fqn>::<attribute name>::<claimType>` (for example `<Model>::<Actor>::email::EMAIL`); a query that selects `name` on `claims` fails with `Field 'name' in type 'ESM_Claim' is undefined`. `claimType` is `EMAIL`, `USERNAME` or `UNDEFINED`. Create one with the actor as parent and the principal's attribute as target (the actor needs a principal first; the attribute must belong to the principal TO):

```bash
judo create -t Claim --ns <Model>::<Actor> --set claimType=EMAIL --set attribute=<Model>::<PrincipalTO>.<attribute>
judo query esm Claim -s fqn,claimType
```

**Authoring chain.** The four elements below must form an unbroken chain before `managed` provisioning and `ACTOR.*` lookups work. Any missing link silently degrades the actor to a transient principal:

| Element | Must reference | Purpose |
| :--- | :--- | :--- |
| `ActorType` | `principal` = the mapped principal `TransferObjectType`; `managed = true` | Declares an actor whose row is owned by the framework. |
| `ActorType.<claims>` (one per claim type) | `attribute` = a `DataMember` on that principal TO; `claimType` = `EMAIL` or `USERNAME` | Tells the runtime which `DataMember` to read / write when the matching JWT claim arrives. |
| principal `TransferObjectType` | `actorType` = the `ActorType` (back-link); outer `createable/updateable/deleteable = false` (the framework owns the row — no public CRUD service) | Declares itself as the actor's projection of the underlying entity. |
| principal TO's identity `DataMember` | `memberType = MAPPED`; `binding` = the corresponding attribute on the backing `EntityType` | Persists the claim value to the DB column so later logins match the existing row. |

With the chain in place, JUDO's behaviour at runtime:

-  **First login** — `#_principal` inserts a new row in the principal entity, populating every column reachable via a `<claims>` binding from the JWT. Non-claim columns remain at their entity defaults.
-  **Subsequent logins** — the same `<claims>` attributes are used to look the row up (by `EMAIL`, `USERNAME`, or both) and refresh them if the IdP values changed.
-  **JQL lookup** — access `getterExpression`s read the persisted attributes via `!getVariable("ACTOR", "<member name>")`, where `<member name>` is the `DataMember.name` on the principal TO (e.g. `email` when `claimType = EMAIL`, `userName` / `preferredUsername` when `claimType = USERNAME` — the model author picks the member name).

Which claim type to choose is an IdP / deployment decision, not a modelling one: use `USERNAME` when the IdP guarantees a stable, unique `preferred_username`; use `EMAIL` when email is the canonical identifier; declare both when the app needs to filter on either (e.g. operator search-by-email on top of username-keyed provisioning).

### Principal back-link exclusivity

`TransferObjectType.actorType` = eOpposite of `ActorType.principal`. Single-valued on both sides. Only ONE TO per actor holds `actorType=<Actor>`.

Setting `TO.actorType` transparently reassigns `ActorType.principal` to that TO. Previously-linked TO loses back-link (cleared to null).

Consequence: cannot keep lean principal TO AND separate full admin TO both carrying `actorType=<Actor>`. Pick one. Other TOs mapping same entity exist as plain mapped TOs without the back-link.

**Source**: `esm.ecore` declares `TransferObjectType.actorType` and `ActorType.principal` as `eOpposite` of each other, both single-valued. **Observed in one project**: pointing a second, wider transfer object at the actor moved the principal to it, and the build then failed in `esm2ui/claim.etl` (*"Could not find attribute: userName"*) because the claims referenced attributes of the original principal.

### Managed-realm sync trigger

When `ActorType.managed=true`, framework delegates CUD on principal TO to Keycloak managed realm (create / update / delete realm user matching the row).

Sync trigger bound to **principal TO's DAO metadata**: `UserManagedWrappedDao` (`judo-runtime-core-security`) syncs only when `KeycloakUserManager.getManagedActorOfPrincipal(clazz)` resolves the DAO call's class to a managed actor. Sync follows TO metadata, not entity.

Other TOs mapping same principal entity (e.g. admin user-management `UserTO`, list `UserListTO`) do NOT auto-sync to Keycloak. Entity row updates; Keycloak realm user does not.

Multiple TOs CAN map same principal entity — admin user-management coexists with lean principal TO. Metamodel allows it; only `actorType` back-link is exclusive (see *Principal back-link exclusivity* above).

**Pattern.** For Keycloak sync from admin user-management surface: custom operation on admin TO that delegates through **principal TO's DAO** (re-dispatch with principal-TO metadata). Direct CUD on admin TOs skips Keycloak.

**Design rule.** Keep ONE lean principal TO owning `actorType` AND framework-managed Keycloak sync. Use other mapped TOs for admin / list projections. Route admin mutations through a custom op calling principal TO's DAO when realm sync required; otherwise accept admin TO mutations are DB-only.

### Three actor shapes (authoring reference)

Three shapes for `ActorType.principal` are supported (there is no `claimPrincipal` flag: the shape follows from `principal`, `managed` and `claims`). The shape dictates which JQL category surfaces the identity data and what the framework persists:

| Shape | `principal` | `managed` | `<claims>` | Framework persists | JQL for JWT claims | JQL for persisted attrs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Token-only** | absent (no `principal`) | `false` | none | nothing | `USER.*` | — |
| **Transient principal** | unmapped `TransferObjectType` | `false` | optional | nothing | `PRINCIPAL.*` | — |
| **Managed mapped principal** | mapped `TransferObjectType` projecting an `EntityType` | `true` | ≥ 1, each pointing at a `MAPPED` `DataMember` | the principal entity row (auto-insert / auto-update from JWT) | `USER.*` (raw claim) | `ACTOR.*` (from the row) |

See [ACTOR vs PRINCIPAL vs USER](../advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables) for the matching JQL decision matrix and the silent-failure pitfall when the chosen category doesn't match the chosen shape.

### Enums

| Enum | Value | Description |
| :--- | :--- | :--- |
| **`ActorKind`** | `HUMAN` | An interactive user operating through the UI. |
| | `SYSTEM` | An automated process, script, or external system. |
| **`ClaimType`** | `EMAIL` | The attribute represents the user's email address. |
| | `USERNAME` | The attribute represents the user's unique username. |
| **`AccessType`**| `ALL` | The access grant applies to all instances (subject to `getterExpression`). |
| | `DERIVED` | The access is derived from another source. |

---

## Behaviour Rules

These rules define how accesspoint elements behave based on their context and attribute values.

### ActorType Page Visibility

| Page | Visible When |
|------|--------------|
| Actor | Always |
| Realm | Always (different groups based on anonymous state) |
| Theme | `kind = HUMAN` |

### ActorType Attribute Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `principal` | Read-only | Display of linked TransferObjectType |
| `kind` | Always | `HUMAN` or `SYSTEM` |
| `isActiveExpression` | Always | JQL expression returning true if actor can login |
| `anonymous` | `principal` is null OR `principal` is NOT mapped | Allow anonymous login |
| `realm` | NOT `isEffectiveAnonymous()` | Keycloak realm identifier |
| `managed` | `principal` is NOT null AND `principal` is mapped | System manages principal lifecycle |
| `claims` | NOT `isEffectiveAnonymous()` | Identity claims list |

**Theme Attributes (only when `kind = HUMAN`):**

| Attribute | Description |
|-----------|-------------|
| `defaultLanguage` | LDML format (e.g., `en-US`) |
| `applicationLogo` | Logo filename |
| `applicationIcon` | Browser tab icon |
| `applicationTitle` | Browser title and footer |
| `applicationBackgroundImage` | Global background image |
| `primaryColor` | Primary theme color (`#rrggbbaa`) |
| `secondaryColor` | Secondary theme color |
| `textPrimaryColor` | Primary text color |
| `textSecondaryColor` | Secondary text color |
| `backgroundColor` | Background color |
| `subtitleColor` | Subtitle text color |
| `paperBackgroundColor` | Paper/card background |
| `menuOrientation` | `VERTICAL` or `HORIZONTAL` |

### ActorKind Behaviour

| ActorKind | UI Generation | Theme Page |
|-----------|---------------|------------|
| `HUMAN` | Yes | Visible |
| `SYSTEM` | No | Hidden |

### Access Page Visibility

| Page | Visible When |
|------|--------------|
| Access | Always |
| CRUD | Always |

### Access Attribute Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `name` | Always | Access grant identifier |
| `target` | Read-only | Display of target TransferObjectType |
| `accessType` | Always | `ALL` or `DERIVED` |
| `cardinality` | `accessType = DERIVED` | `0..1` or `0..*` |
| `getterExpression` | `accessType = DERIVED` | JQL expression for filtering |

### AccessType Behaviour

| AccessType | Cardinality | GetterExpression |
|------------|-------------|------------------|
| `ALL` | Fixed to `0..*` (lower=0, upper=-1) | Disabled |
| `DERIVED` | Configurable (`0..1` or `0..*`) | Enabled |

**On AccessType change:**
- When `ALL` is selected: automatically sets `lower = 0`, `upper = -1`
- When `DERIVED` is selected: cardinality becomes editable

### Access CRUD Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `createable` | `target` is NOT abstract | Allow creating instances |
| `updateable` | Always | Allow modifying instances |
| `deleteable` | Always | Allow deleting instances |
| `exportable` | Always | Allow exporting instances |

Access CRUD flags are rung 2 of the relation-CUD capability ladder. Full ladder (rungs 1–6: target outer flags, relation flag, `enabledBy` chain, parent per-instance `__updateable` / `__deletable`, filter membership invariant, LIST scope) in [relation-driven-crud-with-custom-input.md — §4](../../../best-practices/model/relation-driven-crud-with-custom-input.md#capability-ladder).

### Claim Attribute Rules

| Attribute | Description |
|-----------|-------------|
| `attribute` | Required, selected from `principal.getAllAttributes()` |
| `claimType` | Enum: `EMAIL`, `USERNAME`, `UNDEFINED` |

**Claim Validation:**
- `attribute` is NOT null (required for OK button)

**Claim Candidates:**
- Attributes are selected from the parent `ActorType.principal.getAllAttributes()`

### Anonymous vs Authenticated Behaviour

| State | Realm Group | Claims | Managed |
|-------|-------------|--------|---------|
| `isEffectiveAnonymous() = true` | AnonymousGroup shown | Hidden | Hidden |
| `isEffectiveAnonymous() = false` | RealmGroup shown | Visible | Visible |

**`isEffectiveAnonymous()` returns true when `anonymous = true` and the principal is not mapped:**
- `principal` is null: the `anonymous` flag decides.
- `principal` is set but NOT mapped: the `anonymous` flag decides.
- `principal` is mapped (`principal.mapping` is set): always false, whatever the flag. An actor with a mapped principal and `anonymous = true` is authenticated: it gets a realm, and its calls need a bearer token (401 without one).

- **Exposing an operation without login**: put the operation's transfer object (or an access to it) on an `ActorType` that is effectively anonymous (`anonymous = true` with no principal or an unmapped principal). Such an actor gets no `realm`, so `asm2keycloak` creates no realm or client for it, and the REST layer does not verify a bearer token for its paths: the call runs with no principal and no `ACTOR`. Everything reachable through that actor's accesses is public; keep them minimal and put guards in an interceptor or in the operation itself. *Verify:* access control applied to a call with no principal outside the Keycloak interceptor was not checked.
- **`isActiveExpression`**: a JQL expression on the principal entity (for example `self.active`, a boolean attribute). It is copied to the filter of the mapped actor transfer object type. The runtime resolves the actor from the token in two steps: the token's client (`azp`) selects the actor type, then the actor entity is looked up by claim (USERNAME, then EMAIL, then an identifier attribute) with a search on that actor type. An entity for which the expression is false is not found, and the call fails with `AUTHENTICATED_ENTITY_NOT_FOUND`; the same error appears when no entity matches the claim. Only actors with a mapped principal are looked up (`ActorType` without principal has no filter). *Verify:* that the actor type filter is applied inside `dao.search` for the actor lookup is assumed from the mapped-transfer-object filter.

### Visual Style Indicators

| Condition | Visual Effect |
|-----------|---------------|
| `kind = SYSTEM` | System actor style |
| `Access.target` is NOT mapped | Warning/error style |

### Context Detection Reference

| Check | True When |
|-------|-----------|
| Is Effective Anonymous | `anonymous = true` AND `principal` is NOT mapped (null or unmapped); a mapped principal is never anonymous |
| Principal Is Mapped | `principal` is NOT null AND `principal.mapping` is NOT null |
| Target Is Abstract | `Access.target.abstract = true` |

### UI Requirements on the Target TO

An `Access` with list cardinality (`upper = -1` — every `ALL` grant and any `DERIVED` grant with `cardinality="0..*"`) renders as a navigable table page. EVL therefore requires the target `TransferObjectType` to carry a `<table>` with at least one `<columns>` child; otherwise transformation fails with *"Columns are not defined for the viewable table of `<TO>`. (`<Actor>.<access>`, …)"*. The same TO may appear for multiple actors — the table is defined once on the TO and shared.

| Access cardinality | Required on target TO |
|---|---|
| `upper = 1` (single) | `<form>` (table optional) |
| `upper = -1` (list) | `<table>` with ≥ 1 `<columns>` (`<form>` optional for detail) |

The same requirement applies to any `TransferObjectType` reached via a `TabularReferenceField.dataFeature` (selector pick-lists).

**Column Selection Rules**

The generator renders every listed `DataMember` as a column; no implicit filtering. Apply these rules at modelling time:

| Rule | Rationale |
|---|---|
| Skip `BinaryType` and large-text members | Break row layout; inflate list payloads on every fetch. |
| Skip expensive derived aggregates | Surface them in the detail view instead. |
| Set `visible="false"` on technical columns (hashes, ids, durations) | Kept on the data mask for filters/export; removed from default render. |
| Lead with human-readable keys (name, code, status, date) | Table is meaningful before the user customises visibility. |

**Column element shape.** `<columns>` is typed as abstract `ui:Column`; each child must carry `xsi:type="ui:DataColumn"` and the root `<namespace:Model>` must declare `xmlns:ui`. See [ui Package – DataColumn](./ui.md).

---

## Related Documentation

- [Structure Package](./structure.md) - TransferObjectType and EntityType definitions
- [UI Package](./ui.md) - MenuItem and navigation definitions
- [Operation Package](./operation.md) - Operation access control