---
id: trinary-logic-widget
title: Trinary Logic Combobox for Nullable Booleans
description: "A dropdown widget that shows a nullable boolean as Yes, No or Unknown, for hand-built forms and filters; the generated frontend offers a checkbox or a Yes/No combo."
aliases: [nullable boolean select, three-state boolean]
keywords: [trinary, nullable, boolean, combobox, null, unknown, booleanWidget, filter, widget]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: form
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [view-edit-mode-toggle, promise-based-dialog-system]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An optional boolean attribute has three states: true, false and not set. A checkbox shows only two. This practice renders the field as a three-option dropdown so "not set" is visible and can be chosen, in forms and in table filters.

## Practice

### Platform base

- A boolean attribute in the UI model has a `booleanWidget` setting with two values: `CHECKBOX` and `COMBO`, a dropdown with Yes/No options ([boolean type rules](../../agent-docs/model/esm_metamodel/ui-behaviour.md), [BooleanWidget](../../agent-docs/model/esm_metamodel/ui.md)). Neither documentation page describes a dedicated "unknown" option for the generated widgets, so check the generated form in the target version before building a custom one.
- A model-level alternative is to avoid the third state: make the attribute required with a default, or use a small enumeration with an explicit "unknown" member, which the generated frontend renders natively.

### Practice notes: a custom three-option combobox

This is custom code, written for a frontend with hand-built pages:

- A value-to-label map: `null` is "Unknown", `true` is "Yes", `false` is "No".
- A select component with the usual form props: name, label, value, change handler, `readOnly`, error and helper text.
- The same component serves as the `trinaryLogic` filter type of the filter dialog for boolean columns.

```typescript
// Example code
const TRINARY_LOGIC = new Map<boolean | null, string>([
  [null, 'Unknown'], [true, 'Yes'], [false, 'No'],
]);

<TrinaryLogicCombobox
  name="real" label="Real" readOnly={!editMode}
  value={data?.real}
  error={!!validation.get('real')} helperText={validation.get('real')}
  onChange={(value) => setData({ ...data, real: value })}
/>
```

## Rationale

The widget maps one to one onto what the database and the REST layer carry for a nullable boolean, and it behaves the same in forms and filters. The cost is a custom component to maintain, and "Unknown" may read oddly where users expect "Not set"; the label should be i18n-driven.

## Example

One hand-built app uses the component for several boolean fields of its forms and for boolean column filters. It honours the read-only flag of [[view-edit-mode-toggle]].

## When to avoid

- On generated forms: use the model's `booleanWidget` setting, or an enumeration with an explicit unknown member.
- When the attribute is required: a checkbox or Yes/No combo is enough.

## Related

- [[view-edit-mode-toggle]] — the read-only mode this widget respects
- [[promise-based-dialog-system]] — dialog handling around the same forms and filters
