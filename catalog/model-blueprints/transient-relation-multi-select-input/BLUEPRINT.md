---
id: transient-relation-multi-select-input
title: Transient Relation as Multi-Select Input Picker
description: An unmapped operation input transfer object holds a 0..* or 1..* transient relation to a mapped transfer object, so the user picks several existing records in the input form and the operation body links them.
aliases: [multi select input, input picker collection, transient collection picker, choose many records input]
keywords: [transient, relation, multi select, picker, range, input, operation parameter, collection, mutable, embedded table]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:alba, project:actiongroup-test-react, status:emerging]
category: relation
status: emerging
projects: [alba, actiongroup-test-react]
evidence: ["alba:unrecorded", "actiongroup-test-react:unrecorded"]
alternatives: [transient-relation-single-select-input]
fragment: transient-relation-multi-select-input
diagram: { kinds: [entity, transfer, operation], members: types }
first_seen: 2026-05-13
last_updated: 2026-11-10
---
## Intent

Let the user choose several existing records as part of an operation's input, for example the approvers of an approval task. The input is an unmapped transfer object with a transient relation of cardinality 0..* or 1..* to a mapped transfer object. The generated UI offers a picker for it and the operation body links the chosen records to the entity it creates.

This is the multi-pick variant. For one record see [[transient-relation-single-select-input]]. The model-level parent practice is [[transient-relation-parameter]].

### What the platform gives you

- A relation member of kind TRANSIENT is allowed on a transfer object and is not persisted. On an unmapped transfer object the validator requires aggregation, so the modeling tool sets that kind.
- For a relation with a range the generator emits a `getRangeFor<Name>` operation with a synthesized input (an `owner` relation and, for mapped references, a `queryCustomizer`); values outside the range fail with `NOT_ACCEPTED_BY_RANGE` ([platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md), range and choice operations).
- A range expression and a default expression can be set on a transient relation. See [[range-expression-filtering]].

### What is project practice

Alba assigned the picked users with `mutable input.users` in the body, and actiongroup-test-react did the same for `signs`. The agent-docs only describe `mutable` as a unary prefix operator and `input` as immutable unless declared mutable ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)); the link semantics for a transient collection are project experience, *verify* on your runtime version.

## Structure

- **Mapped target transfer object** (for example `ApproverView`): maps the entity to choose from.
- **Unmapped input transfer object** (for example `TaskInput`): transient attributes plus the picker relation.
- **Transient relation**: cardinality 0..* (optional) or 1..* (at least one), kind aggregation, target the mapped transfer object. Optional range expression (Alba: only active users with an eligible role).
- **Operation** taking the input. The body creates the owning entity and assigns the picked collection to a stored relation.
- **Stored relation** on the owning entity: 0..* association to the target entity.

## Constraints

- **The relation target must be mapped.** Without a persisted instance set there is nothing to list. The source projects observed that an unmapped target (a trivia answer list) renders nested sub-forms, one per element, and no range operation (*verify*).
- **The owning transfer object stays unmapped.**
- **The body must convert the transient collection into a stored one.** In the source projects, assigning without the conversion persisted an empty collection and raised no error. Write an integration test that submits a non-empty selection and asserts the persisted collection size.
- **Eligibility is enforced by the range**, and the platform rejects values outside it. Keep the eligibility rule in the range expression, not only in the UI.
- Interceptors never run around custom, mapped or script operations, so checks around this operation belong in its body.

## Variations

- **Optional or required non-empty**: 0..* or 1..*.
- **Filtered candidates**: a range expression, for example by status or role. See [[range-expression-filtering]].
- **Custom Java implementation**: resolve each picked record through the DAO and assign the collection; the agent-docs give no exact calls, *verify*.
- **Several pickers**: one transient relation each.

## When to use

- An operation creates or updates a record that must reference several existing records picked by the user.
- The choice belongs to the call, not to a stored form state.

## When to avoid

- Only one record is chosen. Use [[transient-relation-single-select-input]].
- The collection is edited on a stored entity. Use the entity's own relation page, see [[many-aggregation-crud-pattern]].
- The elements are new inline objects, not existing records. Use an unmapped transfer object list, see [[unmapped-transfer-dto]].

## Related

- [[transient-relation-single-select-input]] — the single-pick variant
- [[transient-relation-parameter]] — the parent model practice
- [[range-expression-filtering]] — limiting the selectable set
- [[many-aggregation-crud-pattern]] — add, remove and clear on a stored collection
- [[action-group-input-output-routing]] — routing of the operation input page
