---
id: xdocreport-document-generation-pipeline
title: "XDocReport Document Generation Pipeline (DOCX Templates to PDF)"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
---

## Description

A multi-layer document generation pipeline that produces PDF and DOCX reports from Freemarker-powered DOCX templates using the XDocReport library. This is an implementation-only blueprint -- it does not correspond to a single model entity but orchestrates a complete document lifecycle: template retrieval from the database, data model assembly from multiple DAOs, DOCX generation with embedded images, DOCX-to-PDF conversion (via docx4j or JODConverter REST API), optional PDF watermarking, and file storage.

The pattern includes:
- A dedicated `report` Maven module with static utility classes (e.g., `ReportUtil`, `OfferReportUtil`, `JobSheetReportUtil`) that handle XDocReport template loading, Freemarker context binding, and image embedding
- An `ImageProvider` / `StreamImageProvider` abstraction for embedding images from the FileStore into DOCX templates
- A `ReportService` interface and implementation in the `common` module that orchestrates the full pipeline: load template, assemble transfer object model, call report utility, convert to PDF, add watermark, store result
- A `DocumentConversionService` that calls JODConverter (external Docker container) REST API for DOCX-to-PDF conversion as an alternative to docx4j
- A `PdfWatermarkService` that overlays rotated semi-transparent text on PDF pages using PDFBox
- A `ConfigurationTemplateService` that reads DOCX template files from a Configuration singleton entity via FileStoreService

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
