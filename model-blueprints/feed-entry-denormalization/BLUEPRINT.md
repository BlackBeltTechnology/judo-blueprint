---
id: "feed-entry-denormalization"
title: "Feed Entry Denormalization Entity"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A FeedEntry entity that denormalizes content from multiple source types (posts, announcements) into a flat structure optimized for feed display. It stores: entryType (discriminator for what kind of content), contentId (reference to original entity), createdAt, and denormalized display fields (title, summary, organizationName, capabilities, authorName, validUntil, validFrom, isSensitive). Relations link back to the source post (0..1), the ownerOrganization (1..1), and targetOrganizations (0..*) for targeted content. This pattern avoids expensive joins when rendering feeds and supports content targeting to specific organizations.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
