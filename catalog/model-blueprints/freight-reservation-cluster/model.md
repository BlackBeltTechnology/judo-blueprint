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
