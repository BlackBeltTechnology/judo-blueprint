---
id: filestore-mediated-file-transfer
title: FileStore-Mediated File Transfer Pattern
description: "Custom operations that import or produce files exchange them through the platform FileStore service: upload operations read the stored file by id, download operations store the result and return a file reference."
aliases: [file upload, file download, filestore service]
keywords: [filestore, file, upload, download, transfer, binary, FileStoreService]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:viterra_demo", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:workflow-poc", "project:doors-model", "status:established"]
category: integration
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, viterra_demo, park-here, indamedia-adtrack, judo-partner, workflow-poc, doors-model]
evidence: ["trivia:unrecorded", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/_default_transferobjecttypes/entities/initializer/ExcelDataImporter.java", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/services/fault_registry_services/document/GeneratePdfCustomImplementation.java", "alba:unrecorded", "mlszksz-platform:application/app/src/main/java/hu/blackbelt/mlszksz/platform/mlszkszplatform/custom/mlszkszplatform/services/admin/admindashboard/ExportAuditLogCustomImplementation.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/AdminInvitationServiceImpl.java", "viterra_demo:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "doors-model:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Operations that accept an uploaded file or return a generated one (CSV, JSON, DOCX, templates, credentials) go through the FileStore instead of passing bytes through the operation signature. The client holds a file reference; the backend reads and writes content by id.

## Practice

### Platform base: binary members and the token flow

In the model a file is a binary-typed member (binary types carry a MIME type and a maximum size; see [JSL language notes](../../agent-docs/model/jsl-language-notes.md)). An operation that returns a file wraps the binary in a transient member of an unmapped transfer object ([wrapper transfer object for binary outputs](../../agent-docs/model/advanced-modeling-patterns.md)). Over REST the client uses a two-phase token flow: it requests `<attributePath>/~upload-token`, posts the multipart data with the `X-Token` header, and downloads with `?disposition=inline|attachment` ([upload token flow](../../agent-docs/backend/platform-behavior-reference.md)). The generated frontend `fileHandling` helpers wrap this flow.

The backend storage is selected by environment variables (`JUDO_PLATFORM_FILESTORE` with `filesystem`, plus `JUDO_PLATFORM_FILESTORE_DIRECTORY` for the directory; see [application config](../../agent-docs/deployment/application-config.md)). The agent-docs also describe an S3 backend whose access URL is an internal `<protocol>:<fileId>-<filename>` URL, so downloads flow through the Karaf servlet ([filestore S3 details](../../agent-docs/deployment/osgi-runtime-services.md)). Some applications also run an RDBMS-backed store (`rdbms`); the agent-docs do not list that value, so treat it as observed in practice.

### Practice notes: read by id, write and return a reference

The FileStore service is an OSGi service injected with `@Reference`. The calls below are what the examples use; the agent-docs do not document the service API, so verify signatures against the SDK of your version.

```java
// Example code
@Reference
FileStoreService fsService;

// upload operation: read the stored file by the id the client sent
InputStream stream = fsService.get(input.getFile().getId());

// download operation: store the content, return a file reference
String fileId = fsService.put(new ByteArrayInputStream(bytes), "filename.json", "application/json");
return OutputTO.builder()
    .withFile(FileType.builder().withId(fileId).withFileName("filename.json")
        .withMimeType("application/json").build())
    .build();
```

- Keep parsing, validation and entity creation in a service and let the operation only fetch the stream (see [[service-delegation-pattern]]).
- When several models run in one container, an example filters the injected service by model name with an OSGi target filter.
- Where the file is attached to an entity, derived creation helpers on the DAO manage the file references (example: copying attachments to a new product version).

## Rationale

- File handling stays out of the REST layer: the platform owns tokens, transport and size limits, and the operation sees only an id.
- The storage backend (filesystem, RDBMS, S3-compatible) is a deployment choice that needs no code change.
- Cost: an extra indirection, no streaming for large files in the example code, and RDBMS-backed storage grows the database.

## Example

- Upload operations read JSON or YAML by id, parse with Jackson and create entities; a download serializes items to JSON and returns a file reference.
- One application: audit-log CSV export (UTF-8 BOM) stored and returned; bulk invitation CSV upload read from the store; an in-memory FileStore mock in integration tests.
- One application: email templates (Handlebars files) and layout images loaded into the store at init and read back when rendering emails ([[handlebars-email-template]]).
- One application: an uploaded credential JSON file stored and read back by a provider service.
- One application: DOCX templates and generated documents ([[document-generation-pipeline]]).
- A filesystem backend and an RDBMS backend, each with document-processing libraries configured: infrastructure examples.

## When to avoid

- Tiny payloads that fit a normal string or binary attribute of a transfer object.
- Very large files that need streaming: the example usage loads content through streams or byte arrays.

## Related

- [[bulk-json-import-export]] — JSON import and export through the store
- [[email-service-integration]] — templates and images read from the store
- [[document-generation-pipeline]] — templates and generated documents
- [[handlebars-email-template]] — template files kept in the store
- [[service-delegation-pattern]] — keep file parsing in a service
