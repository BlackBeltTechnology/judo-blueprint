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
