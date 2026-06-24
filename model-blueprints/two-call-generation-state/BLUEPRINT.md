---
id: "two-call-generation-state"
title: "Two-Call Generation State (Handle + Document)"
score: 50.0
usage_count: 1
first_seen: "2026-05-12"
last_updated: "2026-05-12"
projects:
  - compsychletter
---
## Description

A pair of non-CRUD entities that separate transient in-progress state from permanent archival result in a two-phase API flow (start → confirm).

**Handle** holds state between the first call ("start generation") and the second call ("confirm / finalize"). It carries an inline body, an optional overflow binary, an expiry timestamp, and a `state` enum (`ACTIVE|CONFIRMED|EXPIRED`). Handles are never modified after creation — state transitions are modelled implicitly via `expiresAt` and the confirm operation creating a Document. No background GC is needed; expiry is detected lazily on read.

**Document** is the permanent archival record written by the confirm call. It survives deletion of the source entities because every cross-cluster relation on the Document is an ASSOCIATION, not a COMPOSITION. It carries an `identifier` attribute for external references (e.g., barcode payload, reference code). An optional `finalFile` (0..1 BinaryType) holds the rendered output for output types that produce a separate file (e.g. PDF); text-only output types (MD, TEXT) have no file, so the relation is nullable.

Both entities share the same 0..1 ASSOCIATION triplet to the same source entities (e.g., Template, DataObject, Design) so the provenance chain is queryable from both sides.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
