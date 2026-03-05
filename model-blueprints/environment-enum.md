---
id: environment-enum
title: "Environment Enum (DEV/TEST/PROD Deployment Stages)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
---

## Description

An enumeration representing deployment environment stages, typically with three members: DEV (development), TEST (testing/staging), and PROD (production). This is a standard software lifecycle classification used to categorize application instances, server deployments, or configuration sets by their target environment. The enum enables filtering and grouping resources by environment in enterprise architecture and operations management contexts.

This enum is typically used as a required attribute on deployment-related entities (e.g., ApplicationInstance, Server, DeploymentItem) to indicate which environment a particular resource belongs to.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members matching DEV, TEST, PROD (or DEVELOPMENT, STAGING, PRODUCTION).

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "Environment"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Environment", name: "DEV", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Environment", name: "TEST", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Environment", name: "PROD", ordinal: 3
} }) { success fqn } }
```

## Examples

### InterfaceRegister
- **Enum**: `InterfaceRegister::entities::Environment` -- DEV(1), TEST(2), PROD(3)
- Used as a required attribute on `ApplicationInstance` entity: environment (Environment, req)
- ApplicationInstance represents a deployed instance of an Application in a specific environment
- The enum enables tracking which environments an application has been deployed to, supporting enterprise operations management workflows
- Other environment-adjacent enums in the same model: `DevelopmentType` (COTS, COTS_WITH_ADDITIONAL_DEVELOPMENTS, CUSTOM_DEVELOPMENT, UNKNOWN) classifies how the application was built
