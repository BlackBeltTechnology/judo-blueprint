---
id: entity-re-fetch-pattern
title: Entity Re-fetch at Operation Start
description: In a bound custom operation, load the entity again through its DAO with a mask before using it, and fail clearly when it is gone.
aliases: [re-fetch this, reload bound instance, getById at start]
keywords: [re-fetch, getById, bound operation, _this, identifier, mask, Optional, orElseThrow, NotFoundException, stale]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:workflow-poc", "status:established"]
category: operation
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, park-here, indamedia-adtrack, judo-partner, workflow-poc]
evidence: ["trivia:unrecorded", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/_default_transferobjecttypes/entities/unit/ToggleActiveCustomImplementation.java", "alba:unrecorded", "mlszksz-platform:application/app/src/main/java/hu/blackbelt/mlszksz/platform/mlszkszplatform/custom/mlszkszplatform/services/admin/admindashboard/DeleteUserCustomImplementation.java", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded"]
alternatives: []
related: [dao-fluent-query-filter, state-lifecycle-operation]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A bound custom operation receives `_this` as a transfer object of the declaring type. Business logic usually needs persisted entity state: current values, a state field, related data. Load the entity again from the DAO by the identifier of `_this` at the start, work on that, and handle "not found" deliberately.

## Practice

### Load the entity from `_this.identifier()`

Call `dao.getById(_this.identifier(), mask)` first. The identifier of `_this` is the reliable part of the bound instance. When `_this` is a service-layer type, the entity DAO wants an entity-layer type, and `getById` is also the conversion (see [Converting Between Layers](../../agent-docs/backend/type-system-guide.md#converting-between-layers)). Use `adaptTo` only when you need no check and no data (see [[identifier-adaptation-pattern]]).

### Pass a mask

`getById` without a mask loads all fields. List only what the logic reads and writes. Fields outside the mask come back `null` or empty, so read only masked fields (see [Using Masks](../../agent-docs/backend/data-access-guide.md#using-masks-projections)). An empty mask is the cheapest existence check.

### Fetch only what you need

When the operation needs only the identity of the entity, for example to pass it on to another call, re-fetch with an empty or minimal mask. One application does this because an unmasked `getById` of a transfer object with aggregating derived members over sub-collections failed at runtime with "Not supported yet". The platform cause is not verified in the agent-docs (*verify*); treat the narrow mask as a workaround and a cheaper read, not as a documented rule.

### Treat the Optional properly

`getById` returns an `Optional`. A bare `.get()` throws `NoSuchElementException`, which the dispatcher wraps as a generic 500 (see [How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)). Choose the outcome on purpose:

- `orElseThrow()` when a missing instance is a programming error.
- A `NotFoundException` built with a `ValidationResult` (code, level, location) for a 404 the client can read.
- A fault declared on the operation, if the UI should show a typed message. Declare it on the model operation or the generated interface has no `throws` clause (see [Modeled Faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).

Helpers such as an `ExceptionUtils` or a `BusinessErrorException` are example code, not platform API. Translate them to the mechanisms above.

### Re-fetch again after your own writes

A loaded DTO is a copy. After code of yours changes the persisted entity (deleting a child, a service call), the copy you hold no longer shows it. Load again before further decisions, and use the object returned by `update` rather than the old one.

### Concurrency is a separate concern

The re-fetch gives current data at the moment of reading, not protection against a concurrent writer. The platform's optimistic lock checks the version only when the update payload contains `__version`, so omitting it disables the guard (see [Optimistic Locking and `__version`](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)). Do not describe the re-fetch as a lock.

## Rationale

- Logic runs on persisted state, whatever the caller's object contained.
- The mask keeps the extra read small. The cost is one more query per call.
- Limit: when the operation delegates to a service that loads the entity itself, a second re-fetch in the operation is waste. Re-fetch where the data is used.

## Example

- Every bound operation starts with `_this = itemDao.getById(_this.identifier()).get()`.
- Several toggle operations use `orElseThrow()` and then flip a flag.
- Product operations load with a mask for the state attribute and convert the identifier to the entity type in the same call.
- Some applications: the re-fetch sits in service methods the operations delegate to.
- A workflow example: the upload operation re-fetches at the start and again after deleting an old version.

## When to avoid

- The operation needs only the identifier, for example it passes `_this` to a service that loads what it needs.
- A list operation touching many instances: query with a mask once instead of calling `getById` per row.

## Related

- [[dao-fluent-query-filter]] — query builder for loading related data
- [[state-lifecycle-operation]] — the state-changing operations that start with a re-fetch
