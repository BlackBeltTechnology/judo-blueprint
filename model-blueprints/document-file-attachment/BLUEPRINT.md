---
id: "document-file-attachment"
title: "Document/File Attachment Entity"
score: 75.3
usage_count: 6
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - reserve-app
  - alba
  - judo-demo-miniworkflow
  - doors-model
---
## Description

A Document entity for file attachments with a binary `file` or `document` attribute and metadata fields. It associates back to the parent entity (e.g., announcement -> Announcement, 0..1). This is a generic file attachment pattern where any content entity can have multiple documents attached via association or composition. The entity is non-CRUD (created through parent entity operations). Transfer objects expose the file and metadata for viewing, and a DocumentInput unmapped TO provides the file field for upload operations. Some variants add versioning (version attribute) and a PDF rendition (documentPDF binary). The simplest variant is an Attachment entity with only a single binary attribute (picture or attachment), composed by the parent. Richer variants add a `type` discriminator attribute alongside the file and an optional description. Some variants store the file directly as an attribute on the parent entity (e.g., Contract.file, Contract.signedFile) rather than creating a separate entity, with upload operations using dedicated input TOs (UploadFileInput, UploadSignedFileInput). URL-based variants (e.g., Kep/Image with a `url` string attribute instead of a binary file) store a reference to an externally-hosted file rather than the file content itself.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
