---
id: "bulk-json-upload-entity"
title: "Bulk JSON Upload Entity with Question/Data Import"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

An Upload entity that records bulk data imports via JSON. The entity captures the raw JSON payload, a timestamp of when the upload occurred, and a count of how many items were imported. It maintains an association (0..*) to the entities that were created from the upload, providing traceability from imported items back to their source batch.

The transfer object layer provides:
- A **JsonData** unmapped TO with a single `json` attribute, used as the input parameter for the upload operation
- An **Upload** mapped TO showing the upload metadata and the imported items via an aggregation relation
- The upload operation is a STATIC operation on the target entity's transfer object (e.g., Question.upload)

A companion **download** STATIC operation exports the same data back as JSON, completing a round-trip import/export cycle.

This pattern is suitable for applications that need batch data ingestion from external sources (e.g., importing quiz questions, product catalogs, reference data) while maintaining audit trail of which import batch produced each record.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
