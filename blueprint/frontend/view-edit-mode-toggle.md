---
id: "view-edit-mode-toggle"
title: "View/Edit Mode Toggle Pattern for Detail Pages"
domain: "frontend"
category: "form"
score: 9.9
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
alternatives:
  - flutter-clone-edit-save-pattern
---
## Description

Detail/view pages use a boolean `editMode` state to toggle between read-only and editable form fields. In view mode, fields use `Mui-readOnly` class and `readOnly: true` InputProps. In edit mode, fields become editable. The action bar switches between Refresh/Delete/Edit buttons (view mode) and Cancel/Save buttons (edit mode). Validation state is cleared when toggling modes. On save, data is refreshed and edit mode exits.

## Structure

```typescript
const [editMode, setEditMode] = useState(false);
const [validation, setValidation] = useState<Map<string, string>>(new Map());

// Clear validation on mode toggle
useEffect(() => { setValidation(new Map()); }, [editMode]);

// Form field with mode toggle
<TextField
  value={data?.name ?? ''}
  className={editMode ? undefined : 'Mui-readOnly'}
  InputProps={{ readOnly: !editMode }}
  error={!!validation.get('name')}
  helperText={validation.get('name')}
  onChange={(e) => setData({ ...data, name: e.target.value })}
/>

// Action bar switches based on mode
{!editMode && <Button onClick={() => setEditMode(true)}>Edit</Button>}
{editMode && <Button onClick={() => { setEditMode(false); fetchData(); }}>Cancel</Button>}
{editMode && <Button onClick={saveData}>Save</Button>}
```

## Examples

### ActionGroupTestReact
Galaxy View and ChooseTheMessiah output pages use `editMode` toggle. View mode shows Refresh/Delete/Edit buttons with read-only fields styled via `Mui-readOnly` CSS class (transparent background, subtle bottom border). Edit mode shows Cancel/Save with editable fields getting box-shadow styling. TrinaryLogicCombobox also respects `readOnly` prop.

## Trade-offs

- **Pros**: Prevents accidental edits; clear visual distinction between modes; validation only shown in edit mode; single page serves both viewing and editing
- **Cons**: All fields must handle both modes; CSS class toggling can be fragile; cancel discards all unsaved changes
- **When to use**: Standard pattern for JUDO React entity detail pages that support both viewing and inline editing

## Related Patterns

- [centralized-error-handling-validation-map](centralized-error-handling-validation-map.md)
- [action-group-input-output-routing](action-group-input-output-routing.md)
- [flutter-clone-edit-save-pattern](flutter-clone-edit-save-pattern.md)
