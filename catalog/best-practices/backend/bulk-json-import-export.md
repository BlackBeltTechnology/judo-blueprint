---
id: bulk-json-import-export
title: Bulk JSON Import/Export via FileStore
description: "Admin operations import entity data from an uploaded JSON file (deserialized with Jackson, deduplicated, created via builders) and export it as a JSON file in the file store."
aliases: [JSON import, JSON export, bulk upload]
keywords: [json, import, export, filestore, jackson, bulk, dedup]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:judo-partner", "status:emerging"]
category: operation
status: emerging
projects: [trivia, judo-partner]
evidence: ["trivia:unrecorded", "judo-partner:unrecorded"]
alternatives: [bulk-csv-import-export]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Admins load or dump a whole set of records (catalog items, master data, reference lists) as one JSON file. The file goes through the file store; the import operation reads it, validates and deduplicates each record and creates entities, and the export operation serializes the entities back to a file.

## Practice

### Platform base

- A file is passed as a binary attribute: upload is two-phase and the operation input carries a file-store token; invalid tokens fail with `INVALID_FILE_TOKEN` ([binary upload tokens](../../agent-docs/backend/platform-behavior-reference.md#binary-upload-tokens)).
- The operation is a custom implementation (OSGi component) that injects DAOs and services with `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). No interceptor protects it, so check the caller's role inside ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Duplicate checks use the fluent query with typed filters and `count()` ([query patterns](../../agent-docs/backend/data-access-guide.md#query-patterns)); records are created through the generated builder ([[builder-pattern-entity-creation]]).
- JSON parsing is not a platform feature of the operation: use Jackson in your own code. The platform's shared `ObjectMapper` for REST is configured separately ([custom REST endpoints and CXF](../../agent-docs/backend/platform-behavior-reference.md#custom-rest-endpoints-and-cxf)); a plain `new ObjectMapper()` in the operation is independent of it.

### Practice notes: JSON through the file store

`FileStoreService` (`fsService`) and the inner record class are example code.

```java
// Import: inner class mirrors one JSON record
public static class Q {
    @JsonProperty(required = true) private String field1;
    @JsonProperty private String optionalField;
}

InputStream stream = fsService.get(input.getFile().getId());
List<Q> items = new ObjectMapper().readValue(stream, new TypeReference<List<Q>>() {});

for (Q item : items) {
    if (entityDao.query().filterByName(StringFilter.equalTo(item.name)).count() == 0) {
        entityDao.create(EntityForCreate.builder()...build());
        count++;
    }
}

// Export: serialize and store
byte[] json = new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsBytes(items);
String fileId = fsService.put(new ByteArrayInputStream(json), "export.json", "application/json");
```

- Mark required fields with `@JsonProperty(required = true)` so a malformed file fails before anything is created.
- Deduplicate on a business key and return the number created.
- Do not swallow `IOException`: report a parse failure to the caller as a validation error ([[validation-exception-hierarchy]]). One variant swallowed it and gave no feedback.
- Resolve lookup values (for example a category by name) once into a map instead of querying per record; the export in one variant did one lookup per record.
- For large or multi-phase migrations, write the records into staging entities first and process them later ([[staged-import-pipeline]]).

## Rationale

- The file store keeps big payloads out of the operation call; Jackson gives typed validation with little code.
- JSON handles nested records, unlike [[bulk-csv-import-export]].
- Cost: the whole file is held in memory, and without staging a failure midway leaves partial data unless the whole operation is a single transaction (a failed operation rolls back its writes).

## Example

An upload and a download operation handle items: upload deserializes the file, skips items already present, shuffles option positions ([[option-order-randomization]]), resolves the category and creates the items; download writes all items as pretty-printed JSON. Another variant reads a master-data JSON file into staged import records for a multi-phase migration and imports reference data from JSON.

## When to avoid

- When rows are flat and users edit them in a spreadsheet: CSV ([[bulk-csv-import-export]]).
- When the file is far larger than memory allows: stream it or load in batches.
- For one-off seed data shipped with the application: see [[init-data-seeding]].

## Related

- [[filestore-mediated-file-transfer]] — how the file gets to and from the operation
- [[builder-pattern-entity-creation]] — creating the records
- [[bulk-csv-import-export]] — CSV variant
- [[staged-import-pipeline]] — staging large imports
- [[option-order-randomization]] — shuffling applied during the import
