## Overview

A custom organization directory component that replaces the generated DiscoveryPanel table with an infinite-scrolling, card-based search interface. Supports filtering by name, address, and capability. Framework: React.

## Implementation Pattern

The pattern replaces a generated table via Pandino custom visual element registration:

- **Registration** -- Registered in `application-customizer.tsx` via `registerServicesFeedDiscoveryPanelDiscoveryPanel_View_EditOrganizationSearchComponentCustomImplementation(context)`, binding a custom `FC<TableProxyProps>` to the discovery panel table component key.
- **DiscoveryContainer** (`custom/discoveryComponent/DiscoveryContainer.tsx`) -- Main container that wires filters, pagination, and infinite scroll. Uses the same `useInfiniteScroll` hook from the feed component.
- **DiscoveryOrganizationCard** (`custom/discoveryComponent/DiscoveryOrganizationCard.tsx`) -- Card with logo avatar (downloaded via `AccessServiceImpl.downloadFile`), name, address with map marker icon, email, phone, and capability chips. Uses `useLogoUrl` hook for binary token-to-blob-URL conversion.
- **DiscoveryFilters** (`custom/discoveryComponent/DiscoveryFilters.tsx`) -- Horizontal chip bar + SwipeableDrawer (top anchor). Three filters: organization name, address (text fields), capability (Autocomplete). Batch-apply UX with Apply/Clear All buttons.
- **useDiscoveryPagination** (`custom/discoveryComponent/hooks/useDiscoveryPagination.ts`) -- Seek-based pagination (same PAGE_SIZE+1 pattern as feed). Always applies `OrganizationStatus.ACTIVE` filter. Builds QueryCustomizer with `StringOperation.like` for text search.
- **useDiscoveryFilters** (`custom/discoveryComponent/hooks/useDiscoveryFilters.ts`) -- Filter state persisted to sessionStorage via `useDataStore`. Manages organizationName, fullAddress, and selectedCapability.

**Key design decisions**:
- Shares `useInfiniteScroll` and `useCapabilitiesAutocomplete` hooks with the feed component for consistency
- Logo images are downloaded as binary blobs and rendered as MUI Avatar with fallback initial letter
- Scroll area uses CSS gradient mask for a fade-out effect at the bottom

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/discoveryComponent/DiscoveryContainer.tsx`, `custom/discoveryComponent/DiscoveryOrganizationCard.tsx`, `custom/discoveryComponent/DiscoveryFilters.tsx`, `custom/discoveryComponent/hooks/useDiscoveryPagination.ts`, `custom/hooks/custom-implementations/registerServicesFeedDiscoveryPanelDiscoveryPanel_View_EditCustomImplementations.tsx`
- Pattern: Replaces generated DiscoveryPanel table via CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY with card-based org directory; reuses useInfiniteScroll from feed
- Notable: Binary logo download via AccessServiceImpl; CSS gradient mask for scroll fade-out; ACTIVE-only status filter hardcoded in QueryCustomizer
