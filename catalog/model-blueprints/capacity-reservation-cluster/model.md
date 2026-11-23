## Model shape

**Reservation entity.** `CapacityReservation` holds the event data: start and end timestamps, a `state` attribute of the `ShipmentState` enumeration (nine members, see [[shipment-state-enum]]), transport details (identifier, driver, phone), handling details (machine, driver, phone, a partial-delivery boolean, origin location) and a technical identifier. Relations:

- `attachments`: 0..* composition to `Attachment`. The attachments live and die with the reservation.
- `items`: 0..* association to `Item`. Each `Item` points back through an optional `capacityReservation` association, so the pair is two independent one-way associations, not one bidirectional relation.
- `dock`, `slot`, `project`, `timeWindow`: optional (0..1) associations to reference entities.
- `partner`: optional association to `Partner`. `recipient`: required association to `Company`.
- `resourceType` and `handlingType`: required (1..1) associations.
- `suspendedByRequester` and `suspendedByApprover`: optional associations to `User`, one for each party that can suspend.

**Line item.** `Item` has an integer `quantity`, a `deleted` boolean used as a soft-delete flag, and optional associations to `ProductCategory`, `Unit` and `StorageType`.

**Reference data.** `Dock`, `Slot`, `ResourceType`, `HandlingType`, `TimeWindow` (adds `minutes`), `ProductCategory`, `Unit` and `StorageType` share a required `name` and a boolean `active`.

**Organizations.** `Partner` (required name, address, contact, phone, external identifier, active; collections of contacts and reservations), `Company` (name, active; contacts) and `Project` (required name, active; collections of users, slots and reservations).

**Access and pages (common practice).** In one project a project links users to slots and reservations, and a user sees only reservations of the projects they are assigned to. The platform offers access filters on the actor side for this; the scoping rule itself is a project convention and is not part of the fragment. Generated View, Form and Table pages for the reservation, its items and attachments are used for the booking actors, and the reference-data pages are kept for administrators.

## Structure diagram

```mermaid
classDiagram
  class Attachment {
    <<Entity>>
    +String name
  }
  class CapacityReservation {
    <<Entity>>
    +String transportIdentifier
    +String transportDriver
    +String transportPhone
    +String handlingMachine
    +String handlingDriver
    +String handlingPhone
    +String originLocation
    +String technicalID
    +Timestamp start
    +Timestamp end
    +Boolean partialDelivery
    +ShipmentState state
  }
  class Company {
    <<Entity>>
  }
  class Contact {
    <<Entity>>
    +String name
  }
  class Dock {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class HandlingType {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class Item {
    <<Entity>>
    +Integer quantity
    +Boolean deleted
  }
  class Partner {
    <<Entity>>
    +String name [1]
    +Boolean active
    +String address
    +String contact
    +String phone
    +String externalIdentifier
  }
  class ProductCategory {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class Project {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class ResourceType {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class ShipmentState {
    <<Enumeration>>
    NOT_SUBMITTED
    SUBMITTED
    REJECTED
    APPROVED
    SUSPENDED
    ARRIVED
    FINISHED
    DELAYED_COMPLETION
    DELAYED_ARRIVAL
  }
  class Slot {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class StorageType {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class TimeWindow {
    <<Entity>>
    +Integer minutes
    +String name [1]
  }
  class Unit {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class User {
    <<Entity>>
    +String name
  }
  CapacityReservation *-- "*" Attachment : attachments
  CapacityReservation --> "*" Item : items
  CapacityReservation --> "0..1" Dock : dock
  CapacityReservation --> "0..1" Partner : partner
  CapacityReservation --> "0..1" Project : project
  CapacityReservation --> "0..1" Slot : slot
  CapacityReservation --> "0..1" TimeWindow : timeWindow
  CapacityReservation --> "0..1" User : suspendedByApprover
  CapacityReservation --> "0..1" User : suspendedByRequester
  CapacityReservation --> "1" Company : recipient
  CapacityReservation --> "1" HandlingType : handlingType
  CapacityReservation --> "1" ResourceType : resourceType
  CapacityReservation ..> ShipmentState : state
  Company --> "*" Contact : contacts
  Item --> "0..1" CapacityReservation : capacityReservation
  Item --> "0..1" ProductCategory : productCategory
  Item --> "0..1" StorageType : storageType
  Item --> "0..1" Unit : unit
  Partner --> "*" CapacityReservation : capacityReservations
  Partner --> "*" Contact : contacts
  Project --> "*" CapacityReservation : capacityReservations
  Project --> "*" Slot : slots
  Project --> "*" User : users
```
