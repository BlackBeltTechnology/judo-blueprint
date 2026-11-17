---
id: interceptor-call-replacement
title: Interceptor Call Replacement via ignoreDecoratedCall
description: "An interceptor whose ignoreDecoratedCall() returns true so the platform's own create, update or other built-in call is skipped and its preCall supplies the result instead, for example creating a different entity than the model operation would."
aliases: ["replace generated operation", "skip decorated call"]
keywords: ["interceptor", "ignoreDecoratedCall", "preCall", "replace operation", "create", "DAO", "payload"]
tags: ["domain:backend", "layer:backend", "project:alba", "status:single-project"]
category: interceptor
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: []
related: [interceptor-crud-lifecycle, interceptor-global-logging, custom-operation-osgi-component]
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

The generated create (or update) of a transfer object is not what the application needs: the submitted data should become a different entity, or the generated write should not happen at all. An interceptor can replace the built-in operation without touching generated code by telling the dispatcher to skip the platform call and doing the work itself in `preCall`.

## Practice

### Platform: what `ignoreDecoratedCall()` does

- `ignoreDecoratedCall()` defaults to `false`. When it returns `true`, the platform's own DAO call is skipped; the decorated call runs only if no interceptor registered for that operation returns `true` ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).
- With the decorated call skipped, `preCall` must return a payload of the decorated call's **return type**, because that value becomes the operation result. The input payload is not the right return value ([contract table](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). Any other type fails with `IllegalArgumentException`.
- Only built-in behaviour operations can be replaced (create, update, delete, list, refresh, reference operations and so on). Custom, mapped and script operations never reach interceptors ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- The interceptor runs inside the operation's transaction; an exception from it rolls the write back. Refuse with `InterceptorCallBusinessException` only ([business error](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- The platform documents this as the "decoupled service creation" pattern: create the resource in another bounded context in `preCall` and suppress the original ([decoupled service creation](../../agent-docs/backend/interceptors.md#decoupled-service-creation-cqrs-like-pattern)).

### Practice notes: build the replacement from the input

```java
// Example code: SourceEntity, AlternateEntityDao and AlternateEntityForCreate are generated types
@Reference AlternateEntityDao alternateDao;

@Override
public boolean ignoreDecoratedCall() { return true; }   // skip the generated create

@Override
public Object preCall(EOperation operation, Object parameterPayload)
        throws InterceptorCallBusinessException {
    if (parameterPayload instanceof CreateInstanceCall.CreateInstanceCallPayload create) {
        SourceEntity profile = SourceEntity.from(create.getInput());
        AlternateEntity created = alternateDao.create(
                AlternateEntityForCreate.builder()
                        .withEmail(profile.getEmail())
                        .withStatus(profile.getStatus())
                        .build());
        return result(created);   // helper: a Payload shaped like the operation's return type
    }
    return OperationCallInterceptor.super.preCall(operation, parameterPayload);
}
```

- Register the interceptor for exactly the one operation it replaces through `getOperations` (resolve it once and cache it; see the [registration and FQN format](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)).
- The platform guide's own example returns the input payload from `preCall`. Treat that as shortcut code: a caller that reads the result (the generated UI reads the created instance, including its identifier) needs a payload of the return type, so build it from the created entity.
- Optional attributes of the source are copied with null-safe checks; relations are set with the DAO relation methods after creating the entity.
- Put the reason in a comment on the class: the replaced call is silent, and the next developer will otherwise look for the missing row in the generated entity's table.

## Rationale

- No generated code is edited, so regeneration keeps the replacement.
- The user-facing form and operation stay as modeled; only the effect changes, for example bridging a profile form to a user entity of another bounded context.
- Cost: nothing in the model or the generated code reveals that the operation is replaced, and the interceptor owns all of the behaviour, including the result shape the UI expects.

## Example

An admin form creates an admin profile. The generated create would store an admin-profile row; the interceptor for that create operation instead reads the form data (name, role, picture, optional institution), creates a user entity in the main user system through that entity's DAO, sets the institution relation if given, and returns the created instance. No admin-profile row is written.

## When to avoid

- When the behaviour can be a normal custom operation with its own name: a replaced built-in call surprises readers and the generated UI still shows the original entity's labels.
- When you only add behaviour around the call; use `preCall` or `postCall` without `ignoreDecoratedCall` ([[interceptor-crud-lifecycle]]).
- When the operation is custom, mapped or a script operation: interceptors never fire for those, so implement the change in the operation itself.

## Related

- [[interceptor-crud-lifecycle]] — hooks that keep the platform call
- [[interceptor-global-logging]] — a global interceptor to see which operations run
- [[custom-operation-osgi-component]] — the alternative: a named custom operation
