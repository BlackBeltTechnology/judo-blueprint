## Examples

### workflow-poc
- **TaskList TO**: `workflow::transfers::TaskList`
  - Attributes: userTasksCount, unassignedTasksCount, supervisedAssignedTasksCount, supervisedUnassignedTasksCount
  - Relations: allTasks (0..* ASSOC), myTasks (0..* ASSOC)
  - Operations: startWorkflow (MAPPED)
  - Provides a dashboard-like view of all pending work items with category counts
- **Task TO**: `workflow::transfers::Task`
  - Display attributes: status, subject, task, workflow, creationTime, assignee
  - Guard attributes: isUnassigned, isAssigned, isCheckoutEnabled, isReleaseEnabled, isAssigneeLogged, isSupervisorLogged, isNavigable
  - Relations: assignables (0..* ASSOC to User), authorizedUsers (0..* ASSOC to User), logEntries (0..* ASSOC to LogEntry)
  - Operations: checkout (MAPPED), release (MAPPED), assign (MAPPED), execute (MAPPED), navigate (MAPPED)
- **Supporting TOs**:
  - `workflow::transfers::User` -- email (for display in assignables/authorizedUsers)
  - `workflow::transfers::LogEntry` -- timestamp, type, userEmail, message, level (for audit trail display)
  - `workflow::transfers::ActionInput` -- tokenID (req), correlationID (for execute operation input)
  - `workflow::transfers::Identifier` -- value (req) (for assign operation input)
- The Task TO maps to Token entities, presenting workflow execution positions as human-readable tasks with lifecycle operations
