---
id: "transient-relation-parameter"
title: "Transient Relation for Operation Parameters"
domain: "model"
category: "relation"
score: 45.8
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - itracker
  - actiongroup-test-react
  - alba
---
## Description

Unmapped transfer objects use transient relations (memberType=TRANSIENT) to hold collections of data that exist only during operation execution and are never persisted. This pattern creates ephemeral parameter containers for operations that accept structured input.

## Structure

- An unmapped transfer object acts as a parameter wrapper
- It contains a relation with `memberType="TRANSIENT"`
- The relation target is another transfer object representing the referenced entity
- The wrapper is used as the input type for an operation
- Transient relations can have default values (e.g., `EntityType!any()`)
- The `mutable` keyword in operation bodies converts transient references to stored

## Examples

### Trivia
`player::AnswerList` has a transient relation `answers -> player::Answer (0..*)`. The `AnswerList` is used as input for `Test.submit`, carrying a collection of individual `Answer` objects (each with `number` and `choice`). Neither AnswerList nor its answers are persisted.

### itracker
`InititativeInput` has two transient relations: `region -> Region (1..1)` with default `Region!any()` and `category -> SRTCategory (1..1)` with default `SRTCategory!any()`. The `createInitiative` operation uses `mutable input.region` and `mutable input.category` to convert transient references to stored entity references on the new Initiative.

### ActionGroupTest
`CreatureTemplate.signs` is a transient AGGREGATION relation to `Sign [0..*]` with limited behaviors (RANGE, REFRESH). Used during creature creation as part of the `Planet.createCreature(input: CreatureTemplate)` operation input, allowing sign selection in the UI without persisting the template relation itself.

### Alba
`ApprovalTaskInput.users` is a transient DERIVED relation (0..*) to User, with a range expression filtering active TEACHER and APPROVER users: `User!filter(u | u.isActive and (u.role == UserRole#TEACHER or u.role == UserRole#APPROVER))`. Used as input for `Product.assignApproval()` to select which users receive approval tasks. The transient relation provides a filtered picker for user selection.

## Trade-offs

- Pros: Clean operation signatures with structured input, no persistence overhead, supports collection parameters
- Cons: Data is ephemeral (lost after operation completes), cannot be referenced later
- Prefer when: An operation needs a structured collection input that should not be stored

## Related Patterns

- [unmapped-transfer-dto](unmapped-transfer-dto.md)
