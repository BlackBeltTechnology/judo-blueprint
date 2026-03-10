## Overview

Holiday management is implemented through custom operation classes that delegate to a shared `HolidayService` for validation, conflict detection, and reservation cancellation. The `DateService` provides calendar-aware logic using AdditionalDay entities to determine working days and holidays.

## Implementation Pattern

- A shared `HolidayService` OSGi `@Component` encapsulates holiday validation, creation, and deletion logic
- Custom operation classes (`HolidayCustomImplementation` on HolidayPanel, UserReservationPanel, and ReservationsPanel; `DeleteHolidayCustomImplementation` on Holiday TO) are thin wrappers that validate the current user's permission, then delegate to `HolidayService`
- Holiday creation flow: (1) resolve User by ID from `HolidayInput`, (2) validate current user has permission via `ActorService.validateCurrentUserHasPermissionTo()`, (3) validate holiday dates via `HolidayService.validateHoliday()`, (4) create holiday via `HolidayService.createHoliday()`
- `HolidayService.validateHoliday()` checks: end date not before start date, start date not in past, and no colliding holidays (via `userDao.queryQueryCollidingHolidays()` query attribute)
- `HolidayService.createHoliday()` auto-cancels conflicting reservations: queries all ACTIVE non-GUEST reservations in the holiday date range, sets their status to DELETED, then creates the Holiday entity via `userDao.createHolidays()`
- Holiday deletion verifies the user owns the holiday via `holidayDao.queryHolidayOwner()` and checks admin permission before deleting
- A `QueryReservationsForHolidayCustomImplementation` operation queries ACTIVE non-GUEST reservations in the proposed holiday range for conflict preview in the UI
- The `DateService` / `DateServiceImpl` provides `isWorkingDay()` and `getWorkingDaysBetween()` methods that combine Hungarian public holidays (computed via Computus algorithm for Easter), AdditionalDay HOLIDAY entries, and AdditionalDay WORK overrides from the database
- AdditionalDay creation (`CreateDayCustomImplementation`) validates no duplicate day exists before creating the calendar override via `configurationDao.createAdditionalDays()`

## Examples

### park-here
- Key files: `custom/.../holidaypanel/HolidayCustomImplementation.java`, `custom/.../holiday/DeleteHolidayCustomImplementation.java`, `custom/.../userforinput/QueryReservationsForHolidayCustomImplementation.java`, `common/HolidayService.java`, `common/impl/HolidayServiceImpl.java`, `common/DateService.java`, `common/impl/DateServiceImpl.java`, `custom/.../configurationsettings/CreateDayCustomImplementation.java`
- Pattern: Three panel-level holiday creation operations (HolidayPanel, UserReservationPanel, ReservationsPanel) all follow the same flow: resolve user, check permission, validate, create. All delegate to the shared `HolidayService`.
- Notable: Holiday creation automatically cancels all conflicting ACTIVE reservations (excluding GUEST type) within the holiday date range. The `QueryReservationsForHolidayCustomImplementation` enables a preview of affected reservations before the user confirms holiday creation, using DAO query filters on date range, reservation type, and status with masked projections for display fields only.
- The `DateServiceImpl` computes Hungarian public holidays including moveable feasts (Easter Monday, Pentecost Monday) and merges them with database-stored AdditionalDay overrides to determine working days for long-reservation expansion and reservation-on-holiday validation.
