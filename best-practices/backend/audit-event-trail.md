---
id: "audit-event-trail"
title: "Audit Event Trail via Entity-Based Event Logging"
domain: "backend"
category: "operation"
score: 67.8
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - mlszksz-platform
  - judo-demo-miniworkflow
  - park-here
  - judo-partner
  - workflow-poc
  - doors-model
---
## Description

An audit trail pattern where every significant state change creates an `Event` entity stored in the database. Events record the event type (enumeration), a human-readable message (often localized), a timestamp, a reference to the affected entity, and a reference to the user who performed the action. Events are queryable and displayable in the UI, providing a persistent, transactional audit history that is part of the same transaction as the business operation.

## Structure

```java
// After performing a state transition, create an audit event
Event event = eventDao.create(EventForCreate.builder()
    .withType(EventType.ENTITY_STATE_CHANGED)
    .withMessage("Description of what happened")
    .withCreatedAt(LocalDateTime.now())
    .withProduct(affectedEntity)
    .withPerformedBy(currentUser)
    .build());
```

Event entity fields:
- `type` -- Enumeration (PRODUCT_CREATED, PRODUCT_FINALIZED, PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED)
- `message` -- Human-readable description (can be localized)
- `createdAt` -- Timestamp of the event
- `product` -- Reference to the affected entity
- `performedBy` -- Reference to the user who triggered the action

## Examples

### ALBA
Five event types across the product lifecycle. `CreateProduct` logs `PRODUCT_CREATED` with Hungarian message "Produktum letrehozva." `Finalize` logs `PRODUCT_FINALIZED` with version number. `ApproveVersion` logs `PRODUCT_APPROVED`. `RevokeApproval` logs `PRODUCT_APPROVAL_REVOKED`. All events include timestamp, product reference, and performing user. Events are stored in the same transaction as the business operation.

### mlszksz-platform
Comprehensive AuditLogService with 20+ action types (USER_LOGIN, POST_PUBLISHED, INVITATION_SENT, REGISTRATION_SUBMITTED, etc.). Each operation calls `auditLogService.log(actionType, entityType, entityId, detailsMap)`. Auto-resolves current user/organization. Details stored as JSON. Safe failure pattern: audit log failures never propagate to break business operations. Supports CSV export for compliance.

### judo-demo-miniworkflow
`DocumentHistoryEntry` entity records every state transition with fields: `fromState` (previous DocumentState, null for initial), `toState` (new DocumentState), `eventTime` (Timestamp), `user` (who performed), `message` (optional). Each Accept/Reject/Close/RequestReview operation appends a new history entry. CreateDocument creates the initial entry with `toState=IN_PROGRESS` and no `fromState`. History entries are attached to the document via a one-to-many relation.

### ParkHere
Lightweight audit via entity fields rather than separate Event entities. Reservations track `created` (LocalDateTime UTC), `createdBy` (user name), `modified` (LocalDateTime UTC), `modifiedBy` (user name) on every state change. `CancelReservation` and `DeleteReservation` set `modified` and `modifiedBy` to current timestamp and user. `DoormanNotified` entity tracks notification timestamps for doorman email deduplication. Scheduled jobs mark `remindedBeforeStart`/`remindedBeforeEnd` flags.

### judo-partner
`PartnerLog` entity records all partner lifecycle events with `LogType` enum (CREATE, UPDATE, DELETE), user email, and partner reference. CREATE/DELETE operations create log entries directly in the custom operation class. UPDATE logging is handled by `PartnerUpdateInterceptor` in postCall, ensuring every update (even from the generated CRUD) is audited. Provides a complete audit trail for partner data changes.

### workflow-poc
`LogEntry` entities record workflow state completions. `WorkflowUtils.logCompletion()` creates a `LogEntryForCreate` with type `COMPLETION`, level `INFO`, and message (state task name or state name). Log entries are created as children of the `Context` via `contextDao.createLogs()`. User email is optionally set from the token's assignee. Logs are queried for auto-assignment preference (most recent completion by email, ordered by descending timestamp).

### doors-model
`ContractLog` entity records contract events with event type enumeration (e.g., SIGNED). The `uploadSignedContract` operation creates a `ContractLog` entry when a signed contract is uploaded, recording the SIGNED event. Approval workflow operations track stage completions with approver, financial/legal approval names and dates. The multi-stage workflow provides full audit visibility into who approved which stage and when.

## Trade-offs

- Pros: Queryable audit history, transactional consistency with business operations, supports UI display, clear event typing via enumeration
- Cons: Events grow linearly with operations (no compaction), localized messages are not easily translatable, no event aggregation or summary
- Alternative: Application log files (not queryable), external event store (Kafka, EventBridge), log-based audit (less structured)

## Related Patterns

- state-lifecycle-operation
- builder-pattern-entity-creation
- data-snapshot-versioning
