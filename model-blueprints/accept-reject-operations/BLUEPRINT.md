---
id: "accept-reject-operations"
title: "Accept/Reject Approval Operations Pattern"
score: 65.1
usage_count: 7
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - judo-demo-miniworkflow
  - trivia
  - itracker
  - doors-model
  - ams-model
  - skillmatrix-model
---
## Description

A pair of instance operations `accept` and `reject` (or `approve` and `reject`) on transfer objects representing requests that require approval. The reject operation typically takes a ModerationInput (or similar) parameter with a `reason` or `message` field. The underlying entity status transitions from VERIFIED (or PENDING or REVIEW_REQUESTED or REVIEW or NEW) to APPROVED/ACCEPTED or REJECTED. This pattern appears on registration requests, user invitation requests, document approval workflows, question moderation, initiative approval, contract approval, access confirmation requests, skill level approval, and any entity following an approval workflow. Guard attributes on the transfer object control when the operations are available. Some variants add additional state transition operations (e.g., requestReview, close, review, sendForApproval, sign, reset) alongside the accept/reject pair, enabling multi-step approval flows. Some variants include a preceding sendForApproval operation that transitions the entity into a review-eligible state before approve/reject can be invoked. Advanced variants chain multiple approval stages dynamically based on workflow configuration, with conditional auto-approval based on contract attributes. Some variants include a `reset` operation to return a decided request back to PENDING status, and a bulk `approveAll` operation on a parent entity for batch approval of all pending requests. In skill management contexts, the approve operation confirms a requested skill level matches the approved level, using a derived boolean `approved` attribute computed from comparing `approvedLevel` and `requestedLevel`.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
