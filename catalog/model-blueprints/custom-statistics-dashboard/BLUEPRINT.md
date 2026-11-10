---
id: custom-statistics-dashboard
title: Custom Statistics Dashboard with KPI Cards
description: Replace the generated statistics panel of an admin dashboard with a custom visual that shows KPI cards, pending-action counters, content breakdowns and a sortable organization table.
aliases: [statistics dashboard, KPI dashboard, admin analytics panel]
keywords: [custom, statistics, dashboard, kpi, cards, admin, analytics]
tags: [domain:frontend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: [mlszksz-platform:unrecorded]
alternatives: []
related: [custom-post-detail-views, interceptor-derived-statistics-calculation, custom-notification-card-inbox]
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---

## Intent

### Statistics panel as a custom visual

Replace the generated statistics panel of an admin dashboard with a custom visual. The visual summarises users, organizations, pending requests and content in one view. It can be shown as a standalone page and embedded in a dashboard tab with the same presentation.

## Structure

The custom visual is a presentation component fed by a small data wrapper. The presentation shows:

- KPI cards for total users, active users (last 30 days), active organizations and total content.
- Pending-action counters for organization requests and user invitations, highlighted when non-zero.
- A content breakdown by type with an all-time total and a 30-day count per type.
- A user visibility split (hidden against visible) with percentages.
- A sortable table of organization statistics.

No entity or attribute is added, but the statistics panel must be declared in the UI model as a custom implementation element so that it can be replaced. The numbers come from an existing read operation whose returned shape includes the nested organization statistics.

## Constraints

- The custom visual receives the same data the generated panel receives. The fetch shape has to include the nested organization statistics.
- The presentation component is pure. Sorting of the organization table happens on the loaded rows, on the client.
- The statistics are computed by the backend. The frontend only renders them.

## Variations

- **Standalone page or tab**: one presentation component, two hosts. The tab host fetches its own data so it works without the page's data context.
- **Frame removal**: when the custom visual sits inside a generated card, the card frame can be removed with a style override on the section.

## When to use

- The admin dashboard needs a layout (cards, counters, tables) that the generated statistics panel cannot express.
- Several counters must be shown together with a sortable breakdown.

## When to avoid

- Only a handful of numbers are needed; the generated panel is enough.
- The organization list is too large for client-side sorting. Sort and page on the backend instead.

## Related

- [[custom-post-detail-views]] — another custom view that replaces a generated page
- [[interceptor-derived-statistics-calculation]] — where the counters can be computed on the backend
- [[custom-notification-card-inbox]] — a card-based custom view with a similar layout approach
