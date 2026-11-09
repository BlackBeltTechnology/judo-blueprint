---
id: "enum-state-machine"
title: "Enum-Based State Machine Pattern"
domain: "model"
category: "enum"
score: 78.6
usage_count: 12
alternative_count: 2
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - mlszksz-platform
  - viterra_demo
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - indamedia-adtrack
  - judo-partner
  - reserve-app
alternatives:
  - derived-state-from-history
  - entity-based-state-machine
---
## Description

Entities use enumeration-typed status attributes to model lifecycle state machines. Each enum member represents a distinct lifecycle state, and named operations on the entity enforce valid state transitions by setting `this.status = EnumType#NEW_STATE`. Multiple entities in a model may each have their own independent state machines.

## Structure

- Entity has a required `status` attribute typed to a dedicated enum
- Enum members represent lifecycle states (e.g., CREATED, STARTED, FINISHED)
- Status attribute has a default value pointing to the initial state
- Instance operations implement transitions: `this.status = EnumType#TARGET_STATE`
- Derived boolean attributes may compute from status (e.g., `isClosed = self.status == CLOSED`)

## Examples

### Trivia
Three state machines: **Question** (REVIEW -> APPROVED/REJECTED, with cycle-back), **Contest** (CLOSED <-> OPEN), and **Test** (CREATED -> STARTED -> FINISHED, plus FAILED and EXCLUDED terminal states). Each transition is a simple named operation like `approve`, `open`, `start`.

### RackInspect
Three status enums: **FaultRegistryStatus** (DRAFT -> DONE), **OfferStatus** (DRAFT -> DONE), and **WorkStatus** (NOT_STARTED -> IN_PROGRESS -> DONE/WONT_FIX). WorkStatus is shared across JobSheet, JobSheetItem, and WorkReport. Transitions triggered by named operations like `finishFaultRegistry`, `closeOffer`, `statusToDone`.

### itracker
**InitiativeStatus** with 5 states: NEW -> REVIEW -> APPROVED/REJECTED, plus COMPLETE. Operations `sendForApproval`, `approve`, `reject` implement transitions. The `approve` operation chains `archiveForecast()` before status change, demonstrating side-effect composition in transitions.

### Alba
Three independent state machines: **ProductState** (DRAFT -> FINALIZED -> APPROVED, with revokeApproval back to DRAFT), **TaskState** (TODO -> APPROVED/REJECTED via `closeTask`), **AccountStatus** (PENDING_APPROVAL -> ACTIVE -> SUSPENDED). Operations `finalize`, `approveVersion`, `revokeApproval` enforce Product transitions; `closeTask` drives Task transitions. Derived booleans: `isFinalizedOrApproved`, `isActive`.

### MLSZKSZPlatform
Six independent state machines across the model: **PostStatus** (DRAFT -> PUBLISHED -> EXPIRED -> DELETED, with PENDING_REVIEW branch), **OrganizationStatus** and **UserStatus** (ACTIVE <-> SUSPENDED -> DEACTIVATED), **RegistrationRequestStatus** (PENDING -> VERIFIED -> APPROVED/REJECTED, or EXPIRED), **InvitationStatus** (same pattern as Registration), **NotificationStatus** (PENDING -> SENT/FAILED with retry). Operations: `publish`, `expired`, `delete`, `activate`, `suspend`, `accept`, `reject`.

### Viterra Demo
**ReportStatus** with 4 states: PENDING -> SUBMITTED -> ACCEPTED, plus REVIEW loopback. Partner calls `submit()` (PENDING -> SUBMITTED), admin calls `accept()` (SUBMITTED/REVIEW -> ACCEPTED) or `review()` (SUBMITTED -> REVIEW). All transitions are simple one-line operations: `this.status = viterra::ReportStatus#SUBMITTED`. Derived booleans `showAcceptButton` and `showReviewButton` control UI visibility based on status.

### KozutEugyfelClient
**BejelentesAllapot** with 2 states: AKTIV (active) and LEZART (closed). `Bejelentes.lezaras` transitions AKTIV -> LEZART, `Bejelentes.megnyitas` transitions LEZART -> AKTIV. All operations guard with `if (this.allapot == BejelentesAllapot#AKTIV)` before executing, and 6 derived `*Engedely` (permission) booleans check state + user role.

