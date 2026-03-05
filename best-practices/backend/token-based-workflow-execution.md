---
id: "token-based-workflow-execution"
title: "Token-Based Workflow Execution with Fork/Join"
domain: "backend"
category: "service"
score: 18.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - workflow-poc
---
## Description

A pattern for implementing a workflow/state machine engine using persistent token entities. Each active workflow instance is tracked through `Token` entities that carry the current state, assignee, and last transition. The engine supports fork semantics (one token splits into multiple tokens for parallel branches) and join semantics (multiple tokens merge into one when all parallel branches complete). State transitions fire lifecycle actions (ON_ENTER, ON_LEAVE, ON_TRANSITION) and automatic transitions (eventless transitions that fire immediately when guards pass).

## Structure

```java
// Set current state on a token
public void setCurrentState(Token token, State state) {
    tokenDao.setState(token, state);
    tokenDao.unsetAssignee(token);
    token.setTimestamp(LocalDateTime.now());
    tokenDao.update(token);

    if (state.getAutoAssign()) { autoAssign(token); }
    executeAction(state, ActionType.ON_ENTER, token);

    // Process immediate (eventless) transitions
    stateDao.queryTransitions(state)
        .filterByHasEvent(BooleanFilter.isFalse())
        .selectList()
        .forEach(transition -> {
            if (evalGuards(context, transition)) {
                step(token, state, transition);
            }
        });
}

// Execute a state transition
public void step(Token token, State currentState, Transition transition) {
    if (!evalGuards(context, transition)) return;

    executeAction(currentState, ActionType.ON_LEAVE, token);
    executeAction(transition, ActionType.ON_TRANSITION, token);
    logCompletion(token, currentState);

    List<State> nextStates = transitionDao.queryNextStates(transition).selectList();
    if (nextStates.size() == 1) {
        // Single next state: simple transition or join
        if (nextState.getJoinState()) { join(token, nextState); }
        else { setCurrentState(token, nextState); }
    } else {
        // Fork: delete current token, create one per branch
        nextStates.forEach(ns -> {
            Token newToken = createNewToken(context);
            setCurrentState(newToken, ns);
        });
        tokenDao.delete(token);
    }
}
```

Key elements:
- `Token` entity tracks current state, assignee, timestamp, and last transition
- Fork: transition with multiple next states deletes the current token and creates new tokens per branch
- Join: collects tokens from parallel branches; when all incoming transitions are satisfied, merges into one
- Immediate transitions: transitions without events fire automatically on state entry if guards pass
- Action delegation: ON_ENTER/ON_LEAVE/ON_TRANSITION actions executed via `ActionOperation.run()`
- Auto-assignment: assigns users based on role authorization and historical completion logs

## Examples

### workflow-poc
`WorkflowUtils` implements the full workflow engine. `setCurrentState()` handles state entry: sets state, clears assignee, auto-assigns if configured, executes ON_ENTER actions, and processes immediate transitions. `step()` handles transitions: evaluates guards, fires ON_LEAVE and ON_TRANSITION actions, logs completion, and handles single (simple/join) vs multiple (fork) next states. `join()` checks if all incoming parallel branches have arrived by comparing incoming join transitions against tokens' last transitions, then merges tokens. `autoAssign()` filters assignable users by role, excludes already-assigned users, prefers users who previously completed tasks, falls back to random selection.

## Trade-offs

- Pros: Persistent state tracking survives restarts, supports complex workflow patterns (fork/join/guards), action extensibility via pluggable operations, auto-assignment for task distribution
- Cons: Database overhead for token CRUD on every transition, fork/join logic is complex and error-prone, no built-in timeout or deadline handling, single-threaded correlation chain processing
- Alternative: External BPM engine (Camunda, jBPM), simple enum-based state machine (for linear workflows), event sourcing with projections

## Related Patterns

- state-lifecycle-operation
- correlation-based-event-chaining
- spel-guard-evaluation
- audit-event-trail
