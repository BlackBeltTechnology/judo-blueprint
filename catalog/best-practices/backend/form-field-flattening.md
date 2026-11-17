---
id: form-field-flattening
title: Form Field Flattening for Complex Create Operations
description: "A create form for a parent with child records uses flat form_ fields on the parent transfer object; a create interceptor maps them into the nested child payload before the platform create runs."
aliases: [form_ fields, flat create form, nested create payload]
keywords: [form, flattening, create, interceptor, preCall, payload, transfer object]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: interceptor
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/partner/PartnerCreateInterceptor.java"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

One create form should fill a parent and its first child (for example an account and its primary address) in one call. The parent transfer object carries extra flat `form_*` members, and a create interceptor turns them into the nested child payload before the platform's create runs.

## Practice

### Platform base: create interceptors and payload manipulation

The platform lets an `OperationCallInterceptor` change the input of the built-in create operation in `preCall`. The returned object replaces the input payload, and `Payload.map()` builds nested payloads; the agent-docs show this exact flat-form-to-nested mapping and a matching `postCall` ([pre-call payload manipulation](../../agent-docs/backend/interceptors.md)). Create is a built-in operation, so interceptors fire for it; custom operations are never intercepted ([which operations are intercepted](../../agent-docs/backend/interceptors.md)). Register the component with `judo.model.name=<model>` and name the create operation by its FQN in `getOperations`.

### Practice notes: the `form_` naming convention

The `form_*` prefix and the flattening itself are a convention, not platform concepts.

- Model: the parent transfer object gets plain (transient) members named `form_<field>` for the child's fields. They exist only for the form.
- `preCall`: validate required form fields, then put the nested child list into the payload under the relation name, copying each `form_*` value to the child attribute key.
- `postCall` (optional): look the created child up and set relations that need the created instance, such as a "primary" reference.

```java
// Example code; ParentAttribute / AddressAttribute / ParentReference are generated constants
@Override
public Object preCall(EOperation op, Object payload) {
    Payload input = ((CreateInstanceCall.CreateInstanceCallPayload) payload).getInput();
    if (!Boolean.TRUE.equals(input.getAs(Boolean.class, ParentAttribute.FORM_IS_HEADQUARTERS.getName()))) {
        throw new ValidationException(List.of(ValidationResult.builder()
            .code("HEADQUARTERS_REQUIRED").level(ValidationResult.Level.ERROR)
            .location(ParentAttribute.FORM_IS_HEADQUARTERS.getName()).build()));
    }
    input.put(ParentReference.ADDRESSES.getName(), List.of(Payload.map(
        AddressAttribute.CITY.getName(), input.get(ParentAttribute.FORM_CITY.getName()),
        AddressAttribute.STREET.getName(), input.get(ParentAttribute.FORM_STREET.getName()))));
    return OperationCallInterceptor.super.preCall(op, payload);
}
```

Use `getAs(...)` with `Boolean.TRUE.equals(...)`: `getAs` returns null for an absent key.

## Rationale

- One API call creates parent and children with no multi-step wizard in the frontend.
- The interceptor runs inside the operation's transaction, so a thrown error rolls the whole create back.
- Cost: string-keyed payload manipulation is fragile, the `form_*` naming must be kept in sync by hand, and the interceptor is hard to unit test. The extra members widen the transfer object.

## Example

One application: an account create interceptor maps many flat `form_*` fields (city, street, postal code, primary flag and others) into a nested address payload and requires the primary flag before transforming. A user create interceptor does the same for address, e-mail and phone fields.

## When to avoid

- The form is a custom operation: interceptors never fire for custom operations, so do the mapping in the operation itself.
- The child needs its own full editing UI: use a normal child create instead of flattening.

## Related

- [[interceptor-crud-lifecycle]] — create and update interceptors around the platform call
- [[interceptor-access-control-flags]] — other interceptor-based payload enrichment
