---
id: state-transition-history-entry
title: "State Transition History Entry Entity"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - judo-demo-miniworkflow
---

## Description

A history entry entity that records state transitions on a parent entity. Each entry captures: `fromState` (the previous state, optional for the initial state), `toState` (the new state, required), `eventTime` (timestamp of the transition, required), `message` (optional commentary, e.g., rejection reason), and a `user` association (1..1) identifying who performed the transition. The entries are composed (0..* COMPOSITION) by the parent entity, forming a chronological audit trail of all state changes.

Unlike the simple History pattern (whoDid/whatDid/whenDid text fields) or the full AuditLog pattern (entityType/entityId string references), this pattern uses structured state fields and a direct user association. The fromState/toState pair makes it possible to reconstruct the complete state machine traversal path. The optional message field allows annotating transitions with context (e.g., a reviewer's rejection reason or an acceptance comment).

The transfer object projection adds a `userRepresentation` denormalized string for displaying the user's name without loading the full user relation.

This pattern is suitable for any entity with an enum-based state machine where state transitions need to be audited with who/when/what-state-change information.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%HistoryEntry%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

Look for entities with `fromState`, `toState`, and `eventTime` attributes.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}HistoryEntry",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "fromState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "toState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "eventTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "user",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "{{HISTORY_RELATION_NAME}}",
  target: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### Transfer object with denormalized user representation

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}HistoryEntryTransfer"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "fromState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "toState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "eventTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "userRepresentation"
} }) { success fqn } }
```

## Examples

### judo-demo-miniworkflow
- **Entity**: `MiniWorkflow::DocumentHistoryEntry` (non-CRUD)
  - Attributes: fromState (optional), toState (req), eventTime (req), message (optional)
  - Relations: user (1..1 ASSOC to User)
  - Composed by Document via `documentHistoryEntries` (0..* COMPOSITION)
- **Transfer Object**: `MiniWorkflow::DocumentHistoryEntryTransfer`
  - Attributes: fromState, toState (req), eventTime (req), message, userRepresentation (denormalized user name)
  - Relations: user (1..1 ASSOC)
- When a Document state transition occurs (requestReview, accept, reject, close), a new DocumentHistoryEntry is created recording fromState (previous state), toState (new state), eventTime (when), message (optional reason), and user (who)
- The message field is populated when a reject operation includes a reason via the Message input TO
- DocumentTransfer exposes `documentHistoryEntries` (0..* AGGREGATION) for viewing the full state transition timeline on the document detail page
