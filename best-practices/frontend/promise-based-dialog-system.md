---
id: "promise-based-dialog-system"
title: "Promise-Based Dialog System with Context Provider"
domain: "frontend"
category: "component"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

Implement a centralized dialog system using React Context where each dialog type (Filter, Range, Confirmation, Page) is exposed via a custom hook that returns a Promise. Callers use `await openDialog(...)` to show a dialog and receive the result when the user confirms or cancels. This replaces callback-based dialog patterns with cleaner async/await flows and supports 4 dialog types: server-side filtering, entity range selection (single/multi), yes/no confirmation, and full page-in-dialog rendering.

## Structure

```typescript
// DialogContext.tsx - Provider wrapping all 4 dialog types
export const DialogProvider: FC = ({ children }) => (
  <>
    {children}
    <FilterDialog />
    <RangeDialog />
    <ConfirmationDialog />
    <PageDialog />
  </>
);

// Each dialog exposed via hook returning Promise
const { openFilterDialog } = useFilterDialog();
const filters = await openFilterDialog(filterOptions, currentFilters);

const { openRangeDialog } = useRangeDialog();
const selected = await openRangeDialog<EntityStored, QueryCustomizer>({
  columns, rangeCall, single: true, alreadySelectedItems, filterOptions
});

const { openConfirmDialog } = useConfirmDialog();
const confirmed = await openConfirmDialog('Are you sure?', 'Title');

const { openPageDialog } = usePageDialog();
await openPageDialog(<OutputComponent data={result} />);
```

## Examples

### ActionGroupTestReact
`DialogProvider` in `src/components/dialog/DialogContext.tsx` combines 4 dialog types. `FilterDialog` supports 7 filter types (boolean, numeric, string, enumeration, date, dateTime, trinaryLogic). `RangeDialog` is generic with `<T extends JudoStored<T>>` for entity selection with server-side pagination. `PageDialog` renders action group output components in modals.

## Trade-offs

- **Pros**: Clean async/await pattern replaces callbacks; centralized dialog management; type-safe generic range dialog; consistent UX across all dialogs
- **Cons**: All dialog state lives in a single context provider; cannot compose dialogs (no dialog-within-dialog); Promise rejection must be handled for cancel
- **When to use**: Any JUDO frontend needing reusable filter, selection, confirmation, or page-embedded dialogs

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [action-group-input-output-routing](action-group-input-output-routing.md)
