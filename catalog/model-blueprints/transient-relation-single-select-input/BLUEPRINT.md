---
id: "transient-relation-single-select-input"
title: "Transient Relation as Single-Select Input Picker"
domain: "model"
category: "relation"
score: 30.0
usage_count: 1
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - itracker
---
## Description

An unmapped `*Input` transfer object holds a transient relation with cardinality `0..1` or `1..1` to a **mapped** transfer object. The JUDO generator emits a `getRangeFor<rel>()` service method on the owning operation/view, and the React frontend renders the field as an `AggregationInput` widget driven by a `RangeDialog` in single-select mode. The operation body uses `mutable input.<rel>` to convert the transient picker selection into a stored relation on the created/updated entity.

This is the **single-pick** variant of the broader pattern; for collection cardinalities see [`transient-relation-multi-select-input`](../transient-relation-multi-select-input/BLUEPRINT.md). The model-side parent best-practice is [`transient-relation-parameter`](../../best-practices/model/transient-relation-parameter.md).

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for the `mutable input.<rel>` operation-body idiom and the silent-discard footgun.

## Frontend Implementation

See [frontend.md](frontend.md) for the `AggregationInput` + `RangeDialog single:true` widget recipe and runtime sequence.
