---
id: table-row-highlighting-hook
title: Table Row Highlighting Hook for Conditional Colors
description: "Colour rows of a generated table by data values with the platform's table row highlighting hook, registered per table component."
aliases: [row colouring, conditional row colors]
keywords: [table, row highlighting, hook, conditional colors, TableRowHighlightingHook, pandino, application-customizer]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: table
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/TableRowHighlightingHooks/ratingTableHighlightHook.tsx", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/TableRowHighlightingHooks/offerItemsTableHighlightHook.tsx"]
alternatives: []
related: [pandino-action-hook-override, custom-visual-element-override, application-customizer-hub]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Rows of a table should be visually distinguished by an enum value, a status or a threshold, without editing the generated table. The platform offers a table row highlighting hook for exactly this; this practice describes how one frontend uses it.

## Practice

### Platform base

The hook is a platform extension point ([table hooks](../../agent-docs/frontend/hooks/table-hooks.md)):

- `TableRowHighlightingHook` and `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY` come from `~/theme/table-row-highlighting`.
- The hook is a function that returns a function that returns an array of rules. Each rule has `name`, `label` (legend text), `backgroundColor` and `condition`, a predicate over the grid row params (`params.row`).
- It is registered in `src/custom/application-customizer.tsx` with `registerService`, and the service property `component` is the generated table component name; read that name from the generated components under `src/containers`.
- The hook file you add in `src/custom/` is not generated, so it survives regeneration without `.generator-ignore` entries ([extension points](../../agent-docs/frontend/extension-points.md)).

```typescript
// Platform shape; the row type and enum come from the generated code
export const productHighlighting: TableRowHighlightingHook<ProductStored> = () => {
  return () => ([
    { name: 'row-physical', label: 'Physical', backgroundColor: '#0095ff',
      condition: (params) => params.row.productType === 'PHYSICAL' },
    { name: 'row-digital', label: 'Digital', backgroundColor: '#e88f00',
      condition: (params) => params.row.productType === 'DIGITAL' },
  ]);
};

context.registerService<TableRowHighlightingHook>(
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
  productHighlighting,
  { component: 'ProductTable' } // the generated table component name
);
```

### Practice notes: one hook per table, rules keyed by enum

This layer is practice:

- One hook per table, each registered with its own `component` so a rule set never leaks onto another table.
- Rules test an enum attribute of the row; a value without a rule stays unhighlighted (a rating table coloured green for the best grade and red for the worst, with the middle grade plain).
- Rule colours are written in the hook; the platform docs recommend theme palette colours over hard-coded hex where the theme has a matching one.

## Rationale

The hook changes only the background, so the generated table, its actions and its access rules stay untouched. The cost is that hex colours are duplicated in code and need review when the theme changes.

## Example

One app registers two hooks in `application-customizer.tsx`: the product table (blue for physical rows, orange for digital rows) and the partner rating table (green for the top grade, red for the lowest).

## When to avoid

- When the row needs more than a background (icons, badges, chips): use a column customizer hook for that column or a custom visual element.
- When the state is better shown by data: add a status column from the model and let the generated table render it.

## Related

- [[pandino-action-hook-override]] — the same registration mechanism for action hooks
- [[custom-visual-element-override]] — richer per-element rendering
- [[application-customizer-hub]] — where these registrations are collected
