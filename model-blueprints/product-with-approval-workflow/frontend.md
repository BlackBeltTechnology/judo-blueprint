## Overview

The product approval workflow blueprint has extensive React frontend customization covering custom card-based product listing views, role-based dashboard routing, table row highlighting by workflow state, custom data masks for optimized fetching, extra container actions for product creation, and comprehensive Hungarian i18n translations for all workflow states and operations.

## Implementation Pattern

- **Custom card views per role**: Cards container config hooks (`CardsContainerConfigHook`) replace the default table view with MUI Card grids for both author and approver product listings. Each card displays product title, goal, author name/avatar, curriculum and audience as Chip elements, version number, and workflow state. The hooks provide both a `CardElement` and a `ToolbarElement` with filter capabilities.
- **Dynamic filters from reference data**: The card toolbar components fetch reference data (audiences, curriculums, resultTypes, institutions) at mount time and build filterable checkbox lists. Filters operate on the Product's denormalized aggregated string fields using `_StringOperation.like` or `_StringOperation.equal`.
- **Table page action hooks with custom masks**: Access table page action hooks override `getMask()` to request a specific set of fields including nested relations (`resultTypes{name}`, `audiences{name}`, `curriculums{name}`), optimizing the data fetch for card rendering.
- **Table row highlighting**: A `TableRowHighlightingHook` registered for the AdminProduct table component applies conditional background colors based on workflow state: orange (`#ff814f`) for products with `isPendingDelegated === true` (not yet assigned to an approver) and green (`#9bc43a`) for `FINALIZED` state (awaiting approval).
- **Extra container actions**: An `ExtraActionsHook` adds a "Produktum letrehozasa" (Create Product) button with a document-plus icon to the author's product table, wiring to the `createProductAction`.
- **Role-based dashboard routing**: The `application-customizer.tsx` registers a custom dashboard component that renders different product table pages based on the principal's role: `ServicesUserAdminProductsAccessTablePage` for admins, `ServicesUserApproverProductsAccessTablePage` for approvers, and the author products page (lazy-loaded) as the default.
- **i18n translations**: The `application_hu-HU.json` file provides Hungarian translations for all ProductState enum values (Vazlat/Draft, Veglegesitett/Finalized, Jovahagyott/Approved), EventType values, menu items, and form labels.

## Examples

### alba
- Framework: React
- Key files: `custom/hooks/cards/AuthorProductsCards.tsx`, `custom/hooks/cards/ApproverProductsCards.tsx`, `custom/hooks/cards/AuthorProductsExtraContainerActions.tsx`, `custom/hooks/custom/authorProductsTablePage.tsx`, `custom/hooks/custom/approverProductsTablePage.tsx`, `custom/hooks/custom/authorPublicProductsTablePage.tsx`, `custom/hooks/highlighting/AdminProductsTableHighlighting.tsx`, `custom/application-customizer.tsx`
- Pattern: The product listing uses custom MUI Card grids with dynamic reference-data filters instead of the default table view. The author and approver each have dedicated card components with role-appropriate fields. The admin view uses the standard table but adds row highlighting for workflow state visibility. A custom dashboard routes users to the appropriate product page based on their role (admin/approver/author). The `authorPublicProductsTablePage` hook disables the `createProductAction` for the public products view by setting it to `null`.
- Notable: The custom masks in table page hooks explicitly include nested relation fields (`resultTypes{name}`, `audiences{name}`, `curriculums{name}`) to ensure the card components can render classification chips. Author cards display curriculum and audience while approver cards also show the product state as a Chip with translated enum labels. The `BoldCardHeader` styled component applies bold font weight to card titles across all card views.
