## Overview

The operation body that consumes the `*Input` TO converts the transient collection of picker selections into a stored relation collection on the target entity using JQL's `mutable` keyword. Without `mutable`, the entire collection is treated as transient and is **silently discarded** on operation return — the owning entity is persisted with an empty collection, no compile-time or runtime error.

## Implementation Pattern

The operation body creates (or updates) the owning entity and assigns the transient collection through `mutable input.<rel>`:

```
operation assignApproval(input: ApprovalTaskInput): Void {
  body: {
    var task := ApprovalTask!create(new ApprovalTask(
      product := self,
      assignees := mutable input.users,
      dueDate := input.dueDate
    ))
    // ...
  }
}
```

Key points:
- `input.users` is a **transient** collection of references to mapped TO instances.
- `mutable input.users` promotes each element to its corresponding stored entity reference, yielding a collection assignable to a stored relation.
- The conversion is per-element; the result preserves order and cardinality.
- For Java custom implementations, the same conversion happens through the generated DAO API (look up each transient reference, collect the resolved entities, assign as the stored collection).

## Footgun: silent discard

> ⚠️ **If the body forgets `mutable`, the entire collection is discarded silently.** The owning entity is persisted with an empty assignees collection. No compile error. No runtime error. The bug is invisible until QA notices the approval task has zero approvers.

Always:
1. Check `mutable` on every right-hand side that targets a stored collection.
2. Write an integration test that calls the operation with a non-empty picker selection and asserts the persisted collection size matches.

## Examples

### Alba
- **Operation**: `Product.assignApproval(input: ApprovalTaskInput)`
- **Body**: `mutable input.users` is assigned to the stored `assignees` relation on the new `ApprovalTask`. The filtered picker (active TEACHER / APPROVER users) ensures only eligible users reach the body.

### ActionGroupTest
- **Operation**: `Planet.createCreature(input: CreatureTemplate)`
- **Body**: `mutable input.signs` is assigned to the new `Creature`'s `signs` relation. The picker selection (zero or more `Sign` instances) is preserved on the persisted creature.
