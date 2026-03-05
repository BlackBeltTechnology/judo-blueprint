---
id: workflow-engine-state-machine-cluster
title: "Workflow Engine State Machine Entity Cluster"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - workflow-poc
---

## Description

A complete, reusable workflow/state machine engine modeled as an interconnected entity cluster. The pattern provides a generic, data-driven workflow execution engine where workflow definitions are stored as entities (not hardcoded), enabling runtime-configurable business processes. The core entities are:

- **Workflow** -- the top-level definition entity with a name and versioning support (headVersionNumber, publishedVersionNumber). It holds multiple WorkflowVersion instances and pointers to the head (latest) and published (active) versions. Operations include upload (import definition), publish (make a version active), and commit (finalize a version).
- **WorkflowVersion** -- a specific revision of a workflow definition, with versionNumber, model (YAML definition), diagram (visual representation), committed flag, commitComment, commitTime, and uploadTime. It composes State entities (0..*) and Event entities (0..*), and associates to an initialState (0..1), a default Role (0..1), and observer URLs (0..*).
- **State** -- a node in the state machine, with name, task (label for human tasks), autoAssign flag, joinState flag (for parallel merges), and finalState flag. It composes outgoing Transition entities (0..*) and associates to incoming transitions (0..*). Optional onEnter and onLeave Action associations allow triggering side effects on state entry/exit. A supervisor Role association enables oversight control.
- **Transition** -- an edge between states, with eventID, onTransitionActionID, isHuman flag (human vs. automatic), and hasEvent flag. It associates to an EventType (0..1 event trigger), an Action (0..1 onTransition side effect), multiple nextStates (0..*), multiple Guard entities (0..* COMPOSITION), and a Role (0..1) for authorization.
- **Guard** -- a condition expression (expression attribute) with an errorMessage, composed by a Transition. Guards are evaluated before a transition fires; all must pass.
- **Action** -- a named executable unit (actionID attribute) with a run (INSTANCE) operation. Concrete action implementations extend Action via generalization (e.g., Action1, Action2, InitDocumentWorkflow), providing a Strategy pattern for pluggable behaviors.
- **EventType** -- a named event definition with eventID, label, and showInTasklist flag. These define the events that can trigger transitions.
- **Event** -- a runtime event instance with eventID, correlationID, processed flag (default: false), and sequence number (auto-generated). Events are composed by WorkflowVersion and represent queued trigger signals.
- **Context** -- a runtime workflow execution instance with label and identifier. It composes ContextAttribute entities (0..* key-value pairs), associates to active Token entities (0..* tracking current positions), the workflow definition (1..1), assignable Users (0..*), LogEntry records (0..*), and a ContextType (1..1). Derived relations provide assignees and lastTransitions. Operations: trigger (INSTANCE, fire an event), createContext (STATIC, start new workflow instance).
- **ContextType** -- a workflow type registry that associates a workflow to an external application entity type. Carries generic flag, name, actor/access/createOperation/idName attributes for integration with the host application's navigation system.
- **ContextAttribute** -- a key-value pair with name, type (ContextAttributeType enum), and value. This allows workflows to carry arbitrary typed data in their execution context.
- **Token** -- tracks a workflow execution's current position in the state machine. It carries tokenID, label, timestamp, and boolean flags isAssigneeLogged/isSupervisorLogged. Relations to state (0..1 current state), assignee (0..1 User), authorizedUsers (0..* DERIVED), context (1..1), and lastTransition (0..1). Operations: trigger, checkout, release, execute, assign, navigate -- providing the full task lifecycle.
- **Role** -- a workflow-scoped role with name, associating to users (0..*) and transitions (0..*). This controls who can execute which transitions.
- **User** -- a minimal user entity with email, associating to roles (0..*) and contexts (0..*). Operation: startWorkflow (INSTANCE).
- **LogEntry** -- an audit log entry with timestamp (default: now()), type (LogEntryType enum), userEmail, message, and level (LogLevel enum). Associated to Context via logs relation.
- **URL** -- a simple entity with address attribute, used as webhook observer endpoints.

Supporting enumerations:
- **ContextAttributeType** -- BOOLEAN, STRING, NUMERIC
- **LogEntryType** -- COMPLETION (extensible for other event types)
- **LogLevel** -- TRACE, INFO

