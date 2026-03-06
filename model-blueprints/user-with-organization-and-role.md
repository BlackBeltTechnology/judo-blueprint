---
id: "user-with-organization-and-role"
title: "User Entity with Organization and Role Enum"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A User entity with core identity attributes (name, email), a role attribute typed to a UserRole enum, a status attribute typed to a UserStatus enum, and an association to an Organization. The user carries notification preference booleans (notifyOffers, notifyRequests, etc.), visibility flags, and maintains relations to Devices and Notifications. The UserRole enum defines platform-level roles (e.g., COMPANY_ADMIN, COMPANY_READER, PLATFORM_ADMIN). The UserStatus enum follows the Active/Suspended/Deactivated tri-state lifecycle.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "User" } }) {
  items { fqn name
    attributes { items { name required } }
    relations { items { name memberType relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "UserRole"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::UserRole", name: "{{ROLE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "UserStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::UserStatus", name: "ACTIVE", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::UserStatus", name: "SUSPENDED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::UserStatus", name: "DEACTIVATED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "role"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "organization",
  target: "{{NAMESPACE}}::Organization", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::User`
  - Attributes: name (req), email (req), role (req), status (req), isVisible (default: true), isSilentMode, emailNotifications, organizationName, notifyOffers (default: true), notifyRequests (default: true), notifyAnnouncements (default: true), notifyNews, lastLogin
  - Relations: organization (1..1), inquiries (0..*), devices (0..*), notifications (0..*)
- **UserRole enum**: `MLSZKSZPlatform::types::UserRole` -- COMPANY_ADMIN(0), COMPANY_READER(1), PLATFORM_ADMIN(2), ASSOCIATION_LEADERSHIP(3)
- **UserStatus enum**: `MLSZKSZPlatform::types::UserStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)
- Transfer objects project different views: admin::CompanyUser (with activate/deactivate/suspend ops), companyreader::ProfilePanel (notification prefs), technical::User (access control flags)
