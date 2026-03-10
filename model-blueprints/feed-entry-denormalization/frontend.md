## Overview

The feed entry denormalization entity has the most extensive React frontend customization in the project. The entire feed page is replaced with a custom infinite-scrolling, card-based feed component with type-aware filtering and navigation.

## Implementation Pattern

- **Custom visual element replacement**: A Pandino-registered component replaces the generated FeedPanel table with `FeedContainer`, a fully custom feed experience. The container manages infinite scroll pagination, filter state, and card-based rendering.
- **FeedEntryCard**: Each denormalized feed entry renders as a styled `Card` with a color-coded left border (by `PostType`), capability chips, organization name link, validity dates (for offers/requests), and a summary preview.
- **Type-aware navigation**: A page actions hook (`registerServicesMLSZKSZFeedDashboardAccessViewPageActionsHook`) overrides `feedEntryTOOpenPageAction` to query the type-specific derived relation (news/offer/request/announcement) and navigate to the corresponding `RelationViewPage`.
- **Feed filters**: Custom `FeedFilters` component provides capability-based autocomplete filtering and entry type selection, backed by `useFeedFilters` and `useCapabilitiesAutocomplete` hooks.
- **Infinite scroll**: `useInfiniteScroll` hook monitors scroll position, `useFeedPagination` manages seek-based pagination, and `useScrollDirection` hides filters when scrolling down.
- **RequestPost drawer**: A floating action button (FAB) opens a `RequestPostDrawer` for company users to request new posts, using `requestPost` operation from the FeedPanel.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/feedComponent/FeedContainer.tsx`, `custom/feedComponent/FeedEntryCard.tsx`, `custom/feedComponent/FeedFilters.tsx`, `custom/feedComponent/hooks/useFeedPagination.ts`, `custom/feedComponent/hooks/useInfiniteScroll.ts`, `custom/hooks/custom-implementations/registerServicesFeedFeedPanelFeedPanel_View_EditCustomImplementations.tsx`, `custom/hooks/pages/registerServicesMLSZKSZFeedDashboardAccessViewPageActionsHook.ts`
- Pattern: The FeedContainer replaces the generated table, uses seek-based pagination with `_orderBy: [{ attribute: 'createdAt', descending: true }]`, and renders FeedEntryCard components with type-colored borders. Navigation resolves the denormalized entryType to the concrete post's signed identifier via derived relation queries.
- Notable: The feed uses `usePrincipal` to check if the current user has a COMPANY_ADMIN or COMPANY_READER role before showing the "Request Post" FAB. Organization names in cards are clickable links that navigate to the organization detail page.
