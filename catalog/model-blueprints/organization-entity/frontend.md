## Overview

The organization entity manifests in the React frontend through two custom view components: a full-page `OrganizationView` for company reader / discovery detail pages, and `DiscoveryOrganizationCard` for the organization discovery list. Both display logo, contact info, capabilities, and membership details.

## Implementation Pattern

- **Custom OrganizationView**: A container extra-actions component registered via Pandino replaces the generated CompanyReaderOrganization form with a richly styled organization profile page. It downloads and displays the organization logo as a blob URL, shows contact information with clickable email/phone actions, capability chips, membership dates, and full address.
- **DiscoveryContainer and DiscoveryOrganizationCard**: The discovery panel replaces the generated table with an infinite-scrolling card grid. Each `DiscoveryOrganizationCard` shows the organization logo, name, city, and capability chips. The container uses `useDiscoveryFilters` for search and capability filtering, and `useDiscoveryPagination` for seek-based pagination.
- **Portal-based injection**: Custom views use `createPortal` with `MutationObserver` to find the generated `TransferObjectViewPageContainer`, hide it, and inject the custom view in its place.
- **Page mask override**: A page actions hook overrides `getMask` on the discovery organization detail page to include `capabilities{name}` for displaying capability chips.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/OrganizationView.tsx`, `custom/discoveryComponent/DiscoveryContainer.tsx`, `custom/discoveryComponent/DiscoveryOrganizationCard.tsx`, `custom/hooks/containers/registerServicesCompanyReaderOrganizationContainerHook.tsx`, `custom/hooks/containers/registerServicesFeedOrganizationSearchContainerHook.tsx`, `custom/hooks/pages/registerServicesFeedDiscoveryPanelOrganizationSearchRelationViewPageActionsHook.tsx`
- Pattern: The OrganizationView uses a `useLogoUrl` hook that downloads the binary logo token via `AccessServiceImpl.downloadFile` and creates a blob URL. ContactActions component provides clickable email (`mailto:`) and phone (`tel:`) links. The DiscoveryContainer reuses the feed's `useInfiniteScroll` hook.
- Notable: The organization view supports both the companyreader profile context (own organization) and the feed discovery context (browsing other organizations), using the same underlying `OrganizationView` component registered via two different container hooks.
