# advanced-modeling-patterns.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/advanced-modeling-patterns.md.

## 1. Architectural Patterns
- View model (dashboard): simple data TOs per item, one higher-level TO for the whole screen; contextual relations are `DERIVED`.
- The actor's `Access` targets the view-model TO, decoupling UI structure from domain structure.
- Fully user-scoped access: getters on `self` or the actor's `USER`/`ACTOR` context reach only the user's rows.

### Pattern: The View Model (Dashboard)
- Identifiers: `TransferObjectType`, `Access`, `DERIVED`, `Getter expression`, `activeReservations`.

### Pattern: Fully User-Scoped Data Access
- Access target must be mapped; getters filter by the current user row.

## 2. Security & UI Patterns
- Mapped managed principal: `ActorType.principal` → mapped TO over the entity storing the user; `ActorType.managed = true` lets the framework insert on first login and update later.
- `ActorType.<claims>` maps standard claims (`EMAIL`, `USERNAME`) to `DataMember`s on the principal TO.
- Access getters read the persisted row through the principal TO member name (not the raw `USER.*` claim).
- Principal TO conventions: createable and updatable off; limits apply to what the framework provisions.
- Role flags on the principal entity: JQL reads the flag; role-scoped access getters; menu items hidden by role.
- Dynamic menu system: multi-level permissions and tenancy in menu access.

### Pattern: Mapped Managed Principal with Claim Mapping
- Identifiers: `ActorType.principal`, `ActorType.managed`, `#_principal`, `EMAIL`, `USERNAME`, `accesspoint`, `AuthenticationInterceptor`.

### Pattern: Role Flags on the Principal Entity
- Flag read in JQL; access getters scoped by role; menu hidden by role.

### Pattern: Dynamic Menu System for Multi-Level Permissions & Tenancy

## 3. Polymorphism Patterns
- Access to an abstract base type (e.g. `VoteDefinition`): concrete types `Generalize` the base; the `Access` targets the abstract base TO.
- Creation through the base collection is platform-managed; no factory operation or custom UI needed.
- Mixed subtype lists: per-subtype `View` definitions give distinct UI metadata (`iconName`, `subTheme`).

### Pattern: Platform-Managed Polymorphic Creation
- Identifiers: `Access`, `Generalize`, `TransferObjectType`, `VoteDefinition`.

### Pattern: Differentiating Polymorphic Types in the UI
- Identifiers: `View`, `iconName`, `subTheme`, `ProTO`, `ConTO`.

## 4. Advanced JQL Concepts
- Three categories read user or session data and differ in purpose.
- `!getVariable('USER', 'claim_name')`: raw JWT claim for any actor shape; only option for token-only actors.
- `!getVariable('PRINCIPAL', 'claim_name')`: value exposed by a framework-populated principal TO (unmapped TO, stateless).
- `!getVariable('ACTOR', 'attribute_name')` and `ACTOR.*`: the actor's own attributes.

### `ACTOR` vs. `PRINCIPAL` vs. `USER` Context Variables
- Pick the category by actor shape: token-only actor → `USER`; unmapped principal TO → `PRINCIPAL`.

## 5. ESM Validator-Enforced Structural Patterns
- Rules enforced by the EVL validator (`judo-meta-esm`, `structure/*.evl`), not by the YAML vocabulary.
- Two-way relation can never be `COMPOSITION` (`TwoWayRelationIsNotComposition`).
- `AGGREGATION` on one end of a two-way relation requires `ASSOCIATION` on the other (`AggregationOnBothSidesAreNotAllowed`).
- At least one end of a two-way relation should have lower bound 0 (warning).
- Unmapped TO may have only `AGGREGATION` relations (`AggregationIfContainerIsUnmapped`).
- Usual shape: both ends of a bidirectional entity relation are `ASSOCIATION`.
- Diagnostic: do not change relation kind just to silence the message; fix the structure.
- Authoring CLI rejects `relationKind=AGGREGATION` on create and update.

### Pattern: Relation kinds per layer and the bidirectional rules
- Relation kind rules differ per layer; check the EVL rule that fires.

### Pattern: Derived-member self-binding
- Derived member self-binding rule: see the source section.

### Pattern: A MAPPED member's `required` flag must match its binding
- Required flag on a MAPPED member must agree with its binding.
- Mixin relations: match an included relation only when bindings are equal; a null mixin binding matches any. Give every mixin relation an explicit binding.

### Pattern: Mandatory UI scaffolding for operation-I/O TOs
- Operation input/output TOs need UI scaffolding views.

### Pattern: Wrapper TO for binary operation outputs
- Binary outputs use a wrapper TO.

### Pattern: Static operations container TO
- Static operations live on a container TO.

### Pattern: Attribute-level regex realized as constrained `StringType`
- Regex on an attribute is realized as a constrained `StringType`.
