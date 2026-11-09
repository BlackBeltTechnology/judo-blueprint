## Examples

### alba
- **Task entity**: `Alba::entities::Task` (non-CRUD)
  - Attributes: createdAt (req), type (req, TaskType), state (req, TaskState), isActive (default: false), createdByName, assigneeName, productTitle, isAssigneeCurrentUser
  - Relations: createdBy (1..1 ASSOC to User), assignee (1..1 ASSOC to User), targetProduct (0..1 ASSOC to Product)
  - Operations: closeTask (custom INSTANCE), activate (INSTANCE), deactivate (INSTANCE)
- **TaskType enum**: `Alba::entities::TaskType` -- APPROVAL(1)
- **TaskState enum**: `Alba::entities::TaskState` -- APPROVED(1), REJECTED(2), TODO(3)
- **Input TOs**:
  - `Alba::entities::CloseTaskInput` (unmapped) -- result (req, TaskState) -- used as input for closeTask operation
  - `Alba::entities::ApprovalTaskInput` (unmapped) -- users (0..* AGGREGATION) -- used for assignApproval to select reviewers
- **Role-specific Task TOs**:
  - `AuthorTask` -- createdAt, createdByName, productTitle, type, state, isTrue (guard), isCloseDisabled (guard); relation: authorProduct (0..1 AGGREGATION); op: closeTask
  - `ApproverTask` -- assigneeName, createdAt, createdByName, productTitle, state, type, isTrue (guard); relation: approverProduct (0..1 AGGREGATION); op: closeTask
  - `AdminTask` -- assigneeName, createdAt, createdByName, productTitle, state, type, isActive, isNotActive (guard); relation: targetProduct (0..1 AGGREGATION); ops: activate, deactivate
- User entity has both `tasks` (0..* ASSOC, tasks assigned to user) and `createdTasks` (0..* ASSOC, tasks created by user) relations
