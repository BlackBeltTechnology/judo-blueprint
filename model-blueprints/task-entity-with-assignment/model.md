## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Task" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "TaskState" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "TaskType" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "TaskType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TaskType", name: "{{TASK_TYPE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "TaskState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TaskState", name: "TODO", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TaskState", name: "APPROVED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TaskState", name: "REJECTED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Task",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "state"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "isActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "createdByName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Task", name: "assigneeName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Task", name: "createdBy",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Task", name: "assignee",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Task", name: "targetProduct",
  target: "{{NAMESPACE}}::Product", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "closeTask",
  customImplementation: true, operationType: "INSTANCE", binding: "{{NAMESPACE}}::Task.closeTask"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "activate",
  customImplementation: false, operationType: "INSTANCE", binding: "{{NAMESPACE}}::Task.activate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "deactivate",
  customImplementation: false, operationType: "INSTANCE", binding: "{{NAMESPACE}}::Task.deactivate"
} }) { success fqn } }
```

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
