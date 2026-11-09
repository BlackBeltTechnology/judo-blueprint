## Overview

FeedEntry entities are created and managed by a `FeedService` OSGi service that synchronizes denormalized feed entries with post lifecycle transitions. When a post is published, a FeedEntry is created with denormalized fields (title, summary, organizationName, etc.). When a post is deleted or expired, the corresponding FeedEntry is removed. A `syncAllFeed` operation allows bulk re-synchronization of feed entries across all active organizations.

## Implementation Pattern

- A `FeedService` interface defines overloaded `createFeedEntry()` methods for each post subtype (Announcement, News, Offer, Request) and corresponding `deleteFeedEntry()` methods
- Feed entry creation denormalizes post data into flat attributes (title, summary, organizationName, capabilities, authorName) and sets the `entryType` discriminator
- Organization targeting: each FeedEntry links to `ownerOrganization` (1..1) and `targetOrganizations` (0..*) using targeting strategies
- Two targeting strategies via `FeedTargetingStrategy` interface: `AllActiveOrganizationsTargetingStrategy` (for News, Offers, Announcements) and `RequestTargetingStrategy` (for Requests -- only organizations with matching capabilities)
- `syncAllFeed()` iterates all feed entries and adds organizations created after the entry's publish date, respecting targeting rules
- `syncFeedForOrganization()` syncs a single new organization into all applicable existing feed entries
- The `SyncFeedCustomImplementation` custom operation on AdminDashboard triggers `feedService.syncAllFeed()`
- The Initializer creates initial FeedEntry records during data seeding for test data

## Examples

### mlszksz-platform
- Key files: `common/services/FeedService.java`, `common/services/feed/FeedTargetingStrategy.java`, `common/services/feed/AllActiveOrganizationsTargetingStrategy.java`, `common/services/feed/RequestTargetingStrategy.java`, `custom/.../admindashboard/SyncFeedCustomImplementation.java`
- Pattern: Lifecycle-driven denormalization -- feed entries are created when posts are published and removed when posts are deleted/expired, keeping the feed always in sync
- Notable: Strategy pattern for organization targeting; Request entries only target organizations with matching capabilities while other post types target all active organizations
