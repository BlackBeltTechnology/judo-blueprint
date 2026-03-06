---
id: "privacy-visibility-enum"
title: "Privacy Visibility Enum (Granular Data Visibility Levels)"
score: 33.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - sanctuary-backend
---
## Description

An enumeration representing granular visibility levels for user data fields. Instead of a binary public/private toggle, this enum provides multiple scoping levels that control who can see a particular piece of user information. The levels form an expanding hierarchy of visibility:

- **publicForPeers** -- visible only to direct peers (closest circle)
- **publicForTeam** -- visible to the user's team members
- **publicForUnit** -- visible to the user's organizational unit
- **publicForEveryone** -- visible to all users in the system

This enum is typically used as the data type for multiple attributes on a UserPrivacySettings entity (composed by the User entity), where each attribute controls the visibility of a specific user data field (e.g., phone number, badges). This enables per-field privacy control rather than a single global privacy setting.

The scoping levels assume an organizational hierarchy (peer < team < unit < everyone) and are suitable for enterprise or community platforms where users belong to nested organizational structures.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members matching a pattern of expanding visibility scopes (e.g., publicForPeers, publicForTeam, publicForUnit, publicForEveryone).

```graphql
{ esm { entitytypes(where: { name: { like: "%PrivacySettings%" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

Look for a PrivacySettings entity with multiple attributes typed to a visibility enum.

## Creation Mutations

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

### UserPrivacySettings entity (using the enum)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "UserPrivacySettings",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::UserPrivacySettings", name: "{{FIELD_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "privacySettings",
  target: "{{NAMESPACE}}::UserPrivacySettings", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

## Examples

### sanctuary-backend
- **Enum**: `Sanctuary::user::PrivacyVisibility` -- publicForPeers(1), publicForTeam(2), publicForUnit(3), publicForEveryone(4)
- **UserPrivacySettings entity**: `Sanctuary::user::UserPrivacySettings` (createable/updateable/deleteable)
  - Attributes (all typed to PrivacyVisibility):
    - phoneNumber -- controls visibility of the user's phone number
    - peerBadges -- controls visibility of peer-awarded badges
    - specialBadges -- controls visibility of special badges
    - systemBadges -- controls visibility of system-awarded badges
- The UserPrivacySettings entity is composed (owned) by the User entity via a [0..1] COMPOSITION relation
- The corresponding `UserPrivacySettingsTO` transfer object is the only TO in this model with CRUD flags enabled, allowing direct privacy settings management through the API
- The enum ordinals (1-4) represent expanding visibility scope, enabling range-based queries (e.g., "show to anyone with visibility level >= publicForTeam")
