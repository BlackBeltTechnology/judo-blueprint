---
id: application-vendor-integration-registry
title: "Application-Vendor Integration Registry (Enterprise Architecture)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
---

## Description

An enterprise integration registry entity cluster for tracking applications, their vendors, connections between applications, and deployment instances. The core entities are:

- **Application** -- a software application with id, name, version, category (enum: CRM, DMS, IMS, etc.), and a required association to its Vendor
- **Vendor** -- the company that provides/develops the application, with id, name, and address
- **HighLevelConnection** -- a business-level connection between two applications (sender and receiver), describing data flow with a name, description, periodicity (enum: ADHOC, HOURLY, DAILY, etc.), and associations to BusinessDataType and Brand entities for classification
- **ConnectionDefinition** -- a technical-level connection specification linking a HighLevelConnection to an InterfaceSpecification, with direction of data transmission, periodicity details, and optional client/server Application references
- **ApplicationInstance** -- a deployed instance of an Application in a specific Environment (DEV, TEST, PROD)
- **DeploymentItem** -- a deployment artifact associated with an ApplicationInstance
- **Server** -- a server hosting applications, with composed IP addresses (IPV4Address, IPV6Address)
- **ProvidedInterface** -- links an InterfaceSpecification to network addressing (port, IPv4/IPv6 address)
- **ClientInterface** -- links an InterfaceSpecification to a client-side endpoint
- **ConcreteConnection** -- connects a ClientInterface to a ProvidedInterface through a ConnectionDefinition, with an optional connect string

This cluster models the full enterprise integration landscape: what applications exist, who provides them, how they connect at both business and technical levels, and where they are deployed. The HighLevelConnection provides business stakeholders with an overview, while ConnectionDefinition, ProvidedInterface, ClientInterface, and ConcreteConnection provide technical details.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Application%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Connection%" } }) {
  items { fqn name
    relations { items { name memberType } }
  }
} } }
```

Look for Application entities with vendor relations and Connection entities linking applications.

## Creation Mutations

### Application entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Application",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Application", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Application", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Application", name: "version"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Application", name: "category"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Application", name: "vendor",
  target: "{{NAMESPACE}}::Vendor", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Vendor entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Vendor",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Vendor", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Vendor", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Vendor", name: "address"
} }) { success fqn } }
```

### HighLevelConnection entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "HighLevelConnection",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "description"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "periodicity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "senderApplication",
  target: "{{NAMESPACE}}::Application", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::HighLevelConnection", name: "receiverApplication",
  target: "{{NAMESPACE}}::Application", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### ApplicationCategory enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ApplicationCategory"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ApplicationCategory", name: "{{CATEGORY_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

### HighLevelPeriodicity enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "HighLevelPeriodicity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::HighLevelPeriodicity", name: "{{PERIODICITY_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

## Examples

### InterfaceRegister
**Core entities:**
- **Application**: `InterfaceRegister::entities::Application` (non-CRUD)
  - Attributes: id (String, req, identifier), name (String, req, identifier), category (ApplicationCategory, req), version (String, req)
  - Relations: vendor [1..1] ASSOC -> Vendor

- **Vendor**: `InterfaceRegister::entities::Vendor` (non-CRUD)
  - Attributes: id (String, req, identifier), name (String, req, identifier), address (String, req)

- **HighLevelConnection**: `InterfaceRegister::entities::HighLevelConnection` (non-CRUD)
  - Attributes: id (String, req, identifier), name (String, req, identifier), description (Text, req), periodicity (HighLevelPeriodicity, req)
  - Relations: senderApplication [1..1] ASSOC -> Application, receiverApplication [1..1] ASSOC -> Application, businessDataTypes [0..*] ASSOC -> BusinessDataType, brands [0..*] ASSOC -> Brand

- **ConnectionDefinition**: `InterfaceRegister::entities::ConnectionDefinition` (non-CRUD)
  - Attributes: id (String, req, identifier), directionOfDataTransmission (DirectionOfDataTransmission), peroiodicity (String, req), connectionDescription (Text, req)
  - Relations: interfaceSpecification [1..1] ASSOC -> InterfaceSpecification, clientApplication [0..1] ASSOC -> Application, serverApplication [0..1] ASSOC -> Application, highLevelConnection [1..1] ASSOC -> HighLevelConnection

