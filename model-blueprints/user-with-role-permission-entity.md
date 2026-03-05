---
id: user-with-role-permission-entity
title: "User Entity with Role and Permission Entities"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---

## Description

A User entity with core identity attributes (name, email) and an association to Role entities (many-to-many). Each Role has a name and a permissions relation (0..*) to Permission entities. Permissions are represented as entities (rather than enum members directly) with a flag attribute typed to a PermissionFlag enum. The PermissionFlag enum lists all controllable areas of the application (e.g., PARTNERS, USERS, ROLES, COMPANY_DATA, CONFIGURATION). The User entity carries denormalized boolean attributes for each permission (permissionToPartners, permissionToUsers, etc., all default: false) so that access control can be checked without traversing relations. A `recalculatePermissions` operation updates these denormalized booleans from the role/permission graph.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Permission" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "PermissionFlag" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "PermissionFlag"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PermissionFlag", name: "{{FLAG_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Permission",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Permission", name: "flag"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Permission", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Role",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Role", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Role", name: "permissions",
  target: "{{NAMESPACE}}::Permission", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: false, updateable: false, deleteable: false
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
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "roles",
  target: "{{NAMESPACE}}::Role", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "permissionTo{{AREA_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::User", name: "recalculatePermissions",
  customImplementation: true, operationType: INSTANCE
} }) { success fqn } }
```

## Examples

### rackinspect
- **User entity**: `rackinspect::entities::User` (non-CRUD)
  - Attributes (28): name (req), email (req), active (default: true), notes, rolesString, plus 23 denormalized permission booleans (permissionToCompanyData, permissionToConfiguration, permissionToDocumentRegistry, permissionToExchangeRates, permissionToPartners, permissionToPaymentDeadlines, permissionToPaymentMethods, permissionToRoles, permissionToUnits, permissionToUsers, permissionToFaultRegistries, permissionToOffers, permissionToItems, permissionToRepairCategories, permissionToDimensionTemplates, permissionToErrorCategories, permissionToRackElements, permissionToRackTypes, permissionToBrands, permissionToRepairTypes, permissionToErrorDestinations, permissionToErrorCodes, permissionToErrorQualifications)
  - Relations: roles (0..* ASSOC to Role), permissions (0..* DERIVED), userAddresses/userEmails/userPhones (0..* COMPOSITION), primaryUserAddress/primaryUserEmail/primaryUserPhone (0..1 ASSOC), tasks (0..* ASSOC)
  - Operations: toggleActive, recalculatePermissions (custom), createExchangeRate, updateExchangeRateForDateInterval
- **Role entity**: `rackinspect::entities::Role` -- name (req), permissions (0..* ASSOC to Permission)
- **Permission entity**: `rackinspect::entities::Permission` -- flag (req), id (req)
- **PermissionFlag enum**: `rackinspect::entities::PermissionFlag` -- 23 members: FAULT_REGISTRIES(1), OFFERS(2), ITEMS(3), REPAIR_CATEGORIES(4), DIMENSION_TEMPLATES(5), ERROR_CATEGORIES(6), RACK_ELEMENTS(7), RACK_TYPES(8), PARTNERS(9), BRANDS(10), REPAIR_TYPES(11), ERROR_DESTINATIONS(12), EXCHANGE_RATES(13), USERS(14), ERROR_CODES(15), ERROR_QUALIFICATIONS(16), UNITS(17), PAYMENT_METHODS(21), COMPANY_DATA(25), ROLES(26), PAYMENT_DEADLINES(28), CONFIGURATION(29), DOCUMENT_REGISTRY(31)
