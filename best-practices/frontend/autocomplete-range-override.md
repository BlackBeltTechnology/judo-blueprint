---
id: "autocomplete-range-override"
title: "Autocomplete Range Override for Context-Filtered Queries"
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

Override `xxxAutocompleteRangeAction` in dialog or page hooks to customize the data source for autocomplete/dropdown fields based on the current context. By default, autocomplete fields use a generic range query that returns all available options. Overriding allows filtering options based on the parent entity, current selection, or other contextual data by redirecting to a specialized service implementation.

## Structure

```typescript
const hookImpl = (ownerData) => ({
  async rackAutocompleteRangeAction(queryCustomizer) {
    // Use specialized service that filters by partner
    return getRackAutocompleteRangeForPartner(ownerData, queryCustomizer);
  },

  async warehouseAutocompleteRangeAction(queryCustomizer) {
    // Use specialized service that filters by fault registry context
    return getWarehouseAutocompleteRangeForFaultRegistry(ownerData, queryCustomizer);
  },

  async rackElementAutocompleteRangeAction(queryCustomizer) {
    // Filter by rack type using dedicated service
    return getRackElementAutocompleteRange(ownerData, queryCustomizer);
  },
});
```

Utility functions encapsulate the service calls with context filtering.

## Examples

### RackInspect
Multiple dialog hooks override rack, warehouse, and rack element autocomplete ranges. `getRackAutocompleteRangeForFaultRegistry()` uses a specialized service to show only racks belonging to the fault registry's partner. `getRackElementAutocompleteRange()` filters rack elements by the current fault's rack type instead of showing all rack elements. Shared utility functions in `rackHelper.ts` centralize the range query logic.

## Trade-offs

- **Pros**: Users see only relevant options; reduces selection errors; leverages backend filtering for performance
- **Cons**: Requires specialized backend service endpoints; more hooks to maintain; context dependency can be complex
- **When to use**: When autocomplete fields should show filtered options based on parent entity relationships or current selection

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
