---
id: interceptor-range-override
title: Range Interceptor for Context-Filtered Dropdowns
description: "A post-call interceptor on the reference range operation that replaces the dropdown or autocomplete options with a query filtered by the owner's current form values, and that is the server-side boundary for relations whose range exposes all instances."
aliases: ["range interceptor", "dependent dropdown", "reference range override"]
keywords: ["interceptor", "range", "getRangeReference", "dropdown", "autocomplete", "owner", "pagination", "security boundary"]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:park-here", "status:emerging"]
category: interceptor
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/faultregistry/elementfaultinput/ElementFaultInputRepairTypesRangeInterceptor.java", "park-here:unrecorded"]
alternatives: []
related: [interceptor-crud-lifecycle, interceptor-access-control-flags, interceptor-security-filter-validation]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

Options for a relation field (a dropdown or autocomplete) often depend on another value on the same form: only the codes of the chosen element, only free resource slots for the chosen days, only non-archived items of the current user. A range interceptor replaces the options the platform returns with a query that uses the current form context.

## Practice

### Platform: what a range interceptor sees

- Range and choice lookups are generated operations (`getRangeFor<Name>` at the REST level, `_getRangeReference<Relation>` as the interceptable operation) whose input carries the `owner` instance and, for mapped references, a `queryCustomizer` ([range operations](../../agent-docs/backend/platform-behavior-reference.md#range-and-choice-operations)). The REST verb is `~range`; the `X-Judo-MarkSelectedRangeItems` header marks already attached items.
- Range interceptors fire **only** on the `_getRangeReference*` operations (reference range), not on plain list or query operations such as `~list` ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Values outside the allowed range are rejected with `NOT_ACCEPTED_BY_RANGE` (same reference). Choosing an option the interceptor hid therefore also fails on save.
- Security: for a relation whose range type exposes every instance (`rangeType=ANY`) a read-only attribute does not stop enumeration, so the range interceptor is the server-side boundary. Model `min`/`max` bounds are UI-only and not enforced on the server ([same section](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Return a payload collection that has the shape the original call returns; the `postCall` result replaces it. The returned payloads carry the `__selected` marker in the range path ([reserved payload keys](../../agent-docs/backend/platform-behavior-reference.md#reserved-payload-keys)).

### Practice notes: re-query with the owner context

```java
// Example code: ParentDao, Entity and the payload helper are generated types
@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
        throws InterceptorCallBusinessException {
    var range = (GetReferenceRangeCall.GetReferenceRangeCallPayload) parameterPayload;
    Payload owner = range.getOwner();
    UUID ownerId = owner.getAs(UUID.class, "relatedEntity.__identifier");   // null when the user has not chosen yet
    if (ownerId == null) {
        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
    List<Entity> filtered = parentDao.queryRelation(parentDao.getById(ownerId).orElseThrow())
            .filterBy(originalFilter)          // keep the client's own filter, order and seek
            .orderBy(attribute, order)
            .selectList(limit, lastItem, isReverse);
    return toPayloads(filtered);               // helper
}
```

- Keep the client's filter, ordering and pagination from the `queryCustomizer`: the range operation is called while the user types and pages, and a replacement that ignores them breaks autocomplete.
- Map attribute names for `orderBy` carefully; applications converted camelCase names to the upper-snake enum names of the generated attribute and found that fragile.
- Handle an owner that has no value for the controlling field yet (return the original range or an empty one).
- Resolve the current user once and filter by ownership where options are per user ([[actor-resolution-variable-resolver]]).
- The operation name is `<model>.services.<Service>#_getRangeReference<Relation>`; resolve and cache it ([FQN format](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference)).

## Rationale

- Context-sensitive options need no frontend code and reuse the generated form.
- The check is on the server, so it also guards against clients that call the API directly.
- Cost: raw payload handling, manual pagination and sorting, and a query that can drift from the model's own range definition. When the filter can be expressed as the relation's range in the model, prefer that.

## Example

A booking form offers item, resource slot and period. The item range interceptor returns only the current user's non-archived items. The slot range interceptor picks the "free slots for one day" or "for several days" query by booking type, excludes exclusive slots for non-admins, and keeps the client's filter and paging. A profile form restricts preferred slots to those the user may access.

## When to avoid

- When the model's range expression can state the restriction: it is simpler and visible in the model.
- To restrict plain lists or queries: this interceptor does not run there; use access definitions or a list interceptor ([[interceptor-security-filter-validation]]).
- For validation of submitted values beyond the range: add a `preCall` on create and update ([[interceptor-crud-lifecycle]]).

## Related

- [[interceptor-crud-lifecycle]] — validation and relation wiring on writes
- [[interceptor-access-control-flags]] — per-row flags on lists
- [[interceptor-security-filter-validation]] — restricting list queries
- [[actor-resolution-variable-resolver]] — resolving the caller for per-user options
