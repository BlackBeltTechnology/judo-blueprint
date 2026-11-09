## Overview

Task entities are created as side effects of the `assignApproval` product operation and closed via a dedicated `closeTask` custom operation. The backend manages task state transitions (TODO -> APPROVED/REJECTED) and wires tasks to both the creating user and the assigned reviewer.

## Implementation Pattern

- Task creation happens inside `AssignApprovalCustomImplementation` (a product operation), not a task-specific operation. For each selected assignee, a Task is created via `taskDao.create(TaskForCreate.builder()...)` with state=TODO, type=APPROVAL, the current user as createdBy, and the product as targetProduct
- The `closeTask` custom operation (`CloseTaskCustomImplementation`) is an OSGi `@Component` implementing the generated `CloseTask` interface. It accepts `CloseTaskInput` with a `result` field (TaskState enum value: APPROVED or REJECTED), loads the task by ID, sets the new state, and calls `taskDao.update()`
- Actor resolution uses `VariableResolver` to get the current user's email and resolve the User entity via `UserDao`
- The activate/deactivate operations are not custom -- they are handled by the framework's built-in set-attribute behavior (toggling `isActive`)
- No service layer abstraction -- task creation and closing are embedded directly in operation classes

## Examples

### alba
- Key files: `custom/.../entities/task/CloseTaskCustomImplementation.java`, `custom/.../entities/product/AssignApprovalCustomImplementation.java`
- Pattern: Tasks are created in bulk within `AssignApprovalCustomImplementation` by iterating over a list of assignee users resolved from the `ApprovalTaskInput.users` collection via `userDao.findAllById()`; each task is created with `isActive(true)` and linked to the product and both the creator and assignee users
- Notable: `CloseTaskCustomImplementation` is minimal (load task, set state from input, update); the operation does not create events or trigger further workflow transitions -- the approval workflow continues via separate product-level operations
- DI: `CloseTaskCustomImplementation` injects `TaskDao`, `ProductDao`, `UserDao`, and `VariableResolver` via OSGi `@Reference`
