## Overview

The notification entity has comprehensive React frontend customization including a card-based notification inbox, push notification integration (Capacitor native + web badge), deep linking from notifications to content, and a notification bell icon with unread badge in the app header.

## Implementation Pattern

- **Custom notification list**: A Pandino-registered `CUSTOM_VISUAL_ELEMENT` replaces the generated notifications table with a card-based list. Each `NotificationCard` renders an icon (mapped from `NotificationType` to MDI icons), title, message, relative timestamp (using `date-fns` `formatDistanceToNow`), and a delete button. Tapping a notification navigates to the referenced content and auto-deletes the notification.
- **Push notification integration**: `PushNotificationAppIntegration` is registered as an `AppBarExtraComponents` hook, rendering a bell icon with unread badge in the header. The `usePushNotifications` hook manages Capacitor PushNotifications plugin on native platforms (Android/iOS) and calls backend `registerDevice`/`deactivateDevice`/`updateDeviceToken` operations.
- **Deep linking**: `navigateToFeedEntry()` resolves a `referenceEntityId` (FeedEntry UUID) to the type-specific post view page by querying the FeedEntryTO derived relations. A `NotificationDeepLinkRoute` handles incoming push notification URLs.
- **Badge state management**: `notificationBadgeStore` is a shared external store (using `useSyncExternalStore`) that keeps the unread count synchronized between the header bell and the bottom menu badge.
- **Page mask override**: A page actions hook overrides `getMask` for the NotificationsDashboard to include `referenceEntityId` for deep linking support.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/notifications/NotificationCard.tsx`, `custom/notifications/PushNotificationAppIntegration.tsx`, `custom/notifications/push-notification-service.ts`, `custom/notifications/navigate-to-feed-entry.ts`, `custom/notifications/notification-badge-store.ts`, `custom/hooks/custom-implementations/registerServicesFeedNotificationsPanelNotificationsPanel_View_EditCustomImplementations.tsx`, `custom/hooks/pages/registerServicesMLSZKSZNotificationsDashboardAccessViewPageActionsHook.ts`
- Pattern: The notification panel uses seek-based pagination (`_seek: { limit: PAGE_SIZE + 1 }`) to implement "Load more" with optimistic UI updates on delete. Push notifications use the Capacitor PushNotifications plugin for native (Android/iOS) and fall back to the badge-only web experience. The `navigateToFeedEntry` function chains three API calls: get FeedPanel, list FeedEntryTO by identifier, then get the type-specific relation.
- Notable: The notification type-to-icon mapping covers 9 types (NEW_POST, NEW_ANNOUNCEMENT, INQUIRY_RECEIVED, REGISTRATION_APPROVED, etc.). The `notificationBadgeStore` uses a subscribe/getCount pattern compatible with React 18's `useSyncExternalStore`.
