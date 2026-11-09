## Overview

The Venue (ParkingGarage) and Slot (ParkingSlot) entities are seeded during initialization and their access control is enforced through interceptors that filter reference ranges based on user permissions and slot exclusivity.

## Implementation Pattern

- Venues and slots are seeded by the `InitCustomImplementation` class: creates ParkingGarage entities with name, isActive, and email templates; creates ParkingSlot entities with floor, id, isExclusive, and floorPlan image associations linked to their parent garage
- Access control is enforced via `OperationCallInterceptor` implementations that intercept `_getRangeReference` operations on transfer objects to filter available slots
- The `ReservationInputParkingSlotRangeInterceptor` intercepts parking slot range requests on the reservation input form, filtering to only show free slots in garages the user has access to, respecting reservation type (single day vs. date range for LONG), and hiding exclusive slots from non-admin users
- The `PreferedParkingSlotRangeInterceptor` intercepts the preferred parking slot range on ProfileSettings, filtering to accessible non-exclusive slots (unless admin)
- The `UserSettingsTemplateInterceptor` strips sensitive fields (emailTemplateOfTheGarage, accessedUsers, isActive) from ParkingGarage payloads in the UserSettings template response
- An `AuthenticationInterceptor` (`LogAuthenticationInterceptor`) auto-creates User entities on first login using Keycloak claims (email, name), with configurable admin email list via OSGi component properties

## Examples

### park-here
- Key files: `interceptors/reservation/input/ReservationInputParkingSlotRangeInterceptor.java`, `interceptors/reservation/input/PreferedParkingSlotRangeInterceptor.java`, `interceptors/usersettings/UserSettingsTemplateInterceptor.java`, `interceptors/LogAuthenticationInterceptor.java`, `custom/.../_default_transferobjecttypes/entities/initializer/InitCustomImplementation.java`
- Pattern: Three `OperationCallInterceptor` implementations filter reference ranges for parking slots based on user access and slot exclusivity; one `AuthenticationInterceptor` handles auto-provisioning of User entities on first login
- Notable: `ReservationInputParkingSlotRangeInterceptor` dynamically selects between single-day and multi-day free-slot queries based on `ReservationType` (LONG vs. others), using `UserForInputDao.queryFreeParkingSlotForADay()` or `queryFreeParkingSlotForDays()`. The interceptor preserves the original filter and orderBy from the query customizer while adding access-control constraints.
- The `LogAuthenticationInterceptor` reads admin emails from OSGi component properties (`admins` parameter) and sets `isAdministrator=true` for matching users during auto-creation.
