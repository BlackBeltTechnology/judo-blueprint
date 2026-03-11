---
id: "column-filter-provider-pattern"
title: "Column and Filter Definition Provider Pattern"
domain: "frontend"
category: "table"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

Extract table column definitions and filter option definitions into separate provider functions or custom hooks, keeping table page components focused on layout and data fetching. Column providers return `GridColDef[]` with i18n-aware header names, and filter providers return `FilterOption[]` with attribute names, labels, and filter types. Both accept `IntlShape` for localization. Providers can be standalone functions (in separate files) or returned from page-specific hooks.

## Structure

```typescript
// columnDefsProvider.ts
type ColumnDefsProvider = (intl: IntlShape) => GridColDef[];

export const getColumns: ColumnDefsProvider = (intl) => [
  {
    field: 'type',
    headerName: intl.formatMessage({ id: 'pages.galaxy.matter.table.type' }),
    sortable: false,
    width: 170,
  },
];

// filterOptionsProvider.ts
type FilterOptionsProvider = (intl: IntlShape) => FilterOption[];

export const getFilterOptions: FilterOptionsProvider = (intl) => [
  {
    attributeName: 'type',
    label: intl.formatMessage({ id: 'pages.galaxy.matter.table.type' }),
    filterType: FilterType.enumeration,
  },
];

// Page-specific hooks alternative
export const useGalaxiesTable = () => {
  const intl = useIntl();
  const columns: GridColDef[] = [/* ... */];
  const filterOptions: FilterOption[] = [/* ... */];
  return { columns, filterOptions, rowClickHandler };
};
```

## Examples

### ActionGroupTestReact
Galaxy Matter table uses standalone `columnDefsProvider.ts` and `filterOptionsProvider.ts` files. Galaxies table uses `useGalaxiesTable()` hook returning columns, filterOptions, and rowClickHandler. Galaxy View uses `useGalaxiesView()` hook returning nested columns (stars, astronomer) and query customizers. Both patterns co-exist in the same project.

## Trade-offs

- **Pros**: Separation of column/filter definitions from page logic; reusable across different table instances; testable in isolation; i18n-aware
- **Cons**: Extra files per table; provider pattern adds indirection; two approaches (files vs hooks) can be inconsistent
- **When to use**: Table pages with complex column definitions, multiple filter types, or shared column configurations

## Related Patterns

- [table-row-actions-utility](table-row-actions-utility.md)
- [session-storage-table-state](session-storage-table-state.md)
