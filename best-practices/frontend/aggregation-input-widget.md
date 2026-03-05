---
id: "aggregation-input-widget"
title: "Aggregation Input Widget for Entity Associations"
domain: "frontend"
category: "form"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

A reusable form widget for displaying and managing entity associations (single-aggregation or required-relation fields). Shows the associated entity's properties as a concatenated label list, with context-sensitive action icons: View and Delete in read-only mode, Remove in edit mode, Create when no entity is set. Opens a RangeDialog for entity selection via the `onSet` callback. Handles the full lifecycle of an entity association in a single widget.

## Structure

```typescript
<AggregationInput
  label="Astronomer"
  labelList={[data.astronomer?.name ?? '', data.astronomer?.born ?? '']}
  value={data.astronomer}
  icon={<Accessibility />}
  readonly={!editMode}
  onSet={async () => {
    const res = await openRangeDialog({ columns, rangeCall, single: true });
    if (res) setData({ ...data, astronomer: res });
  }}
  onView={() => navigate(`/view/${data.astronomer?.__signedIdentifier}`)}
  onCreate={() => navigate('/astronomer/create')}
  onDelete={async () => { await service.delete(data.astronomer); fetchData(); }}
  onRemove={() => setData({ ...data, astronomer: null })}
/>
```

Props: `value`, `labelList`, `icon`, `readonly`, `onSet`, `onView`, `onCreate`, `onDelete`, `onRemove`, `error`, `helperText`.

## Examples

### ActionGroupTestReact
`AggregationInput` at `src/components/AggregationInput.tsx` manages Galaxy-to-Astronomer association. In view mode: shows name + born date with View/Delete icons. In edit mode: shows Remove icon. When empty: shows Create icon. Selection opens RangeDialog with server-side pagination and filtering against `viewGalaxyServiceImpl.getRangeForAstronomer()`.

## Trade-offs

- **Pros**: Single widget handles all association states (set, empty, view, edit); consistent UX for all entity relations; integrates with RangeDialog for selection
- **Cons**: Complex prop interface (7 callbacks); label concatenation is fragile; assumes single-select associations
- **When to use**: Any form field representing an entity association where users need to view, select, create, or remove the associated entity

## Related Patterns

- [promise-based-dialog-system](promise-based-dialog-system.md)
- [view-edit-mode-toggle](view-edit-mode-toggle.md)
