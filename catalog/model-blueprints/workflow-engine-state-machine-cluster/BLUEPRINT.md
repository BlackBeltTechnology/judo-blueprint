---
id: workflow-engine-state-machine-cluster
title: Workflow Engine State Machine Entity Cluster
description: "A data-driven workflow engine modeled as an entity cluster: workflow definitions, versions, states, transitions, guards and actions as entities, with runtime contexts and tokens that move through them."
aliases: [workflow engine, state machine engine, token workflow, runtime workflow definition]
keywords: [workflow, engine, state machine, token, transition, guard, action, context, versions, fork, join]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:workflow-poc", "status:single-project"]
category: pattern
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: [entity-based-state-machine]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Run business processes from workflow definitions stored as data instead of code. A definition (states, transitions, guards, roles, actions) is uploaded, versioned and published at runtime; each started process is a context whose tokens mark the current position in the state machine.

### Definition side and runtime side

The definition side (Workflow, WorkflowVersion, State, Transition, Guard, Action, EventType, Role) describes what may happen. The runtime side (Context, ContextAttribute, Token, Event, LogEntry) records what is happening. A token moves from state to state when an event fires a transition whose guards pass.

## Structure

- **Workflow** has a name and the head and published version numbers. It owns WorkflowVersion entities (0..*, composition) and points to the head and published versions (0..1 each, association). Operations: upload, publish, commit.
- **WorkflowVersion** has versionNumber, a model (the definition text), a diagram (generated diagram source), a committed flag and commit data. It owns State (0..*) and Event (0..*) entities, and points to an initial state and a default Role.
- **State** has name, task label, autoAssign, joinState and finalState flags. It owns its outgoing Transition entities (0..*, composition) and points to optional onEnter and onLeave actions and a supervisor Role.
- **Transition** has an event identifier, an isHuman flag and a hasEvent flag. It points to an EventType, an Action, a Role and one or more next states (0..*, association; several next states mean a fork). It owns its Guard entities (0..*, composition).
- **Guard** has an expression and an error message. All guards of a transition must pass.
- **Action** is the base of pluggable behaviours: an actionID and a run operation. Concrete actions are specializations (generalization) that implement run.
- **Context** is a running instance: label, identifier, ContextAttribute entries (key, typed value; composition), tokens, the workflow, assignable users, log entries and a ContextType. Operation createContext is static.
- **ContextType** registers a workflow for an application entity type (name, generic flag).
- **Token** marks a position: tokenID, label, timestamp, assignee-logged and supervisor-logged flags, the current state (0..1), assignee (0..1), context (1..1) and last transition. Operations: trigger, checkout, release, assign, navigate.
- **Role** and **User** are linked many to many. User has the startWorkflow operation.
- **Enumerations**: ContextAttributeType (BOOLEAN, STRING, NUMERIC) and LogLevel (TRACE, INFO).
- Transfer layer in the source project: a task list transfer object (own and all tasks with counts), a task transfer object mapping a Token with assignment-state flags, admin projections of Workflow and WorkflowVersion, and input transfer objects for upload, commit, action input and redirect.

All core entities are neither createable, updateable nor deleteable through generated actions; they change only through custom operations.

## Constraints

### Definition entities change only through operations

Upload, publish and commit are the only writers of definition entities, which keeps a published version immutable. See [[workflow-versioning-pattern]] for the version lifecycle.

### Operations are custom and bypass interceptors

createContext, trigger, upload and the task operations are custom operations. Interceptors fire only for built-in behaviour operations, so permission and state checks (for example "only the assignee may execute") must live inside the operations or the services they call (see [backend.md](backend.md)).

### Tokens, not the entity, hold the position

A context may hold several tokens at once (parallel branches). Do not store a single "current state" on the context.

## Variations

- Several next states on a transition model a fork; a join state merges the tokens that arrived. Omit both when processes are strictly sequential.
- Replace guard expression text with a fixed set of guard types when no expression language should be exposed.
- A simpler form keeps the status as an enumeration or entity on the business object; see [[entity-based-state-machine]].

## When to use

- Process definitions must change at runtime without a deployment, by a business user.
- Human tasks, assignment and parallel branches are needed.

## When to avoid

- The process is small and stable: a status enumeration plus an operation is far cheaper.
- Compliance needs the process in reviewed code and not in uploaded data.

## Related

- [[workflow-versioning-pattern]] — head and published versions of a definition
- [[entity-based-state-machine]] — the lightweight alternative
- [[contract-management-workflow-cluster]] — a business workflow that could run on such an engine
- [[custom-operation-osgi-component]] — how each custom operation is registered
