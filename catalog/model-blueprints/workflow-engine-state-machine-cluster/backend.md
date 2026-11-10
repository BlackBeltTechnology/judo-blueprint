## Backend guidance

### Operations are custom implementations with injected DAOs

Each custom operation is an OSGi component that gets its DAOs and services injected (see [[custom-operation-osgi-component]] and the [custom operations guide](../../agent-docs/backend/custom-operations.md)). The engine needs three operations and two shared services:

- **createContext** (static): resolves the ContextType and the published version of the workflow, creates the Context and places a first Token on the initial state.
- **trigger** (instance on Token): creates an Event, then processes unprocessed events for the correlation id, one by one, in sequence order. For each it finds the current state's transitions for the event identifier, checks the human-task rule (isHuman against assignee-logged) and hands over to the engine service.
- **upload** (instance on Workflow): parses the uploaded definition, validates cross references (states, roles, events), manages the version number (replaces an uncommitted head), creates the structural entities and generates a diagram.

### Engine service (project helper)

`WorkflowUtils` and `DiagramUtils` in the source project are example project code, plain OSGi service classes injected into the operations. The engine service holds the logic:

- set the current state: clear the assignee, stamp the time, auto-assign, run onEnter actions and fire eventless transitions whose guards pass;
- step: evaluate guards, run onLeave, onTransition and onEnter actions in order, log completion, and branch on one or several next states (fork);
- join: unset the token's state, check that all incoming join transitions were reached, merge into one token;
- auto-assign: intersect assignable and authorized users, prefer the user who last completed a step, otherwise pick one at random.

Guard expressions use the Spring Expression Language with a custom property accessor over the context attributes. This is project practice, not a platform feature. Actions use the Strategy pattern through the polymorphic run operation. Event chaining uses a thread-local correlation id so actions can fire further events inside one trigger.

### Checks live in the operations

Interceptors do not see custom operations (see [interceptors](../../agent-docs/backend/interceptors.md)). Assignee, supervisor and role checks therefore sit in trigger, checkout, release and assign, not in an interceptor. Throw the generated fault or a business error from the operation for a refused transition.

## Examples

### workflow-poc

- Three custom operations, two service classes and one concrete action class as OSGi components. The engine service is the largest class; upload is the second largest, using Java records for the definition format.
- Operation and class names are example project code.
