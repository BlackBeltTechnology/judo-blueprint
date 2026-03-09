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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
