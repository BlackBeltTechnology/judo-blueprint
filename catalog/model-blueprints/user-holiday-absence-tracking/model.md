## Examples

### park-here
- **Holiday entity**: `ParkHere::entities::Holiday` (non-CRUD)
  - Attributes: startDate (req), endDate (req)
  - Relations: holidayOwner (0..1 DERIVED back to User)
- **User entity** composes holidays (0..* COMPOSITION) and has queryCollidingHolidays (query attribute) for conflict detection
- **AdditionalDay entity**: `ParkHere::entities::AdditionalDay` (non-CRUD)
  - Attributes: day (req), typeOfDay (req, DayType enum)
  - Managed via Configuration entity (additionalDays 0..* ASSOC)
- **DayType enum**: `ParkHere::entities::DayType` -- WORK(1), HOLIDAY(2)
  - Allows overriding calendar: marking a Saturday as WORK day, or a weekday as HOLIDAY
- **Transfer Objects**:
  - `Holiday` TO -- startDate, endDate, isNotDeletable (guard); operation: deleteHoliday (custom INSTANCE)
  - `HolidayInput` (unmapped) -- startDate, endDate, hiddenByCustom, userHidden, currentDate; relations: user (1..1 AGGREGATION), reservationsForDeleteInfo (0..* AGGREGATION)
  - `HolidayPanel` TO -- holidays (0..* ASSOC); operation: holiday (custom INSTANCE for creation)
  - `UserReservationPanel` TO -- includes holidays (0..* ASSOC) alongside reservation collections
- Holiday creation checks for colliding reservations via the HolidayInput's reservationsForDeleteInfo relation, enabling the UI to warn users about affected bookings
