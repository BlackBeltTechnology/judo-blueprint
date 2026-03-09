---
id: "notification-entity"
title: "Notification Entity with Status and Type Enums"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A Notification entity for tracking push/email notifications sent to users. It carries a type (enum distinguishing what triggered the notification), a title and message for display, a status enum (PENDING/SENT/FAILED) for delivery tracking, a referenceEntityId to link back to the triggering entity, a createdAt timestamp, and a retryCount for failed delivery attempts. The entity associates to a User (1..1). A companion Device entity tracks user device registrations (FCM tokens, platform type, active status) for push notification delivery. Both are typically non-CRUD, managed by backend services.

Some variants (e.g., kozut-eugyfel-client) use a simpler approach: the notification is composed by a parent Event entity rather than existing independently, carries a boolean delivery status (kezbesitve/delivered) instead of a status enum, and adds derived attributes to flatten the parent event's data (bejelentesAzonosito, idopont, esemenyTipus, kezdemenyezoNev). This variant also adds an `olvasott` (read) boolean and an `elolvas` (markRead) operation for in-app read tracking.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
