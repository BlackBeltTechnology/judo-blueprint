# Blueprint Mutation Conventions

Rules for writing correct GraphQL creation mutations in blueprint files. These are validated by `tests/test-blueprint-mutations.sh` and enforced in CI.

## JUDO Model CLI Overview

Blueprints use the **JUDO Model CLI** (`judo-cli`) to create ESM (Entity Structure Model) elements via GraphQL mutations. The CLI operates in a client-server architecture: a background server holds models in memory, and mutations modify the in-memory ESM. Changes can be persisted with `save` or reverted with `discard --force`.

Key facts:
- Mutations only target the **ESM** (source domain model), not derived models (PSM, ASM, RDBMS, UI)
- Elements are identified by **FQN** (Fully Qualified Name) using `::` as separator (e.g., `demo::entities::Person`)
- The CLI uses the **Input Container Pattern** — each create mutation specifies exactly ONE type slot
- All create inputs require a `container` field (parent namespace FQN) and a `name` field

## Rules

### 1. Mutation format

Every mutation must follow this exact GraphQL structure:

```graphql
mutation { create(input: { <inputType>: {
  <fields>
} }) { success fqn } }
```

The response selector must include `success` and `fqn`.

**Provide exactly ONE type slot per mutation.** Do not nest multiple type slots in a single `create(input: ...)`.

### 2. Only use supported create input types

The CLI GraphQL schema supports these `create` input types (camelCase slot names):

| Input Type | Creates | Typical Container |
|------------|---------|-------------------|
| `package` | Package (sub-namespace) | Root namespace |
| `enumerationType` | Enumeration type | Types namespace |
| `enumerationMember` | Member of an enumeration | The enum type |
| `entityType` | Entity type | Entities namespace |
| `dataMember` | Data attribute on an entity or TO | Entity or TO |
| `oneWayRelationMember` | One-way relation (no back-reference) | Entity or TO |
| `twoWayRelationMember` | Two-way relation (with back-reference) | Entity (primary side) |
| `transferObjectType` | Transfer object type | Service namespace |
| `mapping` | Entity-to-TO mapping | Both must exist |
| `generalization` | Generalization (inheritance) link | Both parent and child must exist |
| `operation` | Operation on entity or TO | Entity or TO |
| `parameter` | Parameter on an operation | The operation |

Do NOT invent input types that don't exist (e.g., `actorType`, `accessPoint`, `constraint`, `stringType`, `numericType`).

### 3. Common fields for all input types

Every create input type accepts:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `container` | String | **YES** | FQN of the parent namespace or element |
| `name` | String | **YES** | Name of the new element |

### 4. Entities must be created before their children (dependency order)

Mutations must follow **dependency order**. A container must exist before its members, and reference targets must exist before they are referenced:

1. `package` (if needed for sub-namespaces)
2. `enumerationType` (if referenced by members later)
3. `enumerationMember` (members of enums)
4. `entityType` (entities — abstract parents before children)
5. `generalization` (inheritance — both parent and child entity must exist)
6. `dataMember` (attributes on entities)
7. `oneWayRelationMember` / `twoWayRelationMember` (relations — target entity must exist)
8. `transferObjectType` (transfer objects)
9. `mapping` (entity-to-TO mapping — both entity and TO must exist)
10. `operation` (on entities or TOs — container must exist)
11. `parameter` (on operations — operation must exist)

### 5. Every blueprint MUST have a `## Creation Mutations` section

This section contains the GraphQL mutation code blocks that recreate the model fragment. Blueprints without mutations are incomplete.

### 6. Enum-like fields must be quoted strings

Fields representing enum values (like `relationKind`, `operationType`, `memberType`) require **quoted string values**, not bare GraphQL enum identifiers.

| Correct | Wrong |
|---------|-------|
| `relationKind: "ASSOCIATION"` | `relationKind: ASSOCIATION` |
| `operationType: "INSTANCE"` | `operationType: INSTANCE` |
| `memberType: "stored"` | `memberType: stored` |

### 7. Reference fields use FQN strings

