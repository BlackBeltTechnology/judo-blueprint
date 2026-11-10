---
id: accept-reject-operations
title: Accept/Reject Approval Operations
description: "A pair of operations, accept and reject, that move a request that needs approval from a pending state to a decided state, with the rejection reason passed as input."
aliases: [approve reject, approval operations, decision operations]
keywords: [accept, reject, approval, decision, status transition, moderation]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, project:judo-demo-miniworkflow, project:trivia, project:itracker, project:doors-model, project:ams-model, project:skillmatrix-model, status:established]
category: pattern
status: established
projects: [mlszksz-platform, judo-demo-miniworkflow, trivia, itracker, doors-model, ams-model, skillmatrix-model]
evidence: ["mlszksz-platform:unrecorded", "judo-demo-miniworkflow:unrecorded", "trivia:unrecorded", "itracker:unrecorded", "doors-model:unrecorded", "ams-model:unrecorded", "skillmatrix-model:unrecorded"]
alternatives: [state-lifecycle-operation]
fragment: accept-reject-operations
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give a request that needs a decision two explicit operations, one to accept it and one to reject it. Each operation changes the status of the request once. The reject operation takes a reason, so the decision is recorded with its explanation.

### Accept and reject are the only decision steps

Both operations act on a request that is still open. Accept sets the status to approved and reject sets it to rejected. Neither can run on a request that has already been decided, unless a reset operation exists to return it to the open state.

### The rejection reason is an input

The reject operation takes a small input transfer object with one text attribute. The reason is not stored on the status; it is passed to the operation and written to the request or to an audit record by the custom implementation.

## Structure

A Request entity has a required title, a required status (an enumeration with the values PENDING, APPROVED and REJECTED), an optional decision time (timestamp) and an optional association to a User (0..1, association kind). The Request entity has two instance operations, accept and reject. Reject takes a RejectInput transfer object with one text attribute. A RequestTO transfer object maps the Request entity and exposes the accept and reject operations to the UI.

## Constraints

- The status enumeration has one initial value (pending) and two decided values (approved and rejected).
- The accept and reject operations change the status only from the pending value. Any other current status is an invalid transition and must be refused by the custom implementation.
- Accept and reject are custom operations. The status check and the state change are written in the operation's own implementation.
- The rejection reason is required input for reject when the domain needs one. Make it a required attribute on RejectInput in that case.
- Guard attributes on the transfer object decide when each operation is shown. They are boolean derived attributes computed from the status, bound to the operation button as enabled or hidden conditions, and they do not replace the check in the implementation.
- A refused transition is reported as a business fault declared on the operation (HTTP 422 with the fault type in the response header), not as a generic error.

## Variations

- **Accept and reject with a reason.** Reject takes RejectInput. This is the most common form.
- **Approve and reject.** The same pair under the name approve. The meaning is unchanged.
- **Extra steps before the decision.** A send-for-review or send-for-approval operation moves the request into a state where accept and reject are allowed. See [[state-lifecycle-operation]] for the status flow.
- **Reset to pending.** A reset operation returns a decided request to pending so it can be decided again.
- **Bulk decision.** A bulk approve operation on a parent entity applies accept to every pending child. Each child is checked on its own.
- **Multi-stage approval.** Accept moves the request to the next approval stage instead of to the final approved state. This needs a stage entity and routing rules.

## When to use

- A request must be approved or rejected by a person, and the decision must be recorded with a reason.
- The approval has one or two decided outcomes.
- The UI must show accept and reject only while the request is open.

## When to avoid

- The decision is a plain yes/no flag with no status history. A boolean attribute is enough.
- Interceptors are expected to enforce the transition. Interceptors do not run for custom operations, so the check must be in the operation itself.
- The request changes status through many steps with rules between them. Use a full state machine instead.

## Related

- [[state-lifecycle-operation]] — the status flow the accept and reject steps belong to
- [[active-inactive-status-enum]] — a two-value status enumeration for the simpler case
- [[active-suspended-deactivated-status-enum]] — a three-value lifecycle status for comparison
- [[toggle-active-operation]] — a single toggle operation instead of a decision pair
- [[audit-log-entity]] — records each decision with the acting user
