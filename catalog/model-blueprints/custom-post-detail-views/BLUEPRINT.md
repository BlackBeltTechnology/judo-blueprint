---
id: custom-post-detail-views
title: "Custom Post Detail View Components"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A set of custom view components that replace generated container layouts for post detail pages (News, Offer, Request, Announcement) and related entities (Organization, ProfilePanel). Each view provides a mobile-optimized, read-only layout with a shared `PostViewLayout` wrapper that adds a type-colored left border accent. The views integrate organization cards with contact actions (email/phone links), image downloads via binary token, and "Interest" buttons for offers/requests. These are registered as Pandino container hooks that replace the default generated container components.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
