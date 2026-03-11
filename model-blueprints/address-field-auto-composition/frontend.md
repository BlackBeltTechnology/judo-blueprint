## Overview

Form action hooks that auto-compose a summary `addressInformation` field by concatenating individual address component fields (street, number, building, floor, etc.) on blur events. A `manualAddressInformation` flag lets users override the auto-composition. Framework: React.

## Implementation Pattern

- **Hook types**: Form action hooks (`*FormActionsHook`) and view/edit action hooks (`*ViewEditActionsHook`) registered directly via `context.registerService` in `application-customizer.tsx`
- **Blur handlers**: Each address component field has a corresponding `onFieldBlurAction` (e.g., `onStreetNameBlurAction`, `onNumberBlurAction`, `onBuildingBlurAction`, `onFloorBlurAction`, etc.)
- **Composition logic**: `extractAddressInformation(data)` concatenates non-empty fields: `streetName + publicPlaceCategory + number + building + staircase + floor + door + ", " + lotNumber`
- **Manual override**: Checks `data.manualAddressInformation` boolean -- if true, skips auto-composition and preserves user's manual entry
- **Reuse across contexts**: The same pattern is applied to both Partner address forms/views and CompanyData address forms/views by registering separate hook instances for each page's interface key

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/FormActionsHooks/customServicesPartnerServiceAddressAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesPartnerServiceAddressAddressViewEditActionsHook.tsx`, `custom/hooks/FormActionsHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressViewEditActionsHook.tsx`
- Pattern: Eight blur handlers (streetName, publicPlaceCategory, number, building, staircase, floor, door, lotNumber) plus a manualAddressInformation toggle handler, all calling a shared `updateAddressInformation` function that concatenates non-empty fields with spaces and commas
- Notable: Applied to four separate Pandino hook registrations (Partner form + view, CompanyData form + view) to cover all address editing contexts; the `manualAddressInformation` flag allows per-address override of auto-composition
