## Overview

The History entity is populated by a `HistoryService` that records audit trail entries (whoDid, whatDid, whenDid) on Task entities whenever significant operations occur (creation, modification, deletion, generation, delegation, status change).

## Implementation Pattern

- `HistoryServiceImpl` is an OSGi `@Component` implementing the `HistoryService` interface with methods: `taskCreated()`, `taskModified()`, `taskDeleted()`, `taskGenerated()`, `taskDelegated()`, `taskStatusChanged()`, `taskNewVersion()`
- Each method calls the private `recordHistory(taskId, whatDid)` which: (1) retrieves the Task via `taskDao.getById()`, (2) resolves the current user's email via `actorService.getCurrentUser()`, (3) builds a `HistoryForCreate` with whoDid, whatDid, and `LocalDateTime.now()`, (4) persists via `taskDao.createHistory(task, historyEntry)`
- History recording is wrapped in a try-catch that logs but does not propagate exceptions -- audit trail failures should not break business logic
- Action descriptions use localized i18n strings from `RackInspectI18n` (e.g., `rackInspectI18n.history_task_created()`, `rackInspectI18n.history_task_delegated_to(assigneeName)`)
- The `HistoryService` is consumed by various custom operations (fault registry, offer, job task operations) that call the appropriate method after completing their business logic

## Examples

### rackinspect
- Key files: `common/utils/services/HistoryService.java`, `common/utils/services/impl/HistoryServiceImpl.java`
- Pattern: `HistoryServiceImpl` injects `TaskDao`, `ActorService`, and `RackInspectI18n`; creates History entries via `taskDao.createHistory()` composition method; silently catches exceptions to avoid disrupting business flows
- Notable: The `taskDelegated()` method includes the assignee name in the action description; all other methods use parameterless i18n strings; the `ActorService` resolves the current authenticated user for the whoDid field
- Consumed by: `CreateFaultRegistryCustomImplementation`, `DelegateFaultRegistryCustomImplementation`, `FinishFaultRegistryCustomImplementation`, `GenerateOfferDocumentCustomImplementation`, and other task-related operations
