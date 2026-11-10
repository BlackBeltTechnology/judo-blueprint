---
id: notification-entity
title: Notification Entity with Status and Type Enums
description: "A non-CRUD Notification entity for one user, with a type enumeration, a delivery status enumeration and a reference to the content it is about."
aliases: [user notification, push notification record, notification inbox, read unread notification]
keywords: [notification, status, type, delivery, retry, reference, read, unread]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: notification-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Record each message sent to a user so the app can show an inbox, track delivery and retry failures. The rows are written by backend delivery code, not by users.

### Delivery state is an enumeration

Status moves from PENDING to SENT or FAILED. A retry job handles the FAILED and stuck PENDING rows. Keep the status as an enumeration so every query and retry rule uses the same values.

### The content is referenced, not owned

The notification stores a reference id to the content it is about. It does not hold the content, so a deleted post does not break the notification record.

## Structure

The Notification entity has a required type (NotificationType), title, created time and status (NotificationStatus), and optional message, reference id and retry count. It has one required association to User (1..1). The NotificationType enumeration lists ALERT, REMINDER and UPDATE. The NotificationStatus enumeration lists PENDING, SENT and FAILED.

## Constraints

- Createable, updateable and deleteable are all false on Notification, so the generated UI has no create, edit or delete controls.
- Type, title, created time, status and user are required.
- Status must be one of PENDING, SENT, FAILED.
- The retry count is written only by the retry logic in the backend.
- The reference id is a plain value. The entity has no relation to the referenced content.

## Variations

- **Separate device-delivery record.** Push delivery per device is tracked in a delivery entity, and the notification keeps only the overall status. Use this when one notification goes to many devices.
- **Event-composed notification.** The notification is created by a parent event entity and carries a boolean delivered flag and a read flag instead of a status enumeration. This suits an email-only channel with in-app read tracking.
- **Email-only channel.** Without push, drop the device entity and keep the same status rules for email.

## When to use

- A user needs an inbox of messages the system sent to them.
- Delivery must be tracked, and failed deliveries must be retried.
- Each message links to one piece of content.

## When to avoid

- Messages are not stored, only sent. Send them directly without a record.
- One notification must go to many recipients with its own state each. Use one row per recipient.
- Users must edit or delete the history. The entity is backend-owned by design.

## Related

- [[firebase-push-notification-pipeline]] — the push delivery pipeline that writes and retries these rows
- [[audit-log-entity]] — an append-only log of changes, not of messages sent to users
- [[multiple-choice-question-entity]] — another entity with a status enumeration
