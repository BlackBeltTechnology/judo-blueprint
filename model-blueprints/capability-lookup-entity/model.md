## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Capability" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Capability",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Capability", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Capability", name: "description"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Capability", name: "isActive"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Capability`
  - Attributes: name (req), description, isActive (req, default: true)
  - No relations on the entity itself; referenced by: Organization (0..*), Offer (0..*), Request (0..*), RegistrationRequest (0..*)
- **Admin TO**: `MLSZKSZPlatform::services::admin::Capability`
  - Operations: activateToggle (toggle isActive), updateCapability
- **Input TO**: `MLSZKSZPlatform::services::admin::CapabilityInput` -- name (req), description
- Used across multiple service packages: admin, companyadmin, companyreader, feed -- all as read-only projections except admin
