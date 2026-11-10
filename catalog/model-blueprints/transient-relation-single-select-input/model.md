## Detection Query

Find unmapped transfer objects that carry a transient single-cardinality relation to a mapped TO and are used as an operation input. The query below filters TOs whose name ends with `Input`, lists transient relations with `upper: 1`, and dumps the target FQN so the consumer can verify the target is mapped.

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%Input" } }) {
  items { fqn name
    relations(where: { memberType: { eq: "TRANSIENT" }, upper: { eq: 1 } }) {
      items { name lower upper memberType relationKind
        target { fqn name }
        rangeExpression
      }
    }
  }
} } }
```

To confirm the target is **mapped** (which is what makes the generator emit `getRangeFor<rel>()`), follow up with:

```graphql
{ esm { transferobjecttypes(where: { fqn: { eq: "<target-fqn>" } }) {
  items { fqn name
    mapping { target { fqn } }
  }
} } }
```

If `mapping.target.fqn` is non-null, the target is mapped — picker will render.

> **Schema note (verified 2026-05-13 on compsych-letter-demo via `__type(name:"ESM_TransferObjectType")` introspection):** `ESM_TransferObjectType.mapping` is a singular `ESM_Mapping` object, not a collection. Earlier revisions of this query used `mappings { items { ... } }` and would fail validation with *"Field 'mappings' in type 'ESM_TransferObjectType' is undefined"*. Use the singular form.

## Creation Mutations

### 1. The mapped target TO (must already exist)

If the target TO does not yet exist, create it and its entity mapping first. For an existing entity `{{NAMESPACE}}::entities::Region` mapped to TO `{{NAMESPACE}}::services::Region`:

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}::services", name: "Region"
} }) { success fqn } }
```

```graphql
mutation { create(input: { mapping: {
  container: "{{NAMESPACE}}::services::Region", name: "Region",
  target: "{{NAMESPACE}}::entities::Region"
} }) { success fqn } }
```

### 2. The unmapped `*Input` wrapper TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}::services", name: "InitiativeInput"
} }) { success fqn } }
```

### 3. The transient single-select relation

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::services::InitiativeInput", name: "region",
  target: "{{NAMESPACE}}::services::Region",
  lower: 1, upper: 1,
  memberType: "transient",
  relationKind: "AGGREGATION"
} }) { success fqn } }
```

Use `lower: 0` instead for `0..1` (optional picker).

### 4. Behaviors and range filtering

Declare `RANGE` and `REFRESH` behaviors explicitly so the generator emits `getRangeFor<rel>()` and the dialog can repaginate. A range expression narrows the selectable set:

```
relations:
  - name: region
    target: services::Region
    cardinality: 1..1
    memberType: transient
    behaviors: [RANGE, REFRESH]
    rangeExpression: "Region!filter(r | r.isActive)"
    defaultExpression: "Region!any()"
```

Cross-reference: [`range-expression-filtering`](../../best-practices/model/range-expression-filtering.md) covers the full filter-expression vocabulary (`!filter(...)`, `!sort(...)`, navigation chains).

> **Note on behaviors:** `CreatureTemplate.signs` (ActionGroupTest) states `{RANGE, REFRESH}` explicitly. Some catalog summaries (e.g. itracker's `InititativeInput.region`) omit the behavior list — the generator may default `RANGE` for transient relations whose target is a mapped TO, but the safe and explicit shape is to declare `{RANGE, REFRESH}`.

## Examples

### itracker
- **Owning TO**: `InititativeInput` (unmapped)
- **Relation**: `region -> Region (1..1)`, `memberType=TRANSIENT`, `defaultExpression="Region!any()"`
- **Operation**: `createInitiative` consumes `InititativeInput`; body uses `mutable input.region` to convert the picker selection to a stored reference on the new `Initiative`.
- **Sister relation**: `category -> SRTCategory (1..1)` (same shape, second single-select picker on the same input).
