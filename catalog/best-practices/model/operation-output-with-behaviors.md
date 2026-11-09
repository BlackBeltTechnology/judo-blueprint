---
id: "operation-output-with-behaviors"
title: "Operation Output with CRUD Behaviors"
domain: "model"
category: "operation"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

An operation's output parameter can specify CRUD behaviors (REFRESH, UPDATE, DELETE) on the returned entity, enabling the UI to immediately operate on the result without navigating away. This creates an OPERATION_OUTPUT_UPDATE page type where the returned entity is both displayed and editable, combining operation result display with inline entity management.

## Structure

- Operation defines an `output` parameter targeting an entity transfer type
- Output parameter includes `behaviours`: REFRESH, UPDATE, DELETE (or a subset)
- The framework generates an OPERATION_OUTPUT_UPDATE page type for the result
- The returned entity is a live reference that supports further CRUD operations
- UI presents the output with action buttons corresponding to the specified behaviors

```xml
<operations name="chooseTheMessiah">
  <output name="output" target="Creature">
    <behaviours>REFRESH</behaviours>
    <behaviours>UPDATE</behaviours>
    <behaviours>DELETE</behaviours>
  </output>
</operations>
```

## Examples

### ActionGroupTest
`Planet.chooseTheMessiah()` returns a `Creature` output with REFRESH, UPDATE, and DELETE behaviors. The UI generates an OPERATION_OUTPUT_UPDATE page that displays the chosen creature's attributes and allows immediate editing or deletion. This is the only OPERATION_OUTPUT_UPDATE page in the model (vs 3 standard OPERATION_OUTPUT pages for loveGod, hateGod, and chooseTheMessiah's view-only variant).

## Trade-offs

- Pros: Seamless workflow from operation result to entity management, no extra navigation step, declarative behavior specification
- Cons: Only applicable when the output is a single entity reference, behaviors are fixed (not conditional)
- Prefer when: An operation returns an entity that the user is likely to want to edit or manage immediately

## Related Patterns

- [unmapped-transfer-dto](unmapped-transfer-dto.md) (for operations returning non-entity data)
- [mapped-operation-delegation](mapped-operation-delegation.md)
