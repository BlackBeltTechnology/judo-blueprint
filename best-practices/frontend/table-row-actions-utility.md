---
id: "table-row-actions-utility"
title: "Table Row Actions Utility with Configurable Display"
domain: "frontend"
category: "table"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

A utility function `columnsActionCalculator()` that generates a DataGrid action column from an array of `TableRowAction` definitions. Each action has a label, icon, and callback. The `shownActions` option controls how many actions appear as standalone buttons versus being collected into a dropdown menu. This creates a consistent action column pattern across all tables with configurable density.

## Structure

```typescript
interface TableRowAction<R> {
  label: string;
  action: (row: R) => void;
  icon: ReactNode;
}

interface ColumnsActionsOptions {
  shownActions?: number;  // -1: all buttons, 0: none, 1: all in dropdown, n: n-1 buttons + dropdown
  showLabel?: boolean;
}

// Usage
const rowActions: TableRowAction<ViewGalaxyStored>[] = [
  { label: 'Delete', action: (row) => deleteRow(row), icon: <Delete /> },
  { label: 'Create Dark Matter', action: (row) => navigate(`/${row.id}/createDarkMatter`), icon: <Icon /> },
];

const columns = [...baseColumns, ...columnsActionCalculator(rowActions, { shownActions: 1 })];
```

Display modes: `shownActions: 0` (hidden), `1` (all in dropdown), `2` (1 button + dropdown), `n` (n-1 buttons + dropdown), `-1` (all as buttons).

## Examples

### ActionGroupTestReact
`columnsActionCalculator()` in `src/utilities/table_row_actions.tsx` generates action columns. Galaxies table has 4 row actions (Delete + 3 matter creation actions) with `shownActions: 1` (all in dropdown). Galaxy Matter table has 1 row action (Remove) shown as a button. DropdownButton renders overflow actions with icon + label menu items.

## Trade-offs

- **Pros**: Consistent action column pattern across tables; configurable density; supports icon + label; handles overflow gracefully
- **Cons**: Fixed column width may not fit all labels; dropdown adds click overhead; no per-row action visibility control
- **When to use**: Any DataGrid table that needs row-level actions (delete, navigate, custom operations)

## Related Patterns

- [seek-based-table-pagination](seek-based-table-pagination.md)
- [session-storage-table-state](session-storage-table-state.md)
