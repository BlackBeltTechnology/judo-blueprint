## Detection Query

Find unmapped transfer objects that carry a transient collection-cardinality relation to a mapped TO:

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%Input" } }) {
  items { fqn name
    relations(where: { memberType: { eq: "TRANSIENT" }, upper: { eq: -1 } }) {
      items { name lower upper memberType relationKind
        target { fqn name }
        rangeExpression
      }
    }
  }
} } }
```

The `upper: { eq: -1 }` filter matches the JUDO encoding of unbounded collections (`*`). Confirm the target is **mapped** with the secondary query in [`../transient-relation-single-select-input/model.md`](../transient-relation-single-select-input/model.md#detection-query).

## Creation Mutations

### 1. Mapped target TO (must already exist)

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}::services", name: "User"
} }) { success fqn } }
```

```graphql
mutation { create(input: { mapping: {
  container: "{{NAMESPACE}}::services::User", name: "User",
  target: "{{NAMESPACE}}::entities::User"
} }) { success fqn } }
```

### 2. Unmapped `*Input` wrapper TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}::services", name: "ApprovalTaskInput"
} }) { success fqn } }
```

### 3. Transient multi-select relation

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::services::ApprovalTaskInput", name: "users",
  target: "{{NAMESPACE}}::services::User",
  lower: 0, upper: -1,
  memberType: "transient",
  relationKind: "AGGREGATION"
} }) { success fqn } }
```

Use `lower: 1` for a required-non-empty collection (`1..*`).

### 4. Behaviors and range filtering

Declare `{RANGE, REFRESH}` on the relation so the generator emits `getRangeFor<rel>()` and the dialog can repaginate. The range expression narrows the selectable set — typically by status or role:

```
relations:
  - name: users
    target: services::User
    cardinality: 0..*
    memberType: transient
    behaviors: [RANGE, REFRESH]
    rangeExpression: "User!filter(u | u.isActive and (u.role == UserRole#TEACHER or u.role == UserRole#APPROVER))"
```

The Alba example above filters the picker to active TEACHER- or APPROVER-role users, enforcing the eligibility rule at the model layer. Cross-reference: [`range-expression-filtering`](../../best-practices/model/range-expression-filtering.md).

## Trade-off: unmapped target ⇒ no picker

> **Mechanical rule.** If the transient relation's target is an **unmapped** TO, the generator does **not** emit `getRangeFor<rel>()` — there is no persisted instance set to enumerate. The React frontend instead renders a **nested structured input form** (one sub-form per element) for the user to fill out. This is a different shape, not covered by this blueprint.
>
> Concrete example: Trivia's `AnswerList.answers -> Answer (0..*)` where `Answer` is unmapped. The user fills out each answer's `number` and `choice` inline; no picker dialog opens.
>
> Rationale: unmapped TOs have no persisted instance set ⇒ nothing to enumerate ⇒ no range method ⇒ no picker.

## Examples

### Alba
- **Owning TO**: `ApprovalTaskInput` (unmapped)
- **Relation**: `users -> User (0..*)`, transient DERIVED with range expression `User!filter(u | u.isActive and (u.role == UserRole#TEACHER or u.role == UserRole#APPROVER))`
- **Operation**: `Product.assignApproval()` consumes `ApprovalTaskInput`; body assigns the selected users to approval tasks via `mutable input.users`.

### ActionGroupTest
- **Owning TO**: `CreatureTemplate` (unmapped, used as operation input for `Planet.createCreature`)
- **Relation**: `signs -> Sign (0..*)`, transient AGGREGATION with explicit `{RANGE, REFRESH}` behaviors
- **UX**: the create-creature input page lets the user pick zero or more astrological signs from the persisted `Sign` set.

### Trivia (counter-example, excluded from this blueprint)
- `AnswerList.answers -> Answer (0..*)` looks structurally identical but `Answer` is **unmapped**. The frontend renders a nested form (one row per answer) rather than a picker. Covered separately under the unmapped-target shape — see the Trade-off above.
