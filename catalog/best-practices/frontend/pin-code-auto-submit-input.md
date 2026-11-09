---
id: "pin-code-auto-submit-input"
title: "PIN Code Multi-Field Auto-Submit Input"
domain: "frontend"
category: "form"
score: 39.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
---
## Description

A multi-field PIN code input component where each digit gets its own `TextField`. Focus auto-advances to the next field on digit entry and auto-submits the form when the last digit is entered. Supports backspace to return to the previous field. Uses `type="tel"` to trigger the numeric keyboard on mobile devices. Auto-focuses the first field on mount.

## Structure

```typescript
// NumberInputAutoFocus - 4 separate single-digit inputs
const refs = [useRef(), useRef(), useRef(), useRef()];

const handleChange = (index, value) => {
  if (value.length === 1 && index < 3) {
    refs[index + 1].current.focus();  // Auto-advance
  }
  const newCode = updateDigit(index, value);
  if (newCode.length === 4) {
    onAutoSubmit(newCode);  // Auto-submit on 4th digit
  }
};

const handleKeyDown = (index, e) => {
  if (e.key === 'Backspace' && index > 0) {
    refs[index - 1].current.focus();  // Back on delete
  }
};

// Auto-focus first field after 300ms delay
useEffect(() => {
  setTimeout(() => refs[0].current?.focus(), 300);
}, []);
```

## Examples

### Trivia
`NumberInputAutoFocus` in `CustomComponents.tsx` provides 4-digit activation code entry for the Player frontend. Each digit is a separate `TextField` with `type="tel"` for mobile numeric keyboard. Auto-advances focus on entry, auto-submits `playerServiceForApplicationImpl.activate()` when 4th digit is entered. 300ms delayed auto-focus on mount.

## Trade-offs

- **Pros**: Excellent mobile UX; no submit button needed; numeric keyboard on mobile; intuitive digit-by-digit entry
- **Cons**: Fixed to a specific digit count; custom implementation (not a library); accessibility may require additional ARIA attributes
- **When to use**: Activation codes, OTP verification, PIN entry, any short numeric code input

## Related Patterns

- [timed-quiz-auto-advance](timed-quiz-auto-advance.md)
- [dialog-based-navigation](dialog-based-navigation.md)
