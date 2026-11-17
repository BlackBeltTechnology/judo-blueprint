---
id: soft-delete-archive-pattern
title: Soft Delete via Archive Flag in a Custom Operation
description: "A delete operation sets a boolean archive flag instead of removing the row, clears related flags, and every query and range filters archived rows out."
aliases: [archive instead of delete, isArchived flag, logical delete operation]
keywords: [soft delete, archive, isArchived, custom operation, BooleanFilter, range interceptor, historical reference]
tags: ["domain:backend", "layer:backend", "project:park-here", "project:judo-partner", "status:emerging"]
category: data
status: emerging
projects: [park-here, judo-partner]
evidence: ["park-here:unrecorded", "judo-partner:unrecorded"]
alternatives: [soft-delete-active-flag]
related: [mutable-entity-update-pattern, dao-fluent-query-filter, soft-delete-active-flag, interceptor-range-override, toggle-boolean-operation]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some entities must stay in the database because older records point to them (an item used in past bookings, an account with history). Deleting the row would break those links. The delete action sets an archive flag and tidies related state, and all readers hide archived rows. This entry is the backend side; the model side (flag, defaults, hiding in the UI) is in [[soft-delete-active-flag]].

## Practice

### Platform base

- A custom operation loads the entity through its DAO, sets the flag and persists it with `update`. The entity from the DAO carries its version, so the optimistic-locking check applies ([platform behaviour](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)).
- Queries exclude archived rows with `BooleanFilter.isFalse()` on the generated `filterBy<Attribute>` method; the boolean filter has only `isTrue()` and `isFalse()`. A row where an optional boolean is unset needs the raw JQL filter ([data access guide](../../agent-docs/backend/data-access-guide.md#booleanfilter)).
- The platform delete stays available unless the model turns it off for the entity's transfer objects and accesses. Soft delete does not stop a direct physical delete by itself ([[soft-delete-active-flag]]).
- Interceptors fire only for built-in operations. A custom delete operation is not intercepted, and a range interceptor fires only for reference-range operations, not for plain lists ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). A range interceptor is the boundary for pickers; lists need a filter in the model or in the DAO query.
- Permission checks for the operation belong inside the implementation, since no interceptor protects it.

### Practice notes: archive, clear, filter everywhere

This layer is a convention built on the platform, not a platform feature:

- The delete operation sets `isArchived = true` and clears flags that only make sense on live rows (a favourite flag). It can also free a unique value: One application nulls the tax identifier so the number can be reused for a new account.
- Every query that feeds a normal view adds the archive filter. Forgetting it is the typical bug; put the filtered query in one service method so there is a single place.
- Dropdown ranges exclude archived rows through a range interceptor ([[interceptor-range-override]]).
- Derived computations such as duplicate flags are recalculated after archiving and exclude archived rows.
- Archived rows are never physically removed; plan for the table growth.

```java
// Example code: service and entityDao are generated members
@Override
public void accept(Entity _this) throws BusinessErrorException {
    Entity entity = service.getEntity(_this);
    entity.setIsFavorite(false);     // clear related flags
    entity.setIsArchived(true);      // soft delete
    entityDao.update(entity);
}

// all normal queries filter out archived records
dao.queryCars(userId)
    .filterByIsArchived(BooleanFilter.isFalse())
    .selectList();
```

## Rationale

- History and referential integrity stay intact, and an archived row can be restored.
- The cost is that every reader must filter, the database grows, and nothing cleans it up.

## Example

- One application: the delete-item operation sets `isArchived` to true and `isFavorite` to false instead of deleting. The range interceptor for the item picker of a booking input filters on `isArchived = false`.
- Another application: the delete-account service method sets `isArchived` and clears the tax identifier. It then recalculates the duplicate-name flags, excluding archived accounts with the archive filter. Accounts are never physically deleted.

## When to avoid

- Nothing references the entity and you have no recovery need: delete it, optionally with a cascade through composition.
- Privacy rules require real erasure: an archive flag keeps personal data.
- The record has more than two states: use a status enumeration ([[soft-delete-active-flag]]).

## Related

- [[soft-delete-active-flag]] — the model-level flag and how to hide rows in lists and pickers
- [[mutable-entity-update-pattern]] — the update call used to set the flag
- [[dao-fluent-query-filter]] — the filter API for excluding archived rows
- [[interceptor-range-override]] — keeping archived rows out of dropdowns
- [[toggle-boolean-operation]] — a generic flag-toggling operation
