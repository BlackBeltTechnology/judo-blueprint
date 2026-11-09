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
