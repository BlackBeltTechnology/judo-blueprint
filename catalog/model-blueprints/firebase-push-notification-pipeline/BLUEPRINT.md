---
id: firebase-push-notification-pipeline
title: Firebase Push Notification Delivery Pipeline
description: "A push notification delivery pipeline on Firebase Cloud Messaging: notifications are created as pending records, then delivered per device on a schedule with retry, token cleanup and email fallback."
aliases: []
keywords: [firebase, push, notification, delivery, pipeline]
tags: [domain:model, layer:backend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/firebase/src/main/java/hu/blackbelt/mlszksz/platform/firebase/FirebaseMessagingService.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/PushNotificationServiceImpl.java", "mlszksz-platform:application/scheduler/src/main/java/hu/blackbelt/mlszksz/platform/scheduler/NotificationDeliveryJob.java"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Deliver a notification to every eligible device of a user, reliably and without blocking the business operation that triggered it. Creating a notification and sending it are two separate steps, so a slow or failing push service does not hold up the request that caused the event.

### Create first, deliver later

The business operation records a pending notification and returns. A scheduled job later sends each pending notification to the user's devices. A failed send stays in the queue for a later retry.

### Permanent and transient failures are separate

A send to an invalid device token deactivates that device at once. A transient failure is retried with growing delays up to a fixed limit.

## Structure

The pipeline has three parts:

- **Push gateway.** A thin wrapper around the push service's SDK. It sends one message to one device token and reports one of three outcomes: success, a retryable failure, or an invalid token.
- **Notification service.** Creates pending notifications for eligible users, honouring their opt-in preferences, and delivers them. It also registers devices and refreshes their tokens.
- **Scheduled jobs.** One job delivers pending and retriable notifications on a short cycle. A daily job deactivates devices whose token has not been refreshed for a set number of days.

The pipeline is common practice built on platform mechanisms: OSGi components with references, the generated data-access objects (DAOs), and an OSGi-registered scheduler. The platform itself supplies no push or scheduling feature. The entities involved are the notification, the device (one per user and device token) and the user. A notification has a type that maps to a deep-link route in the app.

## Constraints

- A notification is created in the pending state and is delivered only by the delivery job. Creation happens inside the triggering operation's transaction, so a rollback removes the pending record; the job runs outside that transaction.
- Duplicate notifications are suppressed when they are created in a batch.
- Retry delay doubles with each retry, is capped at one hour, and stops after five retries.
- A device token belongs to one user at a time. Registering a token that another user holds moves it.
- Messages to Android devices carry data only, with no visible notification payload, so the app handles both foreground and background taps.
- Email is a best-effort fallback sent only to users who opted in. Its failure does not fail the push.
- A delivery failure is logged and recorded on the notification; it is never thrown to a user as a business fault. Failures in the triggering operation's own creation step are platform failures too: fail the operation rather than throwing a bare runtime exception for a user-facing problem.

## Variations

- **Synchronous send.** Send inside the business operation. This is simpler but ties the request's latency to the push service.
- **Dedicated queue.** Move pending notifications to a message queue instead of a table polled by a job. This scales better but adds an infrastructure component.
- **Email only.** Skip the push gateway and send email alone. This fits products without a mobile app.

## When to use

- Users receive event notifications on mobile devices through a push service.
- A user may have several devices, and each needs its own token.
- Delivery must survive transient failures and must not block the triggering operation.

## When to avoid

- Notifications are only shown inside the app and never pushed.
- Each event must reach the user exactly once with no retry. Use a stronger delivery guarantee.
- The volume is so low that a synchronous send is simpler.

## Related

- [[safe-failure-pattern]]: when a side-effect failure must not break the business operation
- [[operation-call-logging-interceptor]]: logging around operations that trigger notifications
- [[external-api-adapter-provider-pattern]]: wrapping a third-party SDK behind an adapter
- [[osgi-scheduled-background-jobs]]: the scheduled job framework that runs the delivery and cleanup jobs
