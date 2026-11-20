# action-hooks.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/action-hooks.md.

## Overview

- Action hooks customize container actions (form/table ops), page actions (custom buttons), operation flow, and enumeration filtering.

## Container Actions

- Key `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY`; type `<Container>ContainerHook`, in `~/containers/<path>/customization`. Example container `ServiceEntityViewEdit`. No generic `CONTAINER_HOOK_INTERFACE_KEY`.
- Scaffold `src/custom/hooks/containers/register<Container>ActionsHook.ts.default` has correct imports and `registerService` call; copy it.
- Hook signature `(data, editMode, storeDiff)`; returned handlers must match the generated action type (check `customization.ts` and `types.ts`). Handler names in examples (`onSave`, `onBeforeSave`, `onAfterSave`, `onBeforeDelete`, `onAfterDelete`, `filter...Options`, `get...Options`) are illustrative.
- Register from `application-customizer.tsx` via `registerServiceEntityViewEditActionsHook(context)`, which calls `context.registerService(KEY, hook)`.
- Throw to cancel: throwing in `onBeforeSave` / `onBeforeDelete` prevents the default action.
- Real examples: validate date range and duplicates in `onBeforeSave`; confirm delete when items exist in `onBeforeDelete`; notify and navigate in `onAfterSave` / `onAfterDelete`.

## Enumeration Filtering

- Filter dropdown options from form state: `filterUserOptions(formData, options)` returns filtered array.
- Cascading: `filterRegionOptions` by `formData.country.__identifier`; `filterCityOptions` returns `[]` when no region.
- Role-based: use `usePrincipal()` roles (`ADMIN`, `MANAGER`) to filter options.

## Typeahead/Autocomplete

- Handler `get<Field>Options(searchText)` returns options; short-circuit below a min length (2-3 chars).
- API-based: `context.actions.getRangeAction('<relation>')({ query, page: 0, size })`, then map `{ label, value: __identifier }`. Use `getRangeAction` from context, not direct fetch.
- Debounce: lodash `debounce` returns the LAST completed result and `undefined` while pending. Treat `undefined` as no suggestions (`result?.data ?? []`), or use a promise-based debounce.

## Page Actions

- Key `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY` (value `'<camelCaseName>_ACTIONS_HOOK'`); type `<Container>ActionsHook`, in page `customization.ts` (dialogs: `~/dialogs/<path>/customization`).
- Hook args depend on page kind: `(data, editMode, storeDiff, [selectionDiff], [refresh], [submit])`. Returns handlers keyed by action name (e.g. `'export-csv'`, `'bulk-activate'`).
- Scaffold `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`. Called from `DefaultApplicationCustomizer.customize`.
- No `page` service property; the key is page-specific. One operation on N generated pages needs N registrations.
- `getMask?: () => string` (view or table pages only, not forms): generated page uses it to build `_mask` for its load request; falls back to generation-time mask. Return only needed fields.
- `_mask` syntax: `{<attr>,<attr>,<relation>{<attr>,...}}`; plain attributes comma-separated and sorted; relation followed by its braces. Example `{name,createdAt,owner{name}}`. Include every attribute referenced by visibility, enabled, required, or range-bound fields.
- `refreshAction(queryCustomizer)`: overriding replaces the load call; pass the received `queryCustomizer` (carries `_mask`, filters, sort, `_seek`) through to the generated service. Tables add `_mask` from `getMask`.
- `post<GetTemplateAction>(ownerData, data, storeDiff)` exists only on dialog (create-form) hooks; runs after the template loads. `storeDiff(attr, value)` writes defaults. Not generated on plain pages.
- Custom components after an operation: generated page does not refresh them. Use `post<Operation>` handler to dispatch `window.dispatchEvent(new CustomEvent('<app>:data-changed'))`; component listens in `useEffect` and removes the listener on cleanup.
- Menu refresh: menu filters by principal (`hiddenBy` names a boolean of the principal). After an operation changing those flags, `await refreshPrincipal()` from `usePrincipal()`; no reload needed.
- Advanced examples: CSV export from `context.getData()`; bulk activate/delete via `context.getSelectedIds()` with confirm and `refresh()`; custom operation via `context.actions.getAction('<op>')(signedIdentifier)` and `context.actions.downloadFile(token, 'attachment')`; errors via `context.showErrorDialog(title, message, 'error')`.

## OperationFlowManager

- Design principle: one representation per concept. Default post-op landing is the standalone `<TO>View` route; the same row is also reachable via `Actor.access.<area>.<rel> → row → detail` (a different page). Use `OperationFlowManager` to redirect post-op landings into the access-context view. Standalone routes stay generated but unvisited.
- See `../../../best-practices/frontend/operation-flow-manager-redirect.md` and `../../../best-practices/model/relation-driven-crud-with-custom-input.md`.
- `OperationFlowManager` and `OPERATION_FLOW_MANAGER_INTERFACE_KEY` (value `'OperationFlowManager'`) exported from `~/utilities/application`.
- Methods: `shouldUseCustomFlow(input)` (boolean; branch on `input.__entityType`) and `handleResult(input)` returning `ProcessProps` `{ actor, access, filterRecords?, operation? }`, or `{ refresh: true }`, or `null`.
- `filterRecords`: `{ field: [{ operator: 'equal', value }] }`.
- Input is the stored operation result; examples with `input.operation`, `entityType`, `id`, `tab` are illustrative.
- Register: `context.registerService<OperationFlowManager>(OPERATION_FLOW_MANAGER_INTERFACE_KEY, manager)`.
- Generated action queue (`src/hooks/useCRUDDialog.tsx`): updates items in place; `runActions` reads `inProgress` but it is missing from deps, so status can be stale. Do not start a second run while one is in progress.

## Best Practices

- Await async validation in `onBeforeSave`; a thrown error prevents save. Wrap in try/catch, notify, rethrow.
- `filterUserOptions` must consider form state, not just the option list.
- Custom hook files under `src/custom` are not generated (only their `.default` twin is): no `.generator-ignore` entry.
- Debounce autocomplete (300ms in example); lodash debounce yields `undefined` while pending.

## Complete Example

- `application-customizer.tsx`: `customize(context)` calls the container actions register fn, the page actions register fn, then registers `customFlowManager` under `OPERATION_FLOW_MANAGER_INTERFACE_KEY`.

## Troubleshooting

- Hook not executing: log at registration; verify the generated `_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` names with `grep -rn "_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY =" src/containers`.
- Filtering not working: log `formData` and `options` inside the filter.
- Operation flow not redirecting: log `input` and the returned object in `handleResult`; check `input.result.__identifier`.

## Related Documentation

- [Hook System Overview](./README.md)
- [Data Hooks](./data-hooks.md)
- [Table Hooks](./table-hooks.md)
- [Validation Hooks](./validation-hooks.md)
- [Navigation and Access](./navigation-and-access.md)
- [Development Workflow](../development-workflow.md)
