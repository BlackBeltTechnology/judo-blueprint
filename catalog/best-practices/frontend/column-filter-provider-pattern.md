---
id: column-filter-provider-pattern
title: Column and Filter Provider Pattern
description: In a hand-written table page, column definitions and filter options are extracted into provider functions or page hooks that take the localization object, so the page keeps only layout and data fetching.
aliases: [column definitions provider, filter options provider]
keywords: [table, column, filter, provider, GridColDef, FilterOption, i18n, hook, data grid]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: table
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [table-row-actions-utility, session-storage-table-state]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Table pages with many columns and filter types get cluttered when definitions sit next to layout and fetching code. Moving them into small providers keeps pages short and lets definitions be reused and tested alone.

## Practice

### Platform base

- In the generated frontend, columns and filters come from the UI model: a table's columns (`DataColumn`) carry label, width or flex, sortable, filterable, hidden, default sort and alignment, and its filters (`DataFilter`) carry label, bound attribute and filter operation type ([tables and navigation mapping](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)). Change them in the model first.
- Per-column adjustments that the model cannot express go through column customizer hooks, which return a customizer that receives the original column definition and returns a changed one (width, hidden, not sortable) ([column width and order](../../agent-docs/frontend/hooks/table-hooks.md)); see also [table column customization](../../agent-docs/frontend/advanced-patterns.md).
- Provider functions are only needed in a hand-written table page. With the generated tables, hooks and the model already do this job.

### Practice notes: providers for columns and filters

This layer is practice, not a platform feature:

- A column provider takes the localization object and returns the column definitions with translated header names; a filter provider returns filter options with attribute name, translated label and filter type.
- Two forms can coexist in one frontend: standalone provider files for a simple table, and a page-specific hook that returns columns, filter options and the row click handler (the view page hook also returns nested columns and query customizers).
- Choose one form per frontend to avoid inconsistency.

```typescript
// Example code: types and ids are illustrative
type ColumnDefsProvider = (intl: IntlShape) => GridColDef[];

export const getColumns: ColumnDefsProvider = (intl) => [
  { field: 'type', headerName: intl.formatMessage({ id: 'pages.item.table.type' }), sortable: false, width: 170 },
];

export const useItemsTable = () => {
  const intl = useIntl();
  return { columns: getColumns(intl), filterOptions: getFilterOptions(intl), rowClickHandler };
};
```

## Rationale

Definitions are separated from page logic, reusable across table instances, testable and localization-aware. The cost: extra files per table, some indirection, and inconsistency when both forms are mixed.

## Example

One app uses standalone column and filter provider files for the line-item table of an order, a table hook for the orders list, and a view hook for the order view with nested product and customer columns plus query customizers. Both forms live side by side.

## When to avoid

- You use the generated tables: configure columns and filters in the model and adjust single columns with a column customizer hook.
- A table has only a few simple columns and no filters.

## Related

- [[table-row-actions-utility]] — row actions for the same tables
- [[session-storage-table-state]] — persisting sort and filter state
