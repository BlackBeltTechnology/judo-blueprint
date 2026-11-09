## Overview

The abstract Post with concrete content subtypes manifests in the React frontend through per-type custom view components (NewsView, OfferView, RequestView, AnnouncementView) that replace the generated forms, and through type-aware navigation in the feed that resolves each entry to its concrete subtype's detail page.

## Implementation Pattern

- **Per-type container hooks**: Each concrete post subtype has a dedicated Pandino container extra-actions hook that replaces the generated form with a custom view component. The hooks use `createPortal` with `MutationObserver` to hide the generated `TransferObjectViewPageContainer` and inject the custom view.
- **Custom view components**: `NewsView`, `OfferView`, `RequestView`, and `AnnouncementView` render type-specific layouts with organization info, capability chips, validity dates (offers/requests), deadlines (requests), price (offers), document attachments (announcements), and inquiry actions.
- **Type-aware feed navigation**: The feed page actions hook resolves `entryType` (from PostType enum: NEWS, OFFER, REQUEST, ANNOUNCEMENT) to the correct derived relation via `feedEntryService.getNews/getOffer/getRequest/getAnnouncement`, then navigates to the subtype-specific `RelationViewPage`.
- **Inquiry support**: Offer and Request views include inquiry functionality via `offerService.inquery()` / `requestService.inquery()`, with page mask overrides to include `hasInquired` and `inqueryNumber` fields.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/custom_views/NewsView.tsx`, `custom/custom_views/OfferView.tsx`, `custom/custom_views/RequestView.tsx`, `custom/custom_views/AnnouncementView.tsx`, `custom/hooks/containers/registerServicesFeedNewsContainerHook.tsx`, `custom/hooks/containers/registerServicesFeedOfferContainerHook.tsx`, `custom/hooks/containers/registerServicesFeedRequestContainerHook.tsx`, `custom/hooks/containers/registerServicesFeedAnnouncementContainerHook.tsx`
- Pattern: Each container hook registers an `FC` component via `CONTAINER_EXTRA_ACTIONS_HOOK_INTERFACE_KEY`. The component uses a `MutationObserver` to find and hide the generated page container, then portals the custom view into the parent element. The custom views receive `data` and `isLoading` props and render a mobile-friendly card layout.
- Notable: The shared `PostViewLayout` component and `ContactActions` component in `custom/custom_views/shared/` provide reusable layout sections across all post type views.
