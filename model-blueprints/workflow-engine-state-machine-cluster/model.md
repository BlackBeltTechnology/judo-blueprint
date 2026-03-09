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
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "head",
  target: "{{NAMESPACE}}::WorkflowVersion", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Workflow", name: "published",
  target: "{{NAMESPACE}}::WorkflowVersion", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "upload",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Workflow"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "publish",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Workflow"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Workflow", name: "commit",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Workflow"
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
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "initialState",
  target: "{{NAMESPACE}}::State", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "events",
  target: "{{NAMESPACE}}::Event", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::WorkflowVersion", name: "workflow",
  target: "{{NAMESPACE}}::Workflow", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
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
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "onEnter",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "onLeave",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::State", name: "supervisor",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
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
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "onTransition",
  target: "{{NAMESPACE}}::Action", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "guards",
  target: "{{NAMESPACE}}::Guard", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "nextStates",
  target: "{{NAMESPACE}}::State", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Transition", name: "role",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
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
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Action"
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
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Token", name: "assignee",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Token", name: "context",
  target: "{{NAMESPACE}}::Context", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "trigger",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "checkout",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "release",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "execute",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "assign",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Token", name: "navigate",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Token"
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
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "tokens",
  target: "{{NAMESPACE}}::Token", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "workflow",
  target: "{{NAMESPACE}}::Workflow", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "logs",
  target: "{{NAMESPACE}}::LogEntry", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Context", name: "type",
  target: "{{NAMESPACE}}::ContextType", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Context", name: "trigger",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Context"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Context", name: "createContext",
  operationType: "STATIC", binding: "{{NAMESPACE}}::Context"
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
