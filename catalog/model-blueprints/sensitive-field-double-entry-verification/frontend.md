## Overview

A custom visual element component that masks a sensitive numeric input after blur and requires re-entry in a confirmation field to prevent data entry errors. Used for exchange rate entry where incorrect values have financial impact. Framework: React.

## Implementation Pattern

- **Registration**: Via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` targeting a specific group component (e.g., `CREATE_EXCHANGE_RATE_INPUT_FORM_RATE_GROUP_COMPONENT`)
- **Component shape**: React FC receiving `GenericProxyProps<TStored, TActionDefs>` with `data`, `validation`, `editMode`, `storeDiff`, `isLoading`, `actions`
- **Input type toggling**: Uses React `useState<'text' | 'password'>('text')` to control the primary field's input type. On `onBlur`, switches to `'password'` if the field has a value. On clear/null, resets to `'text'`
- **Confirmation field**: A second NumericInput field (`rateRepeat`) is disabled when the primary field is empty (`disabled={isLoading || !data.rate || data.rate === null}`); clears automatically when the primary field is emptied
- **Value sync**: In the primary field's `onValueChange`, if the new value is null, `storeDiff('rateRepeat', undefined)` clears the repeat field
- **Validation**: Server-side validation (via the form action hook's `getDateValidationProps` or custom validators) can compare the two values; field-level errors display via `validation.get('rate')` and `validation.get('rateRepeat')`
- **Form action hook companion**: A separate form action hook (registered for the same dialog) provides additional customization like `getDateValidationProps({ disableFuture: true })` for date fields on the same form

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/custom-implementations/registerServicesPartner_serviceCreateExchangeRateInputCreateExchangeRateInput_FormCustomImplementations.tsx`, `custom/hooks/FormPageActionHooks/customServicesPartner_serviceCreateExchangeRateInputCreateExchangeRateInput_FormActionsHook.tsx`
- Pattern: The "RateGroup" visual element replaces the generated exchange rate input form section. The `rate` field uses NumericInput with `decimalScale={4}` and switches between `text`/`password` input types. The `rateRepeat` field is conditionally enabled. Both fields have `readOnly: false` patched to override the generated `isFormUpdateable()` check.
- Notable: The accompanying form action hook adds `getDateValidationProps({ disableFuture: true })` to prevent future-dated exchange rates; the password masking approach is unconventional for numeric fields but effectively prevents the user from copy-pasting between the two fields
