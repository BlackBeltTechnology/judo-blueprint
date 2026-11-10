## Model shape

**Reservation entity.** `FreightReservation` holds the event data: start and end timestamps, a `state` attribute of the `FreightState` enumeration (nine members, see [[freight-logistics-state-enum]]), vehicle details (number plate, driver, phone), loading details (machine, driver, phone, a partial-delivery boolean, origin location) and a technical identifier. Relations:

- `attachments`: 0..* composition to `Attachment`. The attachments live and die with the reservation.
- `items`: 0..* association to `Item`. Each `Item` points back through an optional `freightReservation` association, so the pair is two independent one-way associations, not one bidirectional relation.
- `gate`, `spot`, `project`, `loadingTime`: optional (0..1) associations to reference entities.
- `partner`: optional association to `Partner`. `recipient`: required association to `Company`.
- `vehicleType` and `loadingType`: required (1..1) associations.
- `suspendedByPartner` and `suspendedByLogistician`: optional associations to `User`, one for each party that can suspend.

**Line item.** `Item` has an integer `quantity`, a `deleted` boolean used as a soft-delete flag, and optional associations to `ProductCategory`, `Unit` and `StorageType`.

**Reference data.** `Gate`, `Spot`, `VehicleType`, `LoadingType`, `LoadingTime` (adds `minutes`), `ProductCategory`, `Unit` and `StorageType` share a required `name` and a boolean `active`.

**Organizations.** `Partner` (required name, address, contact, phone, external identifier, active; collections of contacts and reservations), `Company` (name, active; contacts) and `Project` (required name, active; collections of users, spots and reservations).

**Access and pages (project practice).** In the reference project a project links users to spots and reservations, and a user sees only reservations of the projects they are assigned to. The platform offers access filters on the actor side for this; the scoping rule itself is a project convention and is not part of the fragment. Generated View, Form and Table pages for the reservation, its items and attachments are used for the booking actors, and the reference-data pages are kept for administrators.

## Structure diagram

<!-- mermaid:generated fragment=freight-reservation-cluster cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class Attachment {
    <<Entity>>
    +String name
  }
  class Company {
    <<Entity>>
  }
  class Contact {
    <<Entity>>
    +String name
  }
  class FreightReservation {
    <<Entity>>
    +String vehicleNumberPlate
    +String vehicleDriver
    +String vehiclePhone
    +String loadMachine
    +String loadDriver
    +String loadPhone
    +String fromLocation
    +String technicalID
    +Timestamp start
    +Timestamp end
    +Boolean partialDelivery
    +FreightState state
  }
  class FreightState {
    <<Enumeration>>
    NOT_SUBMITTED
    SUBMITTED
    REJECTED
    APPROVED
    SUSPENDED
    ARRIVED
    FINISHED
    DELAYED_UNLOADING
    DELAYED_ARRIVAL
  }
  class Gate {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class Item {
    <<Entity>>
    +Integer quantity
    +Boolean deleted
  }
  class LoadingTime {
    <<Entity>>
    +Integer minutes
    +String name [1]
  }
  class LoadingType {
    <<Entity>>
    +String name [1]
    +Boolean active
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
  class Spot {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  class StorageType {
    <<Entity>>
    +String name [1]
    +Boolean active
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
  class VehicleType {
    <<Entity>>
    +String name [1]
    +Boolean active
  }
  Company --> "*" Contact : contacts
  FreightReservation *-- "*" Attachment : attachments
  FreightReservation --> "*" Item : items
  FreightReservation --> "0..1" Gate : gate
  FreightReservation --> "0..1" LoadingTime : loadingTime
  FreightReservation --> "0..1" Partner : partner
  FreightReservation --> "0..1" Project : project
  FreightReservation --> "0..1" Spot : spot
  FreightReservation --> "0..1" User : suspendedByLogistician
  FreightReservation --> "0..1" User : suspendedByPartner
  FreightReservation --> "1" Company : recipient
  FreightReservation --> "1" LoadingType : loadingType
  FreightReservation --> "1" VehicleType : vehicleType
  FreightReservation ..> FreightState : state
  Item --> "0..1" FreightReservation : freightReservation
  Item --> "0..1" ProductCategory : productCategory
  Item --> "0..1" StorageType : storageType
  Item --> "0..1" Unit : unit
  Partner --> "*" Contact : contacts
  Partner --> "*" FreightReservation : freightReservations
  Project --> "*" FreightReservation : freightReservations
  Project --> "*" Spot : spots
  Project --> "*" User : users
```
<!-- /mermaid:generated -->
