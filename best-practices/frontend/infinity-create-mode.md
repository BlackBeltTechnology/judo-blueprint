---
id: "infinity-create-mode"
title: "Infinity Create Mode with Template Copying"
domain: "frontend"
category: "form"
score: 10.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
---
## Description

Enable rapid sequential creation of similar entities by generating a template that copies most field values from the previously created entry while resetting specific fields. After a create operation completes, instead of closing the form, the dialog reopens with pre-populated values from the last entry. This is particularly useful for data entry workflows where consecutive records share many common fields.

## Structure

```typescript
// Template creation utility
export function createTemplateForEntity(data) {
  return {
    field1: data.field1,          // Carried over
    field2: data.field2,          // Carried over
    field3: data.field3,          // Carried over
    resetField: defaultValue,     // Always reset to default
    // ... more fields
  };
}

// In dialog hook postGetTemplateAction
async postGetTemplateAction(ownerData, data, storeDiff) {
  if (previousData) {
    const template = createTemplateForEntity(previousData);
    Object.entries(template).forEach(([key, value]) => {
      storeDiff(key, value);
    });
  }
}
```

## Examples

### RackInspect
`createTemplateForFaultElement()` creates a fault element template that copies `row`, `level`, `position`, `errorPlacement`, `rackElement`, `errorCode`, `errorType`, `repairType`, `quantity`, `inputGroups`, `rack`, and `registryHeader` from the previous entry, but specifically resets `withMaterial` to `true`. This allows rapid sequential creation of fault elements during rack inspection.

## Trade-offs

- **Pros**: Dramatically speeds up repetitive data entry; reduces user errors on common fields; natural workflow for inspection tasks
- **Cons**: Carried-over values may not always be correct; users must check pre-populated fields; complex for entities with many relations
- **When to use**: Inspection workflows, batch data entry, any scenario where consecutive records share common parent data

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [post-operation-navigation-hook](post-operation-navigation-hook.md)
