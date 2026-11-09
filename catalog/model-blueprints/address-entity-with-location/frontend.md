## Overview

The address entity with location manifests in the React frontend through form and view-edit action hooks that auto-compute the `addressInformation` field by concatenating individual address components (streetName, publicPlaceCategory, number, building, staircase, floor, door, lotNumber) whenever any address field loses focus. This pattern is duplicated across Address, CompanyAddress, and Partner (inline address) variants.

## Implementation Pattern

- **Blur action hooks on address fields**: Pandino-registered form and view-edit action hooks implement `onXxxBlurAction` callbacks for every address field (streetName, publicPlaceCategory, number, building, staircase, floor, door, lotNumber, manualAddressInformation). Each callback calls a shared `updateAddressInformation` function.
- **Auto-computed addressInformation**: The `updateAddressInformation` function concatenates all address components into a single string via `extractAddressInformation`, then writes it to `addressInformation` using `storeDiff`. It respects a `manualAddressInformation` boolean flag -- when true, the auto-computation is skipped so users can override the generated value.
- **Parallel implementations for entity variants**: The same pattern is implemented identically for Partner addresses (via `ServicesPartner_serviceAddressAddress_FormActionsHook` and `_View_EditActionsHook`), CompanyData addresses (via `ServicesCompany_data_serviceCompanyAddressCompanyAddress_FormActionsHook` and `_View_EditActionsHook`), and Partner create form (via `ServicesPartner_servicePartnerPartner_FormActionsHook` with `form_` prefixed field names).

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesCompanyadminOrganizationAdminPanelOrganizationAdminPanel_View_EditUpdateAddressInputFormActionsHook.ts`
- Pattern: The hook fetches the existing address using `organizationAdminPanelService.getAddress()` with a mask covering all address fields plus nested `postalCode{code}` and `city{name}`. The `onPostalCodeBlurAction` checks `data.postalCode?.cities` array length and auto-fills city when exactly one match exists.
- Notable: The postal-code-to-city auto-fill leverages the bidirectional City-PostalCode reference data relationship defined in the model, where a postal code can map to multiple cities.

### rackinspect
- Framework: React
- Key files: `custom/hooks/FormActionsHooks/customServicesPartnerServiceAddressAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesPartnerServiceAddressAddressViewEditActionsHook.tsx`, `custom/hooks/FormActionsHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressViewEditActionsHook.tsx`, `custom/hooks/FormActionsHooks/customServicesPartnerServicePartnerPartnerFormActionsHook.tsx`
- Pattern: Five parallel hooks (form + view-edit for Partner Address and CompanyAddress, plus Partner create form) each implement the same blur-triggered `addressInformation` auto-computation. The `manualAddressInformation` flag allows users to override auto-generated addresses.
- Notable: Unlike mlszksz-platform which uses PostalCode-to-City auto-fill, rackinspect uses a Country association (no City/PostalCode lookup entities) and focuses on the `addressInformation` concatenation pattern across three entity variants (Address, CompanyAddress, Partner inline).
