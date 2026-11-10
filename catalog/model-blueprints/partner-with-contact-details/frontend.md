## Overview

The partner view shows backend validation results next to the fields, uses masked inputs for tax ids and colours rating rows. All of it is customization on top of the generated pages; file names below are example project code.

## Implementation Pattern

- **Server-side validation display.** A page actions hook returns a `postRefreshAction` handler (a generated optional handler on the page hook type, see [PostRefresh Action Hook](../../agent-docs/frontend/advanced-patterns.md#postrefresh-action-hook)). It reads the composed error rows and maps each location to a field message through `setValidation`. See [[post-refresh-validation-propagation]].
- **Masked tax id inputs.** A custom visual element replaces the generated VAT group with masked text inputs (project practice, using a third-party mask library).
- **Rating row colours.** A table row highlighting hook colours rows by the rating result; see [[table-row-highlighting-hook]] and the [table hooks guide](../../agent-docs/frontend/hooks/table-hooks.md).
- **Hook keys.** Registration keys are generated per page or container. Copy them from the generated customizer of your own project.

## Examples

### rackinspect (example project code, not platform API)
- Framework: React
- Key files: `custom/hooks/ViewEditActionHooks/customServicesPartnerServicePartnerPartnerViewEditActionsHook.tsx`, `custom/hooks/TableRowHighlightingHooks/ratingTableHighlightHook.tsx`
- Pattern: the refresh handler builds a map keyed by the error location with the message as value; the highlight hook maps rating result values to background colours.
- Notable: the display is server-authoritative; there is no client-side duplicate of the validation.
