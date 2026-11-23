---
id: interceptor-template-postcall
title: Post-Call Interceptor for Data Stripping/Modification
description: "A post-call interceptor on the template or refresh read operations that removes or rewrites fields in the returned Payload before it reaches the client, to keep internal configuration and user lists out of a screen; payload-level only, not an access rule."
aliases: ["strip fields from response", "payload scrubbing", "template interceptor"]
keywords: ["interceptor", "postCall", "template", "getTemplate", "refresh", "payload", "strip", "sensitive data"]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:park-here", "status:emerging"]
category: interceptor
status: emerging
projects: [trivia, park-here]
evidence: ["trivia:unrecorded", "park-here:unrecorded"]
alternatives: []
related: [interceptor-global-logging, interceptor-security-filter-validation, interceptor-crud-lifecycle, mask-field-projection]
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

A screen receives a transfer object that contains more than it should show: an internal template configuration, a list of other users, a status flag. A `postCall` interceptor on the read operation edits the returned `Payload` before the client gets it.

## Practice

### Platform: where and how

- Built-in read operations are interceptable: getTemplate, refresh, list/query, getMetadata and others. Custom, mapped and script operations are not ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- `postCall` gets the input and the return payload (a `Payload`, or a collection of payloads for list operations); what it returns becomes the result ([contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). `Payload` is a map with typed accessors (`getAs`, `getAsPayload`, `getAsCollectionPayload`) ([payload type](../../agent-docs/backend/platform-behavior-reference.md#payload-type)).
- A `postCall` that enriches the payload is also the documented way to fill a transient transfer-object member that has no binding ([transient member pattern](../../agent-docs/backend/interceptors.md#pattern-backend-computed-to-attribute-jql-escape-hatch)); stripping is the same mechanism in the other direction.
- Operations are named by FQN, for example `<model>.services.<Service>#_getTemplate<Entity>` or `#_refreshInstance...`; resolve once and cache ([FQN format](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)).
- Instance flags such as `__updateable` and `__deleteable` are separate payload metadata ([[interceptor-access-control-flags]]).

### Practice notes: remove what the screen must not carry

```java
// Example code: the operation FQN, relation and field names are application specific
@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
        throws InterceptorCallBusinessException {
    Payload payload = (Payload) returnPayload;
    Collection<Payload> items = payload.getAsCollectionPayload("nestedRelation");
    if (items != null) {
        for (Payload item : items) {
            item.remove("internalConfig");
            item.remove("accessedUsers");
        }
    }
    return returnPayload;
}
```

- Target only the operations that return the object (for example the template and refresh operations of the same transfer object), otherwise the data leaks through the one you forgot.
- Check for absent keys: `getAsCollectionPayload` can return `null`.
- The removed data cannot be recovered downstream, so do not remove what a later interceptor needs. Interceptors for one operation run in registration order and see each other's changes ([ordering](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).
- The removal happens after the data was loaded; it hides the field from the response but does not stop the database read.

## Rationale

- Hides internal configuration and other users' data without changing the operation or the model.
- Cost: field names are strings, the code is not type-safe, and the data is still read. This is a presentation filter, not an authorization mechanism.

## Example

A user-settings screen shows the sites a user may access. The template operation of the settings object returns, for each site, an internal e-mail template, the list of users with access and an active flag. The interceptor removes those three keys from each site payload, so the page shows only what it needs. A second variant keeps the same class as a commented-out starting point for new interceptors.

## When to avoid

- When the field should never leave the server: model a transfer object that does not contain it, or use a narrower mask or view, so it is not loaded at all ([[mask-field-projection]]).
- When the data must be protected, not just hidden from one screen: other operations on the same data (list, refresh) still return it unless they are intercepted too.
- For custom operations: interceptors do not fire there; shape the result in the operation.

## Related

- [[interceptor-global-logging]] — find the operation names
- [[interceptor-security-filter-validation]] — guard the request side
- [[interceptor-crud-lifecycle]] — hooks on writes
- [[interceptor-access-control-flags]] — per-row update and delete flags
- [[mask-field-projection]] — load only the needed fields
