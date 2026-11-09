## Overview

The task list with checkout/release pattern is backed by a shared `WorkflowUtils` utility service that implements the auto-assignment, assignee management, and guard evaluation logic that powers the checkout, release, assign, and execute task lifecycle operations. While the individual token operations (checkout, release, assign, execute, navigate) are model-defined in this project, the underlying engine logic -- state transitions, auto-assignment with preference-based selection, and authorization checks -- is implemented in custom Java.

## Implementation Pattern

- **Auto-assignment**: The `WorkflowUtils.autoAssign()` method is called on every state entry (`setCurrentState`). It filters assignable users against authorized users (intersection of context-level assignables and token-level authorized users), then selects a preferred assignee based on completion log history (most recent completer who is not already assigned elsewhere) with random fallback if no preference match is found.
- **Authorization check**: The `TriggerCustomImplementation.isTransitionAllowed()` method checks `transition.getIsHuman()` against `token.getIsAssigneeLogged()` -- human transitions require an assignee to be logged in, enforcing the checkout-before-execute constraint.
- **Assignee clearing on transition**: `WorkflowUtils.setCurrentState()` calls `tokenDao.unsetAssignee()` on every state change, ensuring the checkout/release cycle resets when a task moves to a new state.
- **Completion logging**: `WorkflowUtils.logCompletion()` records the assignee's email in a `LogEntry` of type `COMPLETION` after each transition, providing the audit trail visible through the Task TO's `logEntries` relation and enabling the preference-based auto-assignment algorithm.
- **Guard evaluation for task operations**: Transition guards are evaluated via Spring SpEL before any `step()` call, using `ContextAttribute` key-value pairs as expression variables. This controls which execute actions are available on a given task.
- **Model-defined task operations**: The checkout, release, assign, execute, and navigate operations on Token are model-defined (not custom Java), but they delegate to the model-level scripts that interact with the entities managed by the custom Java engine (e.g., setting/unsetting assignee, triggering transitions).
- **DI wiring**: `WorkflowUtils` is an OSGi `@Component` injecting `ContextDao`, `TokenDao`, `StateDao`, `TransitionDao`, `LogEntryDao`, `ActionOperation`, and `WorkflowVersionDao`.

## Examples

### workflow-poc
- Key files: `custom/workflow/utils/WorkflowUtils.java` (auto-assign, step, completion logging), `custom/.../entities/token/TriggerCustomImplementation.java` (authorization check, event processing)
- Pattern: `WorkflowUtils` provides `autoAssign()` with a two-stage selection algorithm: (1) filter assignable users against authorized users, (2) find preferred assignee from completion log history ordered by descending timestamp, excluding already-assigned users, with random fallback. `TriggerCustomImplementation` enforces `isHuman`/`isAssigneeLogged` authorization before allowing transitions.
- Notable: The auto-assignment preference algorithm queries `LogEntry` entities filtered by `COMPLETION` type and `isUserEmailDefined=true`, ordered by descending timestamp, to find the most recently active user who is eligible but not currently assigned to another task in the same context. This enables "sticky assignment" where returning users get their familiar tasks.
- DI: `WorkflowUtils` injects 7 services; `TriggerCustomImplementation` injects `TokenDao`, `StateDao`, `EventDao`, and `WorkflowUtils`.
