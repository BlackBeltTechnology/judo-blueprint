---
id: "feed-denormalization-entity"
title: "Feed Denormalization Entity for Precomputed Views"
domain: "model"
category: "entity"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

A dedicated read-only entity stores denormalized copies of data from multiple source entities to enable fast feed/listing rendering without joins. The feed entity is system-managed (no CRUD), populated and synchronized by operations on the source entities, and includes all display-relevant attributes as flat fields. An optional reference to the source entity allows drill-down navigation.

## Structure

- Entity with `createable=false`, `updateable=false`, `deleteable=false` (system-managed)
- Denormalized attributes copied from multiple source entities (title, summary, authorName, organizationName, etc.)
- Classification enum for entry type (to distinguish content subtypes in the feed)
- Optional relation to the source entity (0..1) for detail navigation
- Optional relation to the owning organization (0..1) for filtering
- Empty string defaults on optional display fields to avoid NULL rendering issues
- A manual `syncFeed` operation may be provided for admin-triggered resynchronization
- Feed entries are created/updated/removed as side effects of source entity operations (publish, delete, edit)

## Examples

### MLSZKSZPlatform
`FeedEntry` entity denormalizes data from `Post` (via generalization: News, Offer, Request, Announcement) and `Organization`. Attributes: `entryType` (FeedEntryType enum: NEWS, OFFER, REQUEST, ANNOUNCEMENT), `contentId` (Long, default ""), `createdAt` (Timestamp), `title`, `summary`, `organizationName`, `authorName`, `capabilities`, `validFrom`, `validUntil`, `isSensitive`. Relations: `post [0..1]` (association to Post), `ownerOrganization [0..1]` (two-way with Organization). The `AdminDashboard.syncFeed` operation provides manual feed rebuild. Feed entries are created by `publish` operations and removed by `delete` operations on content entities.

## Trade-offs

- Pros: Fast feed rendering without joins, pre-computed display data, efficient pagination, search-optimized fields
- Cons: Data redundancy, must be kept synchronized with source entities, eventual consistency risk, storage overhead
- Prefer when: Application has a feed/timeline view that aggregates data from multiple entity types and requires high read performance

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md) (feed attributes are flattened from source entities)
- [category-enum-pattern](category-enum-pattern.md) (FeedEntryType classifies entries)
- [default-value-patterns](default-value-patterns.md) (empty string defaults for display fields)
