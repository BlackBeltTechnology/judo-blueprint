---
id: aggregation-input-widget
title: Aggregation Input Widget for Entity Associations
description: A reusable form widget that shows a single entity association as a label list with context-sensitive view, create, remove and delete actions and a range dialog for selection.
aliases: [association input, single relation widget]
keywords: [aggregation, input, widget, association, range dialog, single relation, form]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: form
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [promise-based-dialog-system, view-edit-mode-toggle]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A form field that represents a single aggregation or required relation has several states: set, empty, view mode, edit mode. One widget handles all of them, so every association in the frontend behaves alike.

## Practice

### Platform base

- A single relation is generated as an autocomplete-style selector with view, set and unset actions ([UI model to frontend mapping: single relation](../../agent-docs/frontend/model-screen-layout.md)). Which actions exist follows the relation's create, update and delete flags in the model ([CRUD flags on relations](../../agent-docs/frontend/model-screen-layout.md)).
- The options of a selector come from a generated range operation (`GET_RANGE`): an unbound operation whose input is an unmapped transfer object carrying the owner, with the range type as output ([operation reference](../../agent-docs/model/esm_metamodel/operation.md)).
- The widget below replaces the generated selector. It must keep calling the generated range service so server-side paging, filtering and access rules still apply.

### Practice notes: one widget for the whole association lifecycle

This layer is practice, not a platform feature:

- The widget shows the associated entity's chosen properties as a concatenated label list.
- Icons depend on state: view and delete in read-only mode, remove in edit mode, create when the association is empty.
- Setting the association opens a range dialog for single selection and writes the chosen object into the form data.
- All behavior is passed in as callbacks, so the widget owns no data access.

```tsx
// Example code: AggregationInput is a custom component, not a platform API
<AggregationInput
  label="Parent"
  labelList={[data.parent?.name ?? '', data.parent?.code ?? '']}
  value={data.parent}
  readonly={!editMode}
  onSet={async () => {
    const res = await openRangeDialog({ columns, rangeCall, single: true });
    if (res) setData({ ...data, parent: res });
  }}
  onView={() => navigate(`/view/${data.parent?.__signedIdentifier}`)}
  onCreate={() => navigate('/parent/create')}
  onDelete={async () => { await service.delete(data.parent); fetchData(); }}
  onRemove={() => setData({ ...data, parent: null })}
/>
```

Props: `value`, `labelList`, `icon`, `readonly`, `onSet`, `onView`, `onCreate`, `onDelete`, `onRemove`, `error`, `helperText`.

## Rationale

One component with all states gives a consistent experience for every entity relation and plugs into the range dialog. The cost is a wide prop interface, fragile label concatenation and the assumption of single selection.

## Example

One app uses the widget for an order-to-customer association. In view mode it shows name and email with view and delete icons; in edit mode a remove icon; when empty a create icon. Selection opens a range dialog with server-side paging and filtering against the generated range call of the order page.

## When to avoid

- The generated relation selector already fits the UX.
- The relation is multi-valued; use a table or multi-select instead.
- The relation lacks the create, update or delete flags the icons assume.

## Related

- [[promise-based-dialog-system]] — the range dialog is opened as a promise
- [[view-edit-mode-toggle]] — the readonly flag follows the view/edit mode
