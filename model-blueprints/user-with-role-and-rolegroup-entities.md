---
id: user-with-role-and-rolegroup-entities
title: "User Entity with Role and RoleGroup Entities (Hierarchical Role Assignment)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - sanctuary-backend
---

## Description

A User entity with identity and profile attributes, associated to Role entities via a bidirectional many-to-many relation, and to RoleGroup entities via a separate bidirectional many-to-many relation. RoleGroups aggregate multiple Roles into named collections, enabling bulk role assignment. This provides a two-level role hierarchy: individual roles can be assigned directly to users, and role groups can be assigned to users to grant all roles within the group at once.

The core entities are:

- **User** -- an identity with personal details (email, firstName, lastName), profile attributes (profilePhoto, sex), a status attribute (active/archived enum), and contact information (phoneNumber). The User has composed settings entities (UserPrivacySettings, UserSettings) for user preferences, and a derived `effectiveRoles` relation that computes the aggregate set of roles from direct assignments and role group memberships.
- **Role** -- a named role entity with a bidirectional association to Users. Roles represent individual permission sets or functional access levels.
- **RoleGroup** -- a named group that aggregates multiple Roles (one-way association to Role) and has a bidirectional association to Users. RoleGroups enable batch role assignment by collecting related roles under a single group name.
- **PositionTitle** -- a reference data entity representing a user's job title, with a title attribute and status (active/archived). Users have an optional association to a PositionTitle.
- **UserPrivacySettings** -- a composition child of User that controls visibility of user data fields (phoneNumber, peerBadges, specialBadges, systemBadges) using a PrivacyVisibility enum with granular levels (publicForPeers, publicForTeam, publicForUnit, publicForEveryone).
- **UserSettings** -- a composition child of User for UI preferences (e.g., darkMode boolean).

Key structural patterns:
- Bidirectional many-to-many between User and Role, and between User and RoleGroup
- RoleGroup has a one-way association to Roles (groups contain roles but roles do not back-reference groups)
- Derived `effectiveRoles` relation on User aggregates roles from direct assignment and group membership
- Composition pattern for user settings/preferences (User owns UserPrivacySettings and UserSettings)
- PrivacyVisibility enum for per-field visibility control

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "RoleGroup" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "User" } }) {
  items { fqn name
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

Look for a User entity with both `roles` and `roleGroups` relations, and a RoleGroup entity with a `roles` relation to Role entities.

## Creation Mutations

### Role entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Role",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Role", name: "name"
} }) { success fqn } }
```

### RoleGroup entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "RoleGroup",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::RoleGroup", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::RoleGroup", name: "roles",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### User entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "firstName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "lastName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "roles",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "roleGroups",
  target: "{{NAMESPACE}}::RoleGroup", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### UserPrivacySettings entity (composition child)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "UserPrivacySettings",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserPrivacySettings", name: "phoneNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "privacySettings",
  target: "{{NAMESPACE}}::UserPrivacySettings", lower: 0, upper: 1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### UserSettings entity (composition child)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "UserSettings",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserSettings", name: "darkMode"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "settings",
  target: "{{NAMESPACE}}::UserSettings", lower: 0, upper: 1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### PrivacyVisibility enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "PrivacyVisibility"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PrivacyVisibility", name: "publicForPeers", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PrivacyVisibility", name: "publicForTeam", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PrivacyVisibility", name: "publicForUnit", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PrivacyVisibility", name: "publicForEveryone", ordinal: 4
} }) { success fqn } }
```

### PositionTitle entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "PositionTitle",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PositionTitle", name: "title"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PositionTitle", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "positionTitle",
  target: "{{NAMESPACE}}::PositionTitle", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### sanctuary-backend
**Entity types (all in Sanctuary::user package):**

- **User**: `Sanctuary::user::User` (createable/updateable/deleteable)
  - Attributes: email (Email), title (String), firstName (String), lastName (String), sex (String), profilePhoto (String), status (ActiveStatus), phoneNumber (Phone)
  - Relations:
    - privacySettings [0..1] COMPOSITION -> UserPrivacySettings
    - settings [0..1] COMPOSITION -> UserSettings
    - roles [0..*] ASSOCIATION -> Role (bidirectional, partner=users)
    - roleGroups [0..*] ASSOCIATION -> RoleGroup (bidirectional, partner=users)
    - positionTitle [0..1] ASSOCIATION -> PositionTitle
    - effectiveRoles [0..*] ASSOCIATION -> Role (DERIVED: `self.roles`)

- **Role**: `Sanctuary::user::Role` (createable/updateable/deleteable)
  - Attributes: name (String)
  - Relations: users [0..*] ASSOCIATION -> User (bidirectional, partner=roles)

- **RoleGroup**: `Sanctuary::user::RoleGroup` (createable/updateable/deleteable)
  - Attributes: name (String)
  - Relations:
    - roles [0..*] ASSOCIATION -> Role (one-way)
    - users [0..*] ASSOCIATION -> User (bidirectional, partner=roleGroups)

- **PositionTitle**: `Sanctuary::user::PositionTitle` (createable/updateable/deleteable)
  - Attributes: title (String), status (ActiveStatus)

- **UserPrivacySettings**: `Sanctuary::user::UserPrivacySettings` (createable/updateable/deleteable)
  - Attributes: phoneNumber (PrivacyVisibility), peerBadges (PrivacyVisibility), specialBadges (PrivacyVisibility), systemBadges (PrivacyVisibility)

- **UserSettings**: `Sanctuary::user::UserSettings` (createable/updateable/deleteable)
  - Attributes: darkMode (Boolean)

**Enumerations:**
- `Sanctuary::user::PrivacyVisibility`: publicForPeers(1), publicForTeam(2), publicForUnit(3), publicForEveryone(4)
- `Sanctuary::ActiveStatus`: active(1), archived(2)

**Transfer objects (all mapped, in Sanctuary::user):**
- `UserTO` [maps User] -- all entity attributes + relations to RoleTO, RoleGroupTO, PositionTitleTO, UserPrivacySettingsTO (AGGREGATION), UserSettingsTO (AGGREGATION), effectiveRoles
- `RoleTO` [maps Role] -- name
- `RoleGroupTO` [maps RoleGroup] -- name + roles [0..*] ASSOCIATION to RoleTO
- `PositionTitleTO` [maps PositionTitle] -- title, status
- `UserPrivacySettingsTO` [maps UserPrivacySettings] -- phoneNumber, peerBadges, specialBadges, systemBadges (createable/updateable/deleteable)
- `UserSettingsTO` [maps UserSettings] -- darkMode

**Actor:**
- `Sanctuary::Admin` (anonymous, human, realm=DEFAULT, managed=true)
  - accesses: users [0..*] -> UserTO (full CRUD), roles [0..*] -> RoleTO (full CRUD), roleGroups [0..*] -> RoleGroupTO (full CRUD), positionTitles [0..*] -> PositionTitleTO (full CRUD)
  - Menu items: UsersMenu, RolesMenu, RoleGroupsMenu, PositionTitlesMenu

**Notable features:**
- The model has several empty placeholder packages (unit, article, project, faq) suggesting the project is in early development with planned expansion
- The `effectiveRoles` derived relation currently only resolves to `self.roles` (direct assignments), not yet incorporating roles from RoleGroups
- The UserPrivacySettingsTO is the only transfer object with CRUD flags enabled (createable/updateable/deleteable), allowing direct privacy settings management
