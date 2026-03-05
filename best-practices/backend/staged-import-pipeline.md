---
id: "staged-import-pipeline"
title: "Staged Multi-Phase Import Pipeline"
domain: "backend"
category: "operation"
score: 18.1
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - judo-partner
---
## Description

A multi-phase data import pipeline where raw imported data is first staged into intermediate entities, then validated individually (potentially against external services), and finally migrated into production entities. Each phase can be executed individually or in batch. Status tracking on each staged record enables resumable processing, partial imports, and error isolation. Failed records do not block the overall pipeline.

## Structure

```java
// Phase 1: Import raw data into staging records
Import batch = importDao.create(ImportForCreate.builder().build());
for (RawRecord record : parsedJsonData) {
    importDao.createPartners(batch, StagedRecordForCreate.builder()
        .withName(record.name)
        .withStatus(MigrationStatus.AWAITING)
        .build());
}

// Phase 2: Validate each staged record (individual or batch)
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

// Phase 3: Migrate validated records to production entities
void migrate(StagedRecord record) {
    ProductionEntity entity = productionDao.create(...);
    record.setMigrationStatus(MigrationStatus.MIGRATED);
    stagedRecordDao.update(record);
}

// Batch processing with pagination
int i = 0;
List<StagedRecord> batch;
do {
    batch = parentDao.queryChildren(parent).selectList(i, i += 100);
    for (StagedRecord record : batch) {
        service.validate(record);
    }
} while (batch.size() == 100);
```

Key elements:
- Separate `Import` (batch) and `ImportPartner` (staged record) entities
- `MigrationStatus` enum: AWAITING, MIGRATED, DISABLED
- `ValidationStatus` enum: OK, FAILED
- `ValidationErrorCode` for categorized failure reasons
- Paginated batch processing (100 records at a time)
- Individual and batch operations for both validate and migrate phases

## Examples

### judo-partner
Three-phase partner import pipeline: (1) `PartnerImportCustomImplementation` reads partner JSON from FileStore, parses Hungarian-format fields, creates `Import` batch and `ImportPartner` staging records with addresses. (2) `ValidateCustomImplementation` / `ValidateAllCustomImplementation` validates each `ImportPartner` against the NAV Online API (tax number + name matching), setting validation and migration status. Batch validation processes 100 records at a time. (3) `MigrateCustomImplementation` / `MigrateAllCustomImplementation` creates real `Partner` entities from validated records, copies addresses, adds NAV headquarter data. Failed migrations set status to DISABLED with DUPLICATE_TAX_ID error.

## Trade-offs

- Pros: Resumable processing (resume from where it left off), error isolation (one bad record does not affect others), auditability (staging records preserve original data), supports external validation between phases
- Cons: Extra entities to maintain (staging tables), longer overall import time due to multi-phase approach, status management adds complexity
- Alternative: Direct import (parse and create in one step, simpler but no error isolation), database-level bulk operations (faster but no external validation)

## Related Patterns

- bulk-json-import-export
- filestore-mediated-file-transfer
- upsert-create-or-update
