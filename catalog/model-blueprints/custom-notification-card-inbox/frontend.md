## Overview

A custom notification inbox that replaces the generated notifications table with a card-based list showing type icons, relative timestamps, and tap-to-navigate deep linking. Framework: React.

## Implementation Pattern

The component replaces the generated notifications table via Pandino custom visual element registration:

- **Registration** -- `registerServicesFeedNotificationsPanelNotificationsPanel_View_EditNotificationsComponentCustomImplementation(context)` in `application-customizer.tsx` binds a custom `FC<TableProxyProps>` to the notifications panel table component key.
- **NotificationCard** (`custom/notifications/NotificationCard.tsx`) -- Individual notification card component with:
  - Type-specific icon mapping (`NEW_POST` -> newspaper, `NEW_ANNOUNCEMENT` -> bullhorn, `INQUIRY_RECEIVED` -> email-open, `REGISTRATION_APPROVED` -> check-circle, etc.)
  - Relative timestamp via `date-fns` `formatDistanceToNow` with Hungarian locale support
  - Message text with 3-line clamp (`-webkit-line-clamp: 3`)
  - Delete button (stopPropagation to prevent card tap)
  - Clickable card area when `referenceEntityId` is present
- **Custom implementation** (`custom/hooks/custom-implementations/registerServicesFeedNotificationsPanelNotificationsPanel_View_EditCustomImplementations.tsx`) -- Manages paginated notification loading via `MLSZKSZServiceForNotificationsDashboardImpl`, maps stored rows to `NotificationItem` interface, handles notification deletion with badge count decrement, and navigates to feed entries via `navigateToFeedEntry()`.
- **Badge sync** -- On notification delete, calls `notificationBadgeStore.decrement()` to keep header bell badge in sync.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/notifications/NotificationCard.tsx`, `custom/hooks/custom-implementations/registerServicesFeedNotificationsPanelNotificationsPanel_View_EditCustomImplementations.tsx`
- Pattern: Replaces generated notifications table via CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY with card-based inbox; handles own pagination and deletion
- Notable: Type-specific icon mapping for 9 notification types; relative timestamps with Hungarian locale; badge count sync via shared notificationBadgeStore
