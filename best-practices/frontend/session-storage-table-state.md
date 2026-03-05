---
id: "session-storage-table-state"
title: "SessionStorage Table State Persistence"
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

Persist table sort model and active filters to `sessionStorage` so that navigating away from a table page and returning preserves the user's sort and filter preferences. State is saved on every change via `useEffect` and restored on component mount from a structured key format `pages.{entity}.{table}`. This survives page refreshes and navigation within the SPA but is cleared when the browser tab closes.

## Structure

```typescript
// Key format for persistence
const STORAGE_KEY = 'pages.entity.table';

// Restore on mount
const persisted: PersistedTableData = JSON.parse(
  window.sessionStorage.getItem(STORAGE_KEY) || '{}'
);
const [sortModel, setSortModel] = useState(
  persisted.sortModel || [{ field: 'name', sort: 'asc' }]
);
const [filters, setFilters] = useState(persisted.filters || []);

// Save on change
useEffect(() => {
  window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ sortModel, filters }));
}, [sortModel, filters]);
```

Type definition:
```typescript
interface PersistedTableData {
  sortModel?: GridSortModel;
  filters?: Filter[];
}
```

## Examples

### ActionGroupTestReact
Galaxies table and Galaxy Matter table both persist `sortModel` and `filters` to sessionStorage with keys like `pages.galaxies.table` and `pages.galaxy.matter.table`. On mount, persisted values are parsed and used as initial state. On sort or filter change, new state is serialized back to sessionStorage.

## Trade-offs

- **Pros**: User preferences survive navigation; minimal implementation; no backend storage needed; automatic cleanup when tab closes
- **Cons**: Lost when browser tab closes; no cross-tab sharing; sessionStorage has 5MB limit; stored as JSON strings (no type safety)
- **When to use**: Any table page where users benefit from persistent sort/filter state across navigation within a session

## Related Patterns

- [seek-based-table-pagination](seek-based-table-pagination.md)
- [table-row-actions-utility](table-row-actions-utility.md)
