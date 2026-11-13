---
id: bulk-json-upload-entity
title: Bulk JSON Upload Entity with Question/Data Import
description: An Upload entity that records one bulk JSON import batch and links the items it created back to that batch.
aliases: [bulk import, json import, upload batch]
keywords: [bulk, json, upload, import, export, traceability, batch]
tags: [domain:model, layer:model, layer:backend, project:trivia, status:single-project]
category: pattern
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: bulk-json-upload-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Ingest a batch of records from an external JSON file in one operation, and keep a record of which batch produced each imported item. The batch row holds the raw input, the time, and the count of created items. Items refer back to their batch.

### Each import leaves a batch row

The import operation writes an Upload row before it creates items. The row is the audit trail: it keeps the raw JSON, the time of the upload, and how many items were created. Upload is not created through a generated create action.

### Imported items point back to their batch

Each created item holds a reference to its Upload. Tracing an item to its source batch is a single navigation. Items that already exist are skipped, so a batch can be re-run without duplicating records.

## Structure

The Upload entity has three required attributes: json (text), timestampOfUpload (timestamp) and nrOfUploadedQuestions (integer). Upload has a 0..* association to Question. Question has a required text identifier, an optional back-reference to Upload (0..1) and an optional Category (0..1). Category has a required name identifier.

The import and download operations are not part of the entity shape. They are static operations on a transfer object (an application choice) that take the JSON as an unmapped transfer object input and return a file reference or the export payload.

## Constraints

- Upload rows are created only by the import operation. Create, update and delete flags are set on transfer-object relations, not on the entity: expose Upload through a transfer object without the create, update and delete flags (read-only), so no generated REST create exists for it.
- The import writes the Upload row and its items in one operation call. If the operation throws, the writes of that transaction roll back, including the Upload row (expected behaviour; the agent-docs state this explicitly only for interceptors).
- The import operation is a custom operation that writes, so it must be modelled stateful. A stateless call context makes the DAO writes throw `IllegalStateException`.
- Items that match an existing identifier are skipped, not updated.
- The JSON text is stored whole. Its size is bounded by the database text column, so large files need the file-store path.

## Variations

- **Whole-file import through the file store.** The JSON is uploaded as a binary file, read back by the operation, and parsed there. This is the reference implementation's approach for larger files.
- **Inline JSON input.** The JSON arrives as a text input on an unmapped transfer object. Simpler, but limited by request size.
- **Batch without a Category.** Drop the Category entity when items carry no classification. The Upload and item relations stay the same.
- **Export as a round trip.** A static download operation writes the same item shape back out as JSON. The CSV counterpart is described in the bulk import best practices.

## When to use

- A reference list or catalog of records is loaded from an external file in batches.
- Auditors need to know which batch created an item and when.
- The same record shape must be imported and exported in a round trip.

## When to avoid

- Items must be edited individually after import and the batch link is not needed. A plain entity with a generated create form is simpler.
- Imports are continuous streams rather than batches. Use an event or queue instead of a batch row.
- The file is too large for a single transaction. Split it or use a staged import.

## Related

- [[event-log-entity]]: an append-only log of events, used when every change must be recorded rather than one batch
- [[document-file-attachment]]: how the uploaded file itself is stored and attached
- [[reference-data-lookup-entity]]: the Category reference list that imported items point to
