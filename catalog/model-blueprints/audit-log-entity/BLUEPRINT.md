---
id: audit-log-entity
title: Audit Log Entity
description: "An append-only AuditLog entity that records who did what to which entity and when, with the actor name copied into each record so it stays readable after the user changes."
aliases: [audit trail, event log]
keywords: [audit, timestamp, immutable, history, denormalized]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [audit-event-trail]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep an immutable record of significant changes so that administrators can see who did what, to which entity, and when. Rows are written by backend code only. No user creates, edits or deletes them through the generated actions.

### Audit log is append-only

The entity turns off generated create, update and delete. Rows are written by operations that record their own action.

### Actor name is copied into the record

The user name and organization name are stored as plain attributes, so a record stays readable after the user or organization is renamed or removed. The association to the user is kept for navigation only.

## Structure

The AuditLog entity has a required timestamp, a required action type (an enumeration of the domain events), a required entity type (a string naming the type acted on), an optional entity id, an optional details text, and optional user name and organization name strings. It has one optional association to User (0..1, association kind). The enumeration lists one value per recorded event.

## Constraints

- Createable, updateable and deleteable are all false on the entity.
- Timestamp, action type and entity type are required. The action type must be a value of the enumeration.
- The denormalized names are written once, when the row is created, and are not refreshed later.
- Interceptors run only for the built-in operations (create, update, delete, list and similar); they never run for custom or script operations. A custom operation must therefore write its own audit row. An audit interceptor is an optional variation for the built-in operations only and cannot replace explicit writes in custom operations.
- The audit service, the user lookup and the audit data access class used to write rows are application code, not platform API.
- An audit row written by an interceptor is part of the operation's transaction (synchronous interceptors run inside it), so an exception from the interceptor rolls the operation back. Decide per case whether an audit failure may break the business action.

## Variations

- **Explicit calls from custom operations.** Each custom operation calls one shared audit service after its action. This is the reference implementation's approach and it covers custom operations.
- **Interceptor for built-in operations only.** A post-call interceptor writes the row for built-in create, update and delete. It never sees custom operations, so combine it with explicit calls from them.
- **Event entity inside the transaction.** Model each event as an entity with a reference to the affected entity. See [[audit-event-trail]].

## When to use

- Administrators or auditors must trace changes to domain entities.
- Records must stay readable after the acting user is renamed or deleted.
- A compliance export of the log is needed.

## When to avoid

- The need is the value history of one entity. Use a snapshot or history entry instead.
- Users must be able to edit or delete audit rows. The entity is append-only by design.
- The log grows without bound and no retention plan exists.

## Related

- [[audit-event-trail]]: the same need as an event entity written inside the business transaction
- [[event-log-entity]]: a general event log entity, without the audit-specific denormalized actor names
- [[history-audit-trail-entity]]: a per-entity history instead of one shared audit table
- [[operation-call-logging-interceptor]]: logs built-in operation calls from an interceptor
- [[safe-failure-pattern]]: when audit failures must not break the business operation
