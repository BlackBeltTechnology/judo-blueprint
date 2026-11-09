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
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Reservation", name: "{{RESOURCE_NAME}}",
  target: "{{NAMESPACE}}::{{RESOURCE_TYPE}}", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Reservation", name: "guest",
  target: "{{NAMESPACE}}::Guest", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
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
