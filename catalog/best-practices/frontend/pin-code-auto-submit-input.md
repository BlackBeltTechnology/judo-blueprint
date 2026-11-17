---
id: pin-code-auto-submit-input
title: PIN Code Multi-Field Auto-Submit Input
description: "A multi-field PIN code input where each digit has its own text field: focus advances on entry, backspace goes back, and the last digit submits automatically. Built as a custom component, not a generated widget."
aliases: [OTP input, activation code input, multi-digit code field]
keywords: [pin, code, otp, multi field, auto submit, auto advance, focus, custom component, mobile numeric keyboard]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: form
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [timed-step-auto-advance, dialog-based-navigation, input-masking-react-imask]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Let users enter a short numeric code (activation code, PIN, one-time code) digit by digit on a phone without pressing a submit button.

## Practice

### Platform base

- The generated UI has no multi-field code widget; a text attribute is one `TextField` ([widgets](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md)). Such an input is a custom component.
- A model element that the generator exposes as an extension point is replaced by registering an `FC` under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` with the per-element `component` key from the container's `customization.ts`. The register function comes from the generated `register<Container>CustomImplementations.tsx.default` scaffold and is called from `application-customizer.tsx` ([custom component replacement](../../agent-docs/frontend/advanced-patterns.md)). The real props are the proxy props type of that scaffold.

### Practice notes: the PIN component

The component below is custom code, not a platform feature:

- One `TextField` per digit with `type="tel"`, so phones show the numeric keyboard.
- Entering a digit moves focus to the next field. Backspace in a field moves focus to the previous one.
- When the last field is filled, the component calls an `onAutoSubmit(code)` callback; no submit button.
- The first field gets focus on mount, after a short delay (the example uses 300 ms) so the dialog or page has rendered.
- The digit count is fixed in the component (four in the example).

```typescript
// Illustrative; names are examples
const handleChange = (index: number, value: string) => {
  if (value.length === 1 && index < 3) refs[index + 1].current?.focus();
  const code = updateDigit(index, value);
  if (code.length === 4) onAutoSubmit(code);
};
const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
  if (e.key === 'Backspace' && index > 0) refs[index - 1].current?.focus();
};
```

## Rationale

The input suits mobile entry and needs no extra tap to submit. The cost is a fixed digit count, a hand-written component to maintain, and extra ARIA work for accessibility.

## Example

One app: `NumberInputAutoFocus` in `CustomComponents.tsx` collects the 4-digit activation code in the participant frontend. Completing the fourth digit calls the activation operation through the generated service (`accessServiceImpl.activate()`).

## When to avoid

- The code length varies or may contain letters; use a normal text field, optionally with a mask ([[input-masking-react-imask]]).
- Users paste codes from a message; a single field handles paste more simply.

## Related

- [[timed-step-auto-advance]] — another auto-advancing input flow
- [[dialog-based-navigation]] — dialogs that host such inputs
- [[input-masking-react-imask]] — formatted single-field input
