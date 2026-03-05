---
id: freight-reservation-cluster
title: "Freight Reservation Entity Cluster (Logistics Domain)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - reserve-app
---

## Description

A domain-specific entity cluster for managing freight/logistics reservations at a warehouse or facility. The central FreightReservation entity connects a rich web of reference data entities to model a delivery event:

- **FreightReservation** -- the core booking with time slot (start, end), state lifecycle, vehicle details (numberPlate, driver, phone), loading details (machine, driver, phone), origin (fromLocation), partial delivery flag, and a technical identifier. It composes attachments (photos) and associates to all the reference entities below.
- **Gate** -- physical loading dock/gate at the facility
- **Spot** -- parking/staging area within the facility
- **Project** -- organizational grouping for reservations; scoped to users and spots
- **Partner** -- external delivery company (with name, address, contact, phone, externalIdentifier)
- **Company** -- internal receiving company
- **VehicleType** -- classification of vehicle (truck, van, etc.)
- **LoadingType** -- how goods are loaded/unloaded
- **LoadingTime** -- estimated duration for loading/unloading (name + minutes)
- **Item** -- line items on the reservation with quantity, product category, unit, and storage type
- **ProductCategory**, **Unit**, **StorageType** -- classification entities for items

The Item entity links a reservation to its cargo details: each item references a ProductCategory, Unit, and StorageType, enabling tracking of what is being delivered, in what quantities, using what measurement, and how it should be stored. A `deleted` flag on Item supports soft-removal of line items.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%FreightReservation%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Item" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "FreightReservation",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "start"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "end"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "state"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "fromLocation"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "vehicleNumberPlate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "vehicleDriver"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "vehiclePhone"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "loadMachine"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "loadDriver"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "loadPhone"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "partialDelivery"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "technicalID"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "gate",
  target: "{{NAMESPACE}}::Gate", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "spot",
  target: "{{NAMESPACE}}::Spot", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "project",
  target: "{{NAMESPACE}}::Project", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "partner",
  target: "{{NAMESPACE}}::Partner", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "recipient",
  target: "{{NAMESPACE}}::Company", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "vehicleType",
  target: "{{NAMESPACE}}::VehicleType", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "loadingType",
  target: "{{NAMESPACE}}::LoadingType", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "loadingTime",
  target: "{{NAMESPACE}}::LoadingTime", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "attachments",
  target: "{{NAMESPACE}}::Attachment", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FreightReservation", name: "items",
  target: "{{NAMESPACE}}::Item", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Item",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Item", name: "quantity"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Item", name: "deleted"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Item", name: "productCategory",
  target: "{{NAMESPACE}}::ProductCategory", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Item", name: "unit",
  target: "{{NAMESPACE}}::Unit", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Item", name: "storageType",
  target: "{{NAMESPACE}}::StorageType", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### reserve-app
**Core reservation entity:**
- `ReserveApp::entities::FreightReservation` (non-CRUD)
  - Time: start, end
  - State: state (FreightState enum, 9 states)
  - Vehicle: vehicleNumberPlate, vehicleDriver, vehiclePhone
  - Loading: loadMachine, loadDriver, loadPhone, partialDelivery, fromLocation
  - Identity: technicalID
  - Attachments: attachments (0..* COMPOSITION to Attachment)
  - Resource assignments: gate (0..1), spot (0..1), project (0..1), loadingTime (0..1)
  - Parties: partner (0..1 ASSOC), recipient (1..1 ASSOC to Company)
  - Configuration: vehicleType (1..1 ASSOC), loadingType (1..1 ASSOC)
  - Cargo: items (0..* ASSOC to Item)
  - Suspension tracking: suspendedByPartner (0..1 ASSOC to User), suspendedByLogistician (0..1 ASSOC to User)

**Line item entity:**
- `ReserveApp::entities::Item` (non-CRUD)
  - Attributes: quantity, deleted (soft-delete flag)
  - Relations: productCategory (0..1), unit (0..1), storageType (0..1), freightReservation (0..1)

**Reference data entities** (all name + active pattern):
- Gate, Spot, VehicleType, LoadingType, LoadingTime (adds minutes), ProductCategory, Unit, StorageType

**Organizational entities:**
- Partner -- name (req), address, contact, phone (req), externalIdentifier, active; relations: freightReservations (0..*), contacts (0..*)
- Company -- name (req), active; relation: contacts (0..*)
- Project -- name (req), active; relations: users (0..*), spots (0..*), freightReservations (0..*)

**Project scoping**: Projects link users to spots and reservations, enabling per-project access control: a user sees only reservations for their assigned projects, and spots are organized by project.
