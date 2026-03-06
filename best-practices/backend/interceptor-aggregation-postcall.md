---
id: "interceptor-aggregation-postcall"
title: "Post-Call Interceptor for Denormalized Aggregation Fields"
domain: "backend"
category: "interceptor"
score: 65.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - mlszksz-platform
---
## Description

A post-call interceptor that automatically maintains denormalized aggregated string fields on an entity after update operations. When related collections (e.g., audiences, curriculums) change, the interceptor queries all related entities, builds sorted comma-separated name strings, and updates the parent entity only if the computed values differ from the current ones. This provides efficient query and display performance without requiring JOINs at read time.

## Structure

```java
@Component(property = { "judo.model.name=AppName" })
public class EntityUpdateInterceptor implements OperationCallInterceptor {

    @Reference EntityDao entityDao;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // Target update operations for the entity
        return Stream.of(
            "App.services.Service1#_updateInstanceApp_services_Service1",
            "App.services.Service2#_updateInstanceApp_services_Service2"
        ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
    }

    @Override
    public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
        UpdateInstanceCallPayload payload = (UpdateInstanceCallPayload) paramPayload;
        UUID id = payload.getInstance().getAs(UUID.class, "__identifier");
        Entity entity = entityDao.getById(id, mask).orElseThrow();

        // Compute aggregated strings from relations
        String aggregated = entityDao.queryRelation(entity).selectList().stream()
            .map(Related::getName).sorted()
            .collect(Collectors.joining(", "));

        // Conditional update only if changed
        boolean shouldUpdate = false;
        if (!entity.getAggregated().orElse("").equals(aggregated)) {
            entity.setAggregated(aggregated);
            shouldUpdate = true;
        }
        if (shouldUpdate) {
            entityDao.update(entity, EntityMask.entityMask());
        }

        return OperationCallInterceptor.super.postCall(op, paramPayload, returnPayload);
    }
}
```

## Examples

### ALBA
`ProductUpdateInterceptor` targets both author and admin product update operations. After product update, queries `queryAudience()`, `queryCurriculum()`, `queryResultTypes()` relations, builds sorted comma-separated name strings, and updates `audienceAggregated`, `curriculumAggregated`, `resultTypesAggregated` fields. Only writes if at least one aggregated field changed.

### mlszksz-platform
`StatisticsActiveUsersInterceptor` targets Statistics refresh and list operations. Post-call computes derived fields that JUEL cannot handle: counts active users (lastLogin within 30 days), recent news/offers/requests/announcements. Sets computed values on Payload directly (`activeUsers`, `recentNews`, etc.). Per-organization statistics also computed via `organizationDao.queryUsers(orgId)`.

## Trade-offs

- Pros: Query performance (no JOINs needed for display), transparent to the operation caller, deterministic sorted output
- Cons: Extra DB queries in postCall for every update, aggregated fields can become stale if relations are modified outside the intercepted operations
- Alternative: Computed database views, model-level derived attributes, or frontend-side aggregation

## Related Patterns

- interceptor-crud-lifecycle
- dirty-check-before-update
- permission-denormalization
