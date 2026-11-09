---
id: "getmask-data-optimization"
title: "Custom getMask() Override for Data Fetch Optimization"
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

Override the `getMask()` action in page hooks to specify exactly which fields to fetch from the backend, optimizing network payload for list views. The JUDO framework uses a `_mask` query customizer that follows a JSON-like syntax to select specific fields and nested relations. By default, generated pages fetch all visible fields, but custom masks can reduce this to only the fields needed for a specific view.

## Structure

```typescript
const hookImpl = (data, editMode, storeDiff, refresh, submit) => ({
  getMask(): string {
    return '{closedDate,created,registryNumber,' +
      'assignedTo{email,name},' +
      'facility{facilityName},' +
      'faultHeaders{rackName,rackTypeName}}';
  },
});
```

Mask syntax:
- Simple fields: `{field1,field2,field3}`
- Nested relations: `{relation{nestedField1,nestedField2}}`
- Multiple nesting levels: `{rel1{rel2{deepField}}}`

## Examples

### RackInspect
FaultRegistryPanel list hook overrides `getMask()` to fetch only fields needed for the list view: `closedDate`, `created`, `registryNumber`, status flags, `assignedTo{email,name}`, `facility{facilityName}`, and `faultHeaders{rackName,rackTypeName}`. This avoids loading full fault header details, dimension parameters, and element fault data that the list view does not display.

## Trade-offs

- **Pros**: Significant reduction in network payload; faster list loading; backend only queries needed relations
- **Cons**: Must be manually maintained when page columns change; incorrect masks cause missing data; no compile-time validation of mask strings
- **When to use**: List views or panels with complex entities where the default mask fetches too much data

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
