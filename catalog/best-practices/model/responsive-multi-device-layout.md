---
id: responsive-multi-device-layout
title: Responsive Multi-Device Page Layout Pattern
description: "Responsive layout is expressed in the UI model through a 12-column grid (col spans per component); device variants of each page are an observation of generated UI models, not an authoring step."
aliases: [responsive layout, device containers, mobile tablet desktop layout, 12 column grid]
keywords: [responsive, layout, grid, col, 12 column, mobile, tablet, desktop, page container, breakpoint]
tags: ["domain:model", "layer:model", "project:actiongroup-test-react", "status:single-project"]
category: ui
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [action-group-conditional-enabling, ui-control-transfer-fields]
fragment: none: generated-ui-model, no entity or transfer shape
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Pages must work on phones, tablets and desktops. In JUDO this is handled in the UI model with a column grid and in the generated frontend with theme breakpoints, not with hand-written CSS per screen.

## Practice

### Author with the 12-column grid

The [UI authoring guide, Layout model](../../agent-docs/model/ui-authoring-guide.md) states that a 12-column grid applies to every component. A component's `col` is its column span (1 to 12; the validator enforces at most 12), `layout` on a container is `HORIZONTAL`, `VERTICAL` or default, and sibling `col` values in one horizontal row should sum to at most 12. A group with a vertical layout stacks children, so each child's `col` is its width. The same attributes appear in the [ui package reference](../../agent-docs/model/esm_metamodel/ui.md) (`Group`, `ActionGroup`, fields). Use a full row (12) for tables and long forms, 6 for two-up fields, 4 for three-up.

### Device variants are generated, not authored

The original project's UI model showed every page with four device containers: mobile (4 columns), tablet (8), desktop (12) and a default (12), where components keep their `col` on desktop and tablet and take full width on mobile. This is an observation from that project's generated UI model. The agent-docs do not describe device containers or per-device column counts, and the authoring guide describes a single set of `col` values per element. Treat the per-device structure as generator output: set sensible `col` values once and let the generator adapt.

### Handle the rest in the frontend

Breakpoints and adaptive behaviour belong to the theme and components of the generated React application (see [theming](../../agent-docs/frontend/theming.md): spacing, breakpoints, media queries). Customize there, not in the model.

## Rationale

- One grid vocabulary across all pages gives consistent breakpoints.
- No per-page CSS; layout intent stays in the model.
- Cost: the generated UI model is larger because structure is replicated per device, and per-device tuning requires theme or component customization, not a model attribute.

## Example

A neutral Order view page holds a group with horizontal layout containing two fields at `col` 6 and a table below at `col` 12. A group of action buttons uses `col` 6. The generated page shows the two fields side by side on wide screens and stacked on narrow ones. The original project had 31 pages built this way, including a Play God action group at `col` 6 across table, form, operation input and dashboard pages; this entry has no entity diagram because the shape is UI-only.

## When to avoid

- Pixel-exact layouts that the grid cannot express: customize the generated frontend instead.
- Assuming a model attribute for a per-device override: the agent-docs do not provide one.

## Related

- [[action-group-conditional-enabling]] — action groups that take grid columns
- [[ui-control-transfer-fields]] — UI state driven by model fields
