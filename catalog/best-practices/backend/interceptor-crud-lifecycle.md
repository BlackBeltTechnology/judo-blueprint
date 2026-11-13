---
id: interceptor-crud-lifecycle
title: Interceptor as CRUD Lifecycle Hook
description: "Interceptors on the built-in create, update, delete and reference operations that add behaviour the model cannot express: validation and payload shaping in preCall, relation wiring and cascades in postCall, with the platform's operation scope, ordering and error rules."
aliases: ["CRUD interceptor", "create update interceptor", "lifecycle hook"]
keywords: ["interceptor", "CRUD", "preCall", "postCall", "create", "update", "delete", "payload", "transaction", "InterceptorCallBusinessException"]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:alba", "project:park-here", "project:judo-partner", "project:reserve-app", "status:established"]
category: interceptor
status: established
projects: [rackinspect, alba, park-here, judo-partner, reserve-app]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/companydata/companyemail/CompanyEmailCreateInterceptor.java", "alba:unrecorded", "park-here:unrecorded", "judo-partner:unrecorded", "reserve-app:unrecorded"]
alternatives: []
related: [interceptor-global-logging, interceptor-access-control-flags, interceptor-range-override, form-field-flattening, interceptor-call-replacement, interceptor-aggregation-postcall]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

The generated create, update and delete operations cover the plain write. Real applications need more around it: validate a format, turn flat form fields into a nested structure, set a singular relation after create, cascade a change to other entities. An `OperationCallInterceptor` adds this without editing generated code.

## Practice

### Platform: contract and limits

- An interceptor implements `OperationCallInterceptor` with `preCall` (before the platform call, may replace the input payload) and `postCall` (after it, receives the return payload and may replace it), registered as an OSGi component with the property `judo.model.name=<model>` ([contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract), [registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)).
- `getOperations` names the operations by FQN, for example `<model>.services.ServiceContext#_createInstance<Entities>` for create, `#_updateInstance<EntityFQN with underscores>` for update, `#_deleteInstance<...>` and `#_addReference<Relation>` / `#_removeReference` / `#_setReference` for relations ([FQN format](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)). Resolve them once through `AsmUtils` and cache the list.
- Only built-in behaviour operations are intercepted. Custom, mapped and script operations never are, so guards for those belong in the operation itself ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Several interceptors on one operation run in registration order for `preCall` and for `postCall` (not reversed); all run in the operation's transaction, so an exception anywhere rolls back the write, including the DAO writes of earlier interceptors ([ordering](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).
- The only business-level exception an interceptor may throw is `InterceptorCallBusinessException` (REST 422 with `X-Fault`). A field rule on one attribute is a `ValidationException` (400). A raw `RuntimeException` becomes a 500. A generated `<Fault>Exception` from a service must be caught and rewrapped ([business error](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- Payload access: the create payload is `CreateInstanceCall.CreateInstanceCallPayload` (`getInput()`), the update payload `UpdateInstanceCall.UpdateInstanceCallPayload` (`getInput()`, `getInstance()`); the id of a returned payload is its `__identifier` key. `Payload.getAs` returns `null` for an absent key, so do not unbox it ([payload type](../../agent-docs/backend/data-access-guide.md#the-payload-type)).

### Practice notes: what the hooks typically do

```java
// Example code: Entity, EntityDao, Child, ChildDao are generated types
@Override
public Object preCall(EOperation operation, Object parameterPayload)
        throws InterceptorCallBusinessException {
    if (parameterPayload instanceof CreateInstanceCall.CreateInstanceCallPayload create) {
        Payload input = create.getInput();
        // validate, or reshape flat form fields into the nested payload the create expects
    }
    return OperationCallInterceptor.super.preCall(operation, parameterPayload);
}

@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
        throws InterceptorCallBusinessException {
    UUID id = ((Payload) returnPayload).getAs(UUID.class, "__identifier");
    Entity entity = entityDao.getById(id, EntityMask.entityMask()).orElseThrow();
    // set singular relations, cascade, re-validate
    return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
}
```

- `preCall`: validate input (format by regular expression, required flags) and throw the right exception kind; flatten `form_*` fields into a nested payload ([[form-field-flattening]]).
- `postCall` on create: load the created entity by the returned id (with a mask), set singular relations such as a primary or default child, trigger recalculation or validation services. Set only relations that the model declares settable.
- `postCall` on update: cascade, for example normalise names, check uniqueness, recompute denormalized fields ([[interceptor-aggregation-postcall]]) or write an audit entry.
- One variant assigns ownership in the create `postCall`: it resolves the current user through `VariableResolver` and sets the owner relation on the new record ([[actor-resolution-variable-resolver]]).
- Handle create and update in one class with `instanceof` pattern matching on the payload type, and throw `IllegalArgumentException` for an unexpected type.

## Rationale

- Generated CRUD stays generated and regeneration-safe; cross-cutting write rules live in one class per aggregate.
- Interceptors run in the operation's transaction, so a refusal also undoes the write.
- Cost: interceptors work on raw `Payload` maps (no type safety), several of them on one operation depend on registration order, and they are harder to debug than a named custom operation. A custom operation wrapping the write gives more control but loses the generated UI binding.

## Example

Typical sets across applications: an account create validates the primary address in `preCall`, turns flat form fields into a nested address payload, then sets primary, billing and postal relations in `postCall`; a bank-account create checks the account number format in `preCall` and sets the primary relation after; an item update enforces "one favourite per user" in `postCall` and surfaces a `ValidationException`; an account update normalises names, flags duplicates and writes a log entry; a booking create assigns the calling account as owner.

## When to avoid

- For custom, mapped or script operations: interceptors never fire for them; put the logic in the operation.
- For permission checks that must hold for every path: hiding or intercepting is not enough; use the model's access definitions and write guards inside custom operations.
- When the whole create should differ, not just be extended: see [[interceptor-call-replacement]].
- When the work is slow or calls external systems: it runs inside the transaction and holds it open; use an asynchronous interceptor only for work whose result and failure do not matter, because async exceptions are lost.

## Related

- [[interceptor-global-logging]] — log which operations are intercepted
- [[interceptor-access-control-flags]] — per-row flags on list and refresh
- [[interceptor-range-override]] — interception of reference range operations
- [[form-field-flattening]] — flat form fields into nested payloads
- [[interceptor-call-replacement]] — skip the platform call
- [[interceptor-aggregation-postcall]] — denormalized aggregates after update
- [[actor-resolution-variable-resolver]] — resolving the caller
