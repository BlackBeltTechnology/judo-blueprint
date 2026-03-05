---
id: "soft-delete-archive-pattern"
title: "Soft Delete via Archive Flag Pattern"
domain: "backend"
category: "operation"
score: 35.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - park-here
  - judo-partner
---
## Description

Instead of physically deleting entities, a boolean `isArchived` flag is set to true, preserving the data for historical reference and potential recovery. Related flags (e.g., `isFavorite`) are cleared during archival. Queries throughout the application filter by `isArchived = false` to exclude archived records from normal views. This pattern is especially useful for entities that participate in historical associations (e.g., a car used in past reservations).

## Structure

```java
@Override
public void accept(Entity _this) throws BusinessErrorException {
    Entity entity = service.getEntity(_this);
    entity.setIsFavorite(false);     // Clear related flags
    entity.setIsArchived(true);       // Soft delete
    entityDao.update(entity);
}

// All queries filter out archived records
dao.queryCars(userId)
    .filterByIsArchived(BooleanFilter.isFalse())
    .selectList();
```

## Examples

### ParkHere
`DeleteCarCustomImplementation` sets `isArchived=true` and `isFavorite=false` on the car entity rather than deleting it. Range interceptors (`ReservationInputCarRangeInterceptor`) filter `isArchived=false` to exclude archived cars from dropdown selections.

### judo-partner
`PartnerServices.deletePartner()` sets `isArchived=true` and clears `taxIdentifier` to null (allowing the same tax number to be reused for a new partner). After archival, `setIsDuplicate()` recalculates duplicate name flags excluding archived partners via `filterByIsArchived(BooleanFilter.isFalse())`. Partners are never physically deleted.

## Trade-offs

- Pros: Preserves data history, allows recovery, maintains referential integrity with past records
- Cons: Database grows indefinitely, queries must always include archive filter (easy to forget), no automatic cleanup
- Alternative: Hard delete with cascade, or move to archive table

## Related Patterns

- mutable-entity-update-pattern
- dao-fluent-query-filter
