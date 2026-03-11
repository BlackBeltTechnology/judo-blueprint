## Overview

A custom card-based social feed that replaces the generated data grid with an infinite-scrolling, mobile-first feed panel. Uses Pandino's `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` to replace the default table component. Framework: React.

## Implementation Pattern

The pattern replaces a generated table component via Pandino's custom visual element registration:

- **Registration** -- In `application-customizer.tsx`, the custom implementation is registered via `registerServicesFeedFeedPanelFeedPanel_View_EditGroupComponentCustomImplementation(context)`, which binds a custom `FC<GenericProxyProps>` to the `SERVICES_FEED_FEED_PANEL_FEED_PANEL_VIEW_EDIT_GROUP_COMPONENT` key.
- **FeedContainer** (`custom/feedComponent/FeedContainer.tsx`) -- Main container that orchestrates filters, pagination, infinite scroll, and the Request Post FAB. Accepts `fetchAction`, `openPageAction`, and `owner` from the generated page's action definitions.
- **FeedEntryCard** (`custom/feedComponent/FeedEntryCard.tsx`) -- Memoized card component with color-coded left border per post type, meta row (type/org/author/date), summary (3-line clamp), validity dates for Offer/Request, capability chips, and sensitive content badge. Organization name is a clickable link.
- **FeedFilters** (`custom/feedComponent/FeedFilters.tsx`) -- Horizontal chip bar + SwipeableDrawer with batch-apply workflow. Filters: post type (multi-select chips), title, summary, organization name (text fields), capability (Autocomplete with server-side search).
- **useFeedPagination** (`custom/feedComponent/hooks/useFeedPagination.ts`) -- Seek-based pagination using `_seek: { limit: PAGE_SIZE+1, lastItem }` pattern. Fetches PAGE_SIZE+1 items; if more than PAGE_SIZE returned, there are more pages. Deduplicates by `__identifier`.
- **useFeedFilters** (`custom/feedComponent/hooks/useFeedFilters.ts`) -- Filter state persisted to sessionStorage. Builds `QueryCustomizer` filter arrays with `StringOperation.like` for text fields and `EnumerationOperation.equals` for post type.
- **useInfiniteScroll** (`custom/feedComponent/hooks/useInfiniteScroll.ts`) -- IntersectionObserver hook that watches a sentinel div at the end of the scroll container and calls `loadMore` when it enters the viewport.
- **useCapabilitiesAutocomplete** (`custom/feedComponent/hooks/useCapabilitiesAutocomplete.ts`) -- Server-side autocomplete for capability filtering, debounced, using the owner's `listCapabilities` action.
- **RequestPostDrawer** (`custom/feedComponent/RequestPostDrawer.tsx`) -- FAB + bottom drawer for creating "request post" entries. Shown only when `usePrincipal().role` is COMPANY_ADMIN or COMPANY_READER.

**Key design decisions**:
- Seek-based pagination avoids count queries and offset drift on live data
- Filter state is persisted in sessionStorage to survive tab navigation
- Cards use color-coded left borders and gradient backgrounds to distinguish post types and announcements

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/feedComponent/FeedContainer.tsx`, `custom/feedComponent/FeedEntryCard.tsx`, `custom/feedComponent/FeedFilters.tsx`, `custom/feedComponent/hooks/useFeedPagination.ts`, `custom/feedComponent/hooks/useInfiniteScroll.ts`, `custom/hooks/custom-implementations/registerServicesFeedFeedPanelFeedPanel_View_EditCustomImplementations.tsx`
- Pattern: Replaces generated FeedPanel table via CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY with infinite-scroll card feed; role-gated Request Post FAB
- Notable: Uses GenericProxyProps to receive actions from generated page; seek-based pagination with `lastItem` cursor; filter drawer with batch-apply UX
