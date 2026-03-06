---
id: "audit-log-entity"
title: "Audit Log Entity"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

An AuditLog entity that records system events with a timestamp, action type (typically an enum), the entity type and ID being acted upon, a details text field, and an optional association to the User who performed the action. Denormalized fields like userName and organizationName allow audit records to remain readable even after the referenced user or organization is modified. The entity is typically non-CRUD (createable=false, updateable=false, deleteable=false), created only through backend operations.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%AuditLog%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "AuditLog",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "timestamp"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "actionType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "entityType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "entityId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "details"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::AuditLog", name: "user",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "AuditActionType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::AuditActionType", name: "{{ACTION_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::AuditLog`
  - Attributes: timestamp (req), actionType (req), entityType (req), entityId, details, userName, organizationName
  - Relations: user (0..1 ASSOCIATION to User)
  - Non-CRUD: createable=false, updateable=false, deleteable=false
- **Enum**: `MLSZKSZPlatform::types::AuditActionType` with 32 members covering USER_LOGIN, USER_CREATED, ORGANIZATION_CREATED, POST_PUBLISHED, ANNOUNCEMENT_DELETED, etc.
- **Transfer Object**: `MLSZKSZPlatform::services::admin::AuditLog` (mapped, read-only view for admin dashboard)
- Admin dashboard provides `exportAuditLog` operation for CSV export
