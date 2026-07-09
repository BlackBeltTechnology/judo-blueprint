---
id: "guarded-delete-with-deactivate-fallback"
title: "Guarded Hard-Delete with Deactivate Fallback"
domain: "backend"
category: "operation"
score: 31.0
usage_count: 1
alternative_count: 2
first_seen: "2026-07-09"
last_updated: "2026-07-09"
projects:
  - rackinspect
alternatives:
  - guard-clause-delete
  - soft-delete-active-flag
---
## Description

A retirement strategy where an entity exposes **two explicit, complementary user actions**: a guarded hard-`delete` and a Boolean `active` + `toggleActive`. The delete is allowed **only when the entity is not referenced** by audit-critical data; if it is referenced, the operation raises a **modeled business fault** (HTTP 422, so the reason reaches the UI) and does **not** delete. Referenced records are retired instead via `toggleActive` (deactivate). Deleting a "clean" (unreferenced) record cascades to its composition children.

Unlike [guard-clause-delete](../model/guard-clause-delete.md) (which returns silently on a blocked delete), this pattern **fails loudly with a business error** so the frontend can tell the user *why* the delete was refused and steer them to deactivate.

Also supports a **transitive guard**: a parent entity (e.g. `Warehouse`) is deletable only when none of its composition children (`racks`) are referenced — implemented as a single existence check over the children, not per-child loops.

## Structure

```java
// Service delegate (in application/services or app/, never internal/)
public void deleteRack(Rack rack) throws BusinessErrorException {
    Rack entity = rackDao.getById(rack.identifier().getIdentifier()).orElseThrow(
        () -> ExceptionUtils.createBusinessErrorException("RACK_NOT_FOUND", i18n.rack_not_found(id)));
    if (isReferencedByRegistryHeader(entity)) {            // referential guard
        throw ExceptionUtils.createBusinessErrorException("RACK_IN_USE", i18n.rack_in_use());
    }
    rackDao.delete(entity);   // composition children cascade automatically
}
// Transitive parent guard: block if ANY child rack is in use
boolean anyRackInUse = warehouseDao.queryRacks(entity).selectList().stream()
        .anyMatch(r -> isReferencedByRegistryHeader(r));
```

Model shape:
- Boolean `active` (required, `defaultExpression="true"`) + `toggleActive` INSTANCE op (+ MAPPED service delegate).
- Guarded `delete<Entity>` INSTANCE op declaring `fault BusinessError` (NOT `GenericOperationError` — see related pattern).
- Thin `*CustomImplementation` in `app/` delegating to a service in `common`/`services`.

## Examples

### RackInspect
`EntityLifecycleService.deleteRack` / `deleteWarehouse` guard against `RegistryHeader.rack` references (the FaultRegistry audit link). Rack guard = "no RegistryHeader points at this rack"; Warehouse guard = transitive "no child rack is referenced". Blocked delete raises `RACK_IN_USE` / `WAREHOUSE_IN_USE` as a `BusinessErrorException`; the record is kept and the user deactivates it via `toggleActive` instead. `Partner` is never deletable — it only exposes `toggleActive` (no delete Access/op created at all).

## Trade-offs

- Pros: never orphans audit history; the UI receives an actionable reason (business fault, 422) instead of a silent no-op or an opaque 500; delete and deactivate stay two clear user intents.
- Cons: two actions to reason about; cascade delete of a clean record is irreversible (acceptable because "clean" = never used in audit data).
- Prefer when: some records are safely removable but many are referenced by historical/audit data that must be retained.

## Related Patterns

- [guard-clause-delete](../model/guard-clause-delete.md) — silent early-return variant (no user-facing reason)
- [soft-delete-active-flag](../model/soft-delete-active-flag.md) — the `active` flag half of this pattern
- [business-error-vs-generic-operation-error](business-error-vs-generic-operation-error.md) — why the guard must raise a *business* fault
