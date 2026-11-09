---
id: custom-statistics-dashboard
title: Custom Statistics Dashboard with KPI Cards
description: "A custom admin statistics dashboard that replaces the generated form layout with a rich visual dashboard featuring KPI cards, pending action indicators, content breakdown by type, user visibility metrics, and a sortable organization stat..."
aliases: []
keywords: [custom, statistics, dashboard, kpi, cards]
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

A custom admin statistics dashboard that replaces the generated form layout with a rich visual dashboard featuring KPI cards, pending action indicators, content breakdown by type, user visibility metrics, and a sortable organization statistics table. The dashboard is rendered both as a standalone view page and inline within the AdminDashboard's analytics tab. Implemented via Pandino custom visual element registration for the statistics component and page action hooks for data fetching.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
