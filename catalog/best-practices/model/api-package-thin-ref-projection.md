---
id: "api-package-thin-ref-projection"
title: "Thin ApiRef TO for Cross-Package Input Picker Relations"
domain: "model"
category: "transfer-object"
score: 55.0
usage_count: 1
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - compsych-letter-demo
---

## Description

When an input TO in a stable API package needs a typed picker relation to an entity that is already projected in a dashboard package, two valid shapes exist: **reuse the dashboard TO** as the relation target (minimal surface, cross-package coupling) or **declare a thin ApiRef projection** in the API package itself (stable API surface, +1 TO per target type). This best-practice covers the thin-ref variant and the tradeoff against direct reuse.

The thin-ref shape preserves the boundary that an API-versioning discipline wants: dashboard projections grow derived attrs, lifecycle flags, and embedded grids over time as the UI evolves; the API contract should not move with them. The thin ApiRef carries the minimum the API caller needs to identify and label the target — typically `name` and one or two stable scalars.

## Structure

For each entity `X` reachable from a stable API input, declare in the `services::api::` package (or whichever package hosts the API DTOs):

- `services::api::XApiRef` — `TransferObjectType`, `createable=false`, `updateable=false`, `deleteable=false`.
- A `mapping` child targeting `entities::X`.
- 1–3 MAPPED data members projecting only the stable identification / display attrs (usually `name`, sometimes a single classifier like `originalLanguage` or `state`). Do **not** project mutable lifecycle attrs, derived counts, or embedded relations — those belong on the dashboard TO.

Then declare the relation on the API input TO:

```
services::api::SomeInput
├── relation: target → services::api::XApiRef [1..1]
│   memberType: transient
│   relationKind: AGGREGATION
```

Targets must be `TransferObjectType`s (never `EntityType`s) — TO→Entity coupling lives only inside each TO's `mapping` child.

## Examples

### CompSychLetter — three ApiRef TOs for the document-generation API

The `services::api::StartGenerationInput` and `ConfirmGenerationInput` TOs needed typed picker relations to Template, DataObject, Design, and GenerationHandle. Three of these had only dashboard projections (`TemplateTO`, `DesignTO`, `GenerationHandleTO`) carrying derived attrs (`variantCount`, `tokens`, embedded `variants` grid) irrelevant to API consumers; `DataObjectApiTO` already existed as a thin API projection from Wave 2.4.

The change `add-document-generation-operations` §1.5 adds:

- `services::api::TemplateApiRef` — maps `entities::Template`, attrs: `name`, `originalLanguage`.
- `services::api::DesignApiRef` — maps `entities::Design`, attrs: `name`.
- `services::api::GenerationHandleApiRef` — maps `entities::GenerationHandle`, attrs: `handleId`, `documentId`, `state`.

And four TRANSIENT AGGREGATION 1..1 relations on the input TOs targeting the four refs. The dashboard `*TO` projections remain free to grow without breaking the API contract.

## Trade-offs

| Concern | Thin ApiRef (this pattern) | Reuse dashboard TO |
|---|---|---|
| Model surface | +1 TO per target entity type (with mapping + 1–3 MAPPED members) | 0 new TOs |
| API ABI stability | dashboard projection changes don't move API contract | every dashboard attr addition shows up in API responses |
| Picker behaviour | generator emits `getRangeFor<rel>()` against the ApiRef; range queries hit the same backing entity DAO | identical (generator only needs a mapped TO) |
| Implementation cost in operation body | `mutable input.<rel>` resolves to the same entity reference regardless of which TO mediates | identical |
| Test data builders | one extra factory per ApiRef | none |

Use reuse when the API surface and the UI are explicitly co-versioned (MVP, internal-only APIs, prototype phases). Switch to thin ApiRef when an external HTTP client exists or when the dashboard TO has grown past the attrs the API caller needs (a TO with 20+ attrs and 3 embedded grids is too much for a picker reference).

## Anti-Patterns

- **Mapping the same entity through both a dashboard TO and an ApiRef without an explicit reason.** Adds a TO for no benefit if the dashboard TO is already minimal.
- **Projecting derived attrs or embedded relations on the ApiRef.** Defeats the whole point — the ApiRef becomes a parallel dashboard TO.
- **Targeting `entities::X` directly from the input TO relation.** TO→Entity relations are not how JUDO models cross-type references on transfer objects; the relation target must be a `TransferObjectType`.

## Verification

```bash
# List ApiRef-style TOs (thin mapped projections in an API package)
judo_cli graphql '{ esm { transferobjecttypes(where: {fqn: {startsWith: "<NAMESPACE>::services::api::"}}, limit: 50) {
  items { fqn mapping { target { fqn } }
    attributes { totalCount items { name } }
    relations { totalCount items { name } } } } } }'
```

A healthy ApiRef has: `mapping.target` set, `attributes.totalCount` ≤ 3, `relations.totalCount = 0`. Any ApiRef with embedded relations or > 3 attrs has drifted toward dashboard-shape and should be reviewed.

## Related Patterns

- [transient-relation-single-select-input](../../model-blueprints/transient-relation-single-select-input/BLUEPRINT.md) — the relation mechanism this pattern's targets serve.
- [identifier-attribute-vs-relation](identifier-attribute-vs-relation.md) — the decision rule that drives needing an ApiRef in the first place.
- [actor-based-transfer-projection](actor-based-transfer-projection.md) — companion pattern for actor-scoped projections vs API-scoped projections.
