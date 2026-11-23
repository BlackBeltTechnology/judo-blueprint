## Overview

Implements a multi-stage push notification delivery pipeline using Firebase Cloud Messaging (FCM). A separate `firebase` Maven module wraps the Firebase Admin SDK as an OSGi service, while `PushNotificationServiceImpl` orchestrates notification creation, batch delivery, retry, device management, and email fallback.

## Implementation Pattern

**1. Firebase Module (OSGi service wrapping FCM; application code, not platform API):**
- `FirebaseMessagingService` -- `@Component(service=..., configurationPolicy=REQUIRE)` with `@Designate(ocd=Config.class)` for service account credentials (file path or base64)
- `BridgingClassLoader` -- bridges bundle and system class loaders for Firebase SDK compatibility in OSGi
- `FcmSendResult` enum -- `SUCCESS`, `FAILED_RETRYABLE`, `FAILED_INVALID_TOKEN` enabling callers to distinguish transient vs permanent failures
- `sendMessage()` builds platform-specific configs: Android uses data-only messages (no notification payload) for Capacitor deep link compatibility; APNs uses alert with badge
- Supports collapse keys for notification coalescing and silent mode for do-not-disturb

### 2. PushNotificationService (common module, application code)
- `@Component(immediate=true, service=PushNotificationService.class)` with `@Reference` to `FirebaseMessagingService`, the generated DAOs, `PlatformEmailService`, and `AppI18n`
- **Creation phase:** `sendPostPublishedNotification()` / `sendAnnouncementNotification()` query eligible users respecting opt-in preferences, create PENDING `Notification` records with fast-path batch deduplication
- **Delivery phase:** `deliverPendingNotifications()` (called by scheduler) queries PENDING + retriable FAILED notifications, builds user/device caches to avoid N+1, sends FCM per device, sends email if user opted in
- **Retry logic:** Exponential backoff (`BASE_RETRY_DELAY * 2^retryCount`, capped at 60 min), max 5 retries, cumulative delay check before retry eligibility
- **Device management:** `registerDevice()` does global token dedup (migrates tokens across users), `updateDeviceToken()` handles token refresh, `cleanupStaleTokens()` deactivates devices with old `tokenUpdatedAt`
- **Deep link routing:** Static map from `NotificationType` to route prefix (e.g., `NEW_ITEM` -> a route prefix for the item view)

**3. Scheduler Integration (application-registered jobs; see [[osgi-scheduled-background-jobs]]):**
- Interceptors are not involved: they run only for built-in operations, so custom operations that raise an event call the notification service themselves.
- `NotificationDeliveryJob` -- runs every 30s, delegates to `PushNotificationService.deliverPendingNotifications()`
- `StaleTokenCleanupJob` -- daily, delegates to `cleanupStaleTokens(thresholdDays)` with configurable threshold

## Examples

### Variant seen in practice
- Key files: the Firebase messaging service, the push notification service implementation, the delivery job and the stale token cleanup job.
- Pattern: Separate `firebase` Maven module wraps FCM SDK with OSGi classloader bridging; `PushNotificationServiceImpl` creates PENDING notification records then a scheduler job delivers them in batches with per-device FCM sends and exponential backoff retry
- Notable: Android messages are data-only (no `notification` payload) so Capacitor handles both foreground display and background tap events. `FcmSendResult.FAILED_INVALID_TOKEN` triggers immediate device deactivation. Email notifications are sent alongside push as a best-effort fallback.
- DI wiring: `FirebaseMessagingService` (firebase module) -> `PushNotificationServiceImpl` (@Reference) -> consumed by `FeedServiceImpl`, custom operations, and `NotificationDeliveryJob`
