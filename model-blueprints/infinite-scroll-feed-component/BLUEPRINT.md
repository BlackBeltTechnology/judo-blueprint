---
id: infinite-scroll-feed-component
title: "Infinite-Scroll Card-Based Feed Component"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A custom card-based social feed component that replaces the default generated data grid table with an infinite-scrolling, mobile-optimized feed. The component uses seek-based pagination (cursor-based, not offset-based) with IntersectionObserver for automatic load-more, supports multi-criteria filtering (post type, title, organization name, capability) via a SwipeableDrawer filter panel with chip bar, and renders color-coded feed entry cards with type indicator, organization link, validity dates, and capability tags. The feed includes a "Request Post" floating action button for authorized company roles.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
