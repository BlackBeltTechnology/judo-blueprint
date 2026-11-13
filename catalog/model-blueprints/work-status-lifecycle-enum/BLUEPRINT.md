---
id: work-status-lifecycle-enum
title: "Work Status Lifecycle Enum (Not Started/In Progress/Done/Won't Fix)"
description: "A four-state work item status enumeration: NOT_STARTED, IN_PROGRESS, DONE and WONT_FIX, with two terminal outcomes."
aliases: [work status, task status enum, repair work status]
keywords: [work, status, lifecycle, enum, not started, in progress, done, wont fix]
tags: ["domain:model", "layer:model", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: [draft-done-status-enum]
fragment: work-status-lifecycle-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Track the progress of a work item, such as a repair or maintenance task, through one enumeration with two ways to end: finished (DONE) or abandoned (WONT_FIX).

### Two terminal outcomes

A work item starts as NOT_STARTED, moves to IN_PROGRESS when work begins, and ends as DONE or WONT_FIX. The enumeration only names the states; it does not enforce the order.

## Structure

One enumeration, `WorkStatus`, with four members: IN_PROGRESS (ordinal 1), DONE (ordinal 2), WONT_FIX (ordinal 3) and NOT_STARTED (ordinal 4). Each owning entity has a required `workStatus` attribute of this type. The default is a design choice: IN_PROGRESS suits work that starts at once, while NOT_STARTED is the natural initial value when work is planned before it starts.

## Constraints

### Ordinals are stored and sent

Members persist by ordinal and enumerations travel as integer ordinals on the wire. Ordinals must be unique and between 0 and 9999 in the model. Do not renumber existing members. The ordinals are not in lifecycle order (NOT_STARTED has the highest ordinal), so never infer the order from the ordinal.

### The enumeration is not a state machine

Nothing in the platform stops a write of DONE over WONT_FIX. Project practice: allow changes only through operations of the owning entity. Custom operations are not seen by interceptors, so the check belongs in the operation itself.

## Variations

- Several entities in a chain (for example a work order and the work report that follows it) can each carry the same enumeration so the status is comparable across them.
- Drop WONT_FIX for the two-state form in [[draft-done-status-enum]].

## When to use

- Work items that can be dropped as well as completed, and "not started" differs from "in progress" for users or reports.

## When to avoid

- A review or approval loop is needed; use [[document-review-state-machine]].
- The status is on or off; use [[active-inactive-status-enum]].

## Related

- [[draft-done-status-enum]]: the two-state form without an abandoned outcome
- [[document-review-state-machine]]: adds review steps and history
- [[active-suspended-deactivated-status-enum]]: another small status enumeration with an inactive branch
