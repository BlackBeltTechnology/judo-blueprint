---
id: "many-aggregation-crud-pattern"
title: "Many-Aggregation CRUD Operations Pattern"
domain: "frontend"
category: "page"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

Manage many-to-many or one-to-many entity associations through a dedicated table page with Add, Remove, and Clear operations. The Add button opens a RangeDialog for multi-select entity picking. Remove is a per-row action. Clear replaces the entire association with an empty array via the `set` service method. The pattern uses three distinct service methods: `addEntity()`, `removeEntity()`, and `setEntity([])`, all operating on the parent entity's signed identifier.

## Structure

```typescript
// Add - opens range dialog, then calls addEntity
const selected = await openRangeDialog({
  columns, rangeCall: (qc) => service.getRangeForEntity(undefined, qc),
  alreadySelectedItems: data.map(v => v.__identifier),
});
await service.addEntity(parent, selected);

// Remove - per-row action
await service.removeEntity(parent, [row]);

// Clear - toolbar button
await service.setEntity(parent, []);

// Service method signatures
viewEntityServiceImpl.addMatter(parent, items[])
viewEntityServiceImpl.removeMatter(parent, items[])
viewEntityServiceImpl.setMatter(parent, items[])  // [] = clear all
viewEntityServiceForMatterImpl.list(parent, queryCustomizer)
```

## Examples

### ActionGroupTestReact
Galaxy Matter table at `/galaxy/:id/matterTable` demonstrates all 3 operations. Add button opens RangeDialog with `getRangeForMatter()`, excludes already-selected items via `alreadySelectedItems`. Remove is a row action calling `removeMatter([row])`. Clear toolbar button calls `setMatter([])`. All operations refresh the table after completion.

## Trade-offs

- **Pros**: Complete association management in one page; range dialog handles selection UX; clear operation for bulk reset; consistent with JUDO service API
- **Cons**: Three service methods to coordinate; no optimistic updates; clear is destructive without confirmation; range dialog must exclude existing items
- **When to use**: Any entity with many-aggregation relationships that users need to manage (add/remove/clear associated entities)

## Related Patterns

- [promise-based-dialog-system](promise-based-dialog-system.md)
- [action-group-input-output-routing](action-group-input-output-routing.md)
- [seek-based-table-pagination](seek-based-table-pagination.md)
