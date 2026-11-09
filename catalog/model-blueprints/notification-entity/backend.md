## Overview

The Notification and Device entities are managed by a comprehensive `PushNotificationService` that handles FCM push notification delivery, device registration lifecycle, and retry logic with exponential backoff. Scheduler jobs handle failed notification retries and stale token cleanup.

## Implementation Pattern

- `PushNotificationServiceImpl` is an OSGi `@Component` that injects `FirebaseMessagingService`, `NotificationDao`, `DeviceDao`, `UserDao`, and `PlatformEmailService`
- On post publish, `sendPostPublishedNotification()` queries eligible users (respecting per-type notification preferences: notifyOffers, notifyRequests, notifyNews, notifyAnnouncements), creates a `Notification` entity with PENDING status, and sends FCM multicast to all active devices
- Deduplication: checks for existing notifications with the same type+entityId within a 5-minute window before creating
- Per-device FCM result handling: SUCCESS marks SENT, FAILED_INVALID_TOKEN deactivates the device, FAILED_RETRYABLE marks PARTIALLY_SENT and records retryable devices
- Device registration (`registerDevice()`) handles token migration between users, duplicate cleanup, and platform updates
- `retryFailedNotifications()` processes FAILED, PARTIALLY_SENT, and stuck PENDING notifications with exponential backoff (base 5 min, max 60 min, up to 5 retries)
- Custom operations: `RegisterDeviceCustomImplementation`, `DeactivateDeviceCustomImplementation`, `UpdateDeviceTokenCustomImplementation`, `DeleteNotificationCustomImplementation`, `ClearAllNotificationsCustomImplementation`
- Scheduler jobs: `NotificationRetryJob` (periodic retry), `StaleTokenCleanupJob` (deactivates devices with old tokens)

## Examples

### mlszksz-platform
- Key files: `common/services/PushNotificationService.java`, `common/services/impl/PushNotificationServiceImpl.java`, `firebase/FirebaseMessagingService.java`, `scheduler/NotificationRetryJob.java`, `scheduler/StaleTokenCleanupJob.java`
- Pattern: Notification creation with FCM multicast delivery, per-device result tracking, PARTIALLY_SENT state for partial failures, exponential backoff retry via scheduler
- Notable: Deep link routing maps NotificationType to frontend routes (NEWS, OFFER, REQUEST, ANNOUNCEMENT); dual-channel delivery (FCM push + optional email if user has emailNotifications enabled); collapse key grouping prevents notification spam on multi-device users
