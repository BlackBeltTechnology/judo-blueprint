## Overview

The AdminDashboard transfer object serves as the central hub for admin operations. Its custom operations (createOrganization, createAnnouncement, createCity, createCapability, syncFeed, inviteBulk, exportAuditLog) are each implemented as separate OSGi `@Component` classes that delegate to shared service layers and log audit entries.

## Implementation Pattern

- Each dashboard operation is a separate `@Component` class implementing a generated operation interface (e.g., `CreateOrganization`, `SyncFeed`, `ExportAuditLog`)
- Operations receive the `AdminDashboard` transfer object as `_this` parameter plus an input TO
- Each class injects 1-2 shared services (e.g., `OrganizationService`, `MasterDataService`, `FeedService`, `AdminInvitationService`) plus `AuditLogService`
- The operation class is a thin delegation layer: validate input, call service, log audit entry
- Some operations (like `CreateAnnouncementCustomImplementation`) also inject `ActorService` to resolve the current user's organization context
- The `ExportAuditLog` operation is the most complex: it queries `AuditLogDao`, builds CSV, and stores via `FileStoreService`

## Examples

### mlszksz-platform
- Key files: `custom/.../admindashboard/CreateOrganizationCustomImplementation.java`, `custom/.../admindashboard/SyncFeedCustomImplementation.java`, `custom/.../admindashboard/ExportAuditLogCustomImplementation.java`, `custom/.../admindashboard/InviteBulkCustomImplementation.java`
- Pattern: 7 custom operation classes in the `admindashboard` package, each delegating to a dedicated service (OrganizationService, MasterDataService, FeedService, AdminInvitationService, AnnouncementService)
- Notable: `SyncFeedCustomImplementation` triggers a full feed synchronization via `FeedService.syncAllFeed()`; `ExportAuditLogCustomImplementation` generates CSV with date filtering, UTF-8 BOM for Excel compatibility, and `FileStoreService` persistence
