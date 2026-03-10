---
id: "form-field-flattening"
title: "Form Field Flattening for Complex Create Operations"
domain: "backend"
category: "interceptor"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

Complex create forms use flattened `form_*` fields on the parent transfer object. An interceptor in `preCall` transforms these flat fields into the proper nested structure (child entities, relations) before the create operation executes. This allows a single create form to populate both the parent entity and its child relations simultaneously.

## Structure

```java
@Override
public Object preCall(EOperation op, Object payload) {
    CreateInstanceCallPayload create = (CreateInstanceCallPayload) payload;
    Payload input = create.getInput();

    // Transform flat form_* fields into nested child payload
    input.put(ParentReference.ADDRESSES.getName(), List.of(Payload.map(
        AddressAttribute.CITY.getName(), input.get(ParentAttribute.FORM_CITY.getName()),
        AddressAttribute.STREET.getName(), input.get(ParentAttribute.FORM_STREET.getName()),
        AddressAttribute.POSTAL_CODE.getName(), input.get(ParentAttribute.FORM_POSTAL_CODE.getName()),
        AddressAttribute.IS_HEADQUARTERS.getName(), input.get(ParentAttribute.FORM_IS_HEADQUARTERS.getName())
    )));

    return OperationCallInterceptor.super.preCall(op, payload);
}
```

## Examples

### RackInspect
`PartnerCreateInterceptor` maps 15+ flat `form_*` fields (form_city, form_street, form_postalCode, form_isHeadquarters, etc.) from the Partner create payload into a nested Address sub-payload. Also validates `form_isHeadquarters=true` as a required field before transformation. `UserCreateInterceptor` similarly flattens user address, email, and phone fields.

## Trade-offs

- Pros: Simple flat form for complex entity creation, single API call creates parent + children, no frontend multi-step wizard needed
- Cons: Fragile string-based Payload manipulation, form_* field naming convention must be manually maintained, hard to test
- Alternative: Multi-step create wizard in frontend, or separate create operations for parent and children

## Related Patterns

- interceptor-crud-lifecycle
- interceptor-access-control-flags