The transfer layer provides:
- **TaskList TO** -- aggregates myTasks and allTasks with count attributes (userTasksCount, unassignedTasksCount, supervisedAssignedTasksCount, supervisedUnassignedTasksCount) and a startWorkflow operation.
- **Task TO** -- a rich view of a Token with status, subject, task, workflow, creationTime, assignment state flags (isUnassigned, isAssigned, isCheckoutEnabled, isReleaseEnabled, isNavigable, isAssigneeLogged, isSupervisorLogged), assignables/authorizedUsers/logEntries relations, and operations: checkout, release, assign, execute, navigate.
- **Admin TOs** -- Workflow/WorkflowVersion projections with upload/commit operations and version history.
- **Input TOs** -- ContextInput, ActionInput, YamlData, UploadInput, CommitInput, CreateURLInput, CreateRedirect, UpdateRedirect for workflow management operations.

All core entities are non-CRUD (createable=false, updateable=false, deleteable=false), managed entirely through custom operations.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Workflow" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Token" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "State" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Transition" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

### Workflow entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Workflow",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Workflow", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Workflow", name: "headVersionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Workflow", name: "publishedVersionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "versions",
  target: "{{NAMESPACE}}::WorkflowVersion", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "head",
  target: "{{NAMESPACE}}::WorkflowVersion", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "published",
  target: "{{NAMESPACE}}::WorkflowVersion", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "upload",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "publish",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "commit",
  operationType: INSTANCE
} }) { success fqn } }
```

### WorkflowVersion entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "WorkflowVersion",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "versionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "model"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "diagram"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "committed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "commitComment"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "commitTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "states",
  target: "{{NAMESPACE}}::State", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "initialState",
  target: "{{NAMESPACE}}::State", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "events",
  target: "{{NAMESPACE}}::Event", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "workflow",
  target: "{{NAMESPACE}}::Workflow", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### State entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "State",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::State", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::State", name: "task"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::State", name: "autoAssign"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::State", name: "joinState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::State", name: "finalState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "transitions",
  target: "{{NAMESPACE}}::Transition", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "onEnter",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "onLeave",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "supervisor",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Transition entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Transition",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Transition", name: "eventID"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Transition", name: "isHuman"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "event",
  target: "{{NAMESPACE}}::EventType", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "onTransition",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "guards",
  target: "{{NAMESPACE}}::Guard", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "nextStates",
  target: "{{NAMESPACE}}::State", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "role",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Guard entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Guard",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Guard", name: "expression"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Guard", name: "errorMessage"
} }) { success fqn } }
```

### Action entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Action",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Action", name: "actionID"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Action", name: "run",
  operationType: INSTANCE
} }) { success fqn } }
```

### Token entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Token",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Token", name: "tokenID"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Token", name: "label"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Token", name: "timestamp"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Token", name: "state",
  target: "{{NAMESPACE}}::State", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Token", name: "assignee",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Token", name: "context",
  target: "{{NAMESPACE}}::Context", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "trigger",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "checkout",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "release",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "execute",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "assign",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "navigate",
  operationType: INSTANCE
} }) { success fqn } }
```

### Context entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Context",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Context", name: "label"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Context", name: "identifier"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "attributes",
  target: "{{NAMESPACE}}::ContextAttribute", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "tokens",
  target: "{{NAMESPACE}}::Token", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "workflow",
  target: "{{NAMESPACE}}::Workflow", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "logs",
  target: "{{NAMESPACE}}::LogEntry", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "type",
  target: "{{NAMESPACE}}::ContextType", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Context", name: "trigger",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Context", name: "createContext",
  operationType: STATIC
} }) { success fqn } }
```

### Supporting entities

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "EventType",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EventType", name: "eventID"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EventType", name: "label"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EventType", name: "showInTasklist"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "ContextAttribute",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ContextAttribute", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ContextAttribute", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ContextAttribute", name: "value"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "LogEntry",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LogEntry", name: "timestamp"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LogEntry", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LogEntry", name: "userEmail"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LogEntry", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::LogEntry", name: "level"
} }) { success fqn } }
```

