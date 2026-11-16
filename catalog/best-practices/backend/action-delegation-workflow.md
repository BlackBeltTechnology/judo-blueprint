---
id: action-delegation-workflow
title: Action Delegation via Entity-Bound Operations
description: "Workflow side effects (on state entry, exit or transition) are modeled as action entities with a bound run operation, so the engine only dispatches and new action types need no engine change."
aliases: [workflow actions, pluggable actions]
keywords: [action, delegation, bound operation, workflow, custom implementation, dispatch]
tags: ["domain:backend", "layer:backend", "project:workflow-poc", "status:single-project"]
category: service
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: [service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A workflow engine must run side effects when a token enters or leaves a state or follows a transition. Instead of hardcoding them in the engine, each action is an entity with a bound `run` operation. The engine looks up the action linked to the state or transition and calls the generated operation interface; the concrete behaviour lives in the operation's custom implementation.

## Practice

### Platform base

- A bound operation on an entity gets a generated operation interface. When the operation is custom, you write an OSGi component `<Op>CustomImplementation` that implements it and receives the bound instance (`_this`) and the input transfer object ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)).
- Custom operations are OSGi services, so another component can inject the generated interface with `@Reference` and call it ([data access guide](../../agent-docs/backend/data-access-guide.md#injecting-daos-and-services)).
- A concrete action type that overrides an abstract inherited `run` must be marked `stateful`, and the flag must match every overload ([rules for custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).
- Interceptors and write guards do not fire for custom operations, so any permission check belongs inside the implementation ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

### Practice notes: actions as pluggable entities

This layer is a convention built on the platform, not a platform feature:

- Model an action entity with optional single relations from `State` (on enter, on leave) and from `Transition`; each action type is a subtype with its own `run` implementation.
- The engine resolves the action for the current event through DAO relation queries and calls the generated `run` interface with a small input carrying a correlation id and the token id. The action re-loads whatever it needs from that id.
- Adding an action type means adding an entity subtype and its implementation; the engine is untouched.

```java
// Example code: ActionOperation is the generated interface, WorkflowUtils is a helper class
@Reference
private ActionOperation actionOperation;

private void executeAction(Object target, ActionType type, Token token) {
    Optional<Action> actionOptional = getAction(type, target);
    actionOptional.ifPresent(action -> {
        ActionInput input = ActionInput.builder()
            .withCorrelationID(getCorrelationID())
            .withTokenID(token.getTokenID())
            .build();
        actionOperation.run(action, input);
    });
}

private Optional<Action> getAction(ActionType type, Object target) {
    // the code wrapped the relation queries in Optional; check the generated
    // DAO signature, single-valued relation queries may return the entity directly
    return switch (type) {
        case ON_LEAVE      -> Optional.ofNullable(stateDao.queryOnLeave((State) target));
        case ON_TRANSITION -> Optional.ofNullable(transitionDao.queryOnTransition((Transition) target));
        case ON_ENTER      -> Optional.ofNullable(stateDao.queryOnEnter((State) target));
    };
}

// Pluggable action implementation (one class per action type)
@Component(immediate = true, service = Run.class)
public class RunCustomImplementation implements Run {
    @Reference TokenDao tokenDao;
    @Reference ContextDao contextDao;

    @Override
    public void accept(Action2 _this, ActionInput input) {
        Token token = tokenDao.query()
            .filterByTokenID(StringFilter.equalTo(input.getTokenID()))
            .selectOne().get();
        Context context = tokenDao.queryContext(token);
        context.setLabel("Updated by action");
        contextDao.update(context);
    }
}
```

## Rationale

- The engine and the business effects are separated: the engine only knows the generated interface.
- Actions are ordinary custom operations, so they can use DAOs and services like any other operation.
- The correlation id passed on lets actions take part in the event chain ([[correlation-based-event-chaining]]).
- Cost: indirect dispatch (entity, generated interface, implementation) makes tracing harder, and the input carries only the correlation and token ids.

## Example

A utility method checks for an on-enter, on-leave or on-transition action through DAO relation queries and, when one exists, calls `run` with the correlation id and token id. One concrete action loads the token by id, reads its context, changes the context label and persists it. The action's own changes can raise further events in the same correlation chain.

## When to avoid

- When there are one or two fixed side effects: a direct method call in the engine is simpler.
- When actions must be configured at runtime without deployment: a scripting or expression approach fits better ([[spel-guard-evaluation]]).

## Related

- [[custom-operation-osgi-component]] — how each action's implementation is registered
- [[token-based-workflow-execution]] — the engine that dispatches the actions
- [[correlation-based-event-chaining]] — correlation id carried into actions
- [[service-delegation-pattern]] — alternative delegation to plain services
