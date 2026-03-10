---
id: "notification-entity-pattern"
title: "Asynchronous Notification Entity with Device Management"
domain: "model"
category: "entity"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

A system-managed notification entity models asynchronous push notifications with delivery tracking. Notifications are queued as PENDING, processed by a background job that delivers them via an external service (e.g., Firebase Cloud Messaging), and their status is updated to SENT or FAILED with retry capability. A companion Device entity stores user device tokens for delivery targeting.

## Structure

- **Notification entity** (createable=false, updateable=false, deleteable=false):
  - `type`: Category enum classifying the notification trigger event
  - `title`, `message`: Display content
  - `status`: State machine enum (PENDING -> SENT/FAILED, with retry back to PENDING)
  - `referenceEntityId`: Optional reference to the triggering entity
  - `retryCount`: Integer tracking delivery retry attempts
  - `createdAt`: Timestamp
  - `user`: Required relation to the recipient user (often bidirectional)
- **Device entity** (system-managed):
  - `fcmToken`: External service token
  - `platform`: Category enum (ANDROID, IOS, WEB)
  - `isActive`: Boolean for token validity
  - `lastUsedAt`, `registeredAt`: Timestamps
  - `user`: Bidirectional relation to User
- Notifications are created as side effects of business operations (post publish, registration approval, inquiry received)
- Background processor handles delivery and status updates

## Examples

### MLSZKSZPlatform
`Notification` entity with `NotificationType` (8 members: NEW_POST, NEW_ANNOUNCEMENT, INQUIRY_RECEIVED, REGISTRATION_APPROVED/REJECTED, INVITATION_RECEIVED/APPROVED/REJECTED) and `NotificationStatus` (PENDING -> SENT/FAILED with retry). `Device` entity stores FCM tokens with `DevicePlatform` (ANDROID, IOS, WEB). Both are system-managed (no CRUD). Notification has bidirectional relation to User. Business operations trigger notifications: `publish` creates NEW_POST, `accept` creates REGISTRATION_APPROVED, `inquery` creates INQUIRY_RECEIVED.

### KozutEugyfelClient
`Ertesites` (Notification) entity tracks email notifications with `kezbesitve: Boolean` (delivered flag), `szoveg: String` (body), `targy: String` (subject). Derives `cimzettEmail` (recipient email) from the `cimzett` (recipient) relation and `bejelentesAzonosito` from the parent report. `olvasott: Boolean` (read flag) tracks user acknowledgment via the `elolvas` (mark-as-read) operation. Simpler than MLSZKSZPlatform -- no device management, email-only delivery.

## Trade-offs

- Pros: Decoupled notification delivery from business operations, retry capability for failed deliveries, multi-platform support, complete delivery tracking
- Cons: Requires external service integration (FCM), device token management complexity, growing notification table needs eventual cleanup
- Prefer when: Application needs push notifications to mobile/web clients with delivery guarantees

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (NotificationStatus lifecycle)
- [category-enum-pattern](category-enum-pattern.md) (NotificationType, DevicePlatform)
- [bidirectional-relation](bidirectional-relation.md) (Device <-> User, Notification <-> User)
- [audit-event-entity](audit-event-entity.md) (similar immutable event tracking pattern)
