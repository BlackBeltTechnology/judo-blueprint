## Overview

The contact info composition cluster (EmailAddress, PhoneNumber, Address, BankAccount) manifests in the React frontend through address-specific blur action hooks that auto-compute the `addressInformation` field. The email, phone, and bank account sub-entities use the generated frontend without custom overrides; only the address sub-entities have custom frontend hooks.

## Implementation Pattern

- **Address auto-computation hooks**: For each address variant in the cluster (Partner Address, CompanyAddress), both form and view-edit action hooks are registered via Pandino. Each hook implements blur callbacks for all address fields (streetName, publicPlaceCategory, number, building, staircase, floor, door, lotNumber, manualAddressInformation). When any field loses focus, the hook concatenates address components into `addressInformation` via `storeDiff`, unless `manualAddressInformation` is true.
- **No custom hooks for email/phone/bank**: The EmailAddress, PhoneNumber, and BankAccount contact sub-entities, including their toggleActive and togglePrimary operations, use the generated frontend without any custom hook overrides. The toggle operations are rendered as standard action buttons by the framework.

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/FormActionsHooks/customServicesPartnerServiceAddressAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesPartnerServiceAddressAddressViewEditActionsHook.tsx`, `custom/hooks/FormActionsHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressFormActionsHook.tsx`, `custom/hooks/ViewEditActionHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressViewEditActionsHook.tsx`
- Pattern: Four hooks provide identical `extractAddressInformation` logic that concatenates streetName, publicPlaceCategory, number, building, staircase, floor, door, and lotNumber with appropriate separators. The `manualAddressInformation` flag guards against overwriting user-provided custom address strings.
- Notable: The pattern is duplicated across Partner and CompanyData address variants because each has a separate transfer object type in the service layer, requiring separate hook registrations despite identical logic.
