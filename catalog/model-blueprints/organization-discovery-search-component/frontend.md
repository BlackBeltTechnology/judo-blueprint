## Overview

The generated discovery panel shows organizations as a table. This pattern replaces that table with an infinite-scrolling, card-based directory with filters for name, address and capability.

## Implementation Pattern

**Registration:** the discovery panel must be exposed by the model as a custom implementation element. Register the component with `registerService(CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY, ..., { component: <ELEMENT>_COMPONENT_INTERFACE_KEY })`, using the per-element key generated in the container's `customization.ts` and the register function from the generated scaffold. For a table the props type is `TableProxyProps` from `~/custom`. Do not reuse another project's key.

**Container:** a container component wires the three parts together: the filters, the seek-based pagination and the infinite scroll. The infinite-scroll hook can be shared with other list components in the same frontend.

**Cards:** each organization is one card with a logo avatar (letter fallback), name, address, contact details and capability chips. The logo is a binary token. Convert it to a blob URL with a small hook and release the URL when the card unmounts.

**Filters:** a horizontal chip bar opens a top drawer. Three filters: name, address and capability (autocomplete, backed by the server). Filters apply on "Apply", and "Clear all" resets them. Filter state is kept in session storage so it survives navigation.

**Pagination:** seek-based. Request the page size plus one row; the extra row tells whether a next page exists. The query always includes the status filter for ACTIVE organizations and uses a like-match for text filters.

## Examples

### Example (project code, not platform API)
- Framework: React with MUI
- Pattern: the container reuses the feed's infinite-scroll hook; the card downloads the logo through the access service and displays it as a blob URL.
- Notable: the scroll area uses a CSS gradient mask for a fade at the bottom. The ACTIVE filter is hard-coded in the query builder.
