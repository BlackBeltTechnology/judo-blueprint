---
id: history-audit-trail-entity
title: History Audit Trail Entity (Who/What/When)
description: "A minimal non-CRUD History entity composed by a parent entity, recording who did what and when as plain text and timestamp values."
aliases: []
keywords: [history, audit, trail, who, what, when]
tags: [domain:model, layer:model, layer:backend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: history-audit-trail-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep a simple chronological log of human-readable events on a parent entity. Each event is a History row with three plain values: who acted, what was done, and when. No enumeration of action types is needed.

### Actor and action are plain text

The actor and the action are stored as strings, not as references or enum values. The row stays readable without joins, and the log needs no schema change when a new kind of event appears.

### History is composed by the parent

History rows belong to one parent entity and are removed with it. They are not shared across parents.

## Structure

The History entity is non-CRUD. It has three required attributes: the actor (a string), the action description (a string) and the timestamp of the action. It has no relations of its own.

The parent entity composes History rows through a zero-to-many composition relation.

## Constraints

- The actor, the action and the timestamp are required on every History row.
- History rows are written by backend code, not created by the generated actions.
- The timestamp is set when the event happens and is not changed later.
- The action text is free text, so it cannot be filtered by type. Use an enumeration-based entry instead if filtering by type is needed.

## Variations

- **Enumeration of actions.** Replace the free-text action with an enumeration so events can be filtered and counted. See [[audit-log-entity]].
- **Shared audit table.** Keep one log for all entities instead of a history per parent. See [[audit-log-entity]].
- **Versioned snapshots.** Store the frozen state of the parent at each event instead of a text description. See [[forecast-versioning-snapshot]] for the versioned pattern.

## When to use

- A per-entity chronological log of events is enough.
- Events are read by people, so free-text descriptions are acceptable.
- Writing the log must not require a schema change for each new event kind.

## When to avoid

- Events must be filtered, counted or reported by type. Use an enumeration-based audit entry.
- The audit must be shared across many entity types. Use a shared audit table.
- The value of each attribute at each point in time is needed. Use a snapshot instead.

## Related

- [[audit-log-entity]] — a shared audit table with an enumeration of action types
- [[entity-change-history-snapshot]] — flat attribute snapshots of one entity
- [[forecast-versioning-snapshot]] — versioned monthly snapshots composed by a parent
