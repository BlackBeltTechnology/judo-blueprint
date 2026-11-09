---
id: cards-container-configuration-hook
title: "Cards Container Configuration Hook (Custom Card Layout)"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - park-here
---

## Description

A frontend-only pattern for replacing the default data grid table rendering with a responsive card-based layout using the `CardsContainerConfigHook` Pandino hook. Each table/relation component in JUDO generates a `*_CARDS_CONTAINER_CONFIG_HOOK_INTERFACE_KEY` that allows registering a hook returning a custom `CardElement` FC component (and optionally `ToolbarElement`, `ActionbarElement`, `layout`, and `showPagination` overrides). The custom `CardElement` receives `row`, `columns`, `onRowClick`, and `actions` props, and must be wrapped in a `<Grid item>` with responsive breakpoints (`xs`, `sm`, `md`, `lg`, `xl`) to control card sizing. This pattern is distinct from full custom component replacement (`CUSTOM_COMPONENT_HOOK_INTERFACE_KEY`) -- it works within the existing `CardsContainer` infrastructure, only swapping the card rendering while preserving pagination, filtering, and data fetching. It is commonly used to display relation data as visually rich cards with icons, timelines, images, and action buttons instead of flat table rows.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