### judo-demo-miniworkflow
**DocumentState** with 5 states: IN_PROGRESS -> REVIEW_REQUESTED -> ACCEPTED/REJECTED -> CLOSED. Uniquely, the current state is not stored but derived from the latest `DocumentHistoryEntry` via `self.documentHistoryEntries!head(h | h.eventTime DESC).toState`. Four operations (`requestReview`, `accept`, `reject`, `close`) create history entries with the target state. Derived booleans (`isAcceptable`, `isClosable`, `isReviewable`, `isRejectable`) combine state checks with actor ownership.

### AMS-Model
Two parallel state machines: **Status** (PENDING -> APPROVED/REJECTED) on the abstract `Request` entity, and **CampaignStatus** (OPEN <-> CLOSED) on `Campaign`. `Request.approve()` sets `this.status = Status#APPROVED` and `this.decisionTime = Timestamp!now()`. `Campaign.open()`/`close()` toggle between OPEN and CLOSED. The `isPending = self.status == Status#PENDING` derived boolean and `Campaign` transfer's `isOpen`/`isClosed` booleans compute from status. Campaign.status defaults to `CampaignStatus#OPEN`.

### ParkHere
**ReservationStatus** with 3 states: ACTIVE, DELETED, EXPIRED. ACTIVE is the initial state after creation. ACTIVE -> DELETED via `deleteReservation`/`cancelReservation` operations or automatic holiday cancellation. ACTIVE -> EXPIRED via background job when end time passes. No recovery from DELETED or EXPIRED states. Operations manage transitions through custom implementations with `BusinessError` faults for invalid state transitions.

### IndamediaAdTrack
**CampaignStatus** with 3 states: ONGOING (default), FINISHED, DELETED. Used on both `TrackedCampaign.status` and `AggregatedCampaign.status`. ONGOING -> FINISHED when end date passes; ONGOING -> DELETED via `deleteAggregatedCampaign` or `untrack` operations. Both FINISHED and DELETED are terminal states. Status changes on AggregatedCampaign trigger `AggregatedCampaignHistory` snapshot creation.

### judo-partner
Multiple state machines across both domains: **PartnerStatus** (ACTIVE/DRAFT/DELETED) is derived from entity state (e.g., `isArchived`). **RegisterStatus** (DRAFT/OPEN/CLOSED) and **RecordStatus** (DRAFT/REGISTERED/ARCHIVED) manage the document registry lifecycle. **MigrationStatus** (DISABLED/AWAITING/MIGRATED) tracks bulk import partner migration progress. **ValidationStatus** (NOT_VALIDATED/OK/FAILED) tracks partner validation state.

### KozutEugyfelModelTest
**BejelentesAllapot** with 2 states: AKTIV and LEZART. The `lezaras` operation transitions AKTIV -> LEZART by creating a Lezaras event and setting `allapot`. Operations `tovabbitas` and `megjegyzes` guard with `allapot == AKTIV` before executing. This binary state machine controls the entire complaint lifecycle.

### ReserveApp
**FreightState** with 9 states covering a full logistics lifecycle: NOT_SUBMITTED -> SUBMITTED -> APPROVED/REJECTED/SUSPENDED -> ARRIVED -> FINISHED, plus DELAYED_UNLOADING and DELAYED_ARRIVAL for delay tracking. This is one of the most complex state machines observed, with states covering submission, approval, suspension, arrival, completion, and delay phases.

### AMS-Frontend
Two parallel state machines: **Status** (PENDING/APPROVED/REJECTED) for access requests on abstract `Request`, and **CampaignStatus** (OPEN/CLOSED) for campaigns. `approve()` sets `Status#APPROVED` + `decisionTime`, `reject()` sets `Status#REJECTED` + `decisionTime`. Campaign toggles between OPEN and CLOSED via `open()`/`close()`. Derived booleans `isPending`, `isOpen`, `isClosed` drive UI button enablement.

## Trade-offs

- Pros: Clear lifecycle visualization, transitions enforced by operations, enums are well-supported in JUDO
- Cons: No built-in guard conditions (must be coded in operation bodies), adding states requires enum changes
- Prefer when: Entities have well-defined lifecycle stages with explicit transitions

## Related Patterns

- [conditional-visibility-getter](conditional-visibility-getter.md)
- [default-value-patterns](default-value-patterns.md)
- [derived-state-from-history](derived-state-from-history.md) (alternative: state derived from audit trail)
- [entity-based-state-machine](entity-based-state-machine.md) (alternative: runtime-configurable state machine via entities)
