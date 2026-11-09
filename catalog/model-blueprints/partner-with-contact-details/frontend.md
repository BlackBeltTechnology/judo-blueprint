## Overview

The partner entity with contact details manifests in the React frontend through a view-edit action hook that displays server-side validation errors on partner fields, a custom VatsGroup component with Hungarian VAT ID input masks, and a table row highlighting hook for partner ratings.

## Implementation Pattern

- **Server-side validation display**: A Pandino-registered view-edit actions hook provides a `postRefreshAction` that reads `data.partnerErrors` (a composed collection of PartnerError entities) and maps each error's `location` field to a validation error on the corresponding Partner form field via `setValidation`. This surfaces backend validation results (from the Partner.validate operation) as field-level error messages in the UI.
- **Custom VAT ID input masks**: A custom visual element component replaces the generated VatsGroup with three masked text inputs for vatId, vatIdGroup (both using `00000000-0-00` mask via react-imask), and vatIdEu (free-text). The masks enforce the Hungarian tax number format with placeholder characters and auto-uppercase.
- **Rating table row highlighting**: A `TableRowHighlightingHook` is registered for the Partner ratings table. Rows are color-coded based on `ratingResult`: green (#00cc00) for result A (excellent), red (#cc0000) for result C (non-acceptable).

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/ViewEditActionHooks/customServicesPartnerServicePartnerPartnerViewEditActionsHook.tsx`, `custom/hooks/custom-implementations/registerServicesPartner_servicePartnerPartner_View_EditCustomImplementations.tsx`, `custom/hooks/TableRowHighlightingHooks/ratingTableHighlightHook.tsx`
- Pattern: The `postRefreshAction` in the ViewEdit hook iterates over `data.partnerErrors` and creates a validation Map keyed by `error.location` (field name) with `error.errorMessage` as the value. The VatsGroup component uses react-imask's `IMaskInput` as `inputComponent` for vatId and vatIdGroup fields with mask `00000000-0-00`. The rating highlight hook maps RatingResult enum values to background colors.
- Notable: The partner error display pattern bridges backend validation (Partner.validate operation writes PartnerError entities) with frontend field-level error display, avoiding real-time client-side validation in favor of server-authoritative validation results.
