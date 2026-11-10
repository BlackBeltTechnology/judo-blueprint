---
id: two-call-generation-state
title: Two-Call Generation State (Handle + Document)
description: A pair of non-CRUD entities for a two-step API flow, where a short-lived Handle holds the generated result between the start call and the confirm call, and a permanent Document is written only on confirm.
aliases: [handle and document, start confirm flow, two-phase generation, generation ticket]
keywords: [handle, document, two-call, confirm, expiry, state, generation, archive, ticket]
tags: [domain:model, layer:model, layer:backend, project:compsychletter, status:single-project]
category: pattern
status: single-project
projects: [compsychletter]
evidence: ["compsychletter:unrecorded"]
alternatives: []
fragment: two-call-generation-state
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-05-12
last_updated: 2026-11-10
---
## Intent

Split a generate-then-keep flow into two API calls. The first call (start) produces a result and stores it in a short-lived **Handle**. The second call (confirm) turns the Handle into a permanent **Document**. Until confirm, nothing permanent exists, so a result the user discards leaves only an expiring Handle behind.

### Handle: state between the two calls

The Handle carries the generated content inline, an optional overflow binary for content too large for an inline text attribute, an expiry timestamp and a state enumeration with the values active, confirmed and expired. It is returned to the client as the ticket for the second call. A Handle is never edited by clients. Expiry is detected lazily, when the confirm call reads the Handle and compares the expiry timestamp with the current time; no background job is needed.

### Document: the permanent record

The Document is written by the confirm call. It carries an identifier attribute for external references (a reference code, a barcode payload) and the final content. An optional final file (a binary, 0..1) holds the rendered output for output types that produce a separate file, such as a PDF. Text-only output types have no file, so the relation is optional.

## Structure

- **Handle** (entity): `state` (enumeration `HandleState`: ACTIVE, CONFIRMED, EXPIRED, required), `expiresAt` (timestamp, required), `body` (long text, optional), an optional overflow binary, and 0..1 association relations to each source entity.
- **Document** (entity): `identifier` (string, required), `content` (long text, optional), an optional final file binary, and 0..1 association relations to the same source entities as the Handle.
- **Source entities** (project-specific, for example a template, a data object and a design): each may carry a 0..* association back to Document so the provenance is queryable from both sides.
- Every relation from Handle or Document to a source entity is an **association**, never a composition. A composition would delete the Document together with its source; the association lets the Document outlive it.
- Both entities are created non-createable, non-updateable and non-deletable in the model: all writes go through custom operations.

The shape in the diagram uses one neutral `SourceItem` for the source entities. The binary attributes are described in words only: the fragment base model has no binary type.

## Constraints

- **Both entities are non-CRUD.** Clients never call generated create, update or delete on them. Reads and writes happen inside the start and confirm operations. See [[custom-operation-osgi-component]] for how a custom operation is wired.
- **Copy relations, do not move them.** The Document holds its own associations to the sources, independent of the Handle's, so Handle rows can be purged without touching provenance.
- **Confirm marks the Handle as confirmed before or in the same transaction as it creates the Document**, to prevent a double confirm under concurrent requests (project practice; the platform does not give you this for free, the Handle row must be updated).
- **The identifier is generated at confirm, not at start**, so the stable external reference exists only for finalised documents.
- **Expired Handles accumulate** unless something purges them. Purging is optional and not part of the platform.
- Interceptors never run around custom, mapped or script operations (see [Interceptors](../../agent-docs/backend/interceptors.md)). Anything that must hold for start or confirm, such as the expiry check, belongs inside the operation itself.

## Variations

- **Content storage.** Small results live inline in `body`; large or binary results go to the file store and the Handle keeps only a file reference. See [[filestore-mediated-file-transfer]].
- **Explicit expiry state.** The blueprint keeps the state enumeration but treats expiry as lazy: nothing writes EXPIRED unless a purge job does. A variant drops EXPIRED and derives it from `expiresAt`.
- **Several source entities.** One 0..1 association per source on both Handle and Document.
- **No back-references.** Skip the source-to-Document associations when provenance is only ever read from the Document.

## When to use

- A generation step is expensive or reviewable and the user must approve the result before it is kept.
- The permanent record must survive deletion of the inputs it was generated from.
- The client needs a ticket to complete the flow in a second call.

## When to avoid

- The result is always kept. A single operation that creates the record is simpler.
- The result is cheap to regenerate; pass the inputs again on the second call instead of storing a Handle.
- A multi-step lifecycle with many states and transitions. Use a state machine entity, see [[enum-state-machine]].

## Related

- [[custom-operation-osgi-component]] — how the start and confirm operations are implemented and wired
- [[filestore-mediated-file-transfer]] — the overflow and final file binaries
- [[typed-exception-error-handling]] — rejecting an expired or already-confirmed Handle with a modeled fault
