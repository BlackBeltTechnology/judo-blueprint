---
id: "identity-account-organization-cluster"
title: "Identity-Account-Organization Multi-Tenant Cluster"
score: 44.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---
## Description

A multi-tier entity cluster for identity and multi-tenant organization management. The structure consists of:

- **IdentityEntity** -- the authentication root, representing a unique person identified by email. An identity links to multiple accounts (different platform contexts) and multiple users (organization-scoped identities), plus optional biometric identifiers (face recognition IDs).
- **AccountEntity** -- a platform-level account with userName, email, and a superAdmin flag. An account links to a single identity (1..1 ASSOCIATION) and composes organization accesses (0..* COMPOSITION) that define which organizations the account can manage and with what role.
- **UserEntity** -- an organization-scoped user with userName, email, and an enabled/disabled flag. Users link back to their identity (1..1 ASSOCIATION) and their owning organization (0..1 DERIVED). Enable/disable operations toggle user access.
- **OrganizationEntity** -- a tenant/workspace entity with a name, a registration feature toggle (isRegistrationFeatureSupported), and compositions for applications, invitations, users, and a realm. Organizations also associate to organization accesses.
- **OrganizationAccessEntity** -- a junction entity connecting accounts to organizations with a type (OWNER/ADMIN enum), an enabled flag, and denormalized userName/organizationName. Operations allow changing access level (changeAccessToAdmin, changeAccessToOwner), enabling/disabling access, and canceling access.

The separation of Identity from Account from User enables a single person to have one identity, multiple platform accounts, and multiple organization-scoped users -- supporting true multi-tenancy where a person can participate in many organizations through a single login.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Identity%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%OrganizationAccess%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "IdentityEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::IdentityEntity", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::IdentityEntity", name: "account",
  target: "{{NAMESPACE}}::AccountEntity", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::IdentityEntity", name: "user",
  target: "{{NAMESPACE}}::UserEntity", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "AccountEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AccountEntity", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AccountEntity", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AccountEntity", name: "isSuperAdmin"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::AccountEntity", name: "identity",
  target: "{{NAMESPACE}}::IdentityEntity", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::AccountEntity", name: "organizationAccesses",
  target: "{{NAMESPACE}}::OrganizationAccessEntity", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "UserEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserEntity", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserEntity", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserEntity", name: "enabled"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::UserEntity", name: "identity",
  target: "{{NAMESPACE}}::IdentityEntity", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::UserEntity", name: "enableUser",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::UserEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::UserEntity", name: "disableUser",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::UserEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "OrganizationAccessType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::OrganizationAccessType", name: "OWNER", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::OrganizationAccessType", name: "ADMIN", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "OrganizationAccessEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "enabled"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "organizationName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "organization",
  target: "{{NAMESPACE}}::OrganizationEntity", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "cancelAccess",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::OrganizationAccessEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "changeAccessToAdmin",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::OrganizationAccessEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "changeAccessToOwner",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::OrganizationAccessEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "enableAccess",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::OrganizationAccessEntity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::OrganizationAccessEntity", name: "disableAccess",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::OrganizationAccessEntity"
} }) { success fqn } }
```

## Examples

### ubives
**Entity cluster:**
- **IdentityEntity**: `Ubives::entities::IdentityEntity` (non-CRUD)
  - Attributes: email (req)
  - Relations: faceIdentifier (0..* ASSOC to FaceIdentifierEntity), user (0..* ASSOC to UserEntity), account (0..* ASSOC to AccountEntity)
  - Central identity hub: one person has one identity, which can link to multiple accounts and multiple organization-scoped users
- **AccountEntity**: `Ubives::entities::AccountEntity` (non-CRUD)
  - Attributes: userName (req), email (req), isSuperAdmin (req, default: false), isNotSuperAdmin (derived), isSingleOrganizationForAccount (req, default: true), isNotSingleOrganizationForAccount (derived)
  - Relations: identity (1..1 ASSOC to IdentityEntity), organizationAccesses (0..* COMPOSITION to OrganizationAccessEntity)
  - Operations: createOrganization (INSTANCE)
  - Guard attributes (isNotSuperAdmin, isNotSingleOrganizationForAccount) control UI visibility
- **UserEntity**: `Ubives::entities::UserEntity` (non-CRUD)
  - Attributes: userName (req), email (req), enabled (req, default: true), notEnabled (derived)
  - Relations: identity (1..1 ASSOC), accounts (0..* DERIVED), organization (0..1 DERIVED)
  - Operations: enableUser (INSTANCE), disableUser (INSTANCE)
- **OrganizationEntity**: `Ubives::entities::OrganizationEntity` (non-CRUD)
  - Attributes: name (req), isRegistrationFeatureSupported (req, default: false), isRegistrationFeatureNotSupported (derived), realmName (optional)
  - Relations: applications (0..* COMPOSITION), invitations (0..* COMPOSITION), realm (0..1 COMPOSITION to RealmEntity), users (0..* COMPOSITION), organizationAccesses (0..* ASSOC)
  - Operations: createApplication, inviteAccount, inviteUser, enableOrganizationRegistration, disableOrganizationRegistration, leaveOrganization, deleteOrganization (all INSTANCE)
- **OrganizationAccessEntity**: `Ubives::entities::OrganizationAccessEntity` (non-CRUD)
  - Attributes: type (req, OrganizationAccessType enum), enabled (req, default: true), userName (derived), organizationName (derived)
  - Relations: account (0..1 DERIVED), organization (1..1 ASSOC)
  - Operations: cancelAccess, changeAccessToAdmin, changeAccessToOwner, disableAccess, enableAccess (all INSTANCE)
- **OrganizationAccessType enum**: `Ubives::entities::OrganizationAccessType` -- OWNER(1), ADMIN(2)

**Transfer objects:**
- `Account` TO -- mapped to AccountEntity; operations: createOrganization
- `AccountPrincipal` TO -- mapped to AccountEntity with guard flags: isOrganizationSelected, isNotOrganizationSelected, alwaysTrue, alwaysFalse
- `Profile` TO -- mapped to AccountEntity; operations: createOrganization, leaveOrganization
- `Organization` TO -- mapped to OrganizationEntity with users, applications, invitations, organizationAccounts relations; operations: createApplication, inviteAccount, inviteUser, enable/disableOrganizationRegistration, leaveOrganization
- `DashboardOrganization` TO -- simplified Organization view for dashboard; all operations mapped
- `OrganizationAccount` TO -- mapped to OrganizationAccessEntity; attributes: type, email, userName, isAdministrator, isOwner, enabled; operations: cancelAccess, changeAccessToAdmin, changeAccessToOwner, disableAccess, enableAccess
- `PartnerDashboard` TO -- empty access point TO with static operations: createOrganization, createApplication, inviteAccount, inviteUser, etc.