**Deployment entities:**
- **ApplicationInstance**: `InterfaceRegister::entities::ApplicationInstance` (non-CRUD)
  - Attributes: id (String, req, identifier), environment (Environment, req)
  - Relations: application [1..1] ASSOC -> Application

- **DeploymentItem**: `InterfaceRegister::entities::DeploymentItem` (non-CRUD)
  - Attributes: id (String, req, identifier)
  - Relations: applicationInstance [1..1] ASSOC -> ApplicationInstance

**Network entities:**
- **Server**: `InterfaceRegister::entities::Server` (non-CRUD)
  - Attributes: id (String, req, identifier), name (String, req, identifier)
  - Relations: ipv4Addresses [0..*] COMPOSITION -> IPV4Address, ipv6Addresses [0..*] COMPOSITION -> IPV6Address

- **IPV4Address**: address (IPV4Address type, maxLength: 32)
- **IPV6Address**: address (IPV6Address type, maxLength: 200)

- **ProvidedInterface**: `InterfaceRegister::entities::ProvidedInterface` (non-CRUD)
  - Attributes: id (String, req, identifier), port (Integer, req)
  - Relations: interfaceSpecification [1..1] ASSOC -> InterfaceSpecification, ipv4Address [0..1] ASSOC -> IPV4Address, ipv6Address [0..1] ASSOC -> IPV6Address

- **ClientInterface**: `InterfaceRegister::entities::ClientInterface` (non-CRUD)
  - Attributes: id (String, req, identifier)
  - Relations: interfaceSpecification [1..1] ASSOC -> InterfaceSpecification

- **ConcreteConnection**: `InterfaceRegister::entities::ConcreteConnection` (non-CRUD)
  - Attributes: id (String, req, identifier), connectString (String)
  - Relations: clientInterface [1..1] ASSOC -> ClientInterface, providedInterface [1..1] ASSOC -> ProvidedInterface, connectionDefinition [1..1] ASSOC -> ConnectionDefinition

**Supporting enums:**
- `ApplicationCategory`: CRM(1), DMS(2), IMS(3), FINANCE_AND_ACCOUNTING_SYSTEM(4), DOCUMENT_MANAGEMENT_SYSTEM(5), WORKFLOW_MANAGEMENT_SYSTEM(6), FLEET_MANAGEMENT_SYSTEM(7), OTHER(8), EXTERNAL(9)
- `HighLevelPeriodicity`: ADHOC(1), HOURLY(2), DAILY(3), WEEKLY(4), MONTHLY(5), YEARLY(6), SOME_MINUTES(7), SOME_DAYS(8), SOME_WEEKS(9), SOME_MONTHS(10)

**Transfer objects:**
- `ApplicationTransfer` [maps Application] -- category, id, name, version + vendorTransfer [1..1] AGGREGATION
- `VendorTransfer` [maps Vendor] -- address, id, name
- `HighLevelConnectionTransfer` [maps HighLevelConnection] -- description, id, name, periodicity + brands/businessDataTypes [0..*] AGGREGATION, senderApplication/receiverApplication [1..1] AGGREGATION
- `ConnectionDefinition` TO [maps ConnectionDefinition] -- id, directionOfDataTransmission, peroiodicity, connectionDescription + relations to ApplicationTransfer, HighLevelConnectionTransfer, InterfaceSpecification TO
- `CreateApplicationInput` (unmapped) -- category, version, name, id + vendor [1..1] AGGREGATION to CreateApplicationVendorInput
- `CreateHighLevelConnectionInput` (unmapped) -- description, periodicity, name, id + denormalized sender/receiver fields + relations to CreateHighLevelConnectionApplicationInput, CreateHighLevelConnectionBrandInput, CreateHighLevelConnectionBusinessDataTypeInput, CreateHighLevelConnectionVendorInput

**Actor access:**
- EnterpriseArchitect actor accesses: applications (C, U), vendors (C, U), highLevelConnections (C, U), connectionDefinitions (C, U), dashboard (read-only)
