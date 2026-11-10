---
id: bulk-csv-import-export
title: Bulk CSV Import/Export via FileStore
description: "Custom operations export data as a CSV file (UTF-8 BOM for Excel) stored in the file store and return a FileType, and import operations read an uploaded CSV from the file store and create one entity per row."
aliases: [CSV export, CSV import, bulk invite]
keywords: [csv, import, export, filestore, bulk, bom, file token]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: operation
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [bulk-json-import-export]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Administrative users need to download data as CSV (for example a compliance export of audit rows) and to upload a CSV that drives a bulk action (for example inviting many e-mail addresses). Both are modeled as custom operations whose file goes through the file store, not through the operation payload.

## Practice

### Platform base

- A binary attribute travels as a file-store token: upload is two-phase (request the upload token, upload the content, send the token as the attribute value in the create or operation input), and invalid tokens fail with `INVALID_FILE_TOKEN` ([binary upload tokens](../../agent-docs/backend/platform-behavior-reference.md#binary-upload-tokens)). An import operation therefore receives a `FileType` input whose id the backend resolves against the file store.
- An operation without an output answers 204; an operation that returns a binary hands back a `FileType` the client downloads with the token ([client side of the upload token flow](../../agent-docs/backend/platform-behavior-reference.md#client-side-of-the-upload-token-flow)).
- The platform also has modeled `EXPORT` operations that call the `Export` SPI (Excel through JXLS); without a configured `Export` they fail with `Not implemented` ([Excel export operations](../../agent-docs/backend/platform-behavior-reference.md#excel-export-operations)). A CSV export is a custom operation, not that SPI.
- Custom operations are OSGi components and bring their own services with `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). Interceptors do not guard them, so any role check belongs inside the implementation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- A list query returns all matching rows unless you ask for a seek, so a full export pulls everything into memory ([pagination](../../agent-docs/backend/data-access-guide.md#pagination)). Use filters and masks to limit what is read ([query patterns](../../agent-docs/backend/data-access-guide.md#query-patterns)).

### Project practice: CSV through the file store

`FileStoreService` and the CSV helpers below are example project code (mlszksz-platform), not platform classes.

```java
// Export: query, build CSV with UTF-8 BOM, store, return FileType
List<Entity> data = entityDao.query()
    .filterByTimestamp(TimestampFilter.greaterOrEqualThan(input.getFrom()))
    .selectList();
StringBuilder csv = new StringBuilder();
csv.append('\uFEFF');                        // BOM so Excel detects UTF-8
csv.append("header1,header2,header3\n");
for (Entity entry : data) {
    csv.append(escapeCsv(entry.getField1())).append(",")
       .append(escapeCsv(entry.getField2())).append("\n");
}
byte[] bytes = csv.toString().getBytes(StandardCharsets.UTF_8);
String fileId = fileStoreService.put(new ByteArrayInputStream(bytes), "export.csv", "text/csv");
// return the FileType (id, fileName, mimeType, size) in the output object

// Import: read the uploaded file, parse, create one entity per row
InputStream csvStream = fileStoreService.get(input.getCsvFile().getId());
for (String email : parseCsvEmails(csvStream)) {
    recipientDao.create(RecipientForCreate.builder().withEmail(email).build());
}
```

- Write the BOM, quote every field and double embedded quotes. A CSV library is safer than manual escaping.
- Validate the header and each row before creating anything; collect row errors and report them as a validation error ([[validation-exception-hierarchy]]).
- The whole file is read into memory. For large files stage the rows first ([[staged-import-pipeline]]).
- Per-row side effects such as sending e-mails multiply with the file size; move them to a background job for large imports ([[email-service-integration]]).
- Creation uses the generated builder ([[builder-pattern-entity-creation]]).

## Rationale

- The file store keeps file content out of the REST operation payload and gives clients the standard token download.
- The BOM makes Excel open UTF-8 text correctly.
- Cost: no streaming, manual escaping unless a library is added, no format validation by default, and one side effect per row.

## Example

mlszksz-platform has two operations. An audit-log export builds a CSV with an optional date filter, quoted and escaped fields and a BOM and returns file metadata. A bulk invite reads an uploaded CSV, extracts e-mail addresses, creates an invitation with one recipient per address and sends a verification e-mail to each.

## When to avoid

- When users want a formatted spreadsheet: use the modeled Excel `EXPORT` operation.
- When the file is large or each row is slow to process: stage and process in a background job.
- When the data is structured and nested: see [[bulk-json-import-export]].

## Related

- [[filestore-mediated-file-transfer]] — how files move through the file store
- [[bulk-json-import-export]] — JSON variant for nested data
- [[email-service-integration]] — per-recipient e-mails sent by the bulk invite
- [[staged-import-pipeline]] — staging large imports
- [[builder-pattern-entity-creation]] — creating the row entities
