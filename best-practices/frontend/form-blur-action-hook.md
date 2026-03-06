---
id: "form-blur-action-hook"
title: "Form Blur Action Hook for Field Auto-Composition"
domain: "frontend"
category: "hook"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

Override `onXxxBlurAction` in form or view/edit action hooks to automatically compose or compute field values when a user leaves (blurs) a form field. The most common use case is auto-composing a composite string from individual component fields (e.g., a full address from street, number, floor, door fields). The blur handler reads the current form data and calls `storeDiff` to update the computed field.

## Structure

```typescript
// Hook implementation
const hookImpl = (data, editMode, storeDiff) => ({
  onStreetNameBlurAction: async (data) => {
    if (!data.manualAddressInformation) {
      storeDiff('addressInformation', composeAddress(data));
    }
  },
  onNumberBlurAction: async (data) => {
    if (!data.manualAddressInformation) {
      storeDiff('addressInformation', composeAddress(data));
    }
  },
  // ... more blur handlers for each address component
});

function composeAddress(data) {
  return data.streetName
    + (data.publicPlaceCategory ? ' ' + data.publicPlaceCategory : '')
    + (data.number ? ' ' + data.number : '')
    + (data.building ? ' ' + data.building : '')
    + (data.staircase ? ' ' + data.staircase : '')
    + (data.floor ? ' ' + data.floor : '')
    + (data.door ? ' ' + data.door : '')
    + (data.lotNumber ? ', ' + data.lotNumber : '');
}
```

## Examples

### RackInspect
Six files implement address auto-composition: 3 FormActionsHooks (Partner, Address, CompanyAddress) and 3 ViewEditActionHooks (same entities). Each overrides blur handlers for streetName, publicPlaceCategory, number, building, staircase, floor, door, and lotNumber. Guarded by `manualAddressInformation` boolean toggle.

## Trade-offs

- **Pros**: Real-time field computation without submit; clean user experience; computation logic stays in hook (not generated code)
- **Cons**: Blur-based triggers can miss edge cases (paste, autofill); same logic duplicated across form and view/edit hooks; must handle guard conditions
- **When to use**: When a field value should be auto-computed from other fields on the same form

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [post-refresh-validation-propagation](post-refresh-validation-propagation.md)
