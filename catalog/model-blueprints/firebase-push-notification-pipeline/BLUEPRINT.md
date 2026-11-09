---
id: firebase-push-notification-pipeline
title: "Firebase Push Notification Delivery Pipeline"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A complete push notification delivery pipeline built on Firebase Cloud Messaging (FCM). This is an implementation-only blueprint -- it does not correspond to a single model entity but orchestrates several model entities (Device, Notification, User) through a multi-stage delivery process with retry logic, device management, deduplication, and deep link routing.

The pipeline includes:
- A `firebase` Maven module wrapping the Firebase Admin SDK as an OSGi service with credential management and ClassLoader bridging
- A `PushNotificationService` (common module) implementing the full notification lifecycle: creation with deduplication, batch delivery with per-device FCM sending, exponential backoff retry, invalid token cleanup, and email fallback
- Device registration/deactivation/token refresh operations with global deduplication
- Integration with a scheduler job (`NotificationDeliveryJob`) that processes PENDING and retries FAILED notifications on a 30-second cycle

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
