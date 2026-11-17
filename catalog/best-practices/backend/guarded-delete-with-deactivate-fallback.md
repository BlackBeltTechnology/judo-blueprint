---
id: guarded-delete-with-deactivate-fallback
title: Guarded Hard-Delete with Deactivate Fallback
description: "An entity offers a hard delete allowed only when nothing references it (otherwise a modeled business fault) and a separate active toggle to retire referenced records."
aliases: [delete or deactivate, referential delete guard, loud delete guard]
keywords: [delete, guard, deactivate, toggleActive, business fault, referential integrity, audit, transitive guard]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: operation
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/EntityLifecycleServiceImpl.java"]
alternatives: [guard-clause-delete, soft-delete-active-flag]
first_seen: 2026-07-09
last_updated: 2026-11-10
---
## Intent

An entity exposes two explicit, complementary user actions: a guarded hard `delete` and a Boolean `active` with a `toggleActive` operation. The delete runs only when the entity is not referenced by audit-critical data. If it is referenced, the operation raises a modeled business fault (HTTP 422, so the reason reaches the UI) and deletes nothing; the user retires the record with `toggleActive` instead. Unlike [[guard-clause-delete]], which returns silently on a blocked delete, this fails loudly so the frontend can tell the user why and steer them to deactivate.

## Practice

### Platform base

- The generated DAO of a mapped, non-abstract type offers `getById`, `existsById`, `delete` and per-relation `query...()` accessors ([generated DAO behaviour](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)).
- A refusal the user must see is a modeled fault declared on the operation, thrown as the generated checked exception; it reaches the client as 422 with `X-Fault` ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults), [[business-error-vs-generic-operation-error]]).
- A custom-implemented operation is not intercepted: interceptors fire only for the built-in create/update/delete/reference operations ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). The guard therefore has to live in the implementation itself, and the built-in generated delete would bypass it, so the guarded delete is a custom operation and the entity must not also expose the generic delete to clients (*verify* that access `deleteable` is off).
- Cascade of composition children on `delete` is stated by one application as automatic; the agent-docs do not describe it, *verify*.

### Practice notes: guard, fault, deactivate

This layer is a convention built on the platform, not a platform feature:

- Model shape: a required Boolean `active` with default true and an instance operation `toggleActive`; an instance operation `delete<Entity>` that declares the modeled business fault; a thin custom implementation delegating to a service in the application's common module.
- The service loads the entity, runs the referential guard, throws the business fault with a machine code such as `ITEM_IN_USE` and a localized message, otherwise deletes. A not-found case uses the same fault style.
- Transitive guard: a parent (a container) is deletable only when none of its composition children (items) is referenced, done as one existence check over the children instead of a per-child loop.
- An entity that must never be removed (an account) gets only `toggleActive`, and no delete operation or access is created for it.

```java
// Example code: itemDao is a generated DAO, ExceptionUtils and i18n are helpers
public void deleteItem(Item item) throws BusinessErrorException {
    Item entity = itemDao.getById(item.identifier().getIdentifier()).orElseThrow(
        () -> ExceptionUtils.createBusinessErrorException("ITEM_NOT_FOUND", i18n.item_not_found(id)));
    if (isReferencedByAuditHeader(entity)) {            // referential guard
        throw ExceptionUtils.createBusinessErrorException("ITEM_IN_USE", i18n.item_in_use());
    }
    itemDao.delete(entity);   // composition children cascade (observed in practice)
}
// Transitive parent guard: block if ANY child item is in use
boolean anyItemInUse = containerDao.queryItems(entity).selectList().stream()
        .anyMatch(r -> isReferencedByAuditHeader(r));
```

## Rationale

- Audit history is never orphaned; the UI receives an actionable reason instead of a silent no-op or an opaque 500; delete and deactivate stay two clear intents.
- Cost: two actions to reason about, and cascade delete of a clean record is irreversible (acceptable because clean means never used in audit data).
- Fits when some records are safely removable but many are referenced by historical data that must be kept.

## Example

A lifecycle service guards `deleteItem` and `deleteContainer` against `AuditHeader.item` references (the audit link). The item guard is "no audit header points at this item"; the container guard is "no child item is referenced". A blocked delete raises `ITEM_IN_USE` or `CONTAINER_IN_USE`, the record stays, and the user deactivates it with `toggleActive`. An account can only be deactivated.

## When to avoid

- The user needs no explanation for a refused delete: the silent [[guard-clause-delete]] is simpler.
- Every record is referenced or none is: a pure [[soft-delete-active-flag]] or plain delete suffices.
- A failure that belongs to an input field: use a validation exception instead.

## Related

- [[guard-clause-delete]] — silent early-return variant with no user-facing reason
- [[soft-delete-active-flag]] — the active-flag half of this pattern
- [[business-error-vs-generic-operation-error]] — why the guard raises a modeled business fault
