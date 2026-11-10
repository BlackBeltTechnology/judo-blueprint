---
id: mutable-entity-update-pattern
title: Mutable Entity Update Pattern
description: Change a persisted entity by loading it from its DAO, calling setters on the returned object and passing it back to dao.update, optionally with a mask that limits the written fields.
aliases: [fetch-mutate-update, setter then update, in-place entity update]
keywords: [mutable, update, setter, dao, mask, partial update, optimistic locking, __version]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:workflow-poc", "status:established"]
category: data-access
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, ubives, park-here, indamedia-adtrack, judo-partner, workflow-poc]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "alba:unrecorded", "mlszksz-platform:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Update an existing record without a separate update object: the entity returned by the generated DAO is mutable, so the code changes it with setters and persists it with `dao.update`.

## Practice

### Platform: the DAO update call

- Generated DAOs offer `update(entity)` and `update(entity, mask)`. `update` returns the persisted entity, so assign the result when the code continues with it ([DAO operations](../../agent-docs/backend/data-access-guide.md)).
- With a mask, only the fields named in the mask are written ("Pattern 4: Partial Updates" in the [data access guide](../../agent-docs/backend/data-access-guide.md#using-masks-projections)). Without a mask the whole entity is updated.
- Optimistic locking is on by default, but the version check runs only when the update payload contains `__version`; an entity loaded from the DAO and written back carries its version, while a payload rebuilt by hand without `__version` silently skips the guard. A stale version fails the update ([optimistic locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)).
- Fields not included in the mask used to load an entity are `null` ([mask best practices](../../agent-docs/backend/data-access-guide.md#mask-best-practices)). The docs do not say what an unmasked update does with them, so for an entity loaded with a narrow mask pass an update mask naming only the changed fields.

### Project practice: fetch, mutate, update

```java
// Example project code: Entity, EntityDao and EntityMask are generated types
Entity entity = entityDao.getById(id).orElseThrow();

entity.setStatus(NewStatus.VALUE);
entity.setChangedAt(LocalDateTime.now());
entity.setNote(null);                       // clearing a field is a setter call

entityDao.update(entity);                   // whole entity
// or only some fields:
entityDao.update(entity, EntityMask.entityMask().withStatus().withChangedAt());
```

- Nine projects use this cycle for state transitions, timestamps, flags (archive, enable/disable, processed), and metadata.
- Several projects pass a mask when the change touches few fields or when the entity was loaded with a mask; others call `update(entity)` for small entities.
- Batch changes loop over the entities and call `update` for each; one project calls `updateAll` on a collection.
- Operations that receive a transfer object copy its values onto the entity with setters (guarding optional inputs) and then update.
- Updates inside interceptors (for example a last-login time) follow the same cycle; the entity is loaded, changed and saved.

## Rationale

- Simple and readable; no extra update type, and clearing a field is just a null assignment.
- A mask makes the write explicit and cheaper for wide entities, and keeps unrelated fields untouched.
- Cost: nothing stops accidental changes to the loaded object before it is saved, and an unmasked update of a partially loaded entity has undocumented behaviour (see the mask note above).

## Example

A state change in a custom operation: load the record by its identifier, set the new state and a timestamp, update with a mask naming only those two attributes. A cancellation loop does the same for each reservation in a list; a duplicate-detection job sets a flag on each match and saves the group in one `updateAll`. To avoid a write when nothing changed, compare before and after first ([[dirty-check-before-update]]).

## When to avoid

- For a create, use the builder ([[builder-pattern-entity-creation]]); update needs an existing, persisted entity.
- When the entity was loaded with a narrow mask and you would write unloaded fields: use a mask that names only the changed fields.
- When many rows change with one rule, a bulk operation or a model-level action is cheaper than loading and saving each row.

## Related

- [[builder-pattern-entity-creation]] — the creation counterpart
- [[dao-fluent-query-filter]] — how the entity to update is found
- [[mask-field-projection]] — masks for partial reads and writes
- [[dirty-check-before-update]] — skip the write when nothing changed
