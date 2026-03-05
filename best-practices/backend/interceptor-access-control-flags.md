---
id: "interceptor-access-control-flags"
title: "Access Control via __updateable/__deleteable Payload Flags"
domain: "backend"
category: "interceptor"
score: 28.8
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - judo-partner
---
## Description

Post-call interceptors on list and refresh operations that set special `__updateable` and `__deleteable` flags on returned Payload objects. These flags control whether the frontend UI enables edit and delete buttons for individual rows. The interceptor checks a business condition (e.g., parent entity status, user role) and disables modifications when the entity is in a read-only state or the user lacks permissions.

## Structure

```java
@Override
public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
    List<Map<String, Object>> items = (List<Map<String, Object>>) returnPayload;
    for (Map<String, Object> item : items) {
        if (isReadOnly(item)) {
            item.put("__updateable", false);
            item.put("__deleteable", false);
        }
    }
    return OperationCallInterceptor.super.postCall(op, paramPayload, returnPayload);
}
```

For refresh (single-instance) interceptors, the return is a single `Map<String, Object>`.

## Examples

### RackInspect
5 access control interceptors. `ElementFaultRefreshInterceptor` sets `__updateable=false` when owning fault registry is not in draft status. `ErrorQualificationInstanceListInterceptor` and its refresh counterpart disable edit/delete for document-generated instances. `JobSheetInputItemListInterceptor` disables both when `completionCertificateIsDefinedOnOffer=true`.

### judo-partner
`PartnerInterceptor` targets 12 list/refresh operations across partners, addresses, and contacts. Resolves current user via `VariableResolver` (ACTOR email), checks `user.getIsPartnerAdmin()`, and if non-admin, sets `__updateable=false` and `__deleteable=false` on both single `Payload` and `List<Payload>` results. Implements role-based read-only access for non-admin users.

## Trade-offs

- Pros: Fine-grained row-level access control, integrates seamlessly with generated UI, no frontend changes needed
- Cons: Operates on raw Map payloads (no type safety), must implement both list and refresh interceptors for consistency, business logic duplicated between list and refresh
- Alternative: Model-level access expressions, or custom frontend logic to disable buttons

## Related Patterns

- interceptor-crud-lifecycle
- interceptor-range-override
