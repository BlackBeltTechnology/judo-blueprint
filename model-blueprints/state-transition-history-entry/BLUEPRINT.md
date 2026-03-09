---
id: "state-transition-history-entry"
title: "State Transition History Entry Entity"
score: 16.0
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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
