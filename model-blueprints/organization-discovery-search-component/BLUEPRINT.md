---
id: organization-discovery-search-component
title: "Organization Discovery Search Component"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A custom organization discovery/search component that replaces the generated data grid table with a filterable, infinite-scrolling card-based directory. Organizations are displayed as cards with logo avatar, name, address, contact info, and capability tags. The component supports filtering by organization name, address, and capability (with server-side autocomplete), and only shows ACTIVE organizations. Uses the same infinite scroll and filter drawer patterns as the feed component but is purpose-built for organization search with different card layout and filter criteria.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
