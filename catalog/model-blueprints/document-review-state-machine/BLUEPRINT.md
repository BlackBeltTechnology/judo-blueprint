---
id: document-review-state-machine
title: Document Review State Machine with Guard Attributes
description: A document entity that moves through a review and approval cycle with a state enumeration, instance operations per transition, and guard attributes that enable or disable each transition.
aliases: [review workflow document, approval state machine]
keywords: [document, review, approval, state machine, guard attributes, transition, history]
tags: [domain:model, layer:model, project:judo-demo-miniworkflow, status:single-project]
category: pattern
status: single-project
projects: [judo-demo-miniworkflow]
evidence: [judo-demo-miniworkflow:unrecorded]
alternatives: [entity-based-state-machine]
fragment: document-review-state-machine
diagram: { kinds: [entity, enum, transfer], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Run a document through a review and approval cycle with clear state boundaries. Each transition is an operation on the document, and the UI can see which transitions are allowed right now.

## Structure

The document entity carries a `currentState` attribute of a state enumeration with five members: IN_PROGRESS (initial), REVIEW_REQUESTED, ACCEPTED, REJECTED and CLOSED. Four instance operations implement the transitions: `requestReview`, `accept`, `reject` and `close`. Four boolean guard attributes (`isReviewable`, `isAcceptable`, `isRejectable`, `isClosable`) are derived from the current state. A transfer object exposes the state and the guards, adds a negated guard for each, and maps the four transitions. The document also refers to its owner (one user, association) and to its history entries (composition).

## Constraints

- A transition is valid only from its source state. The operation checks the source state and rejects the call otherwise, with a `ValidationException` or a modeled fault declared on the operation. Guards are for the UI; the operation is the enforcement point. Hiding a button protects nothing, and interceptors do not run on custom operations, so the check cannot live in an interceptor.
- The state enumeration is the single source of truth. Never let a client write `currentState` directly.
- The reject operation takes a message input with the rejection reason, so the reason is stored with the transition.
- Each transition writes a history entry. The history is the audit trail, not the state itself.

## Variations

- **Closing from accepted or rejected.** The close transition can start from ACCEPTED or REJECTED. Keep the source list in one place so the guards and the operation agree.
- **Role-based transitions.** Only users with an approver flag may accept or reject. Check the role in the operation, and derive the guard from the same rule.
- **Creation as a static transfer operation.** A creation operation on the transfer object sets the initial state to IN_PROGRESS.

## When to use

- A document needs a review and approval cycle with more than two states.
- Transitions need guards for the UI and enforcement in the operations.
- Each transition must be recorded with who acted and why.

## When to avoid

- The item has only a draft and a done state. Use [[draft-done-status-enum]].
- The state set is open-ended or changes often. Use an entity-based state machine. See [[entity-based-state-machine]].
- Nothing needs a history. A plain enumeration is enough. See [[enum-state-machine]].

## Related

- [[draft-done-status-enum]] — the simpler two-state form for work items
- [[content-lifecycle-status-enum]] — status for published content, with a soft-delete state
- [[entity-based-state-machine]] — the alternative when states, transitions and guards are data
- [[enum-state-machine]] — the enumeration-based approach this entry uses
- [[mapped-operation-delegation]] — how transfer objects map entity operations
