---
id: shipment-state-enum
title: Shipment Lifecycle State Enum
description: "A multi-state lifecycle enumeration for reservation workflows with handoffs between two parties, covering submission, approval, arrival, completion and schedule delays."
aliases: [freight-logistics-state-enum, freight state enum, logistics lifecycle state, freight lifecycle enum]
keywords: [shipment, reservation, logistics, lifecycle, state, enum, handoff, delay]
tags: [domain:model, layer:model, project:reserve-app, status:single-project]
category: pattern
status: single-project
projects: [reserve-app]
evidence: ["reserve-app:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give a reservation one lifecycle state that covers the whole journey, from a draft that is not yet sent to a finished completion. The states record the handoffs between a requesting party and an approving party, the arrival at the site, and schedule deviations.

### Lifecycle states, not a status flag

The enumeration has one value per stage. A reservation holds exactly one state at a time. Delay states sit beside the main path, so a schedule deviation is recorded without losing the stage the reservation is in.

## Structure

The enumeration has nine members, ordered by their position in the lifecycle:

- Draft and submission: NOT_SUBMITTED, SUBMITTED
- Review outcome: APPROVED, REJECTED
- Hold: SUSPENDED
- Arrival and completion: ARRIVED, FINISHED
- Schedule deviation: DELAYED_ARRIVAL, DELAYED_COMPLETION

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
- Arrival and completion at a site are tracked as stages.
- Schedule deviations must be visible without changing the stage.

## When to avoid

- The workflow has two or three states. Use a simple status enumeration.
- The states depend on more than one independent dimension. Use separate attributes instead of one enumeration.

## Related

- [[active-suspended-deactivated-status-enum]]: a simpler status enumeration with a suspension state
- [[draft-done-status-enum]]: a two-stage draft and completion enumeration
- [[document-review-state-machine]]: a review workflow with explicit transitions
- [[capacity-reservation-cluster]]: the reservation entities that use this enumeration
