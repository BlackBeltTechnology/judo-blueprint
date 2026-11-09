---
id: event-log-entity
title: Event Log Entity with Type Enum and Actor Reference
description: "A non-CRUD Event entity that records domain events in a chronological log, typed by an enumeration and linked by associations to the affected entity and the acting user."
aliases: [event entity, domain event log]
keywords: [event, log, type, enum, actor, reference, timeline, association]
tags: ["domain:model", "layer:model", "layer:backend", "project:alba", "status:single-project"]
category: pattern
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: [audit-event-trail]
fragment: event-log-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Keep a chronological record of domain events, so that an entity can show its own timeline and an administrator can see what happened. Events are written by backend operations when a state changes. Users do not create, edit or delete them through generated actions.

### Events are typed by an enumeration

Each event has one value of an event-type enumeration. The enumeration is the vocabulary of events the domain can emit.

### Actor and subject are associations

The event links to the affected entity and to the acting user with optional associations. The links keep the relation to the live record, so the event can be followed to the entity and user.

## Structure

The Event entity is not createable, updateable or deleteable through generated actions. It has a required type (an enumeration value), an optional text message and a required timestamp. It has two optional associations: one to the affected entity (0..1) and one to the acting user (0..1). The affected entity has the inverse relation, a list of its events (0..*). The enumeration lists one value per event kind.

## Constraints

- Createable, updateable and deleteable are all false on the Event entity.
- The type and the timestamp are required. The type must be a value of the enumeration.
- Events are written inside the operation that changes the state. The event shares that operation's transaction, so a rollback removes it.
- Interceptors do not run for custom operations. A custom operation must write its own event.
- Associations store the id, not the name. If the user or the entity is removed, the reference is cleared, and the event text should therefore carry any name that must stay readable.

## Variations

- **Denormalized actor names.** Store the user name and the organization name as strings on the event, instead of a user association. The record then stays readable after the user is renamed or removed. See [[audit-log-entity]].
- **Notification child entities.** Each event composes child notification entities for delivery to affected users. Use this when events must be delivered, not only listed.
- **Generalization-based event hierarchy.** Replace the type enumeration with an abstract base event and concrete subtypes. The subtype carries the kind, and each subtype can add its own attributes. See [[audit-event-trail]] for the event-as-entity pattern.
- **Filtered views on the parent.** The parent entity exposes derived lists of its events, for example only comments or only forwardings. The derived lists filter the event collection by type.

## When to use

- A single entity needs a visible timeline of its lifecycle events.
- Events are a small, fixed vocabulary that the domain controls.
- The acting user and the affected entity must stay linked for navigation.

## When to avoid

- Administrators need a platform-wide audit trail with names that survive user changes. Use [[audit-log-entity]].
- The need is the value history of one entity. Use a history entry instead.
- Users must edit or delete events. Events are append-only by design.

## Related

- [[audit-log-entity]] — the audit trail with denormalized actor names, for platform-wide review
- [[audit-event-trail]] — the same need as an event entity written inside the business transaction
- [[history-audit-trail-entity]] — a per-entity history instead of one shared event table
- [[operation-call-logging-interceptor]] — logs built-in operation calls from an interceptor
- [[safe-failure-pattern]] — when a failure to write an event must not break the business operation
