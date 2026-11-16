---
id: staged-import-pipeline
title: Staged Import Pipeline (Stage, Validate, Migrate)
description: "Imported data is first stored as status-tracked staging records, validated one by one (also against external services) and only then migrated into production entities, so bad rows do not block the batch."
aliases: [staging tables import, three-phase import, validate then migrate]
keywords: [import, staging, validation, migration, status, batch, resumable, external validation]
tags: ["domain:backend", "layer:backend", "project:judo-partner", "status:single-project"]
category: import
status: single-project
projects: [judo-partner]
evidence: ["judo-partner:unrecorded"]
alternatives: [bulk-json-import-export]
related: [bulk-json-import-export, filestore-mediated-file-transfer, upsert-create-or-update, safe-failure-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A bulk import from a file or another system contains rows that may be wrong, duplicated or rejected by an external check. Writing them straight into production entities makes failures hard to isolate and impossible to resume. The pipeline stores the raw rows in staging entities with a status, validates each one, and migrates only the valid ones.

## Practice

### Platform base

- Every phase is a custom operation: an OSGi component implementing the generated operation interface, with DAOs injected by `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). Interceptors do not fire for custom operations, so permission checks go inside each phase operation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Staging rows are ordinary entities created with the generated `ForCreate` builder through the DAO, and updated with `dao.update` ([data access guide](../../agent-docs/backend/data-access-guide.md#crud-operations)). Staging rows are created under a parent batch entity through the generated relation methods.
- A list query without an explicit seek returns all matching rows, pagination is opt-in ([pagination](../../agent-docs/backend/data-access-guide.md#pagination)). A very large batch must be processed in slices.
- Files reach the backend through the upload-token flow: the client requests the token, uploads the content to the file store, then passes the token to the operation ([binary upload tokens](../../agent-docs/backend/platform-behavior-reference.md#binary-upload-tokens), [[filestore-mediated-file-transfer]]).
- A transaction bounds each operation call; the agent-docs do not describe partial commits inside one call. A "validate all" over a large batch is one call, so test it for time and memory, or drive the slices from the client.
- Faults the phases throw must be declared on the operations ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).

### Practice notes: three phases with status enums

This layer is a convention built on the platform, not a platform feature:

- **Entities**: a batch entity and a staged-record entity owned by it. The staged record has a migration status (awaiting, migrated, disabled), a validation status (ok, failed) and an error code that categorises the failure.
- **Stage**: parse the file, create the batch and one staged record per row, status awaiting, copying the source values including child rows such as addresses.
- **Validate**: per record, call the external check. On success mark it ok and awaiting migration; on failure mark it failed and disabled with a reason. Catch the failure per record so the batch continues ([[safe-failure-pattern]]).
- **Migrate**: create the production entity from a validated record, copy children, enrich if needed, mark migrated. A failure such as a duplicate key marks the record disabled with an error code.
- Offer each of validate and migrate for one record and for the whole batch. The batch variant reads staged records in slices (here 100) and calls the single-record service for each.
- Status lets an interrupted run resume and lets a user retry only failed rows.

```java
// Example code: Import, StagedRecord, importDao, stagedRecordDao and statuses are generated types
Import batch = importDao.create(ImportForCreate.builder().build());
for (RawRecord record : parsedData) {
    importDao.createAccounts(batch, StagedRecordForCreate.builder()
        .withName(record.name)
        .withStatus(MigrationStatus.AWAITING)
        .build());
}

void validate(StagedRecord record) {
    try {
        externalService.validate(record.getTaxNumber());
        record.setValidationStatus(ValidationStatus.OK);
        record.setMigrationStatus(MigrationStatus.AWAITING);
    } catch (Exception e) {
        record.setValidationStatus(ValidationStatus.FAILED);
        record.setMigrationStatus(MigrationStatus.DISABLED);
    }
    stagedRecordDao.update(record);
}

void migrate(StagedRecord record) {
    ProductionEntity entity = productionDao.create(/* ... */);
    record.setMigrationStatus(MigrationStatus.MIGRATED);
    stagedRecordDao.update(record);
}

// batch processing in slices of 100; the slice API shown is the example's usage, check your generated DAO
int i = 0;
List<StagedRecord> slice;
do {
    slice = parentDao.queryChildren(parent).selectList(i, i += 100);
    slice.forEach(service::validate);
} while (slice.size() == 100);
```

## Rationale

- One bad row costs one record, not the whole import, and the original data stays on the staging row for audit.
- External validation can run between stage and migrate without touching production data.
- The price: extra entities, longer import time, and status handling that must be kept consistent.

## Example

An account import runs in three phases. The import operation reads account JSON from the file store, parses the locale-specific fields and creates an import batch with staged account records and their addresses. The validate operations (single and all) check each staged account against an external registry API by tax number and name, and set validation and migration status; the batch version processes 100 records at a time. The migrate operations (single and all) create real accounts from validated records, copy the addresses and add the registry's headquarters data. A failed migration marks the record disabled with a duplicate-tax-id error.

## When to avoid

- A small trusted import with no external validation: import directly, see [[bulk-json-import-export]].
- Rows are idempotent updates keyed by a natural key: [[upsert-create-or-update]] is simpler.
- You need all-or-nothing semantics: staging deliberately allows partial results.

## Related

- [[bulk-json-import-export]] — the direct import this pipeline extends
- [[filestore-mediated-file-transfer]] — how the source file reaches the operation
- [[upsert-create-or-update]] — migrating into existing rows by key
- [[safe-failure-pattern]] — per-record catch that keeps the batch going
