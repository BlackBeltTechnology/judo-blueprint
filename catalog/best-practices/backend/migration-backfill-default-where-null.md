---
id: migration-backfill-default-where-null
title: Hand-Written Migration Backfill for New Columns
description: "A hand-written data-migration changeset runs after the generated schema step to give existing rows the default, or a value derived from a related row, that the generated diff leaves NULL."
aliases: [backfill new column, default where null migration, updateDataAfter backfill]
keywords: [migration, backfill, schema evolution, changeset, nullable column, default, updateDataAfterIncremental, liquibase]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:park-here", "status:emerging"]
category: data-migration
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:application/schema/migration/1_0_0_20260923_100755_SNAPSHOT_to_1_0_0_20260924_103958_SNAPSHOT/06_updateDataAfterIncremental_postgresql.changeset.xml", "park-here:application/schema/migration/1_0_0_20260713_124306_SNAPSHOT_to_1_0_0_20260727_155508_SNAPSHOT/06_updateDataAfterIncremental_postgresql.changeset.xml"]
alternatives: []
related: [init-data-seeding, excel-data-seed-import]
fragment: "none: backend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

When a model change adds an attribute, the generated schema migration adds a plain nullable column and leaves every existing row at NULL. That ignores a required flag or a default expression on the attribute, so old rows read as "unset" while new rows get the default. A small hand-written changeset closes the gap by filling existing rows once, in the same migration step that adds the column.

## Practice

### Platform base

- The schema generator writes one folder per model step under `application/schema/migration/`, with nine changesets. The two data-migration changesets (`updateDataBeforeIncremental` and `updateDataAfterIncremental`) are generated empty, and you write them when the change needs data work ([schema evolution, manual scripts](../../agent-docs/deployment/schema-evolution.md#step-3-manual-migration-scripts-optional)).
- Entity tables are named `T_ENTITIES_<NAME>` and columns `C_<NAME>`. Check the generated changelog for the exact names (same guide).
- Generation overwrites the files of the output folder except review files, so confirm against the guide that a hand-written changeset survives regenerating the folder, and re-check it after every regeneration (*verify*).

### Practice notes: the backfill changeset

This layer is a convention built on the platform, not a platform feature:

- **Put the backfill in the "after" changeset.** The new column is created by the `incremental` step, so in the "before" hook it does not exist yet and the UPDATE would fail. Anything that reads or writes the new column belongs in `updateDataAfterIncremental`.
- **Default backfill.** Update only the rows still NULL: `UPDATE <table> SET <col> = <default> WHERE <col> IS NULL`. The condition keeps the changeset harmless if it runs on rows that already carry a value.
- **Derived backfill.** When a better value exists elsewhere, take it from the related row with a joined UPDATE, restricted to rows that are NULL and whose state says the value should exist. Follow it with a second UPDATE that gives any row still NULL a safe fallback, such as the current time, and choose a fallback whose only cost is mild (for example delaying a retention purge by one period).
- **Say why in a comment.** Open the changeset with a comment that states the generator emits this file empty, which column is backfilled, why it lives in the "after" file, and which columns are left alone on purpose, for example columns holding ids created by application code that SQL cannot produce.
- **Name each changeset after the change** and give it a context equal to the version pair, so the history shows which model step it belongs to.
- **Enum ordinals are gapped.** If the backfill tests an enum column, read the ordinals from the model's own `ordinal` attributes, not from the member order in the file.

```xml
<!-- Example code: table and column names are illustrative -->
<changeSet author="app" context="<from>_<to>" dbms="postgresql" id="add-flag-backfill-false">
    <sql>
        UPDATE T_ENTITIES_ORDER
           SET C_URGENT = false
         WHERE C_URGENT IS NULL;
    </sql>
</changeSet>

<changeSet author="app" context="<from>_<to>" dbms="postgresql" id="backfill-closed-at">
    <sql>
        UPDATE T_ENTITIES_ORDER O
           SET C_CLOSED_AT = L.C_CREATED_AT
          FROM T_ENTITIES_ORDER_LINE L
         WHERE O.C_CLOSED_BY_ID = L.ID
           AND O.C_STATE = 3
           AND O.C_CLOSED_AT IS NULL;
        UPDATE T_ENTITIES_ORDER
           SET C_CLOSED_AT = now()
         WHERE C_STATE = 3
           AND C_CLOSED_AT IS NULL;
    </sql>
</changeSet>
```

## Rationale

- The generator cannot know the intended default for existing data, so a model-level default alone leaves old rows NULL.
- Running after the structural step is the only point where both the old data and the new column exist.
- Filtering on `IS NULL` makes the step safe to read and to re-run, and a two-step derived backfill keeps the best available value while still leaving no row NULL.

## Example

A second variant backfills a newly added required text attribute of a configuration entity with its default in the "after" changeset, using the `WHERE <col> IS NULL` form; its changeset has no explanatory comment, which the practice recommends. The same variant also met the variant of backfilling a file-store reference in SQL together with seeding the file; this is the counter-example for the "cannot be produced in SQL" rule below, so keep that advice and fill such references from application code ([[init-data-seeding]]).

Two migration steps in one application carry this. One adds a Boolean attribute to a record entity and sets it to false for every existing row. The other adds a "converted at" timestamp to a state-machine entity: rows already in the converted state take the creation time of the header row that holds the entity they were converted into, and any row still NULL gets the current time so that the retention job can age it. Both changesets say in their comment that the generator emits the file empty.

## When to avoid

- The column is nullable on purpose and NULL is a valid state for old rows: do not invent a value.
- The value cannot be produced in SQL (file-store ids, generated codes): fill it from application code at boot instead.
- Large tables: a single UPDATE can lock for long, so plan batching or a maintenance window.

## Related

- [[init-data-seeding]] — application-level seeding when SQL cannot produce the value
- [[excel-data-seed-import]] — boot-time data import for values SQL cannot create
