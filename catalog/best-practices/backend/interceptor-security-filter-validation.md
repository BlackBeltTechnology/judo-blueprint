---
id: interceptor-security-filter-validation
title: Security Filter Validation Interceptor
description: "A pre-call interceptor on selected list operations that checks the client-supplied query filter against an allowed pattern and refuses the call otherwise, to stop enumeration of data the actor may not list; an application guard on top of the platform's access rules."
aliases: ["list filter guard", "query filter allow-list"]
keywords: ["interceptor", "security", "filter", "list", "preCall", "enumeration", "queryCustomizer", "regex", "InterceptorCallBusinessException"]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: interceptor
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [interceptor-global-logging, interceptor-template-postcall, interceptor-range-override, interceptor-crud-lifecycle]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

A client of the generated API can send its own filter with a list call. If an actor may list a type only by one key (for example the tests of a given id), the server must refuse any other filter, otherwise the actor can enumerate everything the list operation can reach. A pre-call interceptor validates the filter before the platform runs the query.

## Practice

### Platform: what is available

- List and query calls are built-in operations, so a `preCall` interceptor registered for the exact list operation fires before the query. Custom, mapped and script operations never reach interceptors ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- The list call payload carries the `QueryCustomizer`; its `filter` is a JQL expression string from the client ([low-level DAO and QueryCustomizer](../../agent-docs/backend/data-access-guide.md#low-level-dao-and-querycustomizer)). `preCall` returns the payload (possibly changed); the returned object must be assignable to the expected payload type ([contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).
- Refuse with `InterceptorCallBusinessException`: the dispatcher turns it into a 422 with `X-Fault` and the exception's `errorCode`. A raw `RuntimeException` becomes a generic 500 ([business error](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- Range interceptors do not cover lists: they fire only on `_getRangeReference*` operations ([[interceptor-range-override]]).
- Where the model can express the restriction (an access filter on the actor's relation), that is the primary mechanism; this interceptor is an additional guard.

### Practice notes: allow-list the filter with a pattern

```java
// Example code: the operation FQN and the pattern are application specific
@Override
public Object preCall(EOperation operation, Object parameterPayload)
        throws InterceptorCallBusinessException {
    var list = (ListCall.ListCallPayload<?>) parameterPayload;   // payload type of the list call
    String filter = list.getQueryCustomizer().getFilter();
    if (filter == null || !ALLOWED.matcher(filter).matches()) {  // e.g. only a lookup by one uuid
        throw new InterceptorCallBusinessException(
                "<app>.services.QueryNotAllowed", "QUERY_NOT_ALLOWED",
                Map.of("message", "Unauthorized query pattern"), null, null);
    }
    return OperationCallInterceptor.super.preCall(operation, parameterPayload);
}
```

- Register only the list operations that need it (`getOperations`, resolved once through `AsmUtils` and cached).
- Reject when the filter is absent or not matching; accept only a closed pattern, never a blacklist.
- Use the FQN of a modeled fault transfer object as the exception `type`, so the frontend can translate it; the first version threw a raw exception that the client saw as a 500.
- Test with a hand-made request: the generated UI never sends a hostile filter, so only API-level tests prove the guard.

## Rationale

- One small class blocks enumeration for a list the actor must only use with a specific key.
- It runs on the server, so it holds for any client.
- Cost: regular-expression validation of a JQL string is brittle (any new legitimate filter shape needs a pattern change), and the operation names are hard-coded.

## Example

A restricted actor may list records only by id. The interceptor for that actor's list operation accepts a filter of the form `this.id=="<uuid>"` and rejects every other filter, so the actor cannot list all records or use wildcard filters.

## When to avoid

- When an access definition or a mapped relation can limit what the actor sees; do that in the model.
- When the filters are legitimately free-form (search screens): a pattern guard will block them; scope by actor instead ([[actor-resolution-variable-resolver]]).
- For custom operations: interceptors do not run there; check inside the operation.

## Related

- [[interceptor-global-logging]] — find the list operation names
- [[interceptor-template-postcall]] — strip data on the way out
- [[interceptor-range-override]] — the boundary for reference ranges
- [[interceptor-crud-lifecycle]] — guards on writes
- [[actor-resolution-variable-resolver]] — scope by the calling actor
