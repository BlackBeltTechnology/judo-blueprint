## Overview

The operation body that consumes the `*Input` TO converts the transient picker selection into a stored relation on the target entity using JQL's `mutable` keyword. Without `mutable`, the reference is treated as transient and is **silently discarded** when the operation returns — the created/updated entity is persisted without the link, with no compile-time or runtime error.

## Implementation Pattern

The operation is bound to a JQL body that creates (or updates) the owning entity and assigns the transient picker selection through `mutable input.<rel>`:

```
operation createInitiative(input: InititativeInput): Initiative {
  body: Initiative!create(new Initiative(
    title := input.title,
    region := mutable input.region,
    category := mutable input.category,
    // ...other fields...
  ))
}
```

Key points:
- `input.region` is a **transient** reference to a mapped TO instance.
- `mutable input.region` promotes that transient reference to the corresponding stored entity reference — usable as the value of a stored relation on `Initiative`.
- The exact JQL surface (`mutable`, `!create`, the assignment operator `:=`) is part of the model-side body; the Java custom implementation does not need to do anything special if the body handles the conversion declaratively.
- If the operation body is implemented in Java (custom operation), the same conversion happens via the generated DAO API — the developer assigns the resolved entity reference returned by the DAO lookup of the input's transient reference.

## Footgun: silent discard

> ⚠️ **If the operation body forgets `mutable`, the transient reference is discarded silently.** The created entity ends up with no link to the picker selection. No compile error. No runtime error. The bug is invisible until QA notices the field is empty in the listing.

This is the single most expensive mistake the pattern invites. Always:
1. Check the body's right-hand side for `mutable` whenever the left-hand side is a stored relation.
2. Write an integration test that creates an instance via the operation and asserts the persisted relation is non-null and points to the expected target.

## Examples

### itracker
- **Operation**: `createInitiative`
- **Body**: assigns `region := mutable input.region` and `category := mutable input.category` on the new `Initiative`. Both transient single-select pickers persist correctly because the body uses `mutable`.
- **Failure mode**: dropping `mutable` on either assignment is the canonical reproduction of the silent-discard bug.
