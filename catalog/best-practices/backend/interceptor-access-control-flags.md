---
id: interceptor-access-control-flags
title: Access Control via __updateable/__deleteable Payload Flags
description: "Post-call interceptors on built-in list and refresh operations set __updateable and __deleteable to false on returned payloads so the generated UI disables edit and delete per record; the server must still enforce the rule separately."
aliases: [row-level read-only, per-record update flag, updateable deleteable payload flags]
keywords: [access control, __updateable, __deleteable, payload, flags, postCall, interceptor, read-only]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:judo-partner", "status:emerging"]
category: interceptor
status: emerging
projects: [rackinspect, judo-partner]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/jobsheet/jobsheetitem/JobSheetInputItemListInterceptor.java", "judo-partner:unrecorded"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

The model's updateable and deleteable settings are per relation or entity, not per record. When a record becomes read-only for a business reason (its parent is no longer a draft, the user is not an administrator), a post-call interceptor sets per-record flags in the outgoing payload and the generated UI disables the edit and delete actions for that row.

## Practice

### Platform base

Response payloads of mapped transfer objects carry `__updateable` and `__deleteable`, and clients use them to enable or disable row actions ([REST wire contract](../../agent-docs/backend/platform-behavior-reference.md)). The e2e docs give the precedence: a model flag of `false` disables the action always; a model flag of `true` with a record-level `false` disables it for that record; a record-level `true` or absent flag leaves it enabled ([runtime override via JSON](../../agent-docs/e2e-testing/language-independent-testing.md)). A postCall interceptor receives the call's return payload (a `Payload` or a collection of payloads), may change it, and the returned object becomes the result ([interceptor contract](../../agent-docs/backend/interceptors.md)). Interceptors fire only for built-in operations such as list, query and refresh, and an interceptor is registered with `judo.model.name=<model>` and the operations it targets.

### Practice notes: row-level read-only by interceptor

- Register one interceptor per transfer object that needs it, targeting its list and refresh operations (the same rule in both, otherwise the row and its detail page disagree).
- In `postCall`, evaluate the business condition and put `false` under `__updateable` and `__deleteable`. For list operations the return is a collection of payloads, for refresh a single payload.
- Share the condition between the list and refresh interceptors in one method, to avoid duplicated rules.
- Only ever set a flag to `false`. Leave the others untouched so the model rule still applies.

```java
// Example code
@Override
public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
    Collection<Payload> items = returnPayload instanceof Payload p ? List.of(p) : (Collection<Payload>) returnPayload;
    for (Payload item : items) {
        if (isReadOnly(item)) {
            item.put("__updateable", false);
            item.put("__deleteable", false);
        }
    }
    return OperationCallInterceptor.super.postCall(op, paramPayload, returnPayload);
}
```

### The flags are not security

The flags only drive the UI. An API client can still call update and delete. The interceptor guide states that hiding a UI button does not protect an operation: enforce the same rule in a `preCall` interceptor on the built-in update and delete operations (see [[interceptor-crud-lifecycle]]), and for custom operations inside the implementation, since interceptors never run for custom operations.

## Rationale

- Row-level state-dependent behavior without changes to the generated frontend.
- Cost: payload manipulation is untyped, list and refresh must both be implemented, and the rule is duplicated by the enforcing `preCall`.
- Alternatives: model-level access expressions where the rule can be expressed there, or custom frontend logic.

## Example

- One application: five interceptors on list and refresh operations. A detail element becomes read-only when its owning record is not a draft, generated instances are locked for edit and delete, and work items are locked when a completion flag is set.
- One interceptor covers list and refresh operations across accounts, addresses and contacts. It resolves the current user through the variable resolver (actor e-mail) and, for a non-administrator, sets both flags to false on single and list results ([[actor-resolution-variable-resolver]]).

## When to avoid

- The rule depends on the user and can be expressed by the model's access rules: use those, since they also enforce on the server.
- You need to prevent the change, not just hide the action: add the `preCall` check.

## Related

- [[interceptor-crud-lifecycle]] — enforce the same rule before update and delete
- [[interceptor-range-override]] — interceptor on reference range operations
- [[actor-resolution-variable-resolver]] — resolving the current user in an interceptor
