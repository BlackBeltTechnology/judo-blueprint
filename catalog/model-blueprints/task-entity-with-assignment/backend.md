## Overview

A task is created by a domain operation, not by a task-specific operation, and it is closed by a custom operation that sets its state. The backend writes the state and the links. It does not run a workflow engine.

## Implementation pattern

- **Creation inside a domain operation.** The operation that starts an approval creates one task per selected assignee. Each task starts in the initial state, carries the type, and links to the current user as creator, to the assignee, and to the target entity.
- **Closing with a custom operation.** The close operation is a custom operation. It takes a result input (a TaskState value), loads the task, sets the new state and saves it. Because it is custom, interceptors do not run for it. Any check on the result must be in the operation itself.
- **Activate and deactivate.** These toggle the active flag. In the example they need no custom code, because the platform's built-in behaviour sets the attribute. An interceptor can therefore guard them, but a built-in call can only fail with `InterceptorCallBusinessException`, not with a modeled fault ([error handling](../../agent-docs/backend/error-handling-guide.md#exceptions-thrown-from-interceptors)). A toggle written as a custom operation would not be intercepted.
- **Errors.** A business rule violation (for example, closing an already closed task) is a modeled fault (HTTP 422). A bad field value is a validation exception (HTTP 400). `BusinessErrorException` and `ExceptionUtils` are example project code, not platform API.
- **Service layer.** The example project keeps task creation and closing inside the operation classes. Extract a service only when several operations need the same logic.

## Examples

### alba

- Key files: `custom/.../entities/task/CloseTaskCustomImplementation.java` and `custom/.../entities/product/AssignApprovalCustomImplementation.java` (example project code).
- Creation: the domain operation resolves the assignee users from the input collection, then creates one task per user in the same transaction.
- Close: the close operation loads the task, sets the state from the input and saves it. It does not raise events or start another transition; the approval continues through separate operations on the target.
- Dependencies are injected into the operation classes through the platform's component wiring.
