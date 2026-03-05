---
id: task-entity-with-assignment
title: "Task Entity with Assignee, Type, and State Enums"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - alba
---

## Description

A Task entity that models assignable work items within an approval or review workflow. Each task has a type (TaskType enum categorizing the kind of work, e.g., APPROVAL), a state (TaskState enum tracking progress: TODO/APPROVED/REJECTED), a createdAt timestamp, and an isActive boolean flag (default: false). The task links to a createdBy user (1..1 ASSOC), an assignee user (1..1 ASSOC) responsible for completing the task, and a targetProduct or target entity (0..1 ASSOC) that the task relates to. Denormalized display fields (createdByName, assigneeName, productTitle) provide quick rendering without joins. A derived isAssigneeCurrentUser flag enables UI personalization.

Operations on the Task include:
- **closeTask** (custom) -- resolves the task, typically setting state to APPROVED or REJECTED
- **activate** / **deactivate** -- toggle the isActive flag for task visibility

The CloseTaskInput unmapped TO carries a `result` attribute (the TaskState value) for the closeTask operation. The ApprovalTaskInput unmapped TO carries a `users` relation (0..* AGGREGATION) for selecting which users to assign approval tasks to.

Transfer objects provide role-specific task views: AuthorTask (for the product author, with closeTask operation), ApproverTask (for the assigned approver, with closeTask), AdminTask (for administrators, with activate/deactivate operations to manage task visibility).

This pattern is distinct from the workflow-engine Task/Token pattern in that it is a simple, domain-embedded task model without a full state machine engine. Tasks are created as side effects of product operations (assignApproval) rather than being driven by a generic workflow definition.

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
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Task", name: "assignee",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Task", name: "targetProduct",
  target: "{{NAMESPACE}}::Product", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "closeTask",
  customImplementation: true, operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "activate",
  customImplementation: false, operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Task", name: "deactivate",
  customImplementation: false, operationType: INSTANCE
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
