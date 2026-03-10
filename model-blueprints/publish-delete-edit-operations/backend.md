## Overview

The publish/delete/edit operations are implemented as thin custom operation classes per content type, each delegating to the shared `PostLifecycleService` or `AnnouncementService`. The pattern is identical across News, Offer, Request, and Announcement, with content-type-specific variations for expire and moderationDelete.

## Implementation Pattern

- Each content type has 3-5 custom operation classes in its service package: `PublishCustomImplementation`, `DeleteCustomImplementation`, `EditXxxCustomImplementation`, and optionally `ExpiredCustomImplementation`, `ModerationDeleteCustomImplementation`
- Every operation class: (1) implements the generated operation interface, (2) is an OSGi `@Component`, (3) injects 1-2 services, (4) validates preconditions via the service layer, (5) logs an audit entry
- Publish: validates DRAFT status, sets PUBLISHED + publishedAt timestamp, creates FeedEntry, sends push/email notifications
- Delete: validates not already DELETED, hard-deletes DRAFT posts, soft-deletes PUBLISHED posts (sets DELETED status + removes FeedEntry)
- Edit: validates DRAFT status, updates fields from input TO, manages capability relations for Offer/Request
- Expire: validates PUBLISHED status, sets EXPIRED, removes FeedEntry; triggered both by custom operations and by the `PostExpirationJob` scheduler
- ModerationDelete: validates caller is PLATFORM_ADMIN via `ActorService`, sends notification to content owner, then performs soft-delete

## Examples

### mlszksz-platform
- Key files: `custom/.../companyadmin/offer/PublishCustomImplementation.java`, `custom/.../companyadmin/news/DeleteCustomImplementation.java`, `custom/.../companyadmin/request/EditRequestCustomImplementation.java`, `custom/.../companyadmin/offer/ModerationDeleteCustomImplementation.java`
- Pattern: 4 identical sets of custom operations (News, Offer, Request in companyadmin; Announcement in admin), each a thin delegate to PostLifecycleService/AnnouncementService + AuditLogService
- Notable: Hard vs soft delete distinction (DRAFT = physical delete, PUBLISHED = status transition to DELETED); moderation operations add authorization checks and owner notifications
