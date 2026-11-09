## Overview

A native push notification system for JUDO React + Capacitor apps that manages the full lifecycle: FCM token acquisition, backend device registration, foreground/background notification handling, deep linking to content pages, unread badge count, and cold-start notification capture. Framework: React (Capacitor Android).

## Implementation Pattern

The pattern consists of several cooperating modules registered through the Pandino application customizer:

- **PushNotificationAppIntegration** (`custom/notifications/PushNotificationAppIntegration.tsx`) -- Registered as an `AppBarExtraComponentsHook` via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with `{ component: 'AppBarExtraComponents' }`. Renders a bell icon with MUI Badge in the app header. Fetches initial unread count on mount via `listNotifications` with `{ _seek: { limit: 0 } }` to get only the `__count`. Wires up `usePushNotifications` hook with backend service callbacks.
- **usePushNotifications** (`custom/notifications/usePushNotifications.ts`) -- Core hook that initializes push after 1-second defer, registers device with backend, handles foreground notifications (snackbar toasts with "Open" action button), notification tap navigation, and app resume retry for pending registrations/token updates.
- **push-notification-service** (`custom/notifications/push-notification-service.ts`) -- Low-level Capacitor `@capacitor/push-notifications` wrapper. Handles permission request, listener registration before `register()` call (race condition prevention), monthly token refresh detection.
- **notification-badge-store** (`custom/notifications/notification-badge-store.ts`) -- Lightweight external store using `useSyncExternalStore` pattern. Shared between header bell and bottom navigation to keep badge counts in sync.
- **launch-notification-store** (`custom/notifications/launch-notification-store.ts`) -- Captures cold-start notification taps that fire before OIDC redirect and authenticated component tree mount. Uses Capacitor Preferences for persistence across WebView recreation.
- **navigateToFeedEntry** (`custom/notifications/navigate-to-feed-entry.ts`) -- Resolves a feed entry UUID to a type-specific `RelationViewPage` route (News, Offer, Request, Announcement) via `_identifier` lookup + derived relation query.
- **NotificationDeepLinkRoute** (`custom/notifications/NotificationDeepLinkRoute.tsx`) -- React Router route component at `#/notification/:notificationId/:feedEntryId` that navigates to the post and auto-deletes the notification. Registered in `src/extra-routes.tsx`.
- **retry-utils** (`custom/notifications/retry-utils.ts`) -- Exponential backoff utility (2s, 5s, 10s delays) for device lifecycle API calls.

**Key design decisions**:
- Device registration is idempotent: `Preferences` stores the registered token and skips re-registration on app resume
- Pending registrations and token updates are persisted in Preferences and retried on `appStateChange` resume events
- Auth guard suppresses foreground notifications when not authenticated

## Examples

### mlszksz-platform
- Framework: React (Capacitor Android)
- Key files: `custom/notifications/PushNotificationAppIntegration.tsx`, `custom/notifications/usePushNotifications.ts`, `custom/notifications/push-notification-service.ts`, `custom/notifications/notification-badge-store.ts`, `custom/notifications/launch-notification-store.ts`, `custom/notifications/navigate-to-feed-entry.ts`, `custom/notifications/NotificationDeepLinkRoute.tsx`
- Pattern: FCM push with backend registerDevice/deactivateDevice/updateDeviceToken APIs, snackbar foreground display, deep link navigation to typed post pages, cold-start capture, badge sync via useSyncExternalStore
- Notable: Registered as AppBarExtraComponents Pandino service for header bell icon; extra-routes.tsx adds `notification/:notificationId/:feedEntryId` deep link route
