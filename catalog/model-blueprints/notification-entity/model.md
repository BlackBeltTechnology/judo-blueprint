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
