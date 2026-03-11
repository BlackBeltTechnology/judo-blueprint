---
id: "audit-event-entity"
title: "Dedicated Audit Event Entity for State Change Tracking"
domain: "model"
category: "entity"
score: 67.2
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - mlszksz-platform
  - judo-demo-miniworkflow
  - judo-partner
  - workflow-poc
---
## Description

A dedicated immutable entity records important state transitions as an audit trail. Each event captures what happened (via a category enum), who performed it (relation to the acting user), when it occurred (timestamp), and which entity was affected (relation to the target). Events are created by custom operation implementations and are never updated or deleted, providing a complete chronological history for compliance and debugging.

## Structure

- Entity with no CRUD operations (createable=false, updateable=false, deleteable=false)
- Core attributes:
  - `type`: Category enum classifying the event (e.g., CREATED, APPROVED, REJECTED)
  - `createdAt`: Timestamp recording when the event occurred
  - `message`: Optional RichText or String for additional context
- Core relations:
  - Target entity relation (e.g., `product [0..1]`): What entity was affected
  - Actor relation (e.g., `performedBy [0..1]`): Who performed the action
- Events are created inside custom operation implementations (e.g., `finalize()` creates a PRODUCT_FINALIZED event)
- The target entity has a reverse collection relation to events for audit trail display

## Examples

### Alba
`Event` entity with `type: EventType` (PRODUCT_CREATED, PRODUCT_FINALIZED, PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED), `createdAt: Timestamp`, `message: RichText`. Relations: `product [0..1]` (bidirectional with `Product.events`), `performedBy [0..1]` (one-way to User). Role-specific event transfers: `AuthorEventTransfer` and `AdminEventTransfer` provide role-scoped views of the audit trail.

### MLSZKSZPlatform
`AuditLog` entity with `actionType: AuditActionType` (32 members covering User, Organization, Post, Announcement, Registration, Invitation, Inquiry, and Moderation actions), `timestamp: Timestamp`, `details: String`, `entityType: String`, `entityId: Long`. Relations: `user [0..1]` (optional, allows system-initiated actions). Denormalized fields `userName` and `organizationName` enable direct display without joins. The 32-member `AuditActionType` enum provides comprehensive action coverage with an `exportAuditLog` operation for data extraction.

### KozutEugyfelClient
`Esemeny` (Event) entity with `esemenyTipus: EsemenyTipus` (7 members: LETREHOZAS, LAZARAS, MEGJEGYZES, TOVABBITAS, UJRESZTVEVO, MEGNYITAS, LEIRATKOZAS), `idopont: Timestamp`, `szoveg: Text`. Relations: `bejelentes` (back to parent report), `kezdemenyezo` (initiator user). Every operation (forwarding, commenting, closing, reopening, participant changes) creates a new Esemeny record, providing a complete event-sourced audit trail.

### judo-demo-miniworkflow
`DocumentHistoryEntry` entity with `fromState: DocumentState` (optional, null for initial), `toState: DocumentState` (required), `eventTime: Timestamp`, `message: Text` (optional). Relation: `user [1..1]` (who performed the action). Composed within `Document` via `documentHistoryEntries [0..*]`. Uniquely, the current state is derived from the latest history entry rather than stored separately: `currentState = self.documentHistoryEntries!head(h | h.eventTime DESC).toState`.

### judo-partner
`PartnerLog` entity with `type: LogType` (CREATE/UPDATE/DELETE), `timestamp: Timestamp`, `details: Text` (optional), `userEmail: String` (who performed the action). Relation: `partner [1..1]` (the affected partner). Derived `partnerCode` attribute flattens the partner code for display. The PartnerList dashboard transfer exposes `partnerLogs` as a derived collection for audit trail viewing.

### KozutEugyfelModelTest
`Esemeny` (Event) abstract entity hierarchy with `szoveg: Text`, `idopont: Timestamp`, and `kezdemenyezo -> Felhasznalo [0..1]` (initiator). Concrete subtypes model different event types: `Letrehozas` (creation), `Tovabbitas` (forwarding), `Lezaras` (closure), `Megjegyzes` (comment with `ertesitesiLista` notification recipients). Events use generalization instead of a type enum -- each event kind is a separate entity subtype.

### workflow-poc
`LogEntry` entity with `type: LogEntryType` (COMPLETION), `level: LogLevel` (TRACE, INFO), `timestamp: Timestamp` (default `Timestamp!now()`), `userEmail: String` (optional), `message: String` (optional). Related to `Context` via `Context.logs [0..*]`. Tracks workflow engine events like token completions. The `isUserEmailDefined` derived boolean enables conditional display of user information in the log viewer.

## Trade-offs

- Pros: Complete audit history, immutable records, supports compliance requirements, chronological tracking
- Cons: Growing event table over time, requires custom operation code to create events, additional storage overhead
- Prefer when: Domain requires tracking who did what and when, especially for approval/workflow state transitions

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (events track state transitions)
- [category-enum-pattern](category-enum-pattern.md) (EventType classifies events)
- [custom-implementation-placeholder](custom-implementation-placeholder.md) (events created in custom code)
