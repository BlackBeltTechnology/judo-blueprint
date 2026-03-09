---
id: "workflow-engine-state-machine-cluster"
title: "Workflow Engine State Machine Entity Cluster"
score: 43.0
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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
