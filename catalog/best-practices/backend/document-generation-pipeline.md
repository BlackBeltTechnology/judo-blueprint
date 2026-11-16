---
id: document-generation-pipeline
title: Document Generation Pipeline (XDocReport + PDF Conversion)
description: A custom operation builds a document from a stored template and a deeply masked data model, optionally converts it to PDF and watermarks it, and stores the result in the file store.
aliases: [report generation, DOCX template, PDF export, document from template]
keywords: [document, DOCX, PDF, XDocReport, Freemarker, template, mask, filestore, watermark, JODConverter, report, export]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:doors-model", "status:emerging"]
category: integration
status: emerging
projects: [rackinspect, doors-model]
evidence: ["rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/OfferServiceImpl.java", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/services/fault_registry_services/document/GeneratePdfCustomImplementation.java", "doors-model:unrecorded"]
alternatives: []
related: [filestore-mediated-file-transfer, email-service-integration]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Business users want a Word or PDF document filled with application data (report, letter, certificate) and want to change the layout without a release. Keep the template as a stored file, load the data through DAOs, merge them in a custom operation, and store the result in the file store.

## Practice

### Stages

1. Load the template. It lives in a configuration entity as a binary attribute or file-store token, so an administrator can replace it.
2. Build the data model. Query the entity with a mask that names exactly the fields and nested relations the template uses. Masks control loading depth, and fields outside the mask are null (see [Pattern 3: Detail Views](../../agent-docs/backend/data-access-guide.md#pattern-3-detail-views-nested-masks)). Prepare derived values in a per-document helper class rather than in the template.
3. Merge. XDocReport with Freemarker fills a DOCX template (the libraries are application dependencies, not platform ones).
4. Convert to PDF if needed. One application posted the DOCX to an external JODConverter REST service.
5. Watermark preview versions with a PDF library.
6. Store the output in the file store and return or attach the reference.

### Do it in a custom operation

The generator is a custom operation implementation or a service it delegates to (see [The Custom Service Layer](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer)). A preview and a final version can share the stages and differ in the watermark. An operation that only reads data and returns a file has a typed output: a transfer object with a binary attribute, which travels as a file-store token, not as bytes in the response (see [Response Metadata and Wire Conversion](../../agent-docs/backend/platform-behavior-reference.md#response-metadata-and-wire-conversion)).

### Files reach the client through tokens

Upload and download are token based: the client asks for an upload token for the binary attribute, uploads the content to the file store, and sends the token as the attribute value on create or update (see [Binary Upload Tokens](../../agent-docs/backend/platform-behavior-reference.md#binary-upload-tokens)). A template uploaded through the UI therefore reaches the operation as a stored file.

### Keep it safe and bounded

- The external converter is a network dependency. Set timeouts and map its failures to a declared fault or `ValidationException`, because an unmapped runtime exception becomes a generic 500 (see [How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)).
- Template engines and some PDF libraries are not thread safe. One application serialized the generation methods.
- A custom operation is not protected by interceptors, so check the caller's right to the document inside the operation (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Modeled EXPORT operations are a different feature: the platform's Excel export uses a JXLS-based SPI (see [Excel Export Operations](../../agent-docs/backend/platform-behavior-reference.md#excel-export-operations)). This pipeline is for DOCX and PDF.

## Rationale

- Templates stored as data let non-developers change layout.
- Masks keep the data query bounded even for a document that needs many levels.
- Limit: large masks load a lot, template errors are hard to debug, and PDF conversion needs an extra service to run.

## Example

- A report service produces several document types (for example orders, review reports and completion certificates). Each has a helper preparing its data model. Preview operations add a PREVIEW watermark. A conversion service calls JODConverter over HTTP.
- A `generateDocument` operation on a document loads the DOCX template of its type, applies it, and replaces the stored document. The implementation lives in a separate backend repository.

## When to avoid

- The layout is fixed and simple: generate the PDF directly with a PDF library.
- Only a spreadsheet is needed: use a modeled export operation.
- Documents are very frequent or large: generate asynchronously and store the result, rather than in a request.

## Related

- [[filestore-mediated-file-transfer]] — storing templates and results
- [[email-service-integration]] — sending generated documents by mail
