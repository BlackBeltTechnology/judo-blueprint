---
id: "action-delegation-workflow"
title: "Action Delegation via Entity-Bound Operations"
domain: "backend"
category: "service"
score: 43.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - workflow-poc
---
## Description

A pattern where workflow actions (side effects that execute on state entry, exit, or transition) are modeled as entities with a `run` operation rather than hardcoded in the engine. Action entities (e.g., `Action`, `Action1`, `Action2`) each have a `RunCustomImplementation` that performs domain-specific logic. The workflow engine dispatches action execution through a generated `ActionOperation` interface, allowing new action types to be added by creating new entity types with `run` operations, without modifying the engine.

## Structure

```java
// Workflow engine delegates to ActionOperation interface
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
    return switch (type) {
        case ON_LEAVE      -> stateDao.queryOnLeave((State) target);
        case ON_TRANSITION -> transitionDao.queryOnTransition((Transition) target);
        case ON_ENTER      -> stateDao.queryOnEnter((State) target);
    };
}

// Pluggable action implementation
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

Key elements:
- Three action types: ON_ENTER (state entry), ON_LEAVE (state exit), ON_TRANSITION (during transition)
- Actions are linked to states/transitions as optional relations
- `ActionOperation.run()` is the generated dispatch interface
- `ActionInput` carries `correlationID` and `tokenID` for context resolution
- Each action type has its own `CustomImplementation` class
- New action types can be added without modifying the engine

## Examples

### workflow-poc
`WorkflowUtils.executeAction()` checks for ON_ENTER, ON_LEAVE, and ON_TRANSITION actions via DAO relation queries (`stateDao.queryOnEnter()`, `stateDao.queryOnLeave()`, `transitionDao.queryOnTransition()`). When present, dispatches to `actionOperation.run()` with `ActionInput` containing the correlation ID and token ID. `RunCustomImplementation` (Action2) demonstrates a concrete action: looks up the token by ID, retrieves its context, modifies the context label, and persists the change. Actions participate in the correlation chain, enabling cascading event generation.

## Trade-offs

- Pros: Extensible action system without engine modification, actions are domain-specific custom operations, correlation chain enables cascading effects, clear separation of engine and business logic
- Cons: Indirect dispatch (entity -> operation -> custom implementation), debugging requires tracing through multiple layers, action input is limited to tokenID and correlationID
- Alternative: Direct method calls in engine (simpler but tightly coupled), event listeners (more decoupled), scripting engine for inline actions (more flexible)

## Related Patterns

- custom-operation-osgi-component
- token-based-workflow-execution
- correlation-based-event-chaining
- service-delegation-pattern
