---
id: "state-lifecycle-operation"
title: "State Lifecycle Management via Bound Operations"
domain: "backend"
category: "operation"
score: 57.3
usage_count: 11
alternative_count: 0
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
  - park-here
  - indamedia-adtrack
  - workflow-poc
  - doors-model
---
## Description

Bound operations that manage entity state transitions through a defined lifecycle. Each operation validates the current state before performing the transition, records timestamps, and may trigger side effects. The pattern follows: (1) re-fetch entity, (2) validate state preconditions, (3) perform transition, (4) record metadata, (5) persist.

## Structure

```java
@Override
public ReturnType apply(Entity _this) throws ErrorException {
    // 1. Re-fetch for fresh state
    _this = entityDao.getById(_this.identifier()).get();

    // 2. Validate state preconditions
    if (_this.getStatus() == EntityStatus.TERMINAL) {
        throw new ErrorException(Error.builder()
            .withCode(ErrorCode.INVALID_STATE).withMessage("Already closed.").build());
    }

    // 3. Perform transition
    _this.setStatus(EntityStatus.NEXT_STATE);

    // 4. Record metadata
    _this.setTimestampOfTransition(LocalDateTime.now());

    // 5. Persist
    entityDao.update(_this);
    return result;
}
```

## Examples

### Trivia
Test entity lifecycle: CREATED -> STARTED -> FINISHED/FAILED/EXCLUDED. `StartCustomImplementation` validates contest is OPEN and test is not terminal, sets STARTED + timestamp. `SubmitCustomImplementation` validates STARTED state, calculates score/duration, sets FINISHED. `ExcludeCustomImplementation` sets EXCLUDED with PB recalculation.

### RackInspect
FaultRegistry lifecycle: DRAFT -> DONE via `FinishFaultRegistry`. Offer lifecycle: DRAFT -> DONE via `CloseOffer`. Job sheet items: status transitions (ToDone, ToInProgress, ToWontFix, ToWontStart) delegated to `JobTaskService`. Interceptors guard against DONE-state modifications (e.g., `RegistryHeaderUpdateInterceptor` blocks edits on finished registries).

### itracker
Initiative lifecycle: NEW -> REVIEW -> APPROVED/REJECTED. `SendForApproval` sets REVIEW, `Approve` calls `archiveForecast()` then sets APPROVED, `Reject` sets REJECTED. All defined as model scripts (no custom Java) but follow the same state-transition pattern. Approve triggers a side effect (forecast snapshot) before transition.

### ALBA
Product lifecycle: DRAFT -> FINALIZED -> APPROVED with bidirectional rollback (APPROVED -> FINALIZED via RevokeApproval). Five state operations: `Finalize`, `ApproveVersion`, `RevokeApproval`, `DraftNewVersion`, `AssignApproval`. Each validates state precondition (e.g., only FINALIZED can be approved) and creates an audit Event entity recording the transition.

### mlszksz-platform
Post lifecycle: DRAFT -> PUBLISHED -> EXPIRED/DELETED across 3 post types (News, Offer, Request). Publish sets publishedAt + creates feed entry. Delete does hard-delete for DRAFT, soft-delete (status=DELETED) for PUBLISHED. Expire validates validUntil date. User lifecycle: ACTIVE <-> SUSPENDED <-> DEACTIVATED with last-admin protection. Organization: ACTIVE <-> SUSPENDED.

### viterra_demo
Report lifecycle: PENDING -> SUBMITTED -> REVIEW -> ACCEPTED. Six state-transition stubs across entity-level and transfer-object-level: `Accept` (sets ACCEPTED), `Review` (sets REVIEW), `Submit` (sets SUBMITTED, returns `PartnerClosedReportTransfer`). Operations exist on both `Report` and `ReportTransfer`/`PartnerOpenReportTransfer` transfer objects.

### judo-demo-miniworkflow
Document approval workflow: IN_PROGRESS -> REVIEW_REQUESTED -> ACCEPTED/REJECTED/CLOSED. Four state operations (Accept, Reject, Close, RequestReview) each create a `DocumentHistoryEntry` recording fromState, toState, eventTime, user, and message. Validation via computed boolean attributes (`isAcceptable`, `isClosable`, `isReviewable`, `isRejectable`). CLOSED is the terminal state.

### ParkHere
Reservation lifecycle: ACTIVE -> EXPIRED (via cancel or scheduled job) or ACTIVE -> DELETED (via delete or holiday creation). `CancelReservation` validates reservation is active and within time window, sets endTime to now and status to EXPIRED. `DeleteReservation` validates reservation is future, sets status to DELETED, sends notification email. `SetPastActiveReservationToExpiredJob` batch-expires past reservations daily. Holiday creation cascades DELETED status to conflicting reservations.

### Indamedia-AdTrack
AggregatedCampaign lifecycle: ONGOING -> FINISHED. `dailyArchiveAggregatedCampaigns()` scheduled job finds campaigns with endDate < today, fetches final cost data for all tracked campaigns, and sets status to FINISHED. TrackedCampaign status managed via `UpdateCampaign` operation. Campaign spending recalculated on every state change via `recalculateSpendings()`.

### workflow-poc
Token-based state machine lifecycle managed by `WorkflowUtils.setCurrentState()` and `step()`. Tokens track current state via `tokenDao.setState(token, state)`. Transitions are event-driven: `TriggerCustomImplementation` processes events, finds matching transitions, and delegates to `WorkflowUtils.step()`. States support ON_ENTER/ON_LEAVE/ON_TRANSITION actions, auto-assignment, guard evaluation via SpEL, fork (one token to many), and join (many tokens to one). LogEntry entities record completion events.

### doors-model
Contract lifecycle: CREATED -> PENDING -> APPROVED/REJECTED -> SIGNED -> CLOSED. Multi-stage approval workflow with condition-based stage skipping (SKIP/EXECUTE), net value thresholds, and template-based approval paths. Operations `startApproval`, `setNextStage`, `approve`, `reject` are model-level expressions. `uploadSignedContract` transitions to SIGNED state.

## Trade-offs

- Pros: Clear state machine in code, validation prevents illegal transitions, timestamps provide audit trail
- Cons: State machine logic spread across multiple operation classes, PB recalculation duplicated between Submit and Exclude
- Alternative: Centralized state machine service, or model-level state machine definition

## Related Patterns

- entity-re-fetch-pattern
- typed-exception-error-handling
- data-snapshot-versioning
- audit-event-trail
