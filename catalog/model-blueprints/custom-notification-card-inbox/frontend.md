## Overview

A custom notification inbox that replaces the generated notifications table with a card-based list showing type icons, relative timestamps, and tap-to-navigate deep linking. Framework: React.

## Implementation Pattern

The component replaces the generated notifications table. In the platform this works only for a visual element that the UI model declares as a custom implementation widget; the generator then emits a scaffold with one `register<Interface>CustomImplementation(context)` function per such element and the proxy props type (here `TableProxyProps`). The component is registered as a Pandino service under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the `component` property set to the element's generated key, and the register function is called from `application-customizer.tsx` (see [advanced patterns](../../agent-docs/frontend/advanced-patterns.md), Component Replacement Hook). Arbitrary generated components cannot be replaced this way. The project specifics below are reference implementation code:

- **Registration** -- `registerServicesFeedNotificationsPanelNotificationsPanel_View_EditNotificationsComponentCustomImplementation(context)` in `application-customizer.tsx` binds a custom `FC<TableProxyProps>` to the notifications panel table component key.
- **NotificationCard** -- Individual notification card component with:
  - Type-specific icon mapping (`NEW_POST` -> newspaper, `NEW_ANNOUNCEMENT` -> bullhorn, `INQUIRY_RECEIVED` -> email-open, `REGISTRATION_APPROVED` -> check-circle, etc.)
  - Relative timestamp via `date-fns` `formatDistanceToNow` with locale support
  - Message text with 3-line clamp (`-webkit-line-clamp: 3`)
  - Delete button (stopPropagation to prevent card tap)
  - Clickable card area when `referenceEntityId` is present
- **Custom implementation** -- Manages paginated notification loading via the application's generated notifications dashboard service client (`AppServiceForNotificationsDashboardImpl`), maps stored rows to `NotificationItem` interface, handles notification deletion with badge count decrement, and navigates to feed entries via `navigateToFeedEntry()`.
- **Badge sync** -- On notification delete, calls `notificationBadgeStore.decrement()` (an application store, not a platform API) to keep header bell badge in sync.

## Examples

### Variant seen in practice
- Framework: React
- Pattern: Replaces the notifications table, declared as a custom implementation element in the UI model, via CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY with card-based inbox; handles own pagination and deletion
- Notable: Type-specific icon mapping for 9 notification types; relative timestamps with a second locale; badge count sync via shared notificationBadgeStore
