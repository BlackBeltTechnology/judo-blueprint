---
id: "cards-container-refresh-bridge"
title: "Bridge CardsContainer Refresh to the Card Element via a Store"
domain: "frontend"
category: "state"
score: 50.0
usage_count: 1
alternative_count: 0
first_seen: "2026-06-25"
last_updated: "2026-06-25"
projects:
  - park-here
---
## Description

The generated `CardsContainer` only passes its `refresh` (re-runs the `fetch` prop that lists the
relation rows) to the `ToolbarElement`/`ActionbarElement` config slots — **not** to the per-row
`CardElement` (`CardProps` has no refresh callback). When a per-card operation (generate document,
upload/remove a binary, delete a child row) must reflect new server state, the naive fix is
`window.location.reload()`, which reloads the whole app, drops scroll position, and re-runs the entire
page bootstrap.

Instead, register the container's `refresh` from the toolbar/actionbar slot into a tiny imperative
store keyed per container, and have the card call it imperatively. Only the affected cards list
re-fetches; the rest of the app is untouched. This is the same external-store bridging approach JUDO
projects already use to pass container-level data (counts, gate flags) down to per-row card elements.

## Structure

```typescript
// cardsRefreshStore.ts — keyed imperative registry
type RefreshFn = () => Promise<void>;
const registry = new Map<string, RefreshFn>();

export function useRegisterCardsRefresh(key: string, refresh: RefreshFn): void {
  useEffect(() => {
    registry.set(key, refresh);
    return () => { registry.delete(key); }; // clear on unmount → never call a stale refresh
  }, [key, refresh]);
}

export async function refreshCardsList(key: string): Promise<void> {
  await registry.get(key)?.(); // no-op when that container is not mounted
}

// Toolbar/Actionbar slot — the ONLY slot that receives `refresh`
const Toolbar: FC<ToolbarElementProps<Row>> = ({ refresh, /* ... */ }) => {
  useRegisterCardsRefresh(KEY, refresh); // call before any early return (rules of hooks)
  // ...
};

// CardElement — has no refresh of its own; calls the bridged one
const onUpload = async (file: File) => {
  await service.upload(row, /* ... */);
  await refreshCardsList(KEY); // instead of window.location.reload()
};
```

For an inline PDF/preview dialog that resolves on OPEN (e.g. the shared `downloadFile('inline')`), wrap
it so the refresh runs when the dialog CLOSES (pass an `onClosed` callback), not on open — otherwise the
preview iframe is torn down while the user is still reading it.

Use a distinct key per container (e.g. `travelPanel.currentMonths`, `travelPanel.previousMonths`,
`adminTravelOverview.userTravelMonths`) so a page with multiple containers refreshes the right list.

## Examples

### park-here
The travel month cards (current-month, previous-month, and the admin cross-user overview) share a
`CurrentMonthCard`. After generating a settlement document (on preview close), uploading or removing a
signed document, and admin delete-travel, the card calls `refreshCardsList(key)` to re-list only that
container's `UserTravelMonth` rows — picking up the newly persisted `signedDocument` token via the
widened fetch mask. The container `refresh` is captured into `cardsRefreshStore` by the empty-state
`ActionbarElement` (current month) or the filter `ToolbarElement` (previous/admin).

## Trade-offs

- **Pros**: No full-app reload; preserves scroll/UI state; re-fetches with the container's widened mask
  so newly persisted server fields (e.g. download tokens) appear; reuses the existing external-store idiom
- **Cons**: Module-level registry is global — must key per container and clear on unmount to avoid stale
  refreshes; the card↔toolbar link is implicit (via key string), not type-checked
- **When to use**: A per-row `CardElement` must refresh its own list after a mutation but `CardProps`
  exposes no refresh. Prefer over `window.location.reload()`. For cross-PAGE sync, use the event bus
  instead.

## Related Patterns

- [event-bus-refresh-coordination](event-bus-refresh-coordination.md)
- [pdf-preview-inline-display](pdf-preview-inline-display.md)
- [pandino-action-hook-override](pandino-action-hook-override.md)
