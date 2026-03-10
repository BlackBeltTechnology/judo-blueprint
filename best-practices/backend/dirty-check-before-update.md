---
id: "dirty-check-before-update"
title: "Dirty-Check Before Update to Avoid Unnecessary Writes"
domain: "backend"
category: "data-access"
score: 71.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - alba
---
## Description

Before persisting an entity update, snapshot the entity state, perform modifications, then compare the before and after states. Only issue the DAO update if the entity actually changed. This avoids unnecessary database writes when cascading operations may not actually modify the entity. Uses `entity.toMap()` for snapshot comparison or simple field-level equality checks.

## Structure

```java
// Snapshot before modifications
Map<String, Object> before = new HashMap<>(entity.toMap());

// Perform modifications
entity.setField1(computedValue1);
entity.setField2(computedValue2);
// ... potentially many fields set conditionally

// Only persist if something changed
if (!before.equals(entity.toMap())) {
    entityDao.update(entity, EntityMask.entityMask());
}
```

## Examples

### RackInspect
`RecalculatePermissionsCustomImplementation` iterates all users and recalculates 22 permission boolean fields from roles. Uses `new HashMap<>(user.toMap())` snapshot before setting flags, then `!userState.equals(user.toMap())` guard before `userDao.update()`. Avoids unnecessary writes when role changes do not affect a particular user's permissions.

### ALBA
`ProductUpdateInterceptor` computes aggregated strings from related entities then checks field-by-field: `if (!product.getAudienceAggregated().orElse("").equals(audienceAggregated)) { product.setAudienceAggregated(audienceAggregated); shouldUpdate = true; }`. Only calls `productDao.update()` if at least one aggregated field changed.

## Trade-offs

- Pros: Reduces database writes in cascade scenarios, simple Map comparison, works with any entity type
- Cons: `toMap()` creates a full copy (memory overhead), Map equality may have edge cases with null vs absent keys
- Alternative: Track individual field changes manually, or rely on database-level change detection

## Related Patterns

- mutable-entity-update-pattern
- permission-denormalization
