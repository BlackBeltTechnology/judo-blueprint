---
id: ongoing-finished-deleted-status-enum
title: Ongoing, Finished and Deleted Status Enum
description: A three-state status enumeration for time-bounded entities, with members ONGOING, FINISHED and DELETED.
aliases: [campaign-lifecycle-status-enum, campaign status, operational status enum, lifecycle status enum]
keywords: [time-bounded, lifecycle, status, enum, ongoing, finished, deleted]
tags: [domain:model, layer:model, layer:backend, project:indamedia-adtrack, status:single-project]
category: pattern
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: [content-lifecycle-status-enum, active-suspended-deactivated-status-enum]
fragment: ongoing-finished-deleted-status-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Track where a time-bounded entity is in its life: it is running, it has concluded, or it has been removed. The status is one enumeration, so a query or a screen can filter on it without string matching.

### Status moves forward through services

The status changes when a service runs a transition, either from a user operation or from a scheduled job. The model stores the value and the enumeration. It does not enforce a state machine.

### Deleted is a status, not a removal

DELETED marks an activity as removed while keeping its history. Hard deletion is a separate operation that cascades to children.

## Structure

The ActivityStatus enumeration has three members: ONGOING (ordinal 0), FINISHED (ordinal 1) and DELETED (ordinal 2). Activity has a required name identifier and a required status, which defaults to ONGOING. Activity owns TrackedActivity children through a composition (0..*). TrackedActivity has its own required status of the same enumeration.

## Constraints

- Values are stored as ordinals. Each member has an explicit ordinal that must be unique within the enumeration and between 0 and 9999 (JSL models). Changing an ordinal changes the stored meaning, so new members get a new, unused ordinal.
- The status is required on both Activity and TrackedActivity.
- The enumeration has no operations or relations. Transition rules live in application services.
- Interceptors run only for built-in operations. Custom, mapped and script operations are never intercepted, so a transition's rule must be checked inside the operation or service that performs it.

## Variations

- **Soft delete with a status.** DELETED is set and the row stays. Filters must exclude DELETED explicitly.
- **Hard delete with cascade.** A delete operation removes the activity and its children. DELETED is then unused.
- **Automatic finish by a job.** A scheduled job moves ONGOING activities whose end date has passed to FINISHED.
- **Status only on the owner.** Children without their own status follow the owner. This is simpler when the children never change state alone.

## When to use

- An entity, such as a project or a subscription, has an active period with a defined end.
- Screens and reports must filter by running, finished or removed.
- A scheduled job must find entities whose state is due for change.

## When to avoid

- The workflow has many states or branches. Use a workflow or state-machine blueprint instead.
- The value is editorial (draft and publish). See [[content-lifecycle-status-enum]].
- Access must be switched on and off, with suspension that can be reversed. See [[active-suspended-deactivated-status-enum]].

## Related

- [[content-lifecycle-status-enum]]: the editorial draft and publish status, a different lifecycle
- [[active-suspended-deactivated-status-enum]]: a status for accounts that can be suspended and reinstated
- [[active-inactive-status-enum]]: the simplest two-state status, for comparison
