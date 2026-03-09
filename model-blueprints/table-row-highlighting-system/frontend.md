## Overview

Conditional table row background coloring based on entity attribute values (typically enums), registered as Pandino hooks targeting specific table components. Framework: React.

## Implementation Pattern

- **Hook type**: `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY` from `~/theme/table-row-highlighting`
- **Registration**: In `application-customizer.tsx`, each hook is registered with a `component` property targeting the specific table component name (e.g., `ServicesOffer_servicesOfferOffer_View_EditOfferingItemsComponent`)
- **Hook shape**: `TableRowHighlightingHook<TStored>` -- a function returning a function returning an array of highlight rule objects, each with `name` (CSS class), `label` (legend text), `backgroundColor` (hex color), and `condition` (predicate on row params)
- **Conditions**: Typically check `params.row.<enumField> === EnumType.VALUE` to determine which rows should be highlighted
- **Multiple hooks**: Register separate hooks for different tables, each with its own set of color rules

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/TableRowHighlightingHooks/offerItemsTableHighlightHook.tsx`, `custom/hooks/TableRowHighlightingHooks/ratingTableHighlightHook.tsx`
- Pattern: Two hooks: offer items table highlights MATERIAL rows blue (`#0095ff`) and SERVICE rows orange (`#e88f00`); rating table highlights grade A rows green (`#00cc00`) and grade C rows red (`#cc0000`)
- Notable: Each hook is registered with a specific `component` property in `application-customizer.tsx` to scope the highlighting to the correct table
