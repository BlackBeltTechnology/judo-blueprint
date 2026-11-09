## Overview

The Reservation entity is managed entirely through custom operations on transfer objects -- create, delete, cancel, and modify reservations are all implemented as Java custom operation classes that delegate to a shared `ReservationService` for validation and persistence. Email notifications are sent for each lifecycle event via an `EmailSenderService` that renders Handlebars templates with reservation details.

## Implementation Pattern

- A shared `ReservationService` OSGi `@Component` encapsulates all reservation business logic: input validation, permission checks, slot conflict detection, per-type quota enforcement, and CRUD operations via `ReservationDao`
- Custom operation classes (e.g., `ReservationCustomImplementation`, `CancelReservationCustomImplementation`, `DeleteReservationCustomImplementation`, `ModificateReservationCustomImplementation`) are thin OSGi `@Component` wrappers that delegate to `ReservationService` and `EmailSenderService`
- Reservation creation varies by `ReservationType`: NORMAL/QUICK creates a single reservation with car and time slot; GUEST creates with composed Guest entity; LONG creates one reservation per working day in the date range (using `DateService.getWorkingDaysBetween()`)
- Cancel sets `reservationStatus = EXPIRED` and `endTime = now`; Delete sets `reservationStatus = DELETED`; Modify soft-deletes the old reservation and creates a new one (copy-on-write pattern)
- All mutations set audit trail fields (`modified`, `modifiedBy`) using `Clock.systemUTC()` and the current user's name
- `ReservationService.validateInput()` performs 20+ validation checks: required fields, permission for reservation type, guest data completeness, time validity (not in past, end after start, minimum 30 min), quick-reservation time constraints, slot availability via DAO query filters, per-user quota per type, and parking slot access authorization
- `EmailSenderService` renders Handlebars templates stored in `FileStoreService` for creation, deletion, modification, and reminder emails, using Configuration singleton for sender/contact addresses
- Range interceptors (`ReservationInputParkingSlotRangeInterceptor`, `ReservationInputCarRangeInterceptor`) filter reference ranges on the ReservationInput TO to show only accessible/available slots and non-archived cars for the selected user
- In freight/logistics variants, interceptors auto-wire actor-specific relations (e.g., partner) on reservation creation rather than using a full custom operation service layer

## Examples

### park-here
- Key files: `custom/.../reservationspanel/ReservationCustomImplementation.java`, `custom/.../userreservation/CancelReservationCustomImplementation.java`, `custom/.../userreservation/DeleteReservationCustomImplementation.java`, `custom/.../userreservation/ModificateReservationCustomImplementation.java`, `common/impl/ReservationServiceImpl.java`, `common/impl/EmailSenderServiceImpl.java`, `interceptors/reservation/input/ReservationInputParkingSlotRangeInterceptor.java`, `interceptors/reservation/input/ReservationInputCarRangeInterceptor.java`
- Pattern: Thin custom operation classes delegate to `ReservationService` (validation + persistence) and `EmailSenderService` (Handlebars email rendering). Modify uses copy-on-write: old reservation marked DELETED, new one created with updated times.
- Notable: Supports 4 reservation types (NORMAL, QUICK, GUEST, LONG) with different creation logic and per-type user quotas (`maxNormalReservation`, `maxGuestReservation`, `maxLongReservation`). Quick reservations are restricted to same-day/next-day after 12:00. LONG reservations expand into daily entries for each working day. Range interceptors provide context-aware dropdown filtering for parking slots (only free slots for selected date/time) and cars (only non-archived cars of the selected user).
- DI wiring: `ReservationServiceImpl` injects 10 services via `@Reference` including `UserDao`, `ParkingSlotDao`, `ReservationDao`, `EmailService`, `FileStoreService`, `ActorService`, `EmailSenderService`, `DateService`, and `ParkHereI18n`.

### reserve-app
- Key files: `interceptors/services/PartnerActorInterceptor.java`
- Pattern: Uses an `OperationCallInterceptor` to hook into the PartnerActor's `_createInstanceReservationsForPartner` operation; the `postCall` handler resolves the current user via `VariableResolver` + `UserDao.query().filterByEmail()`, fetches the user's partner association, and auto-links it to the newly created `FreightReservation` via `FreightReservationDao.setPartner()`
- Notable: Unlike park-here's rich custom operation approach with a full `ReservationService`, reserve-app uses the platform's built-in CRUD for reservation creation and augments it with a targeted interceptor for partner auto-assignment. No custom operations with `customImplementation: true` exist on the model -- all reservation lifecycle management relies on standard CRUD operations plus interceptor-based post-processing.
