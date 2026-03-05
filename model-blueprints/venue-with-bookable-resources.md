---
id: venue-with-bookable-resources
title: "Venue with Bookable Resource Slots"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
---

## Description

A two-level resource hierarchy for bookable venues: a Venue/Facility entity (e.g., ParkingGarage) containing multiple bookable Resource/Slot entities (e.g., ParkingSlot). The venue has a name, isActive flag, and optional email template for notifications. It maintains associations to authorized users (accessedUsers) and users with special access (usersWithIdCard). Each resource slot has an identifier (id), physical descriptors (floor, nextToWall, floorPlan), an isActive flag, an isExclusive flag, and a denormalized venue name. The slot links back to its venue (1..1 ASSOC) and has a collection of reservations (0..*). Users have a preferredSlot (0..1) association for default booking, and an accessedVenues (0..*) association listing which venues they can book in. This pattern models any domain where physical spaces are divided into individually bookable units with access control.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%ParkingGarage%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%ParkingSlot%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{VENUE_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{VENUE_NAME}}", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{VENUE_NAME}}", name: "isActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{VENUE_NAME}}", name: "{{SLOT_PLURAL}}",
  target: "{{NAMESPACE}}::{{SLOT_NAME}}", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{VENUE_NAME}}", name: "accessedUsers",
  target: "{{NAMESPACE}}::User", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{SLOT_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "floor"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "isActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "isExclusive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "{{VENUE_RELATION}}",
  target: "{{NAMESPACE}}::{{VENUE_NAME}}", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{SLOT_NAME}}", name: "reservations",
  target: "{{NAMESPACE}}::Reservation", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "preferred{{SLOT_NAME}}",
  target: "{{NAMESPACE}}::{{SLOT_NAME}}", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "accessed{{VENUE_PLURAL}}",
  target: "{{NAMESPACE}}::{{VENUE_NAME}}", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### park-here
- **ParkingGarage entity**: `ParkHere::entities::ParkingGarage` (non-CRUD)
  - Attributes: name (req), isActive (req, default: true), emailTemplateOfTheGarage
  - Relations: parkingSlots (0..* ASSOC to ParkingSlot), accessedUsers (0..* ASSOC to User), usersWithIdCard (0..* ASSOC to User)
- **ParkingSlot entity**: `ParkHere::entities::ParkingSlot` (non-CRUD)
  - Attributes: id (req), floor (req), nextToWall (req, default: false), isActive (req, default: true), isExclusive (req, default: false), floorPlan, aggregaredName, parkingGarageName
  - Relations: parkingGarage (1..1 ASSOC), reservations (0..* ASSOC to Reservation)
- **User entity** carries: preferredParkingSlot (0..1 ASSOC), accessedParkingGarages (0..* ASSOC), idCardsForParkingGarages (0..* ASSOC)
- **Transfer Objects**:
  - `ParkingGarageSettings` -- name, emailTemplateOfTheGarage, isActive; relations: parkingSlots (0..*), accessedUsers (0..*)
  - `ParkingSlotSettings` -- all slot attributes; relation: parkingGarage (1..1)
  - `ParkingSlot` -- simplified view: aggregaredName, nextToWall, isActive, isExclusive
- The garage-slot-reservation three-tier structure enables: a garage contains slots, slots hold reservations, users have access to specific garages, and users can set a preferred slot
