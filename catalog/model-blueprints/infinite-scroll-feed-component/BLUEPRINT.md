---
id: infinite-scroll-feed-component
title: Infinite-Scroll Card-Based Feed Component
description: "A custom card-based social feed component that replaces the default generated data grid table with an infinite-scrolling, mobile-optimized feed."
aliases: []
keywords: [infinite, scroll, card, based, feed, component]
tags: ["domain:model", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

A custom card-based social feed component that replaces the default generated data grid table with an infinite-scrolling, mobile-optimized feed. The component uses seek-based pagination (cursor-based, not offset-based) with IntersectionObserver for automatic load-more, supports multi-criteria filtering (post type, title, organization name, capability) via a SwipeableDrawer filter panel with chip bar, and renders color-coded feed entry cards with type indicator, organization link, validity dates, and capability tags. The feed includes a "Request Post" floating action button for authorized company roles.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
