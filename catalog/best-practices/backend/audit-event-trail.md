---
id: audit-event-trail
title: Audit Event Trail via Entity-Based Event Logging
description: "Significant state changes create an event entity (type, message, timestamp, subject reference, acting user) in the same transaction as the business operation, so the audit history is queryable and shown in the UI."
aliases: [event log, history entries, audit log]
keywords: [audit, event, history, log entry, transaction, interceptor, postCall, state change]
tags: ["domain:backend", "layer:backend", "project:alba", "project:mlszksz-platform", "project:judo-demo-miniworkflow", "project:park-here", "project:judo-partner", "project:workflow-poc", "project:doors-model", "status:established"]
category: operation
status: established
projects: [alba, mlszksz-platform, judo-demo-miniworkflow, park-here, judo-partner, workflow-poc, doors-model]
evidence: ["alba:unrecorded", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/AuditLogServiceImpl.java", "judo-demo-miniworkflow:unrecorded", "park-here:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "doors-model:unrecorded"]
alternatives: [audit-log-entity]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Record who did what and when for every significant change as ordinary rows of an event entity, so the history is persistent, queryable and displayable like any other data. The event is written in the same transaction as the business change, so both succeed or both roll back. The entity shape itself is described in [[audit-log-entity]]; this practice covers how the backend writes the rows.

## Practice

### Platform base

- A custom operation injects the generated DAO of the event entity and creates the row with the generated builder (`<Entity>ForCreate.builder()...build()`, then `dao.create(...)`) ([CRUD operations](../../agent-docs/backend/data-access-guide.md#crud-operations)).
- The operation runs in one transaction. Synchronous interceptors run inside the operation's transaction too, and an exception from `preCall` or `postCall` rolls back the DAO write including earlier interceptors' writes ([ordering and combining interceptors](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).
- Interceptors fire only for built-in operations (create, update, delete, reference operations and similar). Custom, MAPPED and script operations never hit interceptors ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). An async interceptor runs outside the transaction and its exceptions are lost, so it is unsuitable for a transactional audit row.
- The acting user comes from `VariableResolver` ([[actor-resolution-variable-resolver]]).
- Use one clock for stamps and comparisons: `LocalDateTime.now()` follows the JVM zone, while `current_timestamp` in model expressions follows the platform `defaultZoneId` ([time zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones)).

### Practice notes: where the rows are written

Two places, depending on the operation kind:

- **Custom operations** write the event themselves after the state change, usually through a small service (`AuditLogService`, `logCompletion` helpers are example code).
- **Built-in create/update/delete** are audited from an `OperationCallInterceptor` `postCall`, which catches every update, including those from generated CRUD. One variant logs create and delete in the custom operations and update in an interceptor.

```java
// Example code: Event, EventDao, EventType are generated types
Event event = eventDao.create(EventForCreate.builder()
    .withType(EventType.ENTITY_STATE_CHANGED)
    .withMessage("Description of what happened")
    .withCreatedAt(LocalDateTime.now())
    .withProduct(affectedEntity)      // reference to the affected entity
    .withPerformedBy(currentUser)     // resolved acting user
    .build());
```

Typical event fields: an enumeration `type`, a human-readable `message` (possibly localized), a timestamp, a reference to the subject and a reference to the performing user.

Variants seen:

- one event entity with a type enumeration per lifecycle step;
- a history entry per transition with `fromState`, `toState`, time and user, attached to the subject by a composition relation;
- a service-based log with many action types and JSON details, whose failures must not break the business operation ([[safe-failure-pattern]]) at the price of a possibly missing audit row;
- lightweight audit through `created/createdBy/modified/modifiedBy` fields on the entity instead of separate rows.

## Rationale

- Same-transaction writes keep the audit history consistent with the data.
- Events are ordinary data: filterable, exportable and listable in generated pages.
- Cost: rows grow linearly with operations (no compaction), and every audited operation takes an extra write. Swallowing audit failures trades completeness for availability, so decide it deliberately.

## Example

One variant logs five product lifecycle event types (created, finalized, approved, approval revoked) with message, timestamp, product and performing user, each written by the corresponding custom operation. A workflow example appends a history entry with from-state, to-state, time and user for every transition. Another variant writes create and delete logs in operations and update logs in an interceptor `postCall`, so every update is covered.

## When to avoid

- When only creation and modification stamps are needed: entity fields are enough.
- When the audit must survive rollback of the business transaction, or must go to an external store: use a separate sink outside the transaction.
- Do not rely on an interceptor to audit custom operations; it never fires for them.

## Related

- [[audit-log-entity]] — entity shape of the event rows
- [[state-lifecycle-operation]] — transitions that produce events
- [[builder-pattern-entity-creation]] — how the event row is created
- [[data-snapshot-versioning]] — keeping full snapshots instead of events
- [[safe-failure-pattern]] — audit failures that must not break operations
