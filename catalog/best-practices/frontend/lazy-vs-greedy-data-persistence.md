---
id: "lazy-vs-greedy-data-persistence"
title: "Lazy vs Greedy Data Persistence Modes for Custom Components"
domain: "frontend"
category: "state"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

Custom components that manage their own data can implement two data persistence strategies. **Greedy mode**: all changes are batched in local state and submitted to the backend on form save (used in form/creation contexts). **Lazy mode**: each change is immediately persisted to the backend, with local state managed independently from the main page form to avoid triggering edit mode (used in view/edit contexts where the component should not block the page save flow).

## Structure

```typescript
// Greedy mode (forms) - batch changes
const onValueChange = (paramId, newValue) => {
  const updatedGroups = updateParameterValue(groups, paramId, newValue);
  storeDiff('groups', updatedGroups); // Update parent form state
};
// All changes submitted when form saves

// Lazy mode (view/edit) - immediate persistence
const onValueChange = async (paramId, newValue) => {
  setLoadingParam(paramId);
  try {
    await backendService.updateParameter(paramId, newValue);
    refreshLocalState();
  } catch (error) {
    revertToOriginalValue(paramId);
    showError(error.message);
  } finally {
    setLoadingParam(null);
  }
};
```

Lazy mode features: loading spinners during sync, error handling with automatic revert, independent state from page form.

## Examples

### RackInspect
DimensionParametersViewComponent supports both modes. Greedy mode is used in fault element creation forms -- template parameters are fetched eagerly, changes batched via `storeDiff`, submitted on form save. Lazy mode is used in Rack_View_Edit -- each parameter change calls the backend immediately, rows can be added/deleted independently, selectable ENUM values are lazy-loaded on dropdown open, and loading spinners show during operations.

## Trade-offs

- **Pros**: Right persistence strategy for each context; lazy mode avoids blocking page save; greedy mode batches for performance
- **Cons**: Dual implementation adds complexity; lazy mode requires per-operation error handling; state synchronization between modes can be tricky
- **When to use**: Complex custom components embedded in both form (creation) and view/edit (modification) contexts

## Related Patterns

- [custom-visual-element-override](custom-visual-element-override.md)
