---
id: table-row-highlighting-hook
title: Table Row Highlighting Hook for Conditional Colors
description: "Apply conditional background colors to table rows based on data values using the `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY` Pandino service."
aliases: []
keywords: [table, row, highlighting, hook, conditional, colors]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: table
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Apply conditional background colors to table rows based on data values using the `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY` Pandino service. Each hook returns an array of highlighting rules with a name, background color, and boolean condition evaluated per row. Multiple rules can be defined per table, and each rule targets a specific data condition.

## Structure

```typescript
// Hook implementation
const highlightHook = (row: RowType) => [
  {
    name: 'fq-row-theme-material',
    backgroundColor: '#0095ff',
    condition: row.itemType === ItemType.MATERIAL,
  },
  {
    name: 'fq-row-theme-service',
    backgroundColor: '#e88f00',
    condition: row.itemType === ItemType.SERVICE,
  },
];

// Registration in application-customizer.tsx
context.registerService(
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
  highlightHook,
  { component: 'ServicesEntityEntity_View_EditTableComponent' }
);
```

## Examples

### RackInspect
Two highlighting hooks: (1) Offer items table uses blue (`#0095ff`) for MATERIAL rows and orange (`#e88f00`) for SERVICE rows. (2) Partner ratings table uses green (`#00cc00`) for RatingResult.A (excellent) and red (`#cc0000`) for RatingResult.C (non-acceptable), with no highlight for RatingResult.B.

## Trade-offs

- **Pros**: Non-invasive visual enhancement; no generated code modification; clear data-driven styling rules
- **Cons**: Limited to background color; more complex styling (icons, badges) requires custom visual element override; colors are hardcoded
- **When to use**: When table rows need visual differentiation based on enum values, status, or data thresholds

## Related

- [[pandino-action-hook-override]]
- [[custom-visual-element-override]]

