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
