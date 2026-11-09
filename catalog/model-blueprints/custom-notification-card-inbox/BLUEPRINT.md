---
id: custom-notification-card-inbox
title: "Custom Notification Card Inbox Component"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A custom notification inbox component that replaces the generated notifications data grid table with a card-based notification list. Each notification is displayed as a compact card with type-specific icon, title, message (3-line clamp), relative timestamp (date-fns `formatDistanceToNow`), and a delete button. Tapping a notification navigates to the referenced feed entry's detail page. The component handles its own pagination via "Load more" button, notification deletion, and badge count synchronization.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
