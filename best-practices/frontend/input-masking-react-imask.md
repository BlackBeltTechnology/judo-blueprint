---
id: "input-masking-react-imask"
title: "Input Masking with react-imask for Formatted Fields"
domain: "frontend"
category: "form"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

Use the `react-imask` library (IMaskInput) within custom visual element overrides to enforce specific input formats on text fields. The mask defines a pattern (e.g., `00000000-0-00` for Hungarian VAT IDs), placeholder characters appear immediately, and the `onAccept` callback propagates the formatted value to the form state via `storeDiff`. This is implemented through a custom visual element that replaces the generated text input group.

## Structure

```typescript
// Custom visual element component
<TextField
  inputProps={{
    mask: '00000000-0-00',
    onAccept: (value) => {
      let realValue = value === '________-_-__' || value?.length === 0 ? null : value;
      if ((data.field || realValue) && data.field !== realValue) {
        storeDiff('field', realValue ? String(realValue).toUpperCase() : realValue);
      }
    },
    placeholderChar: '_',
    lazy: false,      // Always show mask
    overwrite: true,  // Overwrite mode
  }}
  InputProps={{
    inputComponent: IMaskInput as any,
  }}
/>
```

## Examples

### RackInspect
Partner view/edit uses `react-imask` for three VAT ID fields: `vatId` and `vatIdGroup` use mask `00000000-0-00` (Hungarian tax number format), while `vatIdEu` uses a plain text input without masking. The mask renders placeholder underscores (`_`) immediately, enforces digit positions, and converts to uppercase on accept.

## Trade-offs

- **Pros**: Enforced format prevents invalid input; visual mask guides user; consistent data format
- **Cons**: Requires custom visual element override (not just a hook); `react-imask` adds bundle size; mask pattern must match backend validation
- **When to use**: Tax IDs, phone numbers, postal codes, or any field with a fixed format pattern

## Related Patterns

- [custom-visual-element-override](custom-visual-element-override.md)
