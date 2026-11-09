## Overview

A pattern for extracting reusable form business logic into standalone TypeScript modules under `src/custom/services/`, consumed by multiple Pandino dialog/page action hooks to avoid duplicating field computation, validation, and initialization logic. Framework: React.

## Implementation Pattern

- **File location**: `src/custom/services/<EntityName>Services.ts` -- one module per input transfer object or domain concept
- **Function signature**: Exported functions typically follow the pattern `functionName(data: TInput, storeDiff: (key: keyof TInput, value: any) => void, ...extras)` where `storeDiff` is the JUDO form state updater
- **Common function categories**:
  - **Field auto-computation**: Functions that compute derived field values from other fields (e.g., auto-setting start/end times based on current time and working hours)
  - **Enum-driven visibility**: Functions that toggle boolean visibility flags (`storeDiff('hiddenByCustom', true)`) based on enum field values
  - **Default initialization**: `postGetTemplateAction`-style functions called after form template loads to set initial defaults from user preferences or related data
  - **Validation constraints**: Functions returning `BaseDateValidationProps` objects (`{ minDate, maxDate }`) for date picker constraints
  - **Enum option filtering**: Functions filtering available enum options based on user permissions/flags
  - **Warning text computation**: Functions computing and toggling warning messages based on temporal proximity or data conditions
  - **Relation-based defaults**: Async functions that query related services to resolve default values (e.g., fetching a user's preferred parking slot)
- **Consumer pattern**: Dialog/page action hooks import these functions and wire them to hook callbacks: `onUserBlurAction(data, storeDiff, editMode, submit) { onUserFieldBlurSetDefaults(data, storeDiff, editMode, submit); }`
- **Service instantiation**: Modules may instantiate service implementation classes (e.g., `new ServicesReservationInputServiceImpl(judoAxiosProvider)`) for async operations like range queries
- **Reuse**: A single service module is imported by multiple hook registrations (e.g., both `ReservationsPanel` and `UserReservationPanel` hooks import from the same `ReservationInputServices.ts`)

## Examples

### park-here
- Framework: React
- Key files: `custom/services/ReservationInputServices.ts` (14 exported functions), `custom/services/HolidayInputServices.ts` (4 exported functions)
- Pattern: `ReservationInputServices.ts` provides shared reservation form logic consumed by 4+ dialog action hooks: auto-sets start/end times from current time (`autoSetReservationTimeBasedOnCurrent`), resolves reservation type from user flags (`updateReservationTypeFromUserData`), filters enum options by user permissions (`filterAvailableReservationTypes`), computes date validation props, and resolves favorite parking slot via async service call. `HolidayInputServices.ts` handles holiday form defaults and dynamically queries affected reservations.
- Notable: `getUserFieldsForReservation()` returns a custom `_mask` string for the user relation to eagerly fetch nested fields (cars, working times, preferred parking slot) needed by form logic; `updateReservationWarningText` computes a time-based warning showing minutes until the next half-hour boundary
