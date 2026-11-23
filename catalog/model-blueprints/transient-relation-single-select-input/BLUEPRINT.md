---
id: transient-relation-single-select-input
title: Transient Relation as Single-Select Input Picker
description: An unmapped operation input transfer object holds a 0..1 or 1..1 transient relation to a mapped transfer object, so the user picks one existing record in the input form and the operation body links it.
aliases: [single select input, input picker, transient reference picker, choose one record input]
keywords: [transient, relation, single select, picker, range, input, operation parameter, aggregation, mutable]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:itracker, status:single-project]
category: relation
status: single-project
projects: [itracker]
evidence: ["itracker:unrecorded"]
alternatives: [transient-relation-multi-select-input]
first_seen: 2026-05-13
last_updated: 2026-11-10
---
## Intent

Let the user choose one existing record as part of an operation's input, for example the region and category of an initiative that the operation creates. The input is an unmapped transfer object (named `*Input` in the source project) with a transient relation to a mapped transfer object. The generated UI offers a picker for the relation and the operation body links the chosen record to the entity it creates or updates.

This is the single-pick variant. For collections see [[transient-relation-multi-select-input]]. The model-level parent practice is [[transient-relation-parameter]].

### What the platform gives you

- A relation member of kind TRANSIENT is allowed on a transfer object and is not persisted ([[transient-relation-parameter]] cites the structure reference). On an unmapped transfer object the validator requires the relation to be an aggregation, so the modeling tool sets the kind to aggregation for it.
- For a relation with a range the generator emits a `getRangeFor<Name>` operation. Its input is a synthesized transfer object with an `owner` relation and, for mapped references, a `queryCustomizer` ([platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md), range and choice operations). Values outside the range are rejected with `NOT_ACCEPTED_BY_RANGE`.
- The metamodel offers a default expression and a range for transient relations. See [[range-expression-filtering]].

### What is project practice

The source project linked the picked record in the operation body with `mutable input.<relation>`. The platform docs say that `mutable` is a unary prefix operator, that `input` is immutable unless declared mutable, and that everything read from `input`, including a transient reference, stays immutable ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)). They do not describe the link semantics of a transient reference assigned to a stored relation, so treat the claim that a missing `mutable` silently drops the link as project experience and *verify* it on your runtime version.

## Structure

- **Mapped target transfer object** (for example a view of `Region`): mapped to its entity, so the picker has a persisted set to list.
- **Unmapped input transfer object** (for example `TaskInput`): the operation's input type. It holds the ordinary input fields as transient attributes and the picker relation.
- **Transient relation** on the input: cardinality 1..1 for a required choice, 0..1 for an optional one; kind aggregation (reference without ownership); target is the mapped transfer object, never the entity itself. Optional default expression (for example the first target instance) and an optional range expression (for example only active records).
- **Operation** taking the input transfer object. The body creates or updates the owning entity and assigns the picked reference to a stored relation of that entity.
- **Stored relation** on the owning entity (association) to the target entity. The diagram shows it as `Task --> Region`.

A second picker of the same shape on the same input (a category picker, for example) is simply another transient relation.

## Constraints

- **The relation target must be mapped.** A picker needs a persisted instance set to list. The source projects observed that an unmapped target renders a nested input form instead and no range operation (*verify*; the agent-docs say range operations are generated for mapped references).
- **The owning transfer object stays unmapped.** Entities cannot have transient relations.
- **The body must convert the transient reference into a stored one.** Assigning it without the conversion step loses the link in the source project's experience; test the operation and assert the persisted relation is set and points to the chosen record.
- **Interceptors never run around custom, mapped or script operations**, so a range or eligibility rule must live in the range expression or in the operation body, not in an operation call interceptor around the operation itself.
- The platform range check rejects values outside the range, so keep the range expression and the eligibility rule in one place.

## Variations

- **Required or optional**: 1..1 or 0..1.
- **Preselected value**: a default expression on the relation fills the picker when the form opens.
- **Filtered choices**: a range expression limits the candidates. See [[range-expression-filtering]].
- **Several pickers**: one transient relation each.
- **Custom implementation**: when the operation is a Java custom implementation, the conversion happens through the generated DAO API: look the chosen record up and assign it. Nothing in the agent-docs prescribes the exact calls, *verify*.

## When to use

- An operation creates or updates a record that must reference one existing record chosen by the user.
- The choice belongs to the call, not to a stored form state.

## When to avoid

- The reference lives on an entity the user edits directly. Use the entity's own relation and the generated single-relation selector.
- The target is not an entity with its own instances (free-form nested input). Use an unmapped transfer object attribute set, see [[unmapped-transfer-dto]].
- More than one record must be chosen. Use [[transient-relation-multi-select-input]].

## Related

- [[transient-relation-multi-select-input]] — the collection variant
- [[transient-relation-parameter]] — the parent model practice
- [[range-expression-filtering]] — limiting the selectable set
- [[unmapped-transfer-dto]] — the input object
- [[aggregation-input-widget]] — the frontend widget used for the picker
