---
id: "transient-relation-multi-select-input"
title: "Transient Relation as Multi-Select Input Picker"
domain: "model"
category: "relation"
score: 35.0
usage_count: 2
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - alba
  - actiongroup-test-react
---
## Description

An unmapped `*Input` transfer object holds a transient relation with cardinality `0..*` or `1..*` to a **mapped** transfer object. The JUDO generator emits a `getRangeFor<rel>()` service method on the owning operation/view, and the React frontend renders the field as an embedded table/list backed by a `RangeDialog` in multi-select mode plus add/remove row affordances. The operation body uses `mutable input.<rel>` to convert the picker selection into a stored collection on the created/updated entity.

This is the **multi-pick** variant of the broader pattern; for `0..1` / `1..1` see [`transient-relation-single-select-input`](../transient-relation-single-select-input/BLUEPRINT.md). The model-side parent best-practice is [`transient-relation-parameter`](../../best-practices/model/transient-relation-parameter.md).

> **Mapped-target verification.** This blueprint applies **only when the relation target is a mapped TO**. If the target is unmapped, the generator emits a nested structured input form instead of a picker — see the Trade-off section below.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for the `mutable input.<rel>` collection-assignment idiom and the silent-discard footgun.

## Frontend Implementation

See [frontend.md](frontend.md) for the embedded-table widget recipe, `RangeDialog single:false`, and runtime sequence.
