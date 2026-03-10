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
