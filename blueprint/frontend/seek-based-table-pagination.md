---
id: "seek-based-table-pagination"
title: "Seek-Based (Keyset) Table Pagination"
domain: "frontend"
category: "table"
score: 75.8
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - actiongroup-test-react
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
---
## Description

Table pages in JUDO frontends use seek-based (keyset) pagination instead of offset-based pagination. The client sends the last or first visible item as a cursor along with a `reverse` flag to fetch the next or previous page. This approach performs better than offset pagination on large datasets because the backend can use index seeks rather than counting rows. Embedded tables in view pages use a simpler client-side `sublist()` approach.

## Structure

```dart
// Page store seek pagination (Flutter)
@action
Future<void> getEntities({int? queryLimit, bool? isNext}) async {
  var result = await _repo.listEntities(
    lastItem: isNext == true ? items.last : items.first,
    reverse: isNext == false,
    queryLimit: queryLimit ?? defaultPageSize,
    sortColumn: sortColumnName,
    sortAscending: sortAscending,
    filters: activeFilters,
  );
  // Update next/previous enable flags based on result count
  hasNext = result.length == queryLimit;
  hasPrevious = pageCounter > 0;
}
```

Two strategies:
1. **Server-side seek paging** (table pages): cursor-based with `lastItem` + `reverse`
2. **Client-side sublist paging** (embedded tables): loads all items, paginates with `sublist()`

## Examples

### SkillMatrix
All 14 table pages (Admin Users, HR Employee's 11 entity tables, Professional Subordinates, Report Executions) use server-side seek pagination. Embedded tables in view pages (e.g., Search > Competences, Tags, Result) use client-side `sublist()` pagination loading all items at once.

### ActionGroupTestReact
React implementation fetches `limit + 1` items (e.g., 11 for page size 10). If result length exceeds page size, `isNextButtonEnabled` is set true and the extra item is popped. Custom `CustomTablePagination` component renders Previous/Next buttons with `firstItem`/`lastItem` cursors passed to `_seek` in the query customizer.

### kozut-eugyfel-client
~40 table pages across 3 Flutter actors use cursor-based seek pagination. Each page store tracks `nextPageCounter` and exposes `@computed` getters `nextButtonEnable` and `previousButtonEnable`. Filter types include string, dateTime, numeric, boolean, and enum with `selectableFilters` and `availableFilterList` observable patterns.

### kozut-eugyfel-model-test
Model generates ~40 table pages with seek-based pagination across 3 actors. Admin has 6 top-level tables (Felhasznalok, Bejelentesek, Megyek, etc.), Munkatars has 5 (Feladatok, Aktiv/Lezart Bejelentesek, Ertesitesek), plus sub-entity tables with client-side pagination.

### ams-frontend
Applications table (10 rows, computed as `12.0 - 2`), Campaigns table, Users table, Approval List table, and Subordinates table all use cursor-based seek pagination. Embedded tables in Campaign View use client-side pagination: Confirmation Requests at 100 items per page, Applications at 1 item per page.

## Trade-offs

- **Pros**: Consistent O(1) performance regardless of page depth; no count(*) queries; works well with sorted results; generated automatically
- **Cons**: No random page access (jump to page N); must traverse sequentially; more complex cursor management than offset
- **When to use**: Standard JUDO table pattern -- used in both React and Flutter frontends for server-side paginated tables

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
- [three-layout-responsive-pattern](three-layout-responsive-pattern.md)
- [session-storage-table-state](session-storage-table-state.md)
