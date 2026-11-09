## Overview

The content lifecycle status enums (PostStatus, AnnouncementStatus) drive status transitions implemented in custom backend operations. Each transition (publish, delete, expire, moderationDelete) is a separate custom operation class that delegates to a shared `PostService` or `AnnouncementService`, which handle the actual status field updates and side effects (feed entry creation/deletion, notifications).

## Implementation Pattern

- Each content type (News, Offer, Request, Announcement) has a set of custom operation classes: `PublishCustomImplementation`, `DeleteCustomImplementation`, `EditXxxCustomImplementation`, and optionally `ExpiredCustomImplementation` and `ModerationDeleteCustomImplementation`
- These classes are OSGi `@Component` instances implementing generated operation interfaces (e.g., `Publish`, `Delete`, `Expired`)
- All delegate to either `PostService` (for News/Offer/Request subtypes) or `AnnouncementService` (for Announcements)
- The service layer performs the actual status transition: setting status to PUBLISHED/DELETED/EXPIRED, updating `publishedAt` timestamp, and triggering feed entry creation/removal via `FeedService`
- Every status transition also logs an audit entry via `AuditLogService`
- ModerationDelete operations add authorization checks (validates PLATFORM_ADMIN role) and send push/email notifications to affected company admins

## Examples

### mlszksz-platform
- Key files: `custom/.../companyadmin/offer/PublishCustomImplementation.java`, `custom/.../companyadmin/offer/DeleteCustomImplementation.java`, `custom/.../companyadmin/offer/ExpiredCustomImplementation.java`, `custom/.../companyadmin/offer/ModerationDeleteCustomImplementation.java`, `custom/.../admin/announcement/PublishCustomImplementation.java`
- Pattern: Thin operation classes delegate to `PostService`/`AnnouncementService` for status transitions, then call `AuditLogService.log()` with the appropriate `AuditActionType`
- Notable: ModerationDelete validates `UserRole.PLATFORM_ADMIN` via `ActorService`, sends push notifications via `PushNotificationService`, and emails via `PlatformEmailService` before deleting
- The same publish/delete/edit/expire pattern is repeated identically across News, Offer, and Request in the `companyadmin` package
