---
id: "trinary-logic-widget"
title: "Trinary Logic Combobox for Nullable Booleans"
domain: "frontend"
category: "form"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

A custom form widget for nullable boolean fields that maps three values: `true` ("Yes"), `false` ("No"), and `null` ("Unknown"). Implemented as a Select/Combobox dropdown rather than a checkbox, since checkboxes cannot represent the null/unknown state. Supports read-only mode, validation state, and icon decoration. Uses a Map for value-to-label mapping.

## Structure

```typescript
const TRINARY_LOGIC = new Map([
  [null, 'Unknown'],
  [true, 'Yes'],
  [false, 'No'],
]);

<TrinaryLogicCombobox
  name="real"
  label="Real"
  readOnly={!editMode}
  value={data?.real}
  error={!!validation.get('real')}
  helperText={validation.get('real')}
  onChange={(value) => setData({ ...data, real: value })}
/>
```

Also used in FilterDialog as `trinaryLogic` filter type for boolean column filtering.

## Examples

### ActionGroupTestReact
`TrinaryLogicCombobox` component at `src/components/TrinaryLogicCombobox.tsx` renders a MUI Select with 3 options. Used for Galaxy fields (`real`, `nakedEye`) and Earth fields (`habitable`, `inhabited`, `peaceful`). Also used as a filter type in the FilterDialog for filtering boolean columns in tables.

## Trade-offs

- **Pros**: Handles nullable booleans cleanly; clear user-facing labels; consistent with 3-value logic in database; works in both forms and filters
- **Cons**: Custom widget not part of standard MUI; must be maintained separately; "Unknown" label may confuse users expecting "Not Set"
- **When to use**: Any form or filter that needs to represent a nullable boolean (true/false/null) field

## Related Patterns

- [view-edit-mode-toggle](view-edit-mode-toggle.md)
- [promise-based-dialog-system](promise-based-dialog-system.md)