References to other model elements (like `target`, `dataType`, `partner`) are set using the target element's FQN as a string value.

```graphql
# Correct: target is an FQN string
oneWayRelationMember: {
  container: "{{NAMESPACE}}::Order", name: "customer",
  target: "{{NAMESPACE}}::Customer", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
}
```

### 8. Operations require a `binding` field

Every `operation` mutation must include a `binding` field pointing to the implementation binding FQN.

| Correct | Wrong |
|---------|-------|
| `operation: { container: "...", name: "op", binding: "{{NAMESPACE}}::Entity.op" }` | `operation: { container: "...", name: "op" }` |

### 9. Placeholders use `{{UPPER_SNAKE_CASE}}`

Template variables use double braces with UPPER_SNAKE_CASE names.

| Correct | Wrong |
|---------|-------|
| `{{NAMESPACE}}` | `{namespace}` |
| `{{ENTITY_NAME}}` | `{{entityName}}` |
| `{{TYPES_NAMESPACE}}` | `$TYPES_NS` |

Standard placeholders:
- `{{NAMESPACE}}` — the project's root namespace (e.g., `MyProject`)
- `{{TYPES_NAMESPACE}}` — the types sub-namespace (e.g., `MyProject::types`)
- `{{MEASURES_NAMESPACE}}` — the measures sub-namespace (e.g., `MyProject::measures`)
- `{{ENTITY_NAME}}` — name of the entity being created
- Other `{{UPPER_SNAKE}}` tokens are auto-substituted during testing

During CI testing, placeholders are substituted with Sandbox-compatible values:
- `{{NAMESPACE}}` -> `Sandbox`
- `{{TYPES_NAMESPACE}}` -> `Sandbox::types`
- `{{MEASURES_NAMESPACE}}` -> `Sandbox::measures`
- Name-like placeholders -> `Test` + PascalCase of the token name

---

## Input Type Field Reference

### `entityType`

Creates a domain entity.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent namespace FQN |
| `name` | String | — | **Required.** Entity name |
| `abstract` | Boolean | `false` | Whether the entity is abstract |
| `createable` | Boolean | `false` | Allow create operations |
| `updateable` | Boolean | `false` | Allow update operations |
| `deleteable` | Boolean | `false` | Allow delete operations |
| `queryable` | Boolean | — | Whether the entity is queryable |
| `description` | String | — | Documentation |

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Customer",
  createable: true, updateable: true, deleteable: false
} }) { success fqn } }
```

### `dataMember`

Creates a data attribute on an entity or transfer object.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent entity/TO FQN |
| `name` | String | — | **Required.** Attribute name |
| `memberType` | String | `"stored"` (entity) / `"transient"` (TO) | `"stored"`, `"derived"`, `"mapped"`, `"transient"` |
| `required` | Boolean | `false` | Whether the attribute is required |
| `identifier` | Boolean | `false` | Whether the attribute is an identifier |
| `dataType` | String | — | FQN of the data type (e.g., `{{TYPES_NAMESPACE}}::String`) |
| `getterExpression` | String | — | JQL getter expression for derived members |
| `binding` | String | — | Self-binding FQN (auto-set for stored members) |
| `lower` | Int | — | Lower cardinality bound (0 or 1) |
| `upper` | Int | — | Upper cardinality bound (1 for single, -1 for unbounded) |

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Customer", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Customer", name: "fullName",
  memberType: "derived",
  getterExpression: "self.firstName + ' ' + self.lastName"
} }) { success fqn } }
```

### `oneWayRelationMember`

Creates a one-way relation (no back-reference on the target).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent entity/TO FQN |
| `name` | String | — | **Required.** Relation name |
| `target` | String | — | **Required.** Target entity FQN |
| `lower` | Int | `0` | Lower cardinality (0 or 1) |
| `upper` | Int | `1` | Upper cardinality (1 for single, -1 for collection) |
| `relationKind` | String | — | `"ASSOCIATION"`, `"AGGREGATION"`, `"COMPOSITION"` |
| `memberType` | String | `"stored"` (entity) | `"stored"`, `"derived"` |
| `getterExpression` | String | — | JQL expression for derived relations |
| `required` | Boolean | `false` | Whether the relation is required |

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Order", name: "customer",
  target: "{{NAMESPACE}}::Customer", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Customer", name: "orders",
  target: "{{NAMESPACE}}::Order", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### `twoWayRelationMember`

