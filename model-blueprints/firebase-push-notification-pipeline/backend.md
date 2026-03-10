## Overview

Implements a multi-stage push notification delivery pipeline using Firebase Cloud Messaging (FCM). A separate `firebase` Maven module wraps the Firebase Admin SDK as an OSGi service, while `PushNotificationServiceImpl` orchestrates notification creation, batch delivery, retry, device management, and email fallback.

## Implementation Pattern

**1. Firebase Module (OSGi service wrapping FCM):**
- `FirebaseMessagingService` -- `@Component(service=..., configurationPolicy=REQUIRE)` with `@Designate(ocd=Config.class)` for service account credentials (file path or base64)
- `BridgingClassLoader` -- bridges bundle and system class loaders for Firebase SDK compatibility in OSGi
- `FcmSendResult` enum -- `SUCCESS`, `FAILED_RETRYABLE`, `FAILED_INVALID_TOKEN` enabling callers to distinguish transient vs permanent failures
- `sendMessage()` builds platform-specific configs: Android uses data-only messages (no notification payload) for Capacitor deep link compatibility; APNs uses alert with badge
- Supports collapse keys for notification coalescing and silent mode for do-not-disturb

**2. PushNotificationService (common module):**
- `@Component(immediate=true, service=PushNotificationService.class)` with `@Reference` to `FirebaseMessagingService`, DAOs, `PlatformEmailService`, and `MLSZKSZPlatformI18n`
- **Creation phase:** `sendPostPublishedNotification()` / `sendAnnouncementNotification()` query eligible users respecting opt-in preferences, create PENDING `Notification` records with fast-path batch deduplication
- **Delivery phase:** `deliverPendingNotifications()` (called by scheduler) queries PENDING + retriable FAILED notifications, builds user/device caches to avoid N+1, sends FCM per device, sends email if user opted in
- **Retry logic:** Exponential backoff (`BASE_RETRY_DELAY * 2^retryCount`, capped at 60 min), max 5 retries, cumulative delay check before retry eligibility
- **Device management:** `registerDevice()` does global token dedup (migrates tokens across users), `updateDeviceToken()` handles token refresh, `cleanupStaleTokens()` deactivates devices with old `tokenUpdatedAt`
- **Deep link routing:** Static map from `NotificationType` to route prefix (e.g., `NEW_OFFER` -> `Services/Feed/FeedEntryTO/Offer/RelationViewPage/`)

**3. Scheduler Integration:**
- `NotificationDeliveryJob` -- runs every 30s, delegates to `PushNotificationService.deliverPendingNotifications()`
- `StaleTokenCleanupJob` -- daily, delegates to `cleanupStaleTokens(thresholdDays)` with configurable threshold

## Examples

### mlszksz-platform
- Key files: `firebase/FirebaseMessagingService.java`, `common/services/impl/PushNotificationServiceImpl.java`, `scheduler/NotificationDeliveryJob.java`, `scheduler/StaleTokenCleanupJob.java`
- Pattern: Separate `firebase` Maven module wraps FCM SDK with OSGi classloader bridging; `PushNotificationServiceImpl` creates PENDING notification records then a scheduler job delivers them in batches with per-device FCM sends and exponential backoff retry
- Notable: Android messages are data-only (no `notification` payload) so Capacitor handles both foreground display and background tap events. `FcmSendResult.FAILED_INVALID_TOKEN` triggers immediate device deactivation. Email notifications are sent alongside push as a best-effort fallback.
- DI wiring: `FirebaseMessagingService` (firebase module) -> `PushNotificationServiceImpl` (@Reference) -> consumed by `FeedServiceImpl`, custom operations, and `NotificationDeliveryJob`
