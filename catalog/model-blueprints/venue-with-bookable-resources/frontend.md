## Overview

The venue with bookable resources pattern manifests in the React frontend indirectly through the reservation creation workflow. While the ParkingGarage and ParkingSlot entities do not have dedicated custom components or hooks of their own, the parking slot is deeply integrated into the reservation input form logic: preferred slot auto-selection, slot availability validation via range queries, next-to-wall warning display, and parking slot information rendering in reservation cards.

## Implementation Pattern

- **Preferred slot auto-selection**: When a user is selected in the reservation form, the `setFavoriteParkingSlot` function queries `servicesReservationInputServiceImpl.getRangeForParkingSlot()` with a filter matching the user's `preferredParkingSlot.aggregaredName`. If the preferred slot is available in the current context, it is auto-populated into the form; otherwise the slot field is cleared.
- **Next-to-wall warning**: The `onParkingSlotBlurAction` function checks the selected parking slot's `nextToWall` boolean. If true, it shows a warning text (`extra.message.warningNextToText`) via `storeDiff('warningNextToWallTextHidden', false)`. This warns users that the selected slot is next to a wall, which may require additional care when parking.
- **Parking slot info display in cards**: Both the `UserActiveReservationsCard` and `UserPreviousReservationsCard` custom components display the `parkingSlotInformation` field (a denormalized string combining garage and slot identifiers) with a garage icon (`garage-open-variant`).
- **Custom data mask inclusion**: The `getActiveReservationsMask` hook explicitly includes `parkingSlotInformation` in the fetch mask, and `getUserFieldsForReservation` includes `preferredParkingSlot{aggregaredName,nextToWall}` to fetch slot details along with user data.
- **i18n**: Hungarian translations cover parking garage and slot table labels, slot attributes (floor, nextToWall, isActive, isExclusive, floorPlan), and the aggregated name display used in reservation cards.

## Examples

### park-here
- Framework: React
- Key files: `custom/services/ReservationInputServices.ts` (functions: `setFavoriteParkingSlot`, `onParkingSlotBlurAction`, `getUserFieldsForReservation`), `custom/hooks/components/UserActiveReservationsCard.tsx`, `custom/hooks/components/UserPreviousReservationsCard.tsx`
- Pattern: The venue/slot pattern is consumed by the reservation workflow rather than customized independently. Preferred parking slot is auto-selected during reservation creation by querying the parking slot range API. A next-to-wall warning appears when the selected slot has the `nextToWall` flag. Parking slot information is displayed in reservation cards with the `garage-open-variant` icon.
- Notable: No custom hooks or components target ParkingGarage or ParkingSlot views directly. The venue/slot customizations are entirely embedded in reservation-related hooks, reflecting that the slot is a supporting entity selected during the reservation workflow rather than managed through custom UI flows.
