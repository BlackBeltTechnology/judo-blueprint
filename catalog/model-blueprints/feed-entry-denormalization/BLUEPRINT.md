---
id: feed-entry-denormalization
title: Feed Entry Denormalization Entity
description: "A non-CRUD FeedEntry entity that copies display fields from several kinds of content (posts, announcements) into one flat row per item, so a feed can be read without joins, with targeting to specific organizations."
aliases: [feed row denormalization, flat feed entity]
keywords: [feed, entry, denormalization, targeting, flat, display, organization]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Render a feed of mixed content (announcements, news, offers, requests) with one query and no joins. Each feed row copies the display fields of its source item and records which organizations may see it. The source stays the authority for its own data.

### One flat row per item

The feed row holds a type discriminator, the id of the source item, the creation time and the display fields. The feed reads only this table.

### Targeting is stored on the row

The row links to its owning organization and to the organizations it is shown to. A feed for an organization is a filter on that link.

## Structure

The FeedEntry entity is not createable, updateable or deleteable, so the generated pages offer no such action (backend code still writes it through its data-access object). It has a required entry type (an enumeration of the content kinds), a required content id, and a required creation timestamp. It has display fields: title, summary, organization name, capabilities, author name, validity dates and a sensitivity flag. Its associations are an optional source post (0..1), a required owning organization (1..1), and the target organizations (0..*).

## Constraints

- Createable, updateable and deleteable are all false on the feed entry.
- The entry type, the content id and the creation timestamp are required.
- The display fields are copies. They are written when the row is created and refreshed when the source changes, so the feed never reads stale data for a changed title.
- Each row has exactly one owning organization.
- Interceptors run only for the platform's built-in operations, not for custom ones. A custom operation that publishes or removes content must update the feed in the same transaction.

## Variations

- **Strategy per content kind.** Each content kind has a targeting strategy. One strategy targets all active organizations. Another targets only organizations with matching capabilities.
- **Lifecycle-driven sync.** Rows are created when an item is published and removed when it is deleted or expires. The feed stays in step with the source.
- **Bulk re-synchronization.** A custom operation re-syncs all rows, for example after a new organization is created. Use it to repair drift, not as the normal path.
- **Typed navigation.** The row points to the source by content id and type. The client follows the type to the matching detail page.

## When to use

- A feed or list shows items of several kinds, and the list must load without joins.
- Each viewer sees a different subset of the items, decided by a targeting rule.
- Display fields change rarely, so a copy stays accurate with light sync.

## When to avoid

- The feed shows only one kind of item. Query that kind directly.
- Display fields change often and must always be current. Compute them on read instead; see [[derived-attribute-flattening]].
- The feed has no targeting and no need to be fast. A plain list is enough.

## Related

- [[derived-attribute-flattening]]: computing the display value on read instead of copying it
- [[audit-log-entity]]: another entity that copies names so a row stays readable after a change
- [[infinite-scroll-feed-component]]: the frontend feed that reads these rows
- [[event-log-entity]]: an event log entity that links to the affected entity
