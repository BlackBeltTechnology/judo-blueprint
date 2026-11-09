## Overview

The workflow engine state machine cluster is implemented through a set of interconnected custom operation classes and utility services that provide the complete runtime execution engine: context creation, event-driven state transitions, YAML-based workflow definition upload with validation, Mermaid diagram generation, guard evaluation via Spring Expression Language (SpEL), token forking/joining for parallel execution, auto-assignment, and pluggable action execution via the Strategy pattern.

## Implementation Pattern

- **CreateContext operation**: An OSGi `@Component` implementing a static `createContext` operation. It resolves the ContextType and Workflow by name, fetches the published WorkflowVersion, creates a Context entity linked to the workflow version and type, then creates an initial Token and places it on the initial state via a shared `WorkflowUtils` service.
- **Trigger operation**: An OSGi `@Component` implementing an instance `trigger` operation on Token. It creates an Event entity with a correlationID (ThreadLocal-based), then recursively processes events: for each unprocessed event, it queries the current state's transitions matching the event's eventID, checks human-task authorization (`isHuman` flag vs `isAssigneeLogged`), and delegates to `WorkflowUtils.step()` for the actual transition. After processing, it polls for chained events (same correlationID, unprocessed) and processes them in sequence order.
- **WorkflowUtils utility service**: An OSGi `@Component` registered as a service class (not an operation interface). It provides the core state machine execution logic:
  - `setCurrentState()` -- assigns token to a new state, clears assignee, timestamps, triggers auto-assign, executes onEnter actions, and recursively fires immediate (eventless) transitions whose guards pass
  - `step()` -- evaluates transition guards via SpEL, executes onLeave/onTransition/onEnter actions in order, logs completion, and handles single vs. multiple next states (fork/join)
  - `join()` -- implements parallel merge: unsets token state, checks if all incoming join transitions have been reached via `lastTransitions`, then merges tokens into a single new token on the join state
  - `autoAssign()` -- filters assignable users against authorized users, then selects a preferred assignee based on log history (most recent completer not already assigned) or random fallback
  - Guard evaluation uses Spring SpEL with a custom `PropertyAccessor` (`WorkflowContextVariableResolver`) that reads ContextAttribute key-value pairs as expression variables
  - Action execution uses the polymorphic `ActionOperation.run()` method, enabling the Strategy pattern where concrete Action subtypes provide different behaviors
- **Upload operation**: An OSGi `@Component` implementing the `upload` instance operation on Workflow. It parses YAML (via Jackson YAMLFactory) into Java records, validates cross-references (states, roles, events), manages version lifecycle (deletes uncommitted head, increments version number), creates all structural entities (States, Transitions, EventTypes, Guards), and generates a Mermaid state diagram.
- **DiagramUtils utility service**: An OSGi `@Component` that generates Mermaid state diagram syntax from a WorkflowVersion's states and transitions using Handlebars templating. Handles fork/join stereotypes and final state markers.
- **Action implementations**: Concrete Action subtypes (e.g., Action2) implement the `run` operation as OSGi `@Component` classes, receiving an `ActionInput` with tokenID and correlationID. They resolve the Token by ID, navigate to the Context, and perform domain-specific side effects.
- **Correlation-based event chaining**: A `ThreadLocal<String>` correlationID in WorkflowUtils enables cascading events within a single trigger invocation -- actions can fire new events that are processed in the same correlation chain.
- **DI wiring**: All components use OSGi Declarative Services (`@Component`, `@Reference`). Utility services like `WorkflowUtils` and `DiagramUtils` are registered as their own class type and injected by other components.

## Examples

### workflow-poc
- Key files: `custom/.../entities/context/CreateContextCustomImplementation.java`, `custom/.../entities/token/TriggerCustomImplementation.java`, `custom/.../entities/workflow/UploadCustomImplementation.java`, `custom/workflow/utils/WorkflowUtils.java`, `custom/workflow/utils/DiagramUtils.java`, `custom/.../test/action2/RunCustomImplementation.java`
- Pattern: Full state machine engine with 3 custom operations (createContext, trigger, upload), 2 utility services (WorkflowUtils, DiagramUtils), and pluggable action handlers (Action2.run). The trigger operation implements recursive event processing with correlation-based chaining. Guard evaluation uses Spring SpEL with custom PropertyAccessor for workflow context variables.
- Notable: The WorkflowUtils class (314 lines) is the engine core, handling state transitions, fork/join parallel execution, auto-assignment with preference-based selection, and action dispatch. The UploadCustomImplementation (372 lines) implements a complete YAML-to-entity parser with cross-reference validation and Mermaid diagram generation. The project uses Java records for YAML deserialization (YamlData with nested WorkflowData, RoleData, EventData, StateData, TransitionData records).
- DI: 6 OSGi `@Component` classes; WorkflowUtils injects 7 DAOs plus ActionOperation; UploadCustomImplementation injects 8 DAOs plus FileStoreService, DiagramUtils, and WorkflowUtils.
