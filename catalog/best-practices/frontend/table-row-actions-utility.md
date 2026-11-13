---
id: table-row-actions-utility
title: Table Row Actions Utility with Configurable Display
description: "A project utility that builds a DataGrid action column from a list of row action definitions, with a setting for how many show as buttons and how many collapse into a dropdown."
aliases: [row action column, action column calculator]
keywords: [table, row actions, datagrid, action column, dropdown, utility, rowOperations]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: table
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [seek-based-table-pagination, session-storage-table-state, custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Tables with several row-level actions need one consistent action column whose density can be tuned per table: all buttons, one button plus a dropdown, or everything in a dropdown. This practice wraps that in one helper that turns a list of action definitions into a DataGrid column.

## Practice

### Platform base

- The generated React table is an MUI DataGrid. Row-level actions come from the model: row action definitions such as view, remove and delete (`*RowViewButton`, `*RowRemoveButton`, `*RowDeleteButton`) and custom operations placed in a table's `rowOperations` (`OperationFormTableRowCallOperationButton`). See [row actions](../../agent-docs/frontend/model-screen-layout.md) and [table operations](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md).
- The platform has a supported way to add or replace a single column on a generated table without replacing the table: a column customizer hook registered under `TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY` with the table component name and the column as service properties. Its documented example is an action button column with `renderCell` ([table hooks](../../agent-docs/frontend/hooks/table-hooks.md)).
- Hooks and custom code you add under `src/custom/` are not generated, so they survive regeneration ([extension points](../../agent-docs/frontend/extension-points.md)).

### Practice notes: configurable action column helper

This layer is custom code (a frontend that builds its own tables), not a platform feature. A helper takes an array of `{ label, action, icon }` definitions and returns a column definition, with a `shownActions` option:

- `0`: no action column
- `1`: every action in the dropdown
- `n` (2 or more): `n-1` standalone buttons, the rest in the dropdown
- `-1`: every action as a button

```typescript
// Example code, not a platform API
interface TableRowAction<R> {
  label: string;
  action: (row: R) => void;
  icon: ReactNode;
}

const rowActions: TableRowAction<OrderStored>[] = [
  { label: 'Delete', action: (row) => deleteRow(row), icon: <Delete /> },
  { label: 'Create item', action: (row) => navigate(`/${row.id}/createItem`), icon: <Icon /> },
];

const columns = [...baseColumns, ...columnsActionCalculator(rowActions, { shownActions: 1 })];
```

In one app, a table with four actions shows them all in the dropdown, while a table with a single Remove action shows it as a button.

## Rationale

One helper gives every table the same action column and one place to change spacing, icons or overflow behaviour. The dropdown keeps narrow tables usable when a row carries many actions.

Limits: the column has a fixed width that may not fit long labels, the dropdown adds a click, and the definitions carry no per-row visibility rule. Per-row visibility needs a condition added to the action definition or a derived boolean in the transfer object.

## Example

In one hand-built app the helper lives in a utilities file and builds the action column for the order table (Delete plus three create-item actions, `shownActions: 1`) and for the join table (one Remove action as a button).

When the generated table is kept, prefer model row actions and the column customizer hook. The helper fits a frontend that already builds its own DataGrids.

## When to avoid

- On generated tables: declare the row actions in the model, or use the column customizer hook for a single custom column.
- When actions must appear or disappear per row; model that with a derived boolean and a hidden-by rule instead.

## Related

- [[seek-based-table-pagination]] — pagination of the same DataGrid tables
- [[session-storage-table-state]] — persisted sort and filter state per table
- [[custom-visual-element-override]] — replacing a generated element instead of adding a column
