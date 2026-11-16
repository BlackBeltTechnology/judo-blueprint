## Overview

The checkout, release, assign and execute operations are model-defined mapped operations on the Task transfer object. They bind to the Token operations of the same name. The state transitions, the automatic assignment and the authorization checks are in custom code, because they depend on the workflow engine and not on the model.

## Implementation pattern

- **Mapped operations.** Each Task operation is a MAPPED operation whose binding is the name of the Token operation ([mapped operation rules](../../agent-docs/model/esm_metamodel/operation.md#mapped-operation-rules)). The Token operation holds the custom code. Interceptors never fire for mapped or custom operations, so permission checks go inside the implementation ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). A modeled fault thrown from the implementation must be declared on the operation in the model ([custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).
- **Authorization before a human step.** A human transition is allowed only when an assignee is logged in on the token. The check is in the custom execute path, not in a guard flag.
- **Automatic assignment on entering a state.** When a token enters a state, the engine filters the eligible users against the users authorized for that token. It then picks the user who last completed a similar step, if that user is not already assigned elsewhere. If there is no match, it picks at random.
- **Clearing the assignee on transition.** Each state change clears the assignee, so a checkout belongs to one state only.
- **Completion logging.** After each transition the engine writes a completion log entry with the assignee's email. The entries feed the audit view and the assignment preference.
- **Guard evaluation.** Transition guards are evaluated before a step runs. The result controls which execute actions are shown.
- **Errors.** A business rule violation is a modeled fault (HTTP 422). A bad field value is a validation exception (HTTP 400). `WorkflowUtils` and the utility classes named below are example project code, not platform API.

## Examples

### Example

- Key files: `custom/workflow/utils/WorkflowUtils.java` (automatic assignment, stepping, completion logging) and `custom/.../entities/token/TriggerCustomImplementation.java` (authorization and transition handling). Both are example project code.
- Automatic assignment: the utility first filters the context's assignable users against the token's authorized users. It then looks up the most recent completion entries for that workflow and picks the user who is eligible and not already assigned in the same context. A random eligible user is the fallback.
- The utilities are wired into the operation classes through the platform's component wiring. The example does not use a separate service layer.
