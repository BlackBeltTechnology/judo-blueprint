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
