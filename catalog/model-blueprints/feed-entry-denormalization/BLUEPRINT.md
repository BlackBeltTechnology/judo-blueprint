---
id: feed-entry-denormalization
title: Feed Entry Denormalization Entity
description: "A FeedEntry entity that denormalizes content from multiple source types (posts, announcements) into a flat structure optimized for feed display."
aliases: []
keywords: [feed, entry, denormalization]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A FeedEntry entity that denormalizes content from multiple source types (posts, announcements) into a flat structure optimized for feed display. It stores: entryType (discriminator for what kind of content), contentId (reference to original entity), createdAt, and denormalized display fields (title, summary, organizationName, capabilities, authorName, validUntil, validFrom, isSensitive). Relations link back to the source post (0..1), the ownerOrganization (1..1), and targetOrganizations (0..*) for targeted content. This pattern avoids expensive joins when rendering feeds and supports content targeting to specific organizations.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
