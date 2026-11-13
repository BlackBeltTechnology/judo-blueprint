## Overview

Platform facts: the generated parent DAO offers a create method per composition relation (taking the generated create payload of the child), so a child row is written through the parent. Backend code writes History rows because the entity's own create flag is off. Clocks differ: `Timestamp!now()` in model expressions follows the platform default zone parameter, `LocalDateTime.now()` in Java follows the JVM zone. Use one of them consistently when the log is compared with other timestamps. The service, interface and i18n class names below are reference implementation code.

The History entity is populated by a `HistoryService` that records audit trail entries (whoDid, whatDid, whenDid) on Task entities whenever significant operations occur (creation, modification, deletion, generation, delegation, status change).

## Implementation Pattern

- `HistoryServiceImpl` is an OSGi `@Component` implementing the `HistoryService` interface with methods: `taskCreated()`, `taskModified()`, `taskDeleted()`, `taskGenerated()`, `taskDelegated()`, `taskStatusChanged()`, `taskNewVersion()`
- Each method calls the private `recordHistory(taskId, whatDid)` which: (1) retrieves the Task via `taskDao.getById()`, (2) resolves the current user's email via `actorService.getCurrentUser()`, (3) builds a `HistoryForCreate` with whoDid, whatDid, and `LocalDateTime.now()`, (4) persists via `taskDao.createHistory(task, historyEntry)`
- History recording is wrapped in a try-catch that logs but does not propagate exceptions -- audit trail failures should not break business logic
- Action descriptions use localized i18n strings from `AppI18n` (e.g., `appI18n.history_task_created()`, `appI18n.history_task_delegated_to(assigneeName)`)
- The `HistoryService` is consumed by various custom operations (for example create, delegate and close operations) that call the appropriate method after completing their business logic

## Examples

### Variant seen in practice
- Pattern: `HistoryServiceImpl` injects `TaskDao`, `ActorService`, and `AppI18n`; creates History entries via `taskDao.createHistory()` composition method; silently catches exceptions to avoid disrupting business flows
- Notable: The `taskDelegated()` method includes the assignee name in the action description; all other methods use parameterless i18n strings; the `ActorService` resolves the current authenticated user for the whoDid field
- Consumed by: `CreateFaultRegistryCustomImplementation`, `DelegateFaultRegistryCustomImplementation`, `FinishFaultRegistryCustomImplementation`, `GenerateOfferDocumentCustomImplementation`, and other task-related operations
