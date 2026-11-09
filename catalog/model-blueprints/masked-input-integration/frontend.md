## Overview

Replacing a generated form group with a custom visual element component that renders MUI TextFields with `react-imask` input masks for structured data entry (e.g., VAT IDs with format `00000000-0-00`). Framework: React.

## Implementation Pattern

- **Registration**: Via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` in `application-customizer.tsx`, targeting a specific group component constant (e.g., `SERVICES_PARTNER_SERVICE_PARTNER_PARTNER_VIEW_EDIT_VATS_GROUP_COMPONENT`)
- **Component shape**: A React FC receiving `GenericProxyProps<TStored, TActionDefs>` with `data`, `validation`, `editMode`, `storeDiff`, `isLoading`, `actions`
- **Masked input**: MUI TextField with `InputProps.inputComponent: IMaskInput as any` and `inputProps` containing mask definition (`mask: '00000000-0-00'`), `placeholderChar: '_'`, `lazy: false`, `overwrite: true`
- **Value handling**: Uses `onAccept` callback (not `onChange`) to capture the unmasked value, with null handling for empty/placeholder values
- **Uppercase normalization**: Optionally applies `String(value).toUpperCase()` on accepted values
- **Validation**: Reads from the validation Map via `validation.get('fieldName')` and displays as helperText
- **Disabled/readonly**: Checks `actions?.isFieldDisabled` and `data.__updateable` for conditional editability

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/custom-implementations/registerServicesPartner_servicePartnerPartner_View_EditCustomImplementations.tsx`
- Pattern: Replaces the "VatsGroup" visual element on Partner_View_Edit with three masked VAT ID fields (`vatId`, `vatIdGroup`, `vatIdEu`). The first two use IMaskInput with mask `00000000-0-00` and auto-uppercase; the third is a standard TextField with maxLength
- Notable: The `onAccept` callback handles the empty-mask case (`________-_-__`) by converting to null; fields respect `data.__updateable` for read-only mode
