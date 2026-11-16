## Overview

Replacing a generated form group with a custom visual element component that renders MUI TextFields with `react-imask` input masks for structured data entry (e.g., VAT IDs with format `00000000-0-00`). Framework: React.

## Implementation Pattern

- **Model first**: a string DataField with `textWidget=INPUT`, `textMultiLine=false` and a `textMask` pattern needs no custom code. Use the steps below only when that is not enough.
- **Registration**: the element must be exposed by the model as a custom implementation. Register an FC with `registerService(CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY, ..., { component: <ELEMENT>_COMPONENT_INTERFACE_KEY })` using the per-element key generated in the container's `customization.ts`; the scaffold `register<Container>CustomImplementations.tsx.default` has the function. Call it from `application-customizer.tsx`. The key follows the generated pattern `<CONTAINER>_<ELEMENT>_COMPONENT_INTERFACE_KEY`.
- **Component shape**: A React FC receiving `GenericProxyProps` with `data`, `validation`, `editMode`, `storeDiff`, `isLoading`, `actions`
- **Masked input**: MUI TextField with `InputProps.inputComponent: IMaskInput as any` and `inputProps` containing mask definition (`mask: '00000000-0-00'`), `placeholderChar: '_'`, `lazy: false`, `overwrite: true`
- **Value handling**: Uses `onAccept` callback (not `onChange`) to capture the unmasked value, with null handling for empty/placeholder values
- **Uppercase normalization**: Optionally applies `String(value).toUpperCase()` on accepted values
- **Validation**: Reads from the validation Map via `validation.get('fieldName')` and displays as helperText
- **Disabled/readonly**: Checks `actions?.isFieldDisabled` and `data.__updateable` for conditional editability

## Examples

### Example
- Framework: React
- Pattern: Replaces a VAT group visual element on an edit page with three masked VAT ID fields (`vatId`, `vatIdGroup`, `vatIdEu`). The first two use IMaskInput with mask `00000000-0-00` and auto-uppercase; the third is a standard TextField with maxLength
- Notable: The `onAccept` callback handles the empty-mask case (`________-_-__`) by converting to null; fields respect `data.__updateable` for read-only mode
