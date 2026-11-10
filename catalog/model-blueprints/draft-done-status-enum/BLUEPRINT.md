---
id: draft-done-status-enum
title: Draft/Done Two-State Workflow Enum
description: A two-member status enumeration, DRAFT and DONE, for an item that is prepared and then finalized, with no soft-delete state.
aliases: [draft done enum, two-state status enum]
keywords: [draft, done, two state, workflow, enum, status, finalize]
tags: [domain:model, layer:model, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: [rackinspect:unrecorded]
alternatives: [active-inactive-status-enum]
fragment: draft-done-status-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Track a document-producing item that is first assembled (DRAFT) and then finalized (DONE). The enumeration is the simplest status for that flow: the item is either still in progress or completed.

## Structure

One enumeration, `Status`, with two members: DRAFT (ordinal 0) and DONE (ordinal 1). The entity that owns the item carries a required `status` attribute of this enumeration, with DRAFT as its default. A named operation moves the item from DRAFT to DONE.

## Constraints

- Members persist by ordinal, and the ordinal is also the value on the wire (enumerations travel as integer ordinals). Ordinals must be unique and between 0 and 9999. Do not renumber them.
- There is no deletion state. If the item must be withdrawn, use a separate entity or a different enumeration. See [[content-lifecycle-status-enum]].
- Project practice: the transition belongs to one operation on the owning entity, and other code does not write the attribute directly. The platform does not enforce this. The operation is a custom operation, so no interceptor guards it.

## Variations

- **Separate enumeration per entity.** Each owning entity gets its own two-member enumeration, for example one for a registry and one for an offer. The values do not have to be shared.
- **Three-state form.** When a suspended or rejected step is needed, use [[active-suspended-deactivated-status-enum]] or [[work-status-lifecycle-enum]] instead.

## When to extend

The source project's status enums grow beyond two states: DRAFT, DONE, SUBMITTED, RETURNED and DRAFT, DONE, ACCEPTED, REJECTED. Once a review or hand-back step appears, move to [[enum-state-machine]]; this entry stays a two-state shape.

## When to use

- An item is assembled, then finalized, and no intermediate review step exists.
- Only the in-progress and completed distinction matters to users or reports.

## When to avoid

- The item needs a review or approval loop. Use [[document-review-state-machine]].
- The item can be published, unpublished or deleted. Use [[content-lifecycle-status-enum]].
- The status has a meaning other than work progress, such as on or off. Use [[active-inactive-status-enum]].

## Related

- [[content-lifecycle-status-enum]] — the draft and published form with a soft-delete state, for content
- [[document-review-state-machine]] — a richer document state machine with review and history
- [[active-inactive-status-enum]] — another two-state enumeration, for activation rather than work progress