Creates a two-way relation with a back-reference partner. Only create on the **primary** side; the partner side is created automatically.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent entity FQN (primary side) |
| `name` | String | — | **Required.** Relation name on this side |
| `target` | String | — | **Required.** Target entity FQN |
| `partner` | String | — | **Required.** Name of the back-reference on the target |
| `primary` | Boolean | `true` | Whether this is the primary side |
| `lower` | Int | `0` | Lower cardinality |
| `upper` | Int | `1` | Upper cardinality |
| `relationKind` | String | — | `"ASSOCIATION"`, `"AGGREGATION"`, `"COMPOSITION"` |
| `memberType` | String | `"stored"` | Member type |

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Person", name: "address",
  target: "{{NAMESPACE}}::Address", partner: "resident",
  lower: 0, upper: 1, relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### `enumerationType`

Creates an enumeration type.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent namespace FQN |
| `name` | String | — | **Required.** Enum name |
| `description` | String | — | Documentation |

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "OrderStatus"
} }) { success fqn } }
```

### `enumerationMember`

Creates a member (value) of an enumeration.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent enum FQN |
| `name` | String | — | **Required.** Member name |
| `ordinal` | Int | — | Ordinal value |

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::OrderStatus", name: "PENDING", ordinal: 0
} }) { success fqn } }
```

### `transferObjectType`

Creates a transfer object (DTO) type.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent namespace FQN |
| `name` | String | — | **Required.** TO name |
| `abstract` | Boolean | `false` | Whether the TO is abstract |
| `queryable` | Boolean | — | Whether the TO is queryable |
| `description` | String | — | Documentation |

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "CustomerView"
} }) { success fqn } }
```

**Note:** Data members and relations on a TO default differently than on entities:
- `memberType` defaults to `"transient"` (not `"stored"`)
- `relationKind` defaults to `"AGGREGATION"` for unmapped TOs
- `operationType` defaults to `"STATIC"` (not `"INSTANCE"`)

### `mapping`

Creates an entity-to-transfer-object mapping. Both the entity and the TO must already exist.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Transfer object FQN |
| `name` | String | — | **Required.** Mapping name (usually the entity name) |
| `target` | String | — | **Required.** Entity FQN being mapped |

```graphql
mutation { create(input: { mapping: {
  container: "{{NAMESPACE}}::CustomerView", name: "Customer",
  target: "{{NAMESPACE}}::Customer"
} }) { success fqn } }
```

### `generalization`

Creates an inheritance (generalization) link. Both parent and child must exist.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Child entity/TO FQN |
| `name` | String | — | **Required.** Generalization name |
| `target` | String | — | **Required.** Parent entity/TO FQN |

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::PremiumCustomer", name: "Customer",
  target: "{{NAMESPACE}}::Customer"
} }) { success fqn } }
```

### `operation`

