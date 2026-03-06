---
id: "capability-lookup-entity"
title: "Capability/Tag Lookup Entity"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A Capability (or Tag/Category) entity that serves as a reusable lookup/classification entity. It has a name, optional description, and an isActive boolean flag (default: true) for soft-enabling/disabling. Multiple entities reference it via many-to-many ASSOCIATION relations (e.g., Organization has capabilities, Offer has capabilities, Request has capabilities). This provides a flexible tagging system where platform admins can create and manage capabilities, and other entities can be associated with any combination of them. The transfer object exposes an activateToggle operation for toggling the isActive flag.

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
