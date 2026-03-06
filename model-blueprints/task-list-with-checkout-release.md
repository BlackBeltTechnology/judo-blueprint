---
id: "task-list-with-checkout-release"
title: "Task List with Checkout/Release Assignment Pattern"
score: 43.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - workflow-poc
---
## Description

A transfer object pattern for human task management where tasks (derived from workflow tokens) are presented in a task list with checkout/release semantics for task ownership. The pattern consists of:

- **TaskList TO** -- a container transfer object aggregating categorized task collections with computed counts. It holds separate relations for different task views: myTasks (tasks assigned to the current user) and allTasks (all accessible tasks including unassigned ones). Count attributes (userTasksCount, unassignedTasksCount, supervisedAssignedTasksCount, supervisedUnassignedTasksCount) provide at-a-glance metrics without loading all task data. A startWorkflow operation initiates new workflow instances.
- **Task TO** -- a rich projection of a workflow token with human-task attributes: status (textual state label), subject (workflow context label), task (human task name from state definition), workflow (workflow name), creationTime, and assignee (email of current owner). Boolean guard attributes control which operations are available: isUnassigned, isAssigned, isCheckoutEnabled, isReleaseEnabled, isAssigneeLogged, isSupervisorLogged, isNavigable. Relations include assignables (users eligible for assignment), authorizedUsers (users permitted to interact), and logEntries (audit trail). Operations implement the task lifecycle: checkout (claim an unassigned task), release (unclaim a task back to the pool), assign (delegate to a specific user), execute (trigger an event/transition on the task), navigate (open the associated domain entity).

The checkout/release pattern is a collaborative task management approach: unassigned tasks sit in a shared pool; a user "checks out" a task to claim it; if unable to complete, they "release" it back for others. The assign operation allows supervisors to directly delegate. Execute fires the workflow transition, advancing the state machine. Navigate provides a link back to the domain entity the workflow is tracking.

This pattern is independent of the specific workflow engine implementation and can be applied to any system with assignable work items.

## Detection Query

```graphql
{ esm { transferobjecttypes(where: { name: { eq: "TaskList" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { eq: "Task" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper } }
    operations { items { name operationType } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "TaskList"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::TaskList", name: "userTasksCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::TaskList", name: "unassignedTasksCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::TaskList", name: "supervisedAssignedTasksCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::TaskList", name: "supervisedUnassignedTasksCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "Task"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "subject"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "task"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "workflow"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "creationTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "assignee"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "isUnassigned"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "isAssigned"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "isCheckoutEnabled"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "isReleaseEnabled"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "isNavigable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "checkout",
  binding: "{{SERVICE_NAMESPACE}}::Task.checkout",
  operationType: "MAPPED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "release",
  binding: "{{SERVICE_NAMESPACE}}::Task.release",
  operationType: "MAPPED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "assign",
  binding: "{{SERVICE_NAMESPACE}}::Task.assign",
  operationType: "MAPPED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "execute",
  binding: "{{SERVICE_NAMESPACE}}::Task.execute",
  operationType: "MAPPED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Task", name: "navigate",
  binding: "{{SERVICE_NAMESPACE}}::Task.navigate",
  operationType: "MAPPED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::TaskList", name: "startWorkflow",
  binding: "{{SERVICE_NAMESPACE}}::TaskList.startWorkflow",
  operationType: "MAPPED"
} }) { success fqn } }
```

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
