---
id: session-storage-table-state
title: SessionStorage Table State Persistence
description: "Persist a table's sort model and filters in sessionStorage so they survive navigation within the tab. The generated tables already do this by uniqueId; the pattern is for hand-built tables."
aliases: [sessionStorage table persistence, remember sort and filters]
keywords: [sessionStorage, table state, sort model, filters, persistence, uniqueId, useEffect, restore on mount, hand-built table]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: table
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [seek-based-table-pagination, table-row-actions-utility, localstorage-session-persistence]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Keep a user's sort and filter choices when they leave a table page and come back, without any backend storage.

## Practice

### Platform base

- The generated tables already do this: `LazyTable` and `EagerTable` persist grid state in `sessionStorage` under keys built from the table `uniqueId` (`${uniqueId}-sortModel`, `-filterModel`, `-filters`, `-rowsPerPage`, and `-columnState` with a licensed MUI plan). The keys depend only on `uniqueId`, so it must be unique per table; two tables with the same id read and write each other's state ([table state persistence](../../agent-docs/frontend/extension-points.md)).
- So with the generated tables do nothing; only give each custom table a unique `uniqueId`.

### Project practice: own persistence in a hand-built table (actiongroup-test-react)

For a table not built from the generated components, the project does this itself:

- Use a structured key per table, for example `pages.<entity>.<table>`, and store one JSON object `{ sortModel, filters }`.
- Restore on mount: parse the stored value (default `{}`), then use it as the initial sort model and filters, with a default sort when nothing is stored.
- Save in a `useEffect` whenever the sort model or filters change.
- Type the stored object (`PersistedTableData`) and parse defensively, since storage holds untyped strings.
- sessionStorage lives per tab: it survives refresh and in-app navigation, is cleared when the tab closes, is not shared across tabs and is limited in size.

```typescript
const persisted: PersistedTableData = JSON.parse(window.sessionStorage.getItem(KEY) || '{}');
const [sortModel, setSortModel] = useState(persisted.sortModel ?? [{ field: 'name', sort: 'asc' }]);
const [filters, setFilters] = useState(persisted.filters ?? []);
useEffect(() => {
  window.sessionStorage.setItem(KEY, JSON.stringify({ sortModel, filters }));
}, [sortModel, filters]);
```

## Rationale

Users keep their working context across navigation at tiny cost. The persistence is per tab only and untyped.

## Example

actiongroup-test-react: the galaxies table and the galaxy matter table store their sort model and filters under `pages.galaxies.table` and `pages.galaxy.matter.table`, restore them on mount and write them back on each change.

## When to avoid

- The generated tables are used; they persist state already.
- State must survive closing the browser or be shared across devices; store it in localStorage or the backend ([[localstorage-session-persistence]]).

## Related

- [[seek-based-table-pagination]] — paging that this state sits next to
- [[table-row-actions-utility]] — the same custom tables
- [[localstorage-session-persistence]] — what the generated frontend persists
