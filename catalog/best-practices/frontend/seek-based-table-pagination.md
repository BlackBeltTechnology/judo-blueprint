---
id: seek-based-table-pagination
title: Seek-Based (Keyset) Table Pagination
description: "Page table data with the _seek keyset cursor (last or first visible row plus a reverse flag) instead of offsets; load limit+1 rows to know whether a next page exists. Frontend project practice on top of the opt-in platform seek."
aliases: [keyset pagination, cursor table paging, next/previous pagination]
keywords: [seek, keyset, cursor, pagination, table, lastItem, reverse, limit, next previous, sublist, query customizer]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: table
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [session-storage-table-state]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Page large tables without counting rows or using offsets, so deep pages cost the same as the first.

## Practice

### Platform base

- A list call with no explicit seek returns all matching rows; pagination is opt-in ([pagination](../../agent-docs/backend/data-access-guide.md)).
- List queries combine `_orderBy`, a `_seek` keyset cursor (`lastItem` with the signed identifier and sort key, `limit`, `offset`, `reverse`) and per-attribute filter operators ([resource verbs and list queries](../../agent-docs/backend/platform-behavior-reference.md)). On the backend, the low-level `QueryCustomizer` carries the same `seek` ([data access guide](../../agent-docs/backend/data-access-guide.md)).

### Practice notes: next/previous paging in the table page

This client-side handling is practice; the platform only provides the seek parameters:

- **Server-side seek paging for table pages.** To go forward send the last visible row as `lastItem` with `reverse` false; to go back send the first visible row with `reverse` true. Send the page size as `limit` together with the current sort column, direction and filters.
- **Detect a next page with limit + 1.** Request one more row than the page size; if the extra row arrives, enable Next and drop it (React). The Flutter stores instead compare the result count to the limit.
- **No random access.** Only Next and Previous are offered; no jump to page N and no total count.
- **Embedded tables in view pages** load all their rows once and page them on the client with a sublist. This is fine for small related sets; use seek for large ones.
- Reset the cursor when sort or filters change, and keep the table state across navigation ([[session-storage-table-state]]).

```typescript
// Illustrative: limit + 1 to detect the next page
const rows = await listItems({ _seek: { lastItem, limit: pageSize + 1, reverse: false } });
const hasNext = rows.length > pageSize;
const page = hasNext ? rows.slice(0, pageSize) : rows;
```

## Rationale

Keyset paging avoids count queries and offset scans, so it stays fast on deep pages and sorted data. The cost is sequential navigation and cursor handling in every table page.

## Example

- A hand-built React app: fetches `limit + 1` rows, pops the extra one, and a custom pagination component renders Previous and Next with `firstItem` and `lastItem` cursors passed in the seek.
- A Flutter app: all table pages use server-side seek paging; embedded tables in view pages page on the client.
- Another Flutter app: many table pages across several actors use cursor paging, with next and previous enabled flags per page store.
- A further app: its list tables use cursor paging; embedded tables in a detail view use client paging.

## When to avoid

- Users need to jump to an arbitrary page or see a total count.
- The data set is small; a plain full list is enough.

## Related

- [[session-storage-table-state]] — keeping the page, sort and filters across navigation
