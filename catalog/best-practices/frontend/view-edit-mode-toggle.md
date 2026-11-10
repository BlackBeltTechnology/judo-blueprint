---
id: view-edit-mode-toggle
title: View/Edit Mode Toggle Pattern for Detail Pages
description: "A detail page keeps a boolean edit mode that switches its fields between read-only and editable and its action bar between view and edit buttons."
aliases: [read-only edit toggle, inline edit mode]
keywords: [edit mode, view mode, read-only, detail page, toggle, validation, save, cancel, useNavigationConfirmation]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: form
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [centralized-error-handling-validation-map, action-group-input-output-routing, trinary-logic-widget]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A detail page that shows an entity and also lets the user edit it should not expose editable fields by default. A boolean edit mode makes the page read-only until the user chooses Edit, and returns it to read-only after Save or Cancel.

## Practice

### Platform base

- The generated React frontend already has the concept: a View/Edit container carries an edit mode, and container action hooks receive `(data, editMode, storeDiff)` as their first parameters ([container hook registration](../../agent-docs/frontend/model-screen-layout.md), [action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). The generated page action buttons (refresh, update, cancel, delete) come from the model's action definitions.
- Whether a field is hidden, disabled, read-only or required can be controlled by the model (visual properties) or, with the visual properties hook generated, by `is<Field>Readonly` style handlers of the container hook ([hook generation](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)).
- Navigation away from edited state is gated by the generated `useNavigationConfirmation` hook; custom edit pages should reuse it ([extension points](../../agent-docs/frontend/extension-points.md)).

Use the generated pages when they fit. The pattern below applies to a frontend that builds its own detail pages (here an operation output page).

### Project practice: hand-built edit mode

This is project code (actiongroup-test-react), not a platform feature:

- State: `editMode` (default false) and a validation map keyed by field name.
- An effect clears the validation map whenever `editMode` changes, so stale errors do not follow the user into the other mode.
- Fields get `readOnly: !editMode` and a `Mui-readOnly` class in view mode; the styling gives read-only fields a transparent look and editable ones a visible border or shadow.
- The action bar switches: view mode shows Refresh, Delete and Edit; edit mode shows Cancel and Save.
- Cancel leaves edit mode and refetches the data, which discards unsaved input. Save sends the data, refreshes it from the response and leaves edit mode.
- Every custom field widget must honour the read-only flag (for example [[trinary-logic-widget]]).

```typescript
// Example project code
const [editMode, setEditMode] = useState(false);
const [validation, setValidation] = useState<Map<string, string>>(new Map());
useEffect(() => { setValidation(new Map()); }, [editMode]);

<TextField
  value={data?.name ?? ''}
  className={editMode ? undefined : 'Mui-readOnly'}
  InputProps={{ readOnly: !editMode }}
  error={!!validation.get('name')}
  helperText={validation.get('name')}
/>
{!editMode && <Button onClick={() => setEditMode(true)}>Edit</Button>}
{editMode && <Button onClick={() => { setEditMode(false); fetchData(); }}>Cancel</Button>}
{editMode && <Button onClick={saveData}>Save</Button>}
```

When saving a bound entity again, use the signed identifier from the latest response: it changes after each update ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).

## Rationale

The page prevents accidental edits, makes the two modes visually distinct, and shows validation only while editing, with one page for viewing and editing. The cost: every field must handle both modes, class toggling is fragile, and cancel discards all unsaved changes.

## Example

In actiongroup-test-react the Galaxy view page and an operation output page use the toggle with the button sets above and shared read-only styling.

## When to avoid

- On generated View/Edit pages: configure the model instead of rebuilding edit mode.
- When edits should be saved per field or by autosave.

## Related

- [[centralized-error-handling-validation-map]] — where the validation map comes from
- [[action-group-input-output-routing]] — output pages that use the toggle
- [[trinary-logic-widget]] — a widget that honours the read-only flag
