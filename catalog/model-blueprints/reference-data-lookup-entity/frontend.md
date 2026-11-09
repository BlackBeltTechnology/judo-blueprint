## Overview

The reference data lookup entities manifest in the React frontend through dialog action hooks that customize validation, pre-fill update forms, and provide auto-fill logic between related reference data entities (e.g., postal code to city auto-fill, conditional required fields based on the active flag). In some projects, reference data entities are also used as dynamic filter options in custom card-based product listing views, where the lookup values are fetched at runtime to populate filter dropdowns.

## Implementation Pattern

- **Conditional validation hooks**: View page action hooks override field-level validation properties (e.g., `isNameRequired`) to make the `name` field conditionally required based on the `active` flag state. This allows draft/inactive reference data entries to exist without a name while enforcing the name requirement for active entries.
- **City/Capability update dialog hooks**: Dialog-level action hooks provide `postGetTemplateAction` to pre-fill edit forms with current values when editing City or Capability reference data. The hooks fetch existing data via the parent service and populate the form via `storeDiff`.
- **PostalCode-City auto-fill**: The address update dialog hook includes a `getPostalCodeMask` override that requests `'{code, cities{name}}'`, enabling the `onPostalCodeBlurAction` to auto-fill the city field when a postal code maps to exactly one city.
- **Capability autocomplete in feed**: The `useCapabilitiesAutocomplete` hook queries the active capabilities list and provides type-ahead selection for filtering feed entries and discovery organizations by capability.
- **Dynamic filter population from lookup entities**: Cards container config hooks fetch reference data lists (audiences, curriculums, resultTypes, institutions) at mount time via service classes and populate `CardsFilterDefinition` arrays with `inputType: 'options'` entries, enabling users to filter product cards by classification values rendered as checkbox lists.

## Examples

### reserve-app
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesAdminActorStorageTypesAccessViewPageActionsHook.ts`
- Pattern: A Pandino action hook registered for the AdminActor StorageTypes AccessViewPage overrides `isNameRequired` to return `!!data.active`, making the `name` field required only when the StorageType's `active` flag is true. This is a validation hook pattern that uses the `ServicesStorageTypeStorageType_View_EditActionsHook` interface key.
- Notable: This is the only custom frontend hook in the entire reserve-app project. All other reference data entities (Gate, VehicleType, LoadingType, Spot, ProductCategory, Unit, LoadingTime) use the default generated UI without customization.

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesAdminCityCity_View_EditUpdateCityInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesAdminAdminDashboardAdminDashboard_View_EditCitiesUpdateCityInputFormActionsHook.ts`, `custom/hooks/dialogs/registerServicesAdminCapabilityCapability_View_EditUpdateCapabilityInputFormActionsHook.ts`, `custom/feedComponent/hooks/useCapabilitiesAutocomplete.ts`
- Pattern: City and Capability update hooks follow the standard `postGetTemplateAction` pattern: fetch current entity data, then call `storeDiff` for each field. The capabilities autocomplete hook provides a reusable `CapabilityListFn` type used by both FeedFilters and DiscoveryFilters.
- Notable: Two separate hooks exist for city updates -- one for the standalone City view page and one for the embedded cities table on the AdminDashboard -- both implementing the same autofill logic but registered with different interface keys.

### alba
- Framework: React
- Key files: `custom/hooks/cards/AuthorProductsCards.tsx`, `custom/hooks/cards/ApproverProductsCards.tsx`
- Pattern: The Audience, Curriculum, ResultType, and Institution reference data entities are consumed as dynamic filter options in product card listing views. Both `AuthorProductsCards.tsx` and `ApproverProductsCards.tsx` instantiate service classes (`UserServiceForAudiencesForFilterImpl`, `UserServiceForCurriculumsForFilterImpl`, `UserServiceForResultTypesForFilterImpl`, `UserServiceForInstitutionsForFilterImpl`) at mount time, fetch all entries with a seek limit of 1000, sort them by name using `Intl.Collator`, and build `CardsFilterDefinition` arrays with `inputType: 'options'` for each lookup entity. The filter values are mapped to `_StringOperation.like` queries on the Product's denormalized aggregated fields (`audienceAggregated`, `curriculumAggregated`, `resultTypesAggregated`) and `_StringOperation.equal` for `institutionName`.
- Notable: Reference data names are also displayed directly in the custom card components as MUI `Chip` elements (e.g., `row.curriculum?.map(c => <Chip label={c.name} />)`), showing lookup values inline on each product card. The i18n file provides Hungarian translations for menu items: "Celcsoport" (Audience), "Tantargyak" (Curriculum), "Produktum Tipusok" (ResultType), "Intezmenyek" (Institution).
