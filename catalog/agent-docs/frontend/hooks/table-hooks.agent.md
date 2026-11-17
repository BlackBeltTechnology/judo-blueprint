# table-hooks.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/table-hooks.md.

## Overview
- Imports: `TableRowHighlightingHook` + key from `~/theme/table-row-highlighting`; `ColumnCustomizerHook`, `TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY`, `SidekickComponentProps` from `~/utilities`. No `~/generated` barrel.
- `component` service property = generated table component name (under `src/containers/**/components/`).
- Hook files under `src/custom/` are hand-written; no `.generator-ignore` entry needed.

## Table Row Highlighting
- Hook shape: `TableRowHighlightingHook<T> = () => () => Array<{ name, label, backgroundColor, condition(params) }>`; `params.row` = row data.
- Register: `registerService<TableRowHighlightingHook>(TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY, hook, { component: 'ServiceItemsTable' })`.
- Rules are multiple per hook; `condition` returns boolean. Examples: overdue (`new Date(row.dateField) < now && !row.completed`), same-day, `priorityLevel === 'HIGH'`, status equality, quality/coordinate null checks.
- Type with the entity: `<ServiceItemStored>` from `~/services/data-api/model/ServiceItem`.

## Custom Columns
- `ColumnCustomizerHook<T> = () => ColumnCustomizer<T>`; `ColumnCustomizer<T> = (original: GridColDef<T>) => GridColDef<T>`.
- Consumed only for columns whose `DataColumn` has `customImplementation=true`; matched by `component` + `column` service properties.
- Register: `TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY`, `{ component: 'ServiceLocationsTable', column: 'qualityScore' }`.
- Examples (MUI DataGrid `renderCell`): Chip status by value; action button (e.g. open Google Maps, disable when null coords); LinearProgress with percentage (guard total=0); computed days-until Chip (error <0, warning ≤3, success ≤7).
- Use `{...original, ...}` to keep generated defaults; `sortable:false`/`filterable:false` to disable.

## Sidekick Components
- Sidekick = custom visual element above table, within table container.
- Register under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (from `~/custom`), property `component` = per-table `<TABLE>_SIDEKICK_COMPONENT_INTERFACE_KEY` exported by the generated table component (value `'<componentName>SidekickComponent'`).
- Find key: `grep -rn "_SIDEKICK_COMPONENT_INTERFACE_KEY =" src/containers`.
- Props `SidekickComponentProps<T>` (`~/utilities`): `data`, `editMode`, `isLoading`, `filters`, `onFiltersChange`; plus `filterModel`/`onFilterModelChange` when inline column filters are on. Use `onFiltersChange` to drive table filters.
- Examples: summary counts; stats cards with `useMemo`; quick-filter ToggleButtonGroup (note: example doesn't wire to table); recharts PieChart of status counts.

## Column Width and Order
- Width: `{...original, width: 300}` or `flex: 1`.
- Hide: `hide: true`.
- Non-sortable: `sortable: false, filterable: false`.

## Best Practices
- Type hooks with the entity type (`TableRowHighlightingHook<ServiceEntityStored>`), not untyped.
- `useMemo` for computed stats in sidekicks; don't recompute each render.
- Null-check values in `renderCell` (`No Location` chip when coordinates missing).
- Keep hook files under `src/custom/` (only `.default` twins are generated).
- Use theme colours (`theme.palette.error.light`) over hardcoded hex.

## Complete Example
- One `customize(context)` registering: row highlighting (`TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY`), column customizer (`TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY`, `column` property), sidekick (`CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with generated sidekick key).

## Troubleshooting
- Highlighting not applying: log `params.row` in `condition`; verify component name (`grep -rn "component=" src/containers/components`, or check generated table component name).
- Custom column not showing: check `TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY` registration with matching `component` and `column`.
- Sidekick not rendering: log `data` prop.

## Related Documentation
- `README.md`, `data-hooks.md`, `ui-hooks.md`, `action-hooks.md`, `../development-workflow.md`.
