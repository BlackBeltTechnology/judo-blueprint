---
id: "document-review-state-machine"
title: "Document Review State Machine with Guard Attributes"
score: 16.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - judo-demo-miniworkflow
---
## Description

A Document entity that implements a multi-step review/approval state machine using a state enum, boolean guard attributes, and state-transition operations. The document carries a `currentState` attribute typed to a DocumentState enum with five states: IN_PROGRESS (initial draft), REVIEW_REQUESTED (submitted for review), ACCEPTED (approved by reviewer), REJECTED (declined by reviewer), and CLOSED (finalized). Four instance operations implement the state transitions: `requestReview` (IN_PROGRESS -> REVIEW_REQUESTED), `accept` (REVIEW_REQUESTED -> ACCEPTED), `reject` (REVIEW_REQUESTED -> REJECTED), and `close` (ACCEPTED -> CLOSED or REJECTED -> CLOSED).

Boolean guard attributes on the entity (isAcceptable, isRejectable, isReviewable, isClosable) are derived from the current state and control which operations are available. The transfer object adds negation attributes (isNotAcceptable, isNotRejectable, isNotReviewable, isNotClosable) for disabling UI buttons when the operation is not allowed.

The document carries a `referenceNumber` identifier, an `ownerRepresentation` denormalized string showing the owner's name, and an `owner` association (1..1) back to a User entity. The reject operation takes a Message input TO with a `message` field for providing rejection reasons. A createDocument static operation on the transfer object creates new documents with initial IN_PROGRESS state.

This pattern is suitable for any entity that requires a review/approval cycle with clear state boundaries and role-based transition permissions.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Document%" } }) {
  items { fqn name
    attributes { items { name } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { like: "%DocumentState%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

### DocumentState enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}State"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}State", name: "IN_PROGRESS", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}State", name: "REVIEW_REQUESTED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}State", name: "ACCEPTED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}State", name: "REJECTED", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}State", name: "CLOSED", ordinal: 5
} }) { success fqn } }
```

### Document entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "referenceNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "currentState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "ownerRepresentation"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "isAcceptable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "isClosable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "isReviewable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "isRejectable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "owner",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### State transition operations

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "requestReview",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "accept",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "reject",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "close",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}"
} }) { success fqn } }
```

### Transfer object with guard negations

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}Transfer"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Transfer", name: "isNotAcceptable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Transfer", name: "isNotRejectable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Transfer", name: "isNotReviewable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Transfer", name: "isNotClosable"
} }) { success fqn } }
```

### Message input TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "Message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Message", name: "message"
} }) { success fqn } }
```

## Examples

### judo-demo-miniworkflow
- **Document entity**: `MiniWorkflow::Document` (non-CRUD)
  - Attributes: referenceNumber (req), currentState, ownerRepresentation, isAcceptable, isClosable, isReviewable, isRejectable
  - Relations: files (0..* COMPOSITION to Files), documentHistoryEntries (0..* COMPOSITION to DocumentHistoryEntry), owner (1..1 ASSOC to User)
  - Operations: requestReview (INSTANCE), accept (INSTANCE), reject (INSTANCE), close (INSTANCE)
- **DocumentState enum**: `MiniWorkflow::DocumentState` -- REVIEW_REQUESTED(1), ACCEPTED(2), REJECTED(3), IN_PROGRESS(4), CLOSED(5)
  - State transitions: IN_PROGRESS -> REVIEW_REQUESTED -> ACCEPTED/REJECTED -> CLOSED
- **DocumentTransfer TO**: `MiniWorkflow::DocumentTransfer`
  - Attributes: referenceNumber (req), currentState, ownerRepresentation, plus guard attributes (isAcceptable, isClosable, isRejectable, isReviewable) and their negations (isNotAcceptable, isNotClosable, isNotRejectable, isNotReviewable)
  - Relations: files (0..* AGGREGATION), documentHistoryEntries (0..* AGGREGATION), owner (1..1 ASSOC)
  - Operations: createDocument (STATIC), accept (MAPPED), close (MAPPED), reject (MAPPED), requestReview (MAPPED)
- **NewDocument TO** (unmapped): referenceNumber -- input for createDocument
- **Message TO** (unmapped): message -- input for reject operation (rejection reason)
- **User entity**: `MiniWorkflow::User` with approver (default: false) boolean, used to control who can accept/reject documents
