---
id: "campaign-lifecycle-status-enum"
title: "Campaign/Operational Lifecycle Status Enum (Ongoing/Finished/Deleted)"
score: 57.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---
## Description

A three-state status enumeration for operational or campaign-like entities with members ONGOING (actively running), FINISHED (completed/concluded), and DELETED (soft-removed). Unlike the content lifecycle enum (DRAFT/PUBLISHED/DELETED) which models an editorial workflow, this pattern models the lifecycle of a time-bounded operational entity: it starts running (ONGOING), eventually completes (FINISHED), or can be removed (DELETED). The status typically defaults to ONGOING on creation. This pattern appears on campaign management, project tracking, subscription, and other entities that have an active operational period with a defined end.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
