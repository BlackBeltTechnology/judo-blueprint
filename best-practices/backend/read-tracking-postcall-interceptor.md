---
id: "read-tracking-postcall-interceptor"
title: "Read Tracking Post-Call Interceptor with Deduplication"
domain: "backend"
category: "interceptor"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

A post-call interceptor that tracks first-time reads of content (e.g., announcements) per user for analytics and engagement tracking. On refresh operations, the interceptor extracts the current user via VariableResolver, checks for an existing read-tracking audit log entry (deduplication), and creates one if none exists. This pattern provides read analytics without requiring a dedicated tracking entity.

## Structure

```java
@Component(property = { "judo.model.name=AppName" })
public class ReadTrackingInterceptor implements OperationCallInterceptor {

    @Reference VariableResolver variableResolver;
    @Reference AuditLogService auditLogService;
    @Reference AuditLogDao auditLogDao;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // Target refresh/view operations
        return List.of(asmUtils.resolveOperation(
            "App.services.Entity#_refreshInstance...").orElseThrow());
    }

    @Override
    public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
        try {
            String email = variableResolver.resolve(String.class, "ACTOR", "email");
            if (email == null) return returnPayload;

            Payload payload = (Payload) returnPayload;
            String entityId = payload.getAs(Serializable.class, "__identifier").toString();

            // Deduplication check
            long existing = auditLogDao.query()
                .filterByActionType(EnumerationFilter.equalTo(ActionType.ENTITY_READ))
                .filterByEntityId(StringFilter.equalTo(entityId))
                .filterByUserName(StringFilter.equalTo(email))
                .count();

            if (existing == 0) {
                auditLogService.log(ActionType.ENTITY_READ, "Entity", entityId, Map.of());
            }
        } catch (Exception e) {
            log.warn("Failed to track read", e);
        }
        return returnPayload;
    }
}
```

## Examples

### mlszksz-platform
`AnnouncementReadTrackingInterceptor` targets the announcement refresh operation. Extracts current user email via VariableResolver. Queries audit log for existing `ANNOUNCEMENT_READ` entries matching user + announcement ID. Creates audit log entry on first read only. Safe failure: exceptions caught and logged, never propagated. Captures announcement title in details map.

## Trade-offs

- Pros: First-read analytics without dedicated entity, reuses audit log infrastructure, deduplication prevents double-counting, safe failure
- Cons: Extra DB query per view for deduplication, audit log table grows with reads, no page-view counting (only first read), performance impact on high-traffic pages
- Alternative: Dedicated read-tracking entity, client-side analytics (Google Analytics), Redis-based counters

## Related Patterns

- audit-event-trail
- interceptor-aggregation-postcall
- actor-resolution-variable-resolver
