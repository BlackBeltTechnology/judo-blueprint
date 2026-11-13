---
id: registry-header-with-lines
title: Registry with Headers, Lines and Line Classifications
description: A registry entity with a status enumeration that owns headers, where each header owns line items and each line owns its own classification records, so a whole submission is stored and deleted as one aggregate.
aliases: [header line aggregate, registry header and lines, document header with line items, line qualification]
keywords: [header, line, registry, composition, classification, aggregate, status, submission]
tags: [domain:model, layer:model, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: []
related: [draft-done-status-enum, state-transition-history-entry]
fragment: registry-header-with-lines
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-09-24
last_updated: 2026-11-10
---
## Intent

Store one submission that contains many findings as a single aggregate. A registry is the root. It owns headers, a header owns line items, and each line owns classification records that say how that line was judged. The registry has a status that moves from draft to submitted and on to returned or done.

### The registry is the unit of work

Users create, submit and return the registry as a whole. The headers and lines have no life of their own, so they are composed by the registry and removed with it.

### Classification data belongs to the line

A line is more than a description. Each line carries zero or more classification records (a code, a passed flag and a remark). Keeping them under the line, not under the header, lets a header hold lines that were judged differently.

## Structure

- **Registry** has a stored `status` attribute of an enumeration with the values draft, submitted, returned and done, and a composition to many headers.
- **RegistryHeader** has general attributes (a free-text finding, a creation timestamp) and a composition to many lines.
- **RegistryLine** has descriptive attributes and a composition to many classification records.
- **LineClassification** has a code, a boolean passed flag and a text remark.

All three relations are compositions with cardinality 0..*. Every owned entity is reachable only through its owner.

## Constraints

- Compositions delete the owned records with the owner, so no orphan header, line or classification stays behind.
- A back reference from a line to its header, or from a header to the registry, is a derived relation. The model stores the link in one direction only.
- Status changes go through explicit operations, not through free editing of the status attribute; see [[draft-done-status-enum]].
- Existing rows get a value for any attribute added later. A new required column needs a data step that backfills a default, because the generator emits a bare nullable column.
- Per-line rules (for example a range check on a code) have to run on the line or its classification, not only on the registry.

## Variations

- **Single header.** If every registry has exactly one header, make the relation 0..1 or fold the header attributes into the registry.
- **Attachments on the header.** Add an attachment composition to the header, or to the line, when files belong to a finding.
- **Created from proposals.** The registry can be built from earlier proposal records. Each proposal becomes a line, and the proposal moves to a converted state.
- **Status history.** Record each status change as a history entry; see [[state-transition-history-entry]].

## When to use

- A submission has a root, a grouping level and many detail lines.
- Each detail line needs its own pass/fail or grading data.
- The whole tree is submitted, returned or archived together.

## When to avoid

- Only one level of lines exists. A plain owner with a line collection is simpler; see [[quote-lines-with-price-modifiers]] for that shape with prices.
- Lines are shared between several owners. Use associations, not compositions.
- Lines change state on their own schedule. They then need their own status and their own lifecycle.

## Related

- [[draft-done-status-enum]]: a small status enumeration with the same draft and done values
- [[state-transition-history-entry]]: records each status change of the registry
- [[quote-lines-with-price-modifiers]]: another header and line aggregate, with priced lines
