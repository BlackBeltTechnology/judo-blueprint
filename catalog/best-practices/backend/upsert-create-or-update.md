---
id: upsert-create-or-update
title: Upsert Pattern (Create or Update)
description: A custom operation or service checks with a DAO query whether a singleton or keyed entity exists, then creates it when absent and updates it when present, so first use and later use go through the same call.
aliases: [update or create, create or update, singleton upsert, idempotent import, find or create]
keywords: [upsert, create or update, singleton, configuration, idempotent, DAO, selectOne, query, mask, optimistic locking, race condition]
tags: ["domain:backend", "layer:backend", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "status:emerging"]
category: operation
status: emerging
projects: [park-here, indamedia-adtrack, judo-partner]
evidence: ["park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded"]
alternatives: []
related: [init-data-seeding, mutable-entity-update-pattern, builder-pattern-entity-creation, dao-fluent-query-filter, mask-field-projection]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some data may not exist yet on first use: a single configuration record, a daily cost row per item, a reference entry from an import file. One operation or service method handles both cases. It looks the record up, then creates or updates it. The platform has no upsert call: this is application code on top of the generated DAO.

## Practice

### Look up, then branch

1. Query with the DAO: `dao.query()` for a singleton, or `dao.query().filterBy...(...)` for a keyed record, then `selectOne()` ([[dao-fluent-query-filter]]).
2. Absent: create it from the input with the builder of the `ForCreate` payload ([[builder-pattern-entity-creation]]).
3. Present: set the changed fields on the loaded entity and call `update` with a mask that lists only those fields ([[mutable-entity-update-pattern]], [[mask-field-projection]], and [Partial Updates](../../agent-docs/backend/data-access-guide.md#pattern-4-partial-updates)).

```java
@Override
public void accept(Context _this, Input input) {
    Optional<Configuration> existing = configurationDao.query().selectOne();
    if (existing.isEmpty()) {
        configurationDao.create(ConfigurationForCreate.builder()
            .withField1(input.getField1())
            .withField2(input.getField2())
            .build());
    } else {
        Configuration config = existing.get();
        config.setField1(input.getField1());
        config.setField2(input.getField2());
        configurationDao.update(config,
            ConfigurationMask.configurationMask().withField1().withField2());
    }
}
```

`Configuration`, `ConfigurationDao` and the mask methods are generated from the example model.

### Platform facts to watch

- `selectOne()` on a query that can match several rows does not guarantee uniqueness. A singleton or key must be unique by design. The agent-docs do not describe a platform uniqueness guard for this case, so the guard is this lookup: enforce uniqueness where the data is created (this operation) and treat more than one match as a data error.
- The pattern is not atomic. Two concurrent first calls can both see "absent" and both create. The platform's optimistic lock only protects updates: an update carrying a stale `__version` is rejected, but there is nothing to lock on an absent row ([Optimistic Locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)). For a singleton, create it at start-up through an init operation ([[init-data-seeding]]) and make the operation update-only. For keyed rows, serialise the writers (one sync job) or accept and handle the duplicate.
- Optional attributes arrive as `Optional` getters in the generated DTO when they are not required, and absent is not the same as null ([Absent, Null and Empty Are Different](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)). Decide for each field whether an absent input value means "keep" or "clear".
- A custom operation is not intercepted, so checks and derived writes that interceptors do for built-in create and update do not run here ([Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Put them into the operation.
- The update bumps `__version`, so a signed identifier held by a client becomes stale ([Signed Identifiers](../../agent-docs/backend/platform-behavior-reference.md#signed-identifiers)).

## Rationale

- Safe for first-time setup, idempotent, and the caller does not need to know whether the record exists.
- Costs: not atomic, and an extra query per call.
- Alternatives: a database-level upsert (not available through the DAO), or an init operation that seeds the record so the operation only updates ([[init-data-seeding]]).

## Example

- One application: a configuration operation upserts the singleton configuration entity that stores e-mail templates (deletion, modification, reminder), the contact address and the sender address. The first call creates it, later calls update it.
- Another application: an item service upserts the daily cost rows of tracked items during the data sync. It looks up the cost by date, updates the amount if found and creates it otherwise, so a repeated sync does not duplicate days. Fetched-data snapshots are created fresh on each sync.
- A third application: a reference service imports countries from an ISO 3166 JSON file. For each country it queries by name and creates the record only if it is missing, so the import can run repeatedly.

## When to avoid

- Concurrent first writers are likely and duplicates are harmful: seed the record instead.
- The record must exist: a missing one is an error, so use the plain update with a not-found fault ([[mutable-entity-update-pattern]]).
- Volume is high (thousands of rows): one query per row is slow; load the existing keys once and diff.

## Related

- [[init-data-seeding]] — seed the singleton instead of creating it lazily
- [[mutable-entity-update-pattern]] — the update branch
- [[builder-pattern-entity-creation]] — the create branch
- [[dao-fluent-query-filter]] — the lookup
- [[mask-field-projection]] — the update mask
