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
