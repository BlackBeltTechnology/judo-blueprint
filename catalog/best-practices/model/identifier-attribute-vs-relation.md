---
id: "identifier-attribute-vs-relation"
title: "Identifier as Attribute vs. Identifier as Relation — Decision Heuristic"
domain: "model"
category: "relation"
score: 60.0
usage_count: 1
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - compsych-letter-demo
---

## Description

Identifier-shaped attributes on Transfer Objects fall into two distinct categories: **legitimate domain identifiers** (business values that carry meaning beyond uniqueness) and **antipattern surrogate keys** (opaque strings standing in for what should be a typed relation). The two are visually identical in the model — both look like `*Id : String` — but their downstream behaviour diverges sharply: the first survives every transformation cleanly; the second silently disables the JUDO framework's referential integrity, picker generation, and `mutable input.<rel>` conversion.

This best-practice gives the decision rule: when to keep an `*Id` String attribute, when to replace it with a relation to a typed TO.

## Structure

### Keep as attribute when at least one of these holds

- **Business identifier.** The value is the externally visible identity carried by the entity itself (printed barcode, ISBN, invoice number, NHS number). Replacing with a relation loses the *meaning* — there is no separate entity to relate to; the string IS the thing.
- **Ephemeral / opaque session token.** The value is a system-generated handle whose only purpose is to retrieve the bearer entity (REST session id, OAuth state nonce, generation handle, upload token). No business object exists independently of the bearer.
- **Pre-allocated future identifier.** The value names an entity that does not yet exist at the time the attribute is written (a barcode value reserved at session start before the document materializes at session confirm). A relation cannot point at a non-existent target.
- **Polymorphic target reference.** The value identifies a target whose type varies (an audit-event target could be a Template, a Rule, or a DataObject). ESM has no clean polymorphic association; the canonical shape is a `targetIdentifier : String` plus a `targetType : Enum` pair.

### Replace with relation when at least one of these holds

- **Input picker for an existing typed entity.** The value identifies a row the user picks from an existing collection (selecting a Template / Design / DataObject for a generation operation). The JUDO contract here is a TRANSIENT relation `[1..1]` to a mapped TO; the generator emits a `getRangeFor<rel>()` service method and the React frontend renders an `AggregationInput` picker. A String here disables all of that.
- **Foreign-key-by-string between two stored entities.** The model already carries one entity that needs to reference another; expressing the link as a string defers referential integrity to operation impls and re-resolves on every read. Use an `ASSOCIATION` relation instead.

## Examples

### CompSychLetter — legitimate domain identifiers (kept as attributes)

| Member | Why it stays |
|---|---|
| `entities::Document.documentId` (`BarcodeCode128Type`) | The printed barcode value. It IS the domain identifier — Documents are referenced externally by this string. |
| `entities::GenerationHandle.handleId` (`StringType128`) | Opaque session token; ephemeral. The handle entity is reached *only* by this id. |
| `entities::GenerationHandle.documentId` (`StringType128`) | Pre-allocated barcode value reserved at `startGeneration` time. The Document entity does not exist yet at the moment this attribute is written — no relation possible. |
| `entities::LlmAuditEvent.targetIdentifier` | Polymorphic — target could be Template, Rule, or DataObject. Companion `targetType : LlmAuditEventKind` enum disambiguates. |

### CompSychLetter — antipattern fixed (replaced with relations)

`services::api::StartGenerationInput` and `services::api::ConfirmGenerationInput` originally carried four TRANSIENT String attributes (`objectId`, `templateId`, `designId`, `generationHandle`) as picker-style inputs to the start/confirm operations. The operations had to re-resolve each string by ID lookup in custom Java and raise `*_NOT_FOUND` faults manually; the React form rendered four plain text fields with no validation and no `AggregationInput` widget. The fix (change `add-document-generation-operations` §1.5) replaces the four String attrs with four TRANSIENT `AGGREGATION 1..1` relations targeting mapped TOs (`DataObjectApiTO`, `TemplateApiRef`, `DesignApiRef`, `GenerationHandleApiRef`). The framework now rejects unresolvable references at the binding layer; operation impls drop the `*_NOT_FOUND` paths; the form renders four typed pickers.

## Trade-offs

- **Relation on input TO** adds one TO per target type if the API package wants a stable shape independent of dashboard projections (see [`api-package-thin-ref-projection`](api-package-thin-ref-projection.md) for the thin-ref variant). For a fully UI-internal input, reusing an existing dashboard TO costs nothing.
- **Keeping String for a true business identifier** is not "less safe" — it is the correct shape. Trying to wrap a barcode value in a relation introduces a phantom entity and breaks the printed-on-paper semantic.
- **Polymorphic target via String + Type enum** sacrifices type safety in the model to gain a single audit / event log entity that covers heterogeneous targets. Alternative is one log entity per target type (cleaner types, more model surface). Pick based on how often new target types are added.

## Anti-Patterns

- **`*Id : String` on an input TO that is consumed by an operation creating or updating an entity with a corresponding relation.** Silent loss of referential integrity, no generated picker, manual `*_NOT_FOUND` everywhere.
- **`*Id : String` on a TO when the target is a single stable entity type and the cardinality is `0..1` or `1..1`.** Should be a relation; the String form gains nothing.
- **Replacing a legitimate domain identifier (barcode, session token) with a relation just to satisfy a "no String IDs" rule.** Cargo-culting; loses semantic content.

## Verification

```bash
# Find suspicious *Id / *Identifier members across the project, separating
# the entity-level domain identifiers (likely legitimate) from the input-TO
# antipatterns (likely fixable).
judo_cli graphql '{ esm { datamembers(where: {fqn: {startsWith: "<NAMESPACE>::"}}, limit: 300) {
  items { fqn name memberType dataType { fqn } } } } }' \
  | jq -r '.data.esm.datamembers.items[]
      | select(.name | test("(Id$|Identifier$|Ref$|Uuid$)"))
      | "\(.memberType)\t\(.fqn)\t\(.dataType.fqn)"'
```

Triage each hit against the *Keep* / *Replace* criteria above. For each *Replace* hit, plan the relation target TO (existing or thin ApiRef) before mutating.

## Related Patterns

- [api-package-thin-ref-projection](api-package-thin-ref-projection.md) — when an input TO is in an API package and you don't want to leak dashboard projection through to API consumers.
- [transient-relation-single-select-input](../../model-blueprints/transient-relation-single-select-input/BLUEPRINT.md) — the relation shape that replaces an `*Id` String on an input TO.
- [audit-event-entity](audit-event-entity.md) — the polymorphic `targetIdentifier` + `targetType` shape for cross-type event logging.
- [sequence-based-identifier](sequence-based-identifier.md) — when a String identifier IS the domain (sequence-generated codes, document numbers, barcodes).
