---
id: "publish-delete-edit-operations"
title: "Publish/Delete/Edit Content Operations Pattern"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A recurring set of instance operations on content transfer objects that implement editorial workflow: `publish` (transitions status from DRAFT to PUBLISHED), `delete` (soft-deletes by setting status to DELETED), and an `edit*` operation (updates content while preserving status). Some content types add `expired` (marks time-sensitive content as EXPIRED) and `moderationDelete` (admin-initiated removal with reason). The transfer objects carry boolean guard attributes like isNotPublisheable, isNotDeletable, isNotExpireble to control UI button visibility based on current state. This operation triple appears on every content-managing transfer object.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
