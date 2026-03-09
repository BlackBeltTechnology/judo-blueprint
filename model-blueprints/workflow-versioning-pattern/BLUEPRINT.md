---
id: "workflow-versioning-pattern"
title: "Workflow/Definition Versioning with Head and Published Pointers"
score: 43.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - workflow-poc
---
## Description

A versioning pattern for domain definitions (workflows, templates, configurations) where a parent entity manages an ordered series of version entities. The parent holds:

- **versions** (0..* ASSOCIATION) -- all historical versions
- **head** (0..1 ASSOCIATION) -- the latest (possibly uncommitted) version
- **published** (0..1 ASSOCIATION) -- the currently active version used at runtime
- **headVersionNumber** and **publishedVersionNumber** -- denormalized version numbers for quick display

Each version entity carries:

- **versionNumber** (required) -- monotonically increasing version identifier
- **committed** (required, default: false) -- whether this version has been finalized
- **commitComment** -- human-readable description of what changed
- **commitTime** -- when the version was finalized
- **uploadTime** -- when the version data was initially uploaded
- **model** -- the actual definition content (YAML, JSON, or other format)
- **diagram** -- a visual representation (image binary or SVG)
- **name** / **label** -- human-readable identifiers

The workflow provides three lifecycle operations:
- **upload** (on parent) -- creates a new head version with the uploaded model definition
- **commit** (on version) -- finalizes the version, setting committed=true and recording commitTime
- **publish** (on parent) -- promotes a committed version to be the active published version

This separation of head from published enables a draft/review cycle: new definitions are uploaded and tested as the head version while the published version continues serving production traffic. Only after committing and publishing does the new definition become active.

The version entity typically composes the definition's structural elements (e.g., states and events for workflows) so that each version is a complete, self-contained snapshot.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
