---
id: freight-logistics-state-enum
title: Freight/Logistics Lifecycle State Enum
description: "A multi-state lifecycle enumeration for freight, delivery or logistics reservation workflows, covering submission, approval, arrival, completion and schedule delays."
aliases: []
keywords: [freight, logistics, lifecycle, state, enum]
tags: [domain:model, layer:model, project:reserve-app, status:single-project]
category: pattern
status: single-project
projects: [reserve-app]
evidence: ["reserve-app:unrecorded"]
alternatives: []
fragment: freight-logistics-state-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Give a freight or logistics reservation one lifecycle state that covers the whole journey, from a draft that is not yet sent to a finished unloading. The states record the handoffs between a requesting party and an approving party, the arrival at the facility, and schedule deviations.

### Lifecycle states, not a status flag

The enumeration has one value per stage. A reservation holds exactly one state at a time. Delay states sit beside the main path, so a schedule deviation is recorded without losing the stage the reservation is in.

## Structure

The enumeration has nine members, ordered by their position in the lifecycle:

- Draft and submission: NOT_SUBMITTED, SUBMITTED
- Review outcome: APPROVED, REJECTED
- Hold: SUSPENDED
- Arrival and completion: ARRIVED, FINISHED
- Schedule deviation: DELAYED_ARRIVAL, DELAYED_UNLOADING

The reservation entity holds one attribute of this enumeration type.

## Constraints

- A reservation holds exactly one member of the enumeration at a time.
- Each member has a unique ordinal.
- Member names are fixed values. Adding a member changes every consumer of the enumeration.
- The enumeration describes the state only. Who suspended a reservation is recorded on the reservation, not in the enumeration.

## Variations

- **Single status enum.** A plain ACTIVE, DELETED, EXPIRED enumeration. This fits flows without multi-party handoffs. See [[active-suspended-deactivated-status-enum]].
- **Separate delay flags.** Record delays as booleans on the reservation instead of as states. This keeps the main state machine smaller, but the delay cannot be shown as a lifecycle stage.
- **Two-sided suspension.** Record a suspension by each party as a separate relation on the reservation. The enumeration then only holds the SUSPENDED state.

## When to use

- A reservation moves through handoffs between a requester and an approver.
- Arrival and completion at a facility are tracked as stages.
- Schedule deviations must be visible without changing the stage.

## When to avoid

- The workflow has two or three states. Use a simple status enumeration.
- The states depend on more than one independent dimension. Use separate attributes instead of one enumeration.

## Related

- [[active-suspended-deactivated-status-enum]] — a simpler status enumeration with a suspension state
- [[draft-done-status-enum]] — a two-stage draft and completion enumeration
- [[document-review-state-machine]] — a review workflow with explicit transitions
- [[freight-reservation-cluster]] — the reservation entities that use this enumeration
