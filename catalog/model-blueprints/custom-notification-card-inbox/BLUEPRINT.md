---
id: custom-notification-card-inbox
title: Custom Notification Card Inbox Component
description: A custom notification inbox component that replaces the generated notifications data grid table with a card-based notification list.
aliases: []
keywords: [custom, notification, card, inbox, component]
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

A custom notification inbox component that replaces the generated notifications data grid table with a card-based notification list. Each notification is displayed as a compact card with type-specific icon, title, message (3-line clamp), relative timestamp (date-fns `formatDistanceToNow`), and a delete button. Tapping a notification navigates to the referenced feed entry's detail page. The component handles its own pagination via "Load more" button, notification deletion, and badge count synchronization.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
