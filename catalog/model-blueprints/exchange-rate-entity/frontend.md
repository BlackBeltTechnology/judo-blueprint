## Overview

The exchange rate entity manifests in the React frontend through a custom form component for the rate input group and a form actions hook that restricts date selection. The customizations address two UX concerns: preventing future-dated exchange rates and masking the rate value after entry for confidentiality.

## Implementation Pattern

- **Custom RateGroup visual element**: A Pandino-registered custom component replaces the generated rate/rateRepeat input group on the CreateExchangeRateInput form. The component uses a password-masking pattern: after the user enters the rate value and blurs, the input type switches to `password` to hide the value. The rateRepeat field is disabled until a rate value is entered, enforcing a "type twice" confirmation pattern for sensitive financial data.
- **Date validation hook**: A form actions hook provides `getDateValidationProps` that returns `{ disableFuture: true }`, preventing users from creating exchange rates for future dates.

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/custom-implementations/registerServicesPartner_serviceCreateExchangeRateInputCreateExchangeRateInput_FormCustomImplementations.tsx`, `custom/hooks/FormPageActionHooks/customServicesPartner_serviceCreateExchangeRateInputCreateExchangeRateInput_FormActionsHook.tsx`
- Pattern: The custom RateGroup component overrides the generated NumericInput for the rate field to switch `inputType` from `text` to `password` on blur, masking the entered value. The rateRepeat field is conditionally disabled when no rate is set. The form actions hook adds `disableFuture: true` to the date picker.
- Notable: The rate masking pattern is unusual -- it treats exchange rates as semi-confidential data requiring double-entry confirmation, which is specific to this project's business requirements.
