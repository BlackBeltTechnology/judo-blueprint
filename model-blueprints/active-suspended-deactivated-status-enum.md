---
id: "active-suspended-deactivated-status-enum"
title: "Active/Suspended/Deactivated Status Enum"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A three-state lifecycle enumeration with members ACTIVE, SUSPENDED, and DEACTIVATED. This pattern models entities that can be temporarily suspended (reversible) or permanently deactivated (typically irreversible). It is commonly applied to both User and Organization entities in platforms that require administrative account management. The corresponding transfer objects expose activate/suspend/deactivate operations to transition between states.

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%Status%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "{{ENTITY_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{ENTITY_NAME}}Status", name: "ACTIVE", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{ENTITY_NAME}}Status", name: "SUSPENDED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DEACTIVATED", ordinal: 2
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **OrganizationStatus**: `MLSZKSZPlatform::types::OrganizationStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)
- **UserStatus**: `MLSZKSZPlatform::types::UserStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)
- Both share the exact same member names and ordinals
- Organization admin panel exposes suspend/activate operations on `CompanyUser` TO
- Transfer object `OrganizationAdminPanel` has suspend/activate operations