### Enumerations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ContextAttributeType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ContextAttributeType", name: "BOOLEAN", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ContextAttributeType", name: "STRING", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ContextAttributeType", name: "NUMERIC", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "LogEntryType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LogEntryType", name: "COMPLETION", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "LogLevel"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LogLevel", name: "TRACE", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::LogLevel", name: "INFO", ordinal: 2
} }) { success fqn } }
```

## Examples

### workflow-poc

**Core workflow definition entities:**
- **Workflow**: `workflow::entities::Workflow` (non-CRUD)
  - Attributes: name (req), headVersionNumber, publishedVersionNumber
  - Relations: versions (0..* ASSOC), head (0..1 ASSOC), published (0..1 ASSOC) -- all pointing to WorkflowVersion
  - Operations: upload (INSTANCE), publish (INSTANCE), commit (INSTANCE)
- **WorkflowVersion**: `workflow::entities::WorkflowVersion` (non-CRUD)
  - Attributes: name, label, versionNumber (req), model, diagram, committed (req, default: false), commitComment, commitTime, uploadTime
  - Relations: states (0..* COMPOSITION to State), events (0..* COMPOSITION to Event), initialState (0..1 ASSOC to State), workflow (1..1 ASSOC to Workflow), role (0..1 ASSOC to Role), observers (0..* ASSOC to URL)
  - Operations: commit (INSTANCE)

**State machine entities:**
- **State**: `workflow::entities::State` (non-CRUD)
  - Attributes: name (req), task, autoAssign (req, default: false), joinState (req, default: false), finalState
  - Relations: transitions (0..* COMPOSITION to Transition), onEnter (0..1 ASSOC to Action), onLeave (0..1 ASSOC to Action), supervisor (0..1 ASSOC to Role), incomingTransitions (0..* ASSOC)
- **Transition**: `workflow::entities::Transition` (non-CRUD)
  - Attributes: eventID, onTransitionActionID, isHuman, hasEvent
  - Relations: event (0..1 ASSOC to EventType), onTransition (0..1 ASSOC to Action), guards (0..* COMPOSITION to Guard), nextStates (0..* ASSOC to State), role (0..1 ASSOC to Role)
- **Guard**: `workflow::entities::Guard` (non-CRUD) -- expression (req), errorMessage
- **Action**: `workflow::entities::Action` (non-CRUD) -- actionID (req); op: run (INSTANCE)
  - Concrete subtypes via generalization: Action1, Action2, InitDocumentWorkflow (all in workflow::test)

**Runtime execution entities:**
- **Token**: `workflow::entities::Token` (non-CRUD)
  - Attributes: tokenID (req), label, timestamp, isAssigneeLogged, isSupervisorLogged
  - Relations: state (0..1), assignee (0..1 to User), authorizedUsers (0..* DERIVED), context (1..1 to Context), lastTransition (0..1)
  - Operations: trigger, checkout, release, execute, assign, navigate (all INSTANCE)
- **Context**: `workflow::entities::Context` (non-CRUD)
  - Attributes: label, identifier
  - Relations: attributes (0..* COMPOSITION to ContextAttribute), tokens (0..*), workflow (1..1), assignables (0..* to User), logs (0..*), assignees (0..* DERIVED), lastTransitions (0..* DERIVED), type (1..1 to ContextType)
  - Operations: trigger (INSTANCE), createContext (STATIC)
- **Event**: `workflow::entities::Event` (non-CRUD) -- eventID (req), correlationID, processed (req, default: false), sequence (req, auto-generated)
- **EventType**: `workflow::entities::EventType` (non-CRUD) -- eventID (req), label, showInTasklist (req, default: true)
- **ContextType**: `workflow::entities::ContextType` (non-CRUD) -- generic (req, default: false), name (req), actor, access, createOperation, idName; relations: workflows (0..*)
- **ContextAttribute**: `workflow::entities::ContextAttribute` (non-CRUD) -- name (req), type (req), value (req)
- **LogEntry**: `workflow::entities::LogEntry` (non-CRUD) -- timestamp (req, default: now()), type (req), userEmail, message, level (req), isUserEmailDefined

**User/Role entities:**
- **User**: `workflow::entities::User` (non-CRUD) -- email (req); relations: roles (0..*), contexts (0..*); op: startWorkflow (INSTANCE)
- **Role**: `workflow::entities::Role` (non-CRUD) -- name (req); relations: users (0..*), transitions (0..*)
- **URL**: `workflow::entities::URL` (non-CRUD) -- address (req)

**Enumerations:**
- ContextAttributeType: BOOLEAN(1), STRING(2), NUMERIC(3)
- LogEntryType: COMPLETION(1)
- LogLevel: TRACE(1), INFO(2)

**Transfer Objects:**
- `workflow::transfers::TaskList` -- userTasksCount, unassignedTasksCount, supervisedAssignedTasksCount, supervisedUnassignedTasksCount; relations: allTasks (0..*), myTasks (0..*); op: startWorkflow (MAPPED)
- `workflow::transfers::Task` -- 13 attributes (status, subject, task, workflow, creationTime, assignment flags); relations: assignables (0..*), authorizedUsers (0..*), logEntries (0..*); ops: checkout, release, assign, execute, navigate (all MAPPED)
- `workflow::transfers::admin::Workflow` -- name, headVersionNumber, publishedVersionNumber, committed, commitComment; relations: versions (0..* AGGREGATION); op: upload (MAPPED)
- `workflow::transfers::admin::WorkflowVersion` -- 9 attributes including model/diagram; op: commit (MAPPED)
- Input TOs: ContextInput, ActionInput, YamlData, UploadInput, CommitInput, CreateURLInput, CreateRedirect, UpdateRedirect, WorkflowDiagram
