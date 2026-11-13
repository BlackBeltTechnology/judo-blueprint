---
id: token-based-workflow-execution
title: Token-Based Workflow Execution with Fork/Join
description: A workflow or state-machine engine that tracks every active instance as a persistent token entity pointing at its current state, with fork, join, eventless transitions and lifecycle actions.
aliases: [workflow token, state machine engine, fork join workflow, token game]
keywords: [token, workflow, state machine, fork, join, transition, guard, ON_ENTER, ON_LEAVE, auto-assign, DAO, query]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: service
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [state-lifecycle-operation, correlation-based-event-chaining, spel-guard-evaluation, audit-event-trail, dao-fluent-query-filter, token-based-verification-entity]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A workflow definition (states and transitions) is data in the model. Each running workflow instance is represented by one or more `Token` entities, each holding the current state, an optional assignee, a timestamp and the last transition. Moving a token along a transition is a service method, not model logic. Fork splits a token into several, join merges them back. The persistent tokens let a workflow survive restarts.

This is a custom engine written on top of the platform DAOs. The platform provides entities, relations, DAOs and transactions; it has no workflow concept. The model side of the persistent `Token` is a plain entity ([[token-based-verification-entity]] describes a different kind of token, a verification code).

## Practice

### Token and definition entities

- `State` and `Transition` entities define the graph. A transition has guard expressions, an optional event and zero or more next states. A state can be a join state and can request auto-assignment.
- `Token` has a relation to its current state, an optional relation to the assignee, a timestamp and a relation to the last transition.
- Lifecycle actions (ON_ENTER, ON_LEAVE, ON_TRANSITION) are pluggable action operations attached to states and transitions.

### Entering a state

1. Set the current state on the token. Clear the assignee through the generated `unset` method, because the relation setter does not accept `null` ([Clearing a Relation](../../agent-docs/backend/data-access-guide.md#clearing-a-relation-unset-not-setnull)).
2. Stamp the timestamp and call `update`.
3. Auto-assign if the state asks for it.
4. Run the ON_ENTER actions.
5. Query the state's transitions without an event (`filterByHasEvent(BooleanFilter.isFalse())`, see [[dao-fluent-query-filter]]) and take each one whose guards pass. These eventless transitions fire immediately.

### Stepping along a transition

1. Evaluate the guards; stop if they fail (see [[spel-guard-evaluation]]).
2. Run ON_LEAVE of the current state and ON_TRANSITION of the transition. Log the completion ([[audit-event-trail]]).
3. Load the next states.
   - One next state: a normal move, or a join when the state is a join state.
   - Several next states (fork): create one new token per branch, enter each state, delete the original token.

```java
public void step(Token token, State current, Transition transition) {
    if (!evalGuards(transition)) return;
    executeAction(current, ActionType.ON_LEAVE, token);
    executeAction(transition, ActionType.ON_TRANSITION, token);
    logCompletion(token, current);
    List<State> next = transitionDao.queryNextStates(transition).selectList();
    if (next.size() == 1) {
        if (next.get(0).getJoinState()) join(token, next.get(0));
        else setCurrentState(token, next.get(0));
    } else {
        next.forEach(s -> setCurrentState(createNewToken(), s));
        tokenDao.delete(token);
    }
}
```

`tokenDao`, `transitionDao`, `evalGuards`, `executeAction` and `createNewToken` are example code. `queryNextStates` is the DAO query method generated for a relation or query of the model.

### Join

A join state collects tokens of the parallel branches. When the last incoming join transition has delivered a token, the tokens are merged into one. The check compares the incoming transitions of the join state with the last transition of the tokens waiting there.

### Platform behaviour to design around

- All state changes of one step must succeed or fail together: keep the whole step in one operation or service call, so an exception rolls the transaction back and no token is left half moved. A runtime exception thrown from your code reaches the client as a generic 500 unless it is a platform fault or validation exception (see [How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)).
- If the engine runs as a custom operation or service, interceptors do not run around it: they fire only for built-in operations, never for custom ones ([Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Permission checks and the completion log must be written inside the engine.
- Two concurrent steps on the same token race. Writes bump `__version`, and an update that carries a stale `__version` is rejected ([Optimistic Locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)); a service that loads and updates without the version does not get that protection. Serialise steps per workflow instance or pass the version.

### Auto-assignment

Candidates are the users that hold the roles the state allows. Users already assigned are excluded, users who previously completed a task in the same workflow are preferred, and a random pick is the fallback. This is a local policy.

## Rationale

- Persistent state tracking survives restarts and supports fork, join, guards and extensible actions.
- Costs: a database write per transition, fork/join logic that is hard to get right, no built-in timeout or deadline handling, and processing of event chains that is single-threaded ([[correlation-based-event-chaining]]).
- Alternatives: an external BPM engine, a plain enum state machine for linear flows ([[state-lifecycle-operation]]), or event sourcing with projections.

## Example

- A workflow example: a utility class implements the whole engine. State entry sets the state, clears the assignee, auto-assigns, runs ON_ENTER actions and fires eventless transitions. Stepping evaluates guards, runs ON_LEAVE and ON_TRANSITION actions, logs completion and handles single, join and fork next states. Joining compares the incoming join transitions against the last transitions of waiting tokens before merging.

## When to avoid

- The process is linear with a few states: an enum field and state operations are enough ([[state-lifecycle-operation]]).
- You need timers, deadlines or compensation: use an external workflow engine.
- Many workers will advance the same instance at once and you cannot serialise them.

## Related

- [[state-lifecycle-operation]] — simple state changes without tokens
- [[correlation-based-event-chaining]] — how follow-up events are chained
- [[spel-guard-evaluation]] — guard expressions on transitions
- [[audit-event-trail]] — completion log
- [[dao-fluent-query-filter]] — queries for eventless transitions
- [[token-based-verification-entity]] — a different kind of token entity (verification codes)
