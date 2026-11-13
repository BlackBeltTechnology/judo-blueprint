---
id: document-registry-sequence
title: Document Registry Sequence Number Generator
description: A non-CRUD registry entity that holds a prefix, period boundaries and a numeric range per document type, and hands out consecutive document numbers under a lock.
aliases: [document numbering, registry number sequence]
keywords: [document, registry, sequence, number, prefix, period, transition, lock]
tags: [domain:model, layer:model, layer:backend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: [rackinspect:model/rackinspect.model, rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/RegistryServiceImpl.java]
alternatives: [enum-state-machine]
fragment: document-registry-sequence
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give each kind of numbered document its own sequence, so that fault registries, offers, assessment sheets and other documents each count consecutively under their own prefix, and their numbers stay unique even when two documents are generated at once.

## Structure

One non-CRUD entity, `DocumentRegistry`, holds one row per document type and period. It has a `documentType` (an enumeration with one member per kind of document), a `prefix` string, a financial period (start and end dates), a transition period (start and end dates), and an index range (`startIndex`, `endIndex`) with a running `currentIndex`. The enumeration `DocumentType` holds one member per document kind. Each member has an ordinal that is persisted with the model. A custom service in application code picks the registry row for a date and advances `currentIndex`.

## Constraints

- The platform already offers number sequences (the `SEQUENCE` variable category, database sequences by default). They are gap-tolerant and have no prefix, period or reset. This blueprint is common practice on top of the platform for gap-free, per-period, prefixed numbers.
- The registry row is not created, updated or deleted by clients. Rows are seeded at setup, and only the sequence service advances `currentIndex`.
- The increment and the read happen inside one lock. Without it, two documents generated at the same time can get the same number. This is application code, not a platform feature.
- A number is burned when it is issued, even if the document generation later fails. Decide how failures are handled before the sequence goes live.
- The number width comes from the digit count of `endIndex`, so the width is fixed for a row.
- Periods do not overlap within one document type, except for the transition period, which the lookup handles explicitly.

## Variations

- **One registry per document type.** Each type has its own row set. Use this when the types count independently.
- **One registry shared by types.** Use one counter for all types only when the business needs a single number space. The prefix then carries the type.
- **Transition period.** A date inside the transition period uses the period that matches the target date rather than the current date.

## When to use

- Documents need consecutive, human-readable numbers that restart by period.
- Several document kinds need separate counters.
- The numbers must stay unique under concurrent generation.

## When to avoid

- The numbers only need to be unique identifiers. Use a generated identifier, or the platform sequence through a default expression; see [[sequence-based-identifier]].
- The number space is global and never resets. A single counter attribute on a settings entity is enough.
- The documents are never shown to users. Use an internal identifier.

## Related

- [[enum-state-machine]]: the enumeration pattern used for the document type
- [[document-review-state-machine]]: a document lifecycle that often runs after the number is issued
- [[sequence-based-identifier]]: the platform sequence variable, for numbers without periods or prefixes
- [[category-enum-pattern]]: choosing an enumeration for the document type
