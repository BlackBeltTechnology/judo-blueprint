---
id: "draft-done-status-enum"
title: "Draft/Done Two-State Workflow Enum"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A minimal two-state status enumeration with DRAFT and DONE members, representing the simplest possible workflow: an item starts in DRAFT (being prepared), then transitions to DONE (finalized/completed). This is used for document-producing processes like fault registries and offers where the document is first assembled and then finalized. Unlike content lifecycle enums (DRAFT/PUBLISHED/DELETED), this pattern has no soft-delete state -- the entity is either in-progress or completed.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
