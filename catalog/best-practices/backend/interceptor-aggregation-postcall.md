---
id: interceptor-aggregation-postcall
title: Post-Call Interceptor for Denormalized Aggregation Fields
description: "A post-call interceptor on built-in update operations that keeps a denormalized, sorted, comma-separated name string on an entity in sync with its related collection, and the related transient-member variant for read-time values."
aliases: ["denormalized aggregate maintenance", "aggregated string field"]
keywords: ["interceptor", "postCall", "denormalization", "aggregation", "update", "transient member", "DAO", "mask"]
tags: ["domain:backend", "layer:backend", "project:alba", "project:mlszksz-platform", "status:emerging"]
category: interceptor
status: emerging
projects: [alba, mlszksz-platform]
evidence: ["alba:unrecorded", "mlszksz-platform:unrecorded"]
alternatives: []
related: [interceptor-crud-lifecycle, dirty-check-before-update, permission-denormalization, mask-field-projection, read-tracking-postcall-interceptor]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

A list or search screen needs one display string per row, for example the names of all tags, audiences or result types related to an item. Computing it with a join at read time is slow, and the model's derived members cannot always express it. The practice stores the aggregate on the entity and refreshes it in a `postCall` interceptor after each update of the entity.

## Practice

### Platform: what an interceptor can do here

- `OperationCallInterceptor.postCall(operation, parameterPayload, returnPayload)` runs after the platform's own call. For an update the parameter payload is an `UpdateInstanceCall.UpdateInstanceCallPayload`; the stored instance is `getInstance()` and its id is the `__identifier` key ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract), [aggregation example](../../agent-docs/backend/interceptors.md#data-denormalization-and-aggregation)).
- Interceptors fire only for the built-in behaviour operations (create, update, delete, list, refresh, set/add/remove reference and so on). Custom, mapped and script operations never reach them ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). `getOperations` must name the exact operations; an empty result means all built-in operations, which is rarely wanted here.
- A synchronous interceptor runs inside the operation's transaction, so an exception from `postCall` rolls back the update itself. Only `InterceptorCallBusinessException` may be thrown ([business error from an interceptor](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).

### Project practice: refresh only when the value changed

```java
// Example project code: Entity, EntityDao, EntityMask, Related are generated or project types
@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
        throws InterceptorCallBusinessException {
    if (parameterPayload instanceof UpdateInstanceCall.UpdateInstanceCallPayload update) {
        UUID id = update.getInstance().getAs(UUID.class, "__identifier");
        Entity entity = entityDao.getById(id, EntityMask.entityMask().withAggregated()).orElseThrow();

        String aggregated = entityDao.queryRelated(entity)
                .maskedBy(RelatedMask.relatedMask().withName())
                .selectList().stream()
                .map(Related::getName).sorted()
                .collect(Collectors.joining(", "));

        if (!entity.getAggregated().orElse("").equals(aggregated)) {
            entity.setAggregated(aggregated);
            entityDao.update(entity, EntityMask.entityMask().withAggregated());
        }
    }
    return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
}
```

- Register the interceptor for the update operation of every transfer-object service that edits the entity (one operation name per service, for example an author view and an admin view). The operation name formats are in the [operation FQN reference](../../agent-docs/backend/interceptors.md#operation-fqn-format-reference).
- Load and write with masks so only the aggregate attribute is read and updated ([masks](../../agent-docs/backend/data-access-guide.md#using-masks-projections), [[mask-field-projection]]).
- Sort the names so the string is deterministic, and compare before writing so an unchanged aggregate causes no write ([[dirty-check-before-update]]). The aggregate attribute is optional in the model, so the generated getter returns an `Optional` ([absent, null and empty](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)).
- Variant for values nobody needs to filter on: do not store them. Declare a transient member without a binding on the transfer object and fill it in a `postCall` on the read operations (refresh and list) by putting the value into the returned `Payload` ([transient member pattern](../../agent-docs/backend/interceptors.md#pattern-backend-computed-to-attribute-jql-escape-hatch)). One project computes statistics counters this way, because the model expression language could not express them.

## Rationale

- List screens read one column instead of joining a collection per row, and the value can be sorted and filtered at the database.
- The caller of the update does not know about the aggregate; the interceptor keeps it consistent in the same transaction.
- Cost: extra reads in every update, and the string is stale when the related collection changes through an operation that is not intercepted (for example an add or remove reference operation that is not listed in `getOperations`, or a custom operation). List those operations too, or recompute from a custom operation.
- The transient variant has no staleness and no write, but cannot be used in filters or sort at the database ([why not a view](../../agent-docs/backend/interceptors.md#pattern-backend-computed-to-attribute-jql-escape-hatch)).

## Example

An item entity has three many-to-many relations (audience, curriculum, result types). Each has a stored `...Aggregated` text attribute. Both the author-facing and the admin-facing update operation of the item are intercepted; after each update the three strings are rebuilt from the sorted related names and written only if one of them changed. A second project fills statistics counters (active users in the last 30 days, recent news items) into the payload of the statistics refresh and list operations instead of storing them.

## When to avoid

- When the value is expressible as a derived member in the model: it is then always current and needs no interceptor.
- When the aggregate must change on operations that are not intercepted and you cannot list them all; recompute in the custom operation that changes the data instead.
- When the related collection is large: the `postCall` reads all of it on every update; keep the aggregate small or compute it lazily.

## Related

- [[interceptor-crud-lifecycle]] — the same hook for other create and update side effects
- [[dirty-check-before-update]] — compare before writing
- [[permission-denormalization]] — another stored denormalization
- [[mask-field-projection]] — masks used for the reads and the update
- [[read-tracking-postcall-interceptor]] — a postCall on read operations