Creates an operation (method) on an entity or transfer object.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent entity/TO FQN |
| `name` | String | — | **Required.** Operation name |
| `binding` | String | — | **Required.** Implementation binding FQN |
| `operationType` | String | `"INSTANCE"` (entity) / `"STATIC"` (TO) | `"INSTANCE"` or `"STATIC"` |

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Customer", name: "activate",
  binding: "{{NAMESPACE}}::Customer.activate",
  operationType: "INSTANCE"
} }) { success fqn } }
```

### `parameter`

Creates a parameter on an operation. The operation must already exist.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent operation FQN |
| `name` | String | — | **Required.** Parameter name |
| `lower` | Int | — | Lower cardinality |
| `upper` | Int | — | Upper cardinality |
| `target` | String | — | Parameter type FQN |

```graphql
mutation { create(input: { parameter: {
  container: "{{NAMESPACE}}::Customer::activate", name: "input",
  target: "{{NAMESPACE}}::ActivateInput", lower: 1, upper: 1
} }) { success fqn } }
```

### `package`

Creates a sub-namespace (package).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `container` | String | — | **Required.** Parent namespace FQN |
| `name` | String | — | **Required.** Package name |

```graphql
mutation { create(input: { package: {
  container: "{{NAMESPACE}}", name: "services"
} }) { success fqn } }
```

---

## Quick Reference: Common Field Values

| Field | Valid Values | Notes |
|-------|-------------|-------|
| `relationKind` | `"ASSOCIATION"`, `"AGGREGATION"`, `"COMPOSITION"` | Always quoted strings |
| `operationType` | `"INSTANCE"`, `"STATIC"` | Always quoted strings |
| `memberType` | `"stored"`, `"derived"`, `"mapped"`, `"transient"` | Always quoted strings |
| `lower` | Integer (typically 0 or 1) | 0 = optional, 1 = required |
| `upper` | Integer (typically 1 or -1) | 1 = single, -1 = unbounded collection |
| `createable` | `true` / `false` | Unquoted boolean |
| `updateable` | `true` / `false` | Unquoted boolean |
| `deleteable` | `true` / `false` | Unquoted boolean |
| `abstract` | `true` / `false` | Unquoted boolean |
| `required` | `true` / `false` | Unquoted boolean |
| `identifier` | `true` / `false` | Unquoted boolean |
| `ordinal` | Integer (0, 1, 2, ...) | For enum members |
| `target` | FQN string | Reference to another element |
| `dataType` | FQN string | Reference to a data type |
| `binding` | FQN string | Operation implementation binding |
| `partner` | String | Partner relation name (twoWayRelationMember) |

---

## Cardinality Patterns

| Pattern | `lower` | `upper` | Meaning |
|---------|---------|---------|---------|
| 0..1 | 0 | 1 | Optional single |
| 1..1 | 1 | 1 | Required single |
| 0..* | 0 | -1 | Optional collection |
| 1..* | 1 | -1 | Required non-empty collection |

---

## Relation Kind Semantics

| Kind | Meaning | Use When |
|------|---------|----------|
| `"ASSOCIATION"` | Reference without lifecycle coupling | Independent entities referencing each other |
| `"AGGREGATION"` | Weak ownership | Parent logically groups children but doesn't control lifecycle |
| `"COMPOSITION"` | Strong ownership with lifecycle coupling | Parent owns children; deleting parent deletes children |

---

## Entity vs Transfer Object Defaults

When creating members, the CLI applies **different defaults** depending on whether the container is an entity or a transfer object:

| Field | Entity Default | Transfer Object Default |
|-------|---------------|------------------------|
| `memberType` | `"stored"` | `"transient"` |
| `relationKind` | — | `"AGGREGATION"` (unmapped TOs) |
| `operationType` | `"INSTANCE"` | `"STATIC"` |

---

## Mutation Response Format

All mutations return a result object. The response selector in blueprints must include at least `success` and `fqn`:

```graphql
{ success fqn }
```

The full response fields are:

| Field | Type | Description |
|-------|------|-------------|
| `success` | Boolean | Whether the mutation succeeded |
| `fqn` | String | FQN of the created/modified element |
| `type` | String | Element type name |
| `message` | String | Human-readable status message |

---

## Testing

Blueprints are validated by `tests/test-blueprint-mutations.sh` against a `tests/fixtures/Sandbox.model`:

1. All ```` ```graphql ```` blocks starting with `mutation` are extracted
2. `{{PLACEHOLDER}}` tokens are substituted with Sandbox-compatible values
3. Each mutation is executed via `judo-cli graphql` against the Sandbox model
4. After each blueprint, `discard --force` resets the model to original state
5. A mutation passes if the response contains `"success": true`
6. A mutation fails if the response contains `"success": false` or GraphQL errors

Run tests:
```bash
tests/test-blueprint-mutations.sh                    # test all blueprints
tests/test-blueprint-mutations.sh --blueprint <id>   # test one blueprint
```
