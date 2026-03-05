---
id: "entity-based-state-machine"
title: "Entity-Based State Machine Pattern"
domain: "model"
category: "entity"
score: 16.8
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - workflow-poc
alternatives:
  - enum-state-machine
---
## Description

Instead of using an enum to represent lifecycle states, a full entity model implements the state machine pattern using separate State, Transition, Guard, and Action entities. States are entity instances rather than enum members, transitions are modeled as relations between states with guards and actions, and tokens track the current position of each workflow instance. This enables runtime-configurable workflows where the state machine structure can be modified without model changes.

## Structure

- **State** entity: represents positions in the workflow (name, task, flags like autoAssign, joinState, finalState)
- **Transition** entity: connects states, composed within the source State, with `nextStates [0..*]` associations
- **Guard** entity: composed within Transition, holds conditional expressions and error messages
- **Action** entity: polymorphic base with a `run` operation, extended by concrete action implementations
- **Token** entity: tracks the current state for a workflow instance, references the active State and Context
- **Event/EventType** entities: trigger transitions on tokens
- The state machine structure is data-driven (uploadable as YAML), not hardcoded in the model

## Examples

### workflow-poc
Full workflow engine implementation: `State` defines positions with optional `onEnter`/`onLeave` actions and `supervisor` role. `Transition` connects states with event triggers, guard conditions, `onTransition` actions, and role-based access. `Token` tracks position with `state [0..1]` reference and operations `trigger`, `checkout`, `release`, `execute`, `assign`. `WorkflowVersion` owns states and events via composition. `Action` base entity uses generalization with 3 test subtypes (`Action1`, `Action2`, `InitDocumentWorkflow`) each overriding the `run(ActionInput)` operation -- implementing the Strategy pattern for pluggable workflow behavior.

## Trade-offs

- Pros: Runtime-configurable workflows, no model changes needed for new states/transitions, supports complex workflow patterns (join states, guards, role-based transitions), full audit trail via tokens
- Cons: Much more complex entity model than enum-based state machines, requires workflow engine logic, harder to understand at a glance
- Prefer enum-state-machine when: States are few, fixed, and known at design time
- Prefer entity-based-state-machine when: Workflows must be configurable at runtime, states/transitions are user-defined, or complex workflow features (guards, actions, roles) are needed

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (simpler alternative for fixed lifecycle states)
- [generalization-base-entity](generalization-base-entity.md) (Action uses generalization for pluggable behavior)
- [composition-ownership](composition-ownership.md) (states composed within versions, transitions within states)
- [custom-implementation-placeholder](custom-implementation-placeholder.md) (Action.run uses placeholder body)
