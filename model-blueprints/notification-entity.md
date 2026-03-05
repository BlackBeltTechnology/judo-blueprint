---
id: notification-entity
title: "Notification Entity with Status and Type Enums"
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - kozut-eugyfel-client
---

## Description

A Notification entity for tracking push/email notifications sent to users. It carries a type (enum distinguishing what triggered the notification), a title and message for display, a status enum (PENDING/SENT/FAILED) for delivery tracking, a referenceEntityId to link back to the triggering entity, a createdAt timestamp, and a retryCount for failed delivery attempts. The entity associates to a User (1..1). A companion Device entity tracks user device registrations (FCM tokens, platform type, active status) for push notification delivery. Both are typically non-CRUD, managed by backend services.

Some variants (e.g., kozut-eugyfel-client) use a simpler approach: the notification is composed by a parent Event entity rather than existing independently, carries a boolean delivery status (kezbesitve/delivered) instead of a status enum, and adds derived attributes to flatten the parent event's data (bejelentesAzonosito, idopont, esemenyTipus, kezdemenyezoNev). This variant also adds an `olvasott` (read) boolean and an `elolvas` (markRead) operation for in-app read tracking.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Notification" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Ertesites%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "NotificationType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::NotificationType", name: "{{NOTIFICATION_TYPE}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "NotificationStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::NotificationStatus", name: "PENDING", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::NotificationStatus", name: "SENT", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::NotificationStatus", name: "FAILED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Notification",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "title"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "referenceEntityId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Notification", name: "retryCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Notification", name: "user",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Notification entity**: `MLSZKSZPlatform::entities::Notification`
  - Attributes: type (req), title (req), message, status (req), referenceEntityId, createdAt (req), retryCount
  - Relations: user (1..1 ASSOCIATION)
- **NotificationType enum**: `MLSZKSZPlatform::types::NotificationType` -- NEW_POST(0), NEW_ANNOUNCEMENT(1), INQUIRY_RECEIVED(2), REGISTRATION_APPROVED(3), REGISTRATION_REJECTED(4), INVITATION_RECEIVED(5), INVITATION_APPROVED(6), INVITATION_REJECTED(7)
- **NotificationStatus enum**: `MLSZKSZPlatform::types::NotificationStatus` -- PENDING(0), SENT(1), FAILED(2)
- **Device entity**: `MLSZKSZPlatform::entities::Device`
  - Attributes: fcmToken (req), platform (req, DevicePlatform enum), isActive (req), lastUsedAt, registeredAt (req)
  - Relations: user (1..1 ASSOCIATION)
- **DevicePlatform enum**: `MLSZKSZPlatform::types::DevicePlatform` -- ANDROID(0), IOS(1), WEB(2)

### kozut-eugyfel-client
- **Ertesites (Notification) entity**: `e_ugyfelszolgalat::entities::Ertesites`
  - Attributes: kezbesitve (delivered, boolean), szoveg (text/message), targy (subject), olvasott (read, req boolean), plus DERIVED attributes flattened from parent event: cimzettEmail (recipient email), bejelentesAzonosito (report ID), idopont (timestamp), kezdemenyezoNev (initiator name), esemenyTipus (event type)
  - Relations: cimzett (recipient 1..1 TwoWay ASSOC to Felhasznalo), bejelentes (report 0..1 DERIVED ASSOC to Bejelentes)
  - Operations: elolvas (markRead, instance operation)
- **No NotificationType or NotificationStatus enums** -- the notification type is derived from the parent Esemeny's esemenyTipus attribute, and delivery status is a simple boolean (kezbesitve) rather than a tri-state enum
- Ertesites entities are COMPOSED by their parent Esemeny (Event) entity via `ertesitesek` (0..* COMPOSITION)
- The Felhasznalo (User) entity has a `ertesitesek` (notifications 0..*) TwoWay ASSOC relation
- An `EmailKuldo` (EmailSender) unmapped TO references `kezbesitetlenErtesitesek` (undelivered notifications 0..* AGGREGATION) for batch email sending
- **Transfer Objects**:
  - `munkatars::Ertesites` -- bejelentesAzonosito, cimzettEmail, esemenyTipus, idopont, kezbesitve, kezdemenyezoNev, szoveg, targy + bejelentes (0..1 ASSOC) relation + elolvas (MAPPED) operation
- **Key differences from mlszksz-platform**:
  - Composed by Event entity (event-driven notification creation) rather than independently created
  - Simple boolean delivery status instead of tri-state enum
  - Adds in-app read tracking (olvasott flag + elolvas operation) alongside email delivery tracking (kezbesitve)
  - Notification content (subject, text) is stored directly rather than using a type enum for template selection
  - No Device entity -- notifications are email-only, no push notification infrastructure
