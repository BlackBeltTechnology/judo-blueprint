---
id: "address-entity-with-location"
title: "Address Entity with Geolocation"
score: 61.0
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - doors-model
---
## Description

An Address entity that captures structured address fields (street, building, floor, door, postal code) along with a composed Location entity for geographic coordinates (latitude, longitude). The address references a City and PostalCode via associations, and a Location via composition. A computed `fullAddress` attribute provides a concatenated display string. This pattern is common in platforms that need to store physical addresses with map-pinning capability. Variants include type-flags (isBilling, isHeadquarters, isPostal, isDelivery) with corresponding toggle operations, and a Country association instead of (or in addition to) City/PostalCode references. Simpler variants store city, country, street, and zipCode as direct string attributes rather than referencing lookup entities, with a derived `fullAddress` computed from the concatenation of these fields.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Address%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name relationKind memberType } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Location",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Location", name: "latitude"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Location", name: "longitude"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Address",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "streetName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "number"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "building"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "floor"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "door"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Address", name: "fullAddress"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Address", name: "location",
  target: "{{NAMESPACE}}::Location", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Address", name: "city",
  target: "{{NAMESPACE}}::City", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Address", name: "postalCode",
  target: "{{NAMESPACE}}::PostalCode", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Address entity**: `MLSZKSZPlatform::entities::Address`
  - Attributes: streetName (req), publicPlaceCategory, number, building, staircase, floor, door, lotNumber, fullAddress (req), addressInformation (req)
  - Relations: location (0..1 COMPOSITION to Location), city (1..1 ASSOCIATION to City), postalCode (1..1 ASSOCIATION to PostalCode)
- **Location entity**: `MLSZKSZPlatform::entities::Location`
  - Attributes: latitude (req), longitude (req)
- **City entity**: `MLSZKSZPlatform::entities::City` with name, isActive; composes PostalCode
- **PostalCode entity**: `MLSZKSZPlatform::entities::PostalCode` with code attribute
- Used by: Organization (composition), RegistrationRequest (composition)

### rackinspect
- **Address entity**: `rackinspect::entities::Address` (non-CRUD)
  - Attributes (23): streetName (req), city (req), postalCode (req), building, floor, door, number, lotNumber, staircase, publicPlaceCategory, fullAddress (req, default: "-"), addressInformation (req), manualAddressInformation (req), region, notes, active (default: true), isBilling (default: false), isDelivery (default: false), isHeadquarters (default: false), isPostal (default: false), cityAndPostalCode, fullAddressMultiline, transportationDistance
  - Relations: country (1..1 ASSOC), warehouses (0..* COMPOSITION), container (0..1 DERIVED)
  - Operations: toggleActive, toggleBilling, toggleDelivery, toggleHeadquarters, togglePostal -- all custom INSTANCE
- **CompanyAddress entity**: `rackinspect::entities::CompanyAddress` (non-CRUD)
  - Same core address fields, plus toggleActive, toggleBilling, toggleHeadquarters, togglePostal, togglePrimary operations
  - Relations: country (1..1 ASSOC), container (0..1 DERIVED)
- **UserAddress entity**: `rackinspect::entities::UserAddress` (non-CRUD)
  - Simplified: city (req), postalCode (req), addressInformation (req), fullAddress, active (default: true), notes
  - Operations: toggleActive, togglePrimary
- Used by: Partner (addresses 0..* COMPOSITION), CompanyData (companyAddresses 0..* COMPOSITION), User (userAddresses 0..* COMPOSITION)

### doors-model
- **Address entity**: `doors::entities::Address` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: street (req), city (req), country (req), zipCode (req), fullAddress (DERIVED: `self.country + ", " + self.zipCode + " " + self.city + ", " + self.street`)
  - No relations -- no Location, City, or PostalCode references; all address fields are stored as direct string attributes
- Simplified variant: stores city, country, street, and zipCode as flat string attributes rather than referencing lookup entities
- The `fullAddress` attribute is a derived/computed field that concatenates the address components in the format "country, zipCode city, street"
- Used by multiple Partner subtypes via COMPOSITION:
  - Partner -> postalAddress [0..1]
  - CompanylikePartner -> hqAddress [0..1] (headquarters address)
  - OrganizationPartner -> siteAddresses [0..*] (multiple site addresses)
  - PrivatePartner -> livingAddress [0..1]
  - OtherPartner -> address [0..1]
- The Address TO in the employee actor package exposes all stored fields plus the derived fullAddress, along with edit operations for managing addresses on partners
