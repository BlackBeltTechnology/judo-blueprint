---
id: input-masking-react-imask
title: Input Masking with react-imask for Formatted Fields
description: "Use the `react-imask` library (IMaskInput) within custom visual element overrides to enforce specific input formats on text fields."
aliases: []
keywords: [input mask, react-imask, IMaskInput, textMask, custom visual element, formatted field]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: form
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/custom-implementations/registerServicesPartner_servicePartnerPartner_View_EditCustomImplementations.tsx"]
alternatives: []
related: [custom-visual-element-override, masked-input-integration]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A text field must accept only a fixed format (tax numbers, phone numbers, postal codes) and show the format while the user types. This practice uses `react-imask` in a custom component when the model's own mask is not enough.

## Practice

### Platform base

- The model already carries an input mask: `textMask` on a string widget is applied only when `textWidget=INPUT` and `textMultiLine=false` ([widget attributes](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md)). Try this first.
- A format rule that must be enforced as validation belongs on the data type, not the UI: a regular expression is a property of a dedicated string type, not of the attribute ([advanced modeling patterns](../../agent-docs/model/advanced-modeling-patterns.md)). The backend validates; a mask only guides input.
- `imask` and `react-imask` are added as npm dependencies, and an `IMaskInput` can be wrapped in a MUI text field ([advanced patterns, IMaskInput integration](../../agent-docs/frontend/advanced-patterns.md)).
- A model-designated custom element is rendered by a component you register ([[custom-visual-element-override]]).

### Practice notes: masked fields in a custom element

When the model mask cannot express the behaviour (placeholder shown at once, empty mask mapped to null, upper-casing), a custom visual element replaces the generated input group. This is practice, not a platform feature.

- The text field uses `IMaskInput` as its input component, with a mask such as `00000000-0-00`, a placeholder character, `lazy: false` (mask always visible) and `overwrite: true`.
- `onAccept` pushes the value into page state with `storeDiff`. A value that equals the bare mask is converted to null, and it writes only when the value really changed.
- Read validation messages and the disabled / read-only state from the page actions and data, so the field behaves like the generated ones.

```tsx
// Example code (inside a custom element component)
<TextField
  inputProps={{
    mask: '00000000-0-00',
    placeholderChar: '_',
    lazy: false,
    overwrite: true,
    onAccept: (value: string) => {
      const real = !value || value === '________-_-__' ? null : value;
      if ((data.taxId || real) && data.taxId !== real) {
        storeDiff('taxId', real ? String(real).toUpperCase() : real);
      }
    },
  }}
  InputProps={{ inputComponent: IMaskInput as any }}
/>
```

## Rationale

The mask prevents malformed input before the server sees it and shows users the expected shape. It is only convenience: the server-side type constraint stays the authority, and the mask pattern has to match it. The cost is a custom element plus an extra dependency.

## Example

One app's partner view/edit page replaces a group of three tax-number fields. Two use the mask `00000000-0-00` (a national tax number format) with upper-casing; the third (an EU tax number) is a plain text field because its format varies. See [[masked-input-integration]] for the blueprint view.

## When to avoid

- The model `textMask` already gives the format you need.
- Format errors can be reported by backend validation alone.
- The field is read-only or free text.

## Related

- [[custom-visual-element-override]] — how the replacing component is registered
- [[masked-input-integration]] — the blueprint with the same example
