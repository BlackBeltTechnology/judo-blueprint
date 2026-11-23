---
id: read-tracking-postcall-interceptor
title: Read Tracking Post-Call Interceptor with Deduplication
description: Practice that records the first read of an item per user from a postCall interceptor on the built-in refresh operation, checking for an existing audit row so each user is counted once.
aliases: [first read tracking, read receipt, view tracking, announcement read log]
keywords: [read, tracking, postCall, interceptor, deduplication, refresh, audit, analytics, VariableResolver]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: interceptor
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/AnnouncementReadTrackingInterceptor.java"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Know which users have opened an item (for example a published notice) without any change in the client: a `postCall` interceptor on the item's refresh operation writes one event row per user and item. This is a convention that reuses an audit log; the platform only supplies the interceptor hook.

## Practice

### Platform: the interceptor contract the pattern uses

- An interceptor implements `OperationCallInterceptor`, is registered with `@Component(property = { "judo.model.name=<app>" })`, and selects operations in `getOperations(AsmModel)`; an empty result means all built-in operations, never custom ones ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract), [registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)).
- Interceptors fire only for built-in behaviour operations; refresh is one of them, so a read of a single instance through the generated page triggers it. A read through a custom operation, a list or a query does not count as a refresh and is not tracked ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- `postCall` receives the operation, the input payload and the return payload (a `Payload` for refresh, a collection of payloads for lists) and must return the payload it wants to hand on; the returned object becomes the result ([contract table](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). The instance identifier is read from the `__identifier` payload key.
- A synchronous interceptor runs inside the operation's transaction, so an exception from `postCall` rolls back the operation and earlier interceptor writes ([ordering and combining](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)). An `async()` interceptor runs outside the transaction with no context variables, so it cannot read the `ACTOR` variable, and its exceptions are lost; this pattern needs the actor, so it stays synchronous.
- The current user comes from `VariableResolver.resolve(String.class, "ACTOR", "email")` ([[actor-resolution-variable-resolver]]); the actor value exists only when the request carries a principal.
- Error handling: `preCall` and `postCall` declare only `InterceptorCallBusinessException`, and a modeled fault cannot be thrown from an interceptor. See [error handling](../../agent-docs/backend/error-handling-guide.md#exceptions-thrown-from-interceptors).

### Practice notes: record once per user and item

```java
// Example code: AuditLogDao, AuditLogService and ActionType are types
@Component(property = { "judo.model.name=<app>" })
public class ReadTrackingInterceptor implements OperationCallInterceptor {
    @Reference VariableResolver variableResolver;
    @Reference AuditLogService auditLogService;
    @Reference AuditLogDao auditLogDao;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        return List.of(/* the refresh operation of the item, resolved with AsmUtils */);
    }

    @Override
    public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
        try {
            String email = variableResolver.resolve(String.class, "ACTOR", "email");
            if (email == null) return returnPayload;
            String entityId = ((Payload) returnPayload).getAs(Serializable.class, "__identifier").toString();

            long existing = auditLogDao.query()
                .filterByActionType(EnumerationFilter.equalTo(ActionType.ENTITY_READ))
                .filterByEntityId(StringFilter.equalTo(entityId))
                .filterByUserName(StringFilter.equalTo(email))
                .count();
            if (existing == 0) {
                auditLogService.log(ActionType.ENTITY_READ, "Entity", entityId, Map.of());
            }
        } catch (Exception e) {
            log.warn("Failed to track read", e);   // tracking must not break the read
        }
        return returnPayload;
    }
}
```

- Deduplication is a count query on action type, item id and user before each insert.
- Failures are caught and logged so a tracking problem does not fail the read. The docs do not cover the state of the transaction after a failed database statement inside such a catch, so keep the body to the count query and one insert.
- Details such as the item title go into the event's details map.

## Rationale

- First-read analytics come from the existing audit log, with no new entity and no client change.
- The deduplication makes the number a count of distinct readers.
- Costs: one extra count query on every item view, an audit table that grows with every user and item, and only the first read is recorded (no view counts). Reads through lists or custom operations are invisible.

## Example

An announcement is opened by 40 users; the audit table holds 40 read rows for it, one per user, and a report counts them. Opening it a second time adds no row because the count query finds the first.

## When to avoid

- When read counts or repeated views are needed: use a dedicated tracking entity or client analytics.
- When the item is read mainly through lists or a custom operation, since the interceptor never fires there.
- On high-traffic pages where the extra query per view matters; check whether the user is already known with a cheaper lookup.

## Related

- [[audit-event-trail]] — the audit rows this writes into
- [[interceptor-aggregation-postcall]] — another postCall interceptor on refresh
- [[actor-resolution-variable-resolver]] — resolving the current user
