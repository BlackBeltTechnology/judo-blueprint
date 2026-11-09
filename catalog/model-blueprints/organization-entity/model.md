## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Organization%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name relationKind lower upper } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "OrganizationStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::OrganizationStatus", name: "ACTIVE", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::OrganizationStatus", name: "SUSPENDED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::OrganizationStatus", name: "DEACTIVATED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Organization",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "contactEmail"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "contactName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "contactPhone"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Organization", name: "logo"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Organization", name: "address",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Organization", name: "users",
  target: "{{NAMESPACE}}::User", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Organization", name: "capabilities",
  target: "{{NAMESPACE}}::Capability", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Organization`
  - Attributes: name (req), contactEmail (req), status (req), cityName, fullAddress, contactName, contactPhone, logo, membershipStart, membershipDescription, isUserCountHidden (default: false), isAdminOrganization (default: false), userCount
  - Relations: address (0..1 COMPOSITION), capabilities (0..* ASSOC), users (0..* ASSOC), news (0..* ASSOC), offers (0..* ASSOC), requests (0..* ASSOC), ownedFeedEntries (0..* ASSOC), feedEntries (0..* ASSOC), post (0..* ASSOC), invitations (0..* COMPOSITION)
- **OrganizationStatus enum**: `MLSZKSZPlatform::types::OrganizationStatus` -- ACTIVE(0), SUSPENDED(1), DEACTIVATED(2)
