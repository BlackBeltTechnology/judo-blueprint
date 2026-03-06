---
id: "interceptor-range-override"
title: "Range Interceptor for Context-Filtered Dropdowns"
domain: "backend"
category: "interceptor"
score: 68.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - park-here
---
## Description

Post-call interceptors that override the default reference range results (dropdown/autocomplete data) by filtering based on the current editing context. When a form field's available options should depend on another field's value (e.g., error codes depend on selected rack element), a range interceptor intercepts the `_getRangeReference*` operation and replaces the results with a context-filtered query.

## Structure

```java
@Override
public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
    GetReferenceRangeCallPayload rangePayload = (GetReferenceRangeCallPayload) paramPayload;
    Payload owner = rangePayload.getOwner();
    UUID ownerId = owner.getAs(UUID.class, "relatedEntity.__identifier");

    // Query filtered results based on owner context
    List<Entity> filtered = parentDao.queryRelation(parentDao.getById(ownerId).orElseThrow())
        .filterBy(originalFilter)
        .orderBy(attribute, order)
        .selectList(limit, lastItem, isReverse);

    // Convert to List<Map<String, Object>> and return
    return OperationCallInterceptor.super.postCall(op, paramPayload, filteredResults);
}
```

Includes camelCase-to-UPPER_SNAKE_CASE attribute name conversion for orderBy mapping.

## Examples

### RackInspect
5 range interceptors. `ElementFaultErrorCodesRangeInterceptor` filters error codes by the selected rack element's available codes. `ElementFaultRepairTypesRangeInterceptor` does the same for repair types. `JobSheetInputRangeInterceptor` filters offer items by the selected offer. Each implements pagination with `QueryCustomizer` and custom attribute name conversion.

### ParkHere
3 range interceptors for reservation input. `ReservationInputCarRangeInterceptor` filters cars to non-archived only for the current user. `ReservationInputParkingSlotRangeInterceptor` returns only free parking slots for the requested time range (using `queryFreeParkingSlotForADay` or `queryFreeParkingSlotForDays` depending on reservation type), filtering exclusive slots for non-admins. `PreferedParkingSlotRangeInterceptor` filters accessible slots for profile settings. All preserve client-specified filter, orderBy, and pagination.

## Trade-offs

- Pros: Context-sensitive dropdowns without frontend code, reuses existing range operation infrastructure
- Cons: Complex Payload manipulation, must handle pagination/sorting manually, camelCase-to-UPPER_SNAKE conversion is fragile
- Alternative: Model-level range filtering expressions, or custom frontend autocomplete with dedicated query operation

## Related Patterns

- interceptor-crud-lifecycle
- interceptor-access-control-flags
