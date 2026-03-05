---
id: reservation-booking-entity
title: "Reservation/Booking Entity with Time Slots and Status"
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
  - reserve-app
---

## Description

A Reservation (or Booking) entity that models time-bounded resource reservations. It captures a date, startTime, endTime for the time slot, a reservationStatus enum (ACTIVE/DELETED/EXPIRED) for lifecycle management, and a reservationType enum to distinguish different booking categories (e.g., NORMAL, QUICK, GUEST, LONG). The entity carries audit trail attributes (created, createdBy, modified, modifiedBy) for tracking who made and last changed the booking. It associates to an owner User (1..1), the reserved resource (e.g., ParkingSlot 1..1), and optionally to a guest entity (0..1 COMPOSITION) for third-party bookings and a vehicle/asset reference (0..1). Denormalized display fields (reserverName, reserverEmail, reserverCarId) enable quick display without joining. Reminder tracking fields (hasToNotify, reminderTimer, remindedBeforeStart, remindedBeforeEnd) support notification workflows. The entity is typically non-CRUD, managed entirely through custom operations on transfer objects.

Some variants model freight/logistics reservations with richer status lifecycles (NOT_SUBMITTED -> SUBMITTED -> APPROVED/REJECTED -> ARRIVED -> FINISHED with delay states) and associations to logistics resources (gates, spots, loading types, vehicle types) instead of simple parking slots.

The ReservationStatus enum follows a lifecycle from active through completion or cancellation. The ReservationType or state enum categorizes bookings by their nature, privilege level, or workflow stage.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Reservation%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { like: "%ReservationStatus%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { like: "%ReservationType%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ReservationStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ReservationStatus", name: "ACTIVE", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ReservationStatus", name: "DELETED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ReservationStatus", name: "EXPIRED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ReservationType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ReservationType", name: "{{TYPE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Reservation",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "startTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "endTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "reservationStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "reservationType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "created"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "createdBy"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "modified"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "modifiedBy"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Reservation", name: "hasToNotify"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Reservation", name: "owner",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Reservation", name: "{{RESOURCE_NAME}}",
  target: "{{NAMESPACE}}::{{RESOURCE_TYPE}}", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Reservation", name: "guest",
  target: "{{NAMESPACE}}::Guest", lower: 0, upper: 1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

## Examples

### park-here
- **Reservation entity**: `ParkHere::entities::Reservation` (non-CRUD)
  - Time slot attributes: date (req), startTime (req), endTime (req)
  - Status/type: reservationStatus (req, ReservationStatus enum), reservationType (req, ReservationType enum)
  - Audit: created (req), createdBy (req), modified, modifiedBy
  - Notification: hasToNotify (req, default: true), reminderTimer, remindedBeforeStart (default: false), remindedBeforeEnd (default: false)
  - Denormalized display: reserverName, reserverCarId, reserverEmail
  - Relations: owner (1..1 ASSOC to User), parkingSlot (1..1 ASSOC), car (0..1 ASSOC), guest (0..1 COMPOSITION to Guest), parkingGarage (0..1 DERIVED)
- **ReservationStatus enum**: `ParkHere::entities::ReservationStatus` -- ACTIVE(1), DELETED(2), EXPIRED(3)
- **ReservationType enum**: `ParkHere::entities::ReservationType` -- NORMAL(1), QUICK(2), GUEST(3), LONG(4)
- **Guest entity**: `ParkHere::entities::Guest` -- name (req), email (req), licensePlate (req); composed by Reservation for third-party bookings
- **Transfer Objects**:
  - `UserReservation` -- displays reservation details with guard attributes (isNotDeletable, isNotCancelable); operations: deleteReservation, cancelReservation, modificateReservation (all custom INSTANCE)
  - `ReservationInput` (unmapped) -- 26 attributes including date, startTime, endTime, reservationType, guest fields, warning texts, and UI visibility flags; relations: user (1..1), car (0..1), parkingSlot (1..1)
  - `ReservationModificationInput` (unmapped) -- startTime, endTime for time-only modifications
  - `ReservationsPanel` -- groups todayReservations, previousReservations, futureReservations; operations: holiday, reservation
- **User entity** carries per-type reservation limits: maxNormalReservation (default: 5), maxGuestReservation (default: 5), maxLongReservation (default: 2), and per-type permission booleans: isNormalReservation, isQuickReservation, isGuestReservation, isLongReservation

### reserve-app
- **FreightReservation entity**: `ReserveApp::entities::FreightReservation` (non-CRUD)
  - Time slot attributes: start, end
  - State: state (FreightState enum -- 9 states covering the full logistics lifecycle)
  - Vehicle info: vehicleNumberPlate, vehicleDriver, vehiclePhone
  - Loading info: loadMachine, loadDriver, loadPhone, partialDelivery, fromLocation
  - Identifier: technicalID
  - Relations: attachments (0..* COMPOSITION to Attachment), vehicleType (1..1 ASSOC), loadingType (1..1 ASSOC), recipient (1..1 ASSOC to Company), partner (0..1 ASSOC), gate (0..1 ASSOC), project (0..1 ASSOC), spot (0..1 ASSOC), loadingTime (0..1 ASSOC), items (0..* ASSOC to Item), suspendedByPartner (0..1 ASSOC to User), suspendedByLogistician (0..1 ASSOC to User)
- **FreightState enum**: `ReserveApp::entities::FreightState` -- NOT_SUBMITTED(1), SUBMITTED(2), REJECTED(3), APPROVED(4), SUSPENDED(5), ARRIVED(6), FINISHED(7), DELAYED_UNLOADING(8), DELAYED_ARRIVAL(9)
  - Full logistics lifecycle: creation -> submission -> approval/rejection -> arrival -> completion, with suspension and delay states
- **Transfer Objects**: Role-specific projections of the reservation:
  - `ReservationForPartner` -- 18 attributes including denormalized string fields (projectAsString, recipientAsString, gateAsString, spotAsString, duration, durationHuman); relations via AGGREGATION: recipient, spot, project, gate, partner, loadingType, vehicleType
- Freight reservations are assigned to specific gates and spots within a project, with vehicle and loading configuration managed via reference data entities
