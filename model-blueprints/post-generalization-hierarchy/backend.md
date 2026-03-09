## Overview

The abstract Post entity and its concrete subtypes (News, Offer, Request, Announcement) are managed through a layered service architecture: `PostService` (facade), `PostCreationService` (factory operations), and `PostLifecycleService` (state transitions). Each subtype has separate custom operation classes that delegate to these shared services.

## Implementation Pattern

- `PostServiceImpl` is a facade OSGi `@Component` that delegates to `PostCreationService` and `PostLifecycleService`
- `PostCreationServiceImpl` handles `createNews()`, `createOffer()`, `createRequest()`: sets common Post fields (title, description, status=DRAFT, createdAt, postType discriminator, author, organization) then adds subtype-specific fields (image for News, validFrom/validUntil/price/capabilities for Offer, deadline/capabilities for Request)
- `PostLifecycleServiceImpl` handles publish/delete/expire/edit: validates state preconditions, updates status, and triggers side effects (FeedService for feed entry management, PushNotificationService for push, PlatformEmailService for email)
- Delete behavior is differentiated: DRAFT/PENDING_REVIEW posts are hard-deleted; PUBLISHED posts are soft-deleted (status=DELETED) with feed entry removal
- The `adaptTo(Post.class)` method is used to upcast subtypes to the abstract Post type when creating feed entries
- Capability relations on Offer and Request are managed via DAO `addCapabilities()`/`removeCapabilities()` methods
- Scheduler `PostExpirationJob` queries PUBLISHED offers with expired `validUntil` and requests with expired `deadline`, auto-expiring them

## Examples

### mlszksz-platform
- Key files: `common/services/PostService.java`, `common/services/post/PostCreationService.java`, `common/services/post/PostLifecycleService.java`, `common/services/post/impl/PostLifecycleServiceImpl.java`, `scheduler/PostExpirationJob.java`
- Pattern: Facade + creation service + lifecycle service; creation sets DRAFT status with PostType discriminator; publish transitions to PUBLISHED and creates FeedEntry; delete is soft (PUBLISHED) or hard (DRAFT)
- Notable: PostExpirationJob automatically expires time-sensitive content (Offers by validUntil, Requests by deadline); `adaptTo(Post.class)` enables polymorphic feed entry creation from any subtype
