## Model shape

The shape is the entity cluster described in the blueprint, drawn with its custom operations and two enumerations. Names are neutral and follow the source project's own vocabulary because they are the engine's domain terms.

- Ownership: Workflow owns WorkflowVersion; WorkflowVersion owns State and Event; State owns Transition; Transition owns Guard; Context owns ContextAttribute. These are compositions. Everything else is an association; Token, Context, Role and User are free-standing.
- Pointers: head and published version on Workflow, initial state and default role on WorkflowVersion, onEnter, onLeave and supervisor on State, event type, action, role and next states on Transition.
- Action is specialized by a concrete subtype to show the strategy hook; each subtype implements run.
- Operations are instance or static custom operations: Workflow upload, publish, commit; Context createContext (static); Token trigger, checkout, release, assign, navigate; Action run; User startWorkflow.
- Not drawn: the transfer objects (task list, task, admin projections, inputs), derived relations (assignees, last transitions, authorized users) and the actor access that exposes them. They are implied by the engine and are project specific.
- All core entities have create, update and delete switched off; the UI reaches them through the task list and admin transfer objects.

Generated UI pages: keep the task list table and the task view as the main user screens, hide generated forms for the core entities, and use the admin projections for definition upload and version history.

## Structure diagram

<!-- mermaid:generated fragment=workflow-engine-state-machine-cluster cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class Action {
    <<Entity>>
    +String actionID [1]
    +run()
  }
  class ActionImpl {
    <<Entity>>
  }
  class Context {
    <<Entity>>
    +String label
    +String identifier
    +createContext()
  }
  class ContextAttribute {
    <<Entity>>
    +String name [1]
    +ContextAttributeType type [1]
    +String value
  }
  class ContextAttributeType {
    <<Enumeration>>
    BOOLEAN
    STRING
    NUMERIC
  }
  class ContextType {
    <<Entity>>
    +String name [1]
    +Boolean generic [1]
  }
  class Event {
    <<Entity>>
    +String eventID [1]
    +String correlationID
    +Boolean processed [1]
    +Integer sequence
  }
  class EventType {
    <<Entity>>
    +String eventID [1]
    +String label
    +Boolean showInTasklist [1]
  }
  class Guard {
    <<Entity>>
    +String expression [1]
    +String errorMessage
  }
  class LogEntry {
    <<Entity>>
    +Timestamp timestamp [1]
    +String userEmail
    +String message
    +LogLevel level [1]
  }
  class LogLevel {
    <<Enumeration>>
    TRACE
    INFO
  }
  class Role {
    <<Entity>>
    +String name [1]
  }
  class State {
    <<Entity>>
    +String name [1]
    +String task
    +Boolean autoAssign [1]
    +Boolean joinState [1]
    +Boolean finalState [1]
  }
  class Token {
    <<Entity>>
    +String tokenID [1]
    +String label
    +Timestamp timestamp
    +Boolean isAssigneeLogged [1]
    +Boolean isSupervisorLogged [1]
    +trigger()
    +checkout()
    +release()
    +assign()
    +navigate()
  }
  class Transition {
    <<Entity>>
    +String eventID
    +Boolean isHuman [1]
    +Boolean hasEvent [1]
  }
  class User {
    <<Entity>>
    +String email [1]
    +startWorkflow()
  }
  class Workflow {
    <<Entity>>
    +String name [1]
    +Integer headVersionNumber
    +Integer publishedVersionNumber
    +upload()
    +publish()
    +commit()
  }
  class WorkflowVersion {
    <<Entity>>
    +Integer versionNumber [1]
    +Text model
    +Text diagram
    +Boolean committed [1]
    +String commitComment
    +Timestamp commitTime
    +Timestamp uploadTime
  }
  Action <|-- ActionImpl
  Context *-- "*" ContextAttribute : attributes
  Context --> "*" LogEntry : logs
  Context --> "*" Token : tokens
  Context --> "*" User : assignees
  Context --> "1" ContextType : contextType
  Context --> "1" Workflow : workflow
  ContextAttribute ..> ContextAttributeType : type
  ContextType --> "0..1" Workflow : workflow
  LogEntry ..> LogLevel : level
  Role --> "*" User : users
  State *-- "*" Transition : transitions
  State --> "0..1" Action : onEnter
  State --> "0..1" Action : onLeave
  State --> "0..1" Role : supervisor
  Token --> "0..1" State : state
  Token --> "0..1" Transition : lastTransition
  Token --> "0..1" User : assignee
  Token --> "1" Context : context
  Transition *-- "*" Guard : guards
  Transition --> "*" State : nextStates
  Transition --> "0..1" Action : action
  Transition --> "0..1" EventType : eventType
  Transition --> "0..1" Role : role
  User --> "*" Role : roles
  Workflow *-- "*" WorkflowVersion : versions
  Workflow --> "0..1" WorkflowVersion : headVersion
  Workflow --> "0..1" WorkflowVersion : publishedVersion
  WorkflowVersion *-- "*" Event : events
  WorkflowVersion *-- "*" State : states
  WorkflowVersion --> "0..1" Role : defaultRole
  WorkflowVersion --> "0..1" State : initialState
```
<!-- /mermaid:generated -->
