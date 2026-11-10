---
id: entity-change-history-snapshot
title: Entity Change History Snapshot
description: "A companion history entity that stores a snapshot of a parent entity's key attributes each time a significant change is saved, giving a dated trail of how the values evolved."
aliases: [attribute snapshot history, change snapshot]
keywords: [change, history, snapshot, versioned attributes, budget, timeline]
tags: ["domain:model", "layer:model", "layer:backend", "project:indamedia-adtrack", "status:single-project"]
category: pattern
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: [history-audit-trail-entity]
fragment: entity-change-history-snapshot
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep the values of an entity's key attributes as they were at each significant change, so that reports and compliance checks can see the value that applied at a given date. Each snapshot copies the fields and adds a timestamp.

### Snapshot copies values, not references

The history row holds copies of the attributes at that moment. A later change to the parent does not alter an earlier snapshot.

### Snapshots are written, not edited

The history entity turns off generated create, update and delete. Only backend code writes snapshots.

## Structure

The parent entity has a list of history rows (0..*). Each history row is non-CRUD and holds the copied key attributes (for example a name, a start and an end date, and budget amounts) plus a required `changed` timestamp. Each row has one required association back to its parent.

## Constraints

- Createable, updateable and deleteable are all false on the history entity.
- The `changed` timestamp is required and is set when the snapshot is taken.
- The copied fields are the fields a user can change. A field that never changes adds no value to the trail.
- Project practice: write the snapshot inside the operation that changes the parent, so both succeed or fail together. The platform gives no snapshot mechanism of its own.
- Interceptors run only for built-in operations (create, update, delete, list). A custom operation must write its own snapshot.
- Deleting the parent must also delete its snapshots. In the shown shape the history is a plain association, so nothing cascades. Making the history a composition of the parent would let the platform delete the rows with it.

## Variations

- **Snapshot on create and on update.** The first snapshot is the baseline. Each later save adds one snapshot with the new values.
- **Snapshot on significant change only.** Write a snapshot only when a chosen set of fields changes, not on every save. This keeps the trail short.
- **Interceptor for built-in operations.** A post-call interceptor writes the snapshot for built-in create and update. It does not cover custom operations, so combine it with explicit calls.
- **Generic event history.** When the need is a textual record of who did what rather than values, use [[history-audit-trail-entity]] instead.

## When to use

- Reports or billing must use the value an attribute had on a given date.
- Configuration changes (budgets, prices, terms) must be traceable.
- The entity is changed often, and the current row alone does not show how it got there.

## When to avoid

- The need is a record of actions and actors, not of values. Use [[history-audit-trail-entity]] or [[audit-log-entity]].
- The entity has many large or binary fields. Snapshot only the key fields.
- The entity is never changed after creation. A single row is enough.

## Related

- [[history-audit-trail-entity]] — a textual record of who did what, instead of attribute values
- [[audit-log-entity]] — a platform-wide audit trail with denormalized actor names
- [[event-log-entity]] — a typed event log linked to the affected entity and the acting user
- [[operation-call-logging-interceptor]] — logs built-in operation calls from an interceptor
