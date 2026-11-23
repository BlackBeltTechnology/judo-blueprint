---
id: xdocreport-document-generation-pipeline
title: XDocReport Document Generation Pipeline (DOCX Templates to PDF)
description: "A backend pipeline that fills Freemarker DOCX templates with data and images through XDocReport, converts them to PDF, optionally watermarks them and stores the result in the file store."
aliases: [docx to pdf pipeline, report generation, xdocreport, document templates]
keywords: [xdocreport, freemarker, docx, pdf, template, watermark, conversion, file store, report]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [document-generation-pipeline]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Produce PDF and DOCX documents (offers, reports, certificates) from templates that business users maintain as Word files. The pipeline is backend code; the model only needs a place to keep the templates and the generated result.

> **Legacy.** This DOCX/XDocReport pipeline is treated as legacy; Handlebars-based templates are preferred. Prefer [[document-generation-pipeline]] and [[handlebars-email-template]] for new work; keep this blueprint for existing DOCX-based applications.

### Templates are data, not code

Each document type has a DOCX template with Freemarker placeholders. Templates are stored as binary attributes on a singleton configuration entity, so a template can be replaced without a deployment.

## Structure

The pipeline is a chain of services behind one orchestrator, called from custom operations:

- A configuration entity (singleton) holds one binary attribute per template.
- A template service reads a template stream from the file store by the stored token or id.
- Report utilities, one per document type, load the template with XDocReport, fill a context from a transfer object, embed images and produce the DOCX.
- A conversion service turns DOCX into PDF, either in-process or through an external converter service over HTTP.
- A watermark service overlays text on every page of a PDF for preview documents.
- The orchestrator runs the steps in order and stores the result in the file store.

There is no model shape of its own: only the template binaries on the configuration entity and the file fields that receive the output. `fragment` is therefore none.

## Constraints

### Data model assembly is the expensive step

Build the data for the template from transfer objects loaded with the DAOs of every entity involved. Convert optional values to plain values before they reach Freemarker, and mark optional images so a missing image removes its placeholder.

### XDocReport is not thread-safe in this setup

The source project serialises generation with synchronized methods. Treat concurrency as a design decision and keep it in one place.

### The pipeline runs in custom operations

The operations that start generation are custom operations, so interceptors never see them (see [backend.md](backend.md)). Permission checks belong in the operation.

## Variations

- Two conversion backends: in-process for simple templates and an external converter service for complex layouts. The external base URL comes from an environment variable that overrides the component configuration (project practice).
- Skip conversion when DOCX is the final format.
- Skip the watermark when no preview mode exists.

## When to use

- Users need printable documents with company logos and photos, and templates change more often than code.

## When to avoid

- A fixed, simple document where a table export or an HTML print view is enough.
- The document must be signed or archived in a specialised system; call that system instead.

## Related

- [[document-generation-pipeline]] — the practice-level description of the same pipeline
- [[custom-operation-osgi-component]] — how the starting operation and the services are registered
