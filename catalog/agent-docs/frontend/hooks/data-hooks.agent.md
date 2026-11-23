# data-hooks.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/data-hooks.md.

## Overview
- Data hooks: current user (`usePrincipal`), page/dialog data (`useViewData`), app state.
- Backend enforces authorization; frontend only hides controls.

## usePrincipal Hook
- Import from `~/auth/principal-context`; generated only when app has a principal. Never write own `usePrincipal`, `PrincipalProvider` or fetch principal manually.
- Members: `principal` (`<Actor>Stored`; `{}` until loaded or unauthenticated), `setPrincipal(p)`, `getPrincipal()` (calls access service, returns REST response), `refreshPrincipal()` (reload into context), `errorCode` (set on 403).
- Shape = modeled principal TO, not fixed `roles`/`permissions`. Use modeled attributes (e.g. derived `isAdmin`).
- Loading check: `principal?.__identifier`.
- Usable inside hooks (they are React hooks).

## useViewData Hook
- Import from `~/hooks`. Does NOT load data; no `data`/`isLoading`/`refresh`.
- Members: `getLatestViewData()` (view navigated from, or `null`), `getRouterPageData()` (background page, regardless of dialog chain), `setLatestViewData(data)` and `setRouterPageData(data)` (set by generated pages only).
- Must be inside `ViewDataProvider` (generated in app root). Never create own `useViewData`.
- `getLatestViewData()` is null for dialogs opened from dashboard.

- Current page data: hook args `data`, `editMode`, `storeDiff(attributeName, value)`; page hooks may also get `selectionDiff`, `refresh()`, `submit()` depending on page kind (see action-hooks.md).
- Reload with `await refresh()` after mutation.
- Relation service signatures: non-access relation `create(owner, target, queryCustomizer?)` and `getRange(owner, queryCustomizer?, headers?)` take required `owner`. Only access relations have no `owner`.

## Combining Data Hooks
- Call `usePrincipal()` and `useViewData()` together inside one page/dialog hook.

## Custom Data Hooks
- Live in `src/custom/hooks/`; generated `.default` twins exist, the custom file itself is not generated, so no `.generator-ignore` entry.
- Pattern: service impl `new <Entity>ServiceImpl(judoAxiosProvider)` from `~/services/data-axios/`; types from `~/services/data-api/model/`.
- `useCurrentEntity(id)`: fetch in `useEffect`, returns `{ entity, loading, error }`.
- `useFilteredItems(filters)`: `listItems({ page, size, filters })`, returns `{ items, loading }`.
- Names are illustrative; service/method names follow the model.

## Best Practices
- Use `usePrincipal()` from generated context; no own fetch/provider.
- Take page data from hook arguments (`data`, `editMode`, `storeDiff`, `refresh`) typed by generated hook type.
- Change page state with `storeDiff('field', value)`, never mutate `data` (keeps validation and diff tracking).
- Memoize computed values (`useMemo(() => ..., [data])`).

## Troubleshooting
- Principal empty: `principal` is `{}` until request finishes and when unauthenticated. Check `principal?.__identifier` and `errorCode`.
- `getLatestViewData` returns null: only set after a generated page navigated away.
- Stale data: `await refresh()` (page hook) or `refreshPrincipal()`.

## Related Documentation
- README.md (hook system overview), ui-hooks.md, table-hooks.md, action-hooks.md, ../development-workflow.md
