---
id: many-aggregation-crud-pattern
title: Many-Aggregation CRUD Operations Pattern
description: "Manage many-to-many or one-to-many entity associations through a dedicated table page with Add, Remove, and Clear operations."
aliases: []
keywords: [many aggregation, add, remove, clear, range dialog, relation table, set]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: page
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [promise-based-dialog-system, action-group-input-output-routing, seek-based-table-pagination, aggregation-input-widget]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A to-many aggregation (a list of independent entities linked to a parent) must be managed from the parent's page: add existing entities, remove single links, and clear the whole list. This practice gives the relation a dedicated table page with those three actions, each backed by one service method.

## Practice

### Platform base

- For an aggregation, the model gives the relation table add and remove actions (the add action opens a selector dialog); a composition gets create and delete instead ([UI authoring guide](../../agent-docs/model/ui-authoring-guide.md)). The generator maps them to `*AddSelectorButton`, `*RowRemoveButton`, `*BulkRemoveButton`, `*ClearButton` and `*SetSelectorButton` ([table actions](../../agent-docs/frontend/model-screen-layout.md)). Prefer these generated actions; only the cases below need custom code.
- The REST layer exposes the relation verbs `~add`, `~remove`, `~set` and `~unset`, and a range query `~range` for the selectable candidates ([REST wire contract](../../agent-docs/backend/platform-behavior-reference.md)).
- Removing an aggregation link does not delete the target entity (a composition delete does).
- Bound calls use the parent's current signed identifier from the latest response; it changes after every update ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).

### Practice notes: one table page with Add, Remove and Clear

This is practice for a frontend that builds its own pages, not a platform feature.

- The page lives at a route below the parent, for example `/{parent}/:signedIdentifier/{relation}Table`.
- **Add**: open a range dialog over the range call, pass the already linked identifiers so they are excluded, then call the add method with the parent and the picked rows ([[promise-based-dialog-system]]).
- **Remove**: a per-row action calling the remove method with that row.
- **Clear**: a toolbar action calling the set method with an empty array; ask for confirmation, since it is destructive.
- Reload the table after every call.

```typescript
// Example code: service and method names are generated per relation
const selected = await openRangeDialog({
  columns,
  rangeCall: (qc) => parentService.getRangeForItems(undefined, qc),
  alreadySelectedItems: data.map((v) => v.__identifier),
});
await parentService.addItems(parent, selected);

await parentService.removeItems(parent, [row]);   // row action
await parentService.setItems(parent, []);         // clear
```

## Rationale

All association changes sit on one page, the range dialog handles selection, and the three methods map directly to the REST verbs. The cost is three calls to coordinate, no optimistic updates, and a destructive clear that needs a confirmation.

## Example

One app has an order line-item table that offers all three operations: Add opens a range dialog and excludes already linked items, Remove is a row action, and a toolbar button clears the list. Every call refreshes the table.

## When to avoid

- The generated add, remove and clear actions already cover the page.
- The relation is a composition: use create and delete.
- Only a single relation is edited: use a set selector instead ([[aggregation-input-widget]]).

## Related

- [[promise-based-dialog-system]] — the range dialog used by Add
- [[action-group-input-output-routing]] — other custom pages of the same frontend
- [[seek-based-table-pagination]] — paging for the table and range dialog
- [[aggregation-input-widget]] — the single-relation counterpart
