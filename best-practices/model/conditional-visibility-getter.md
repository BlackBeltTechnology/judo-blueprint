---
id: "conditional-visibility-getter"
title: "Conditional Visibility Getter Expression"
domain: "model"
category: "transfer"
score: 27.3
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - park-here
---
## Description

Derived attributes on transfer objects use conditional (ternary) getter expressions to reveal or hide data based on the state of a parent or related entity. This provides model-level security by controlling data visibility without requiring custom backend code.

## Structure

- Uses ternary expression in getter: `condition ? realValue : sentinelValue`
- Condition typically checks a status enum on a parent/container entity or the presence of a related entity
- Uses `self!container(ParentType)` for composition navigation to check parent state
- Uses `self.relation!isDefined()` to check optional relation existence
- Sentinel value is usually an enum member like `NONE` or a null/empty value

```
answer: self!container(Test).status == TestStatus#FINISHED ? self.answer : Choice#NONE
```

## Examples

### Trivia
`player::Prompt.answer` and `player::Prompt.solution` both use conditional getters: they return `Choice#NONE` while the test is active and only reveal actual values when `self!container(Test).status == TestStatus#FINISHED`. This prevents players from seeing answers during the quiz.

### ParkHere
Reservation entity uses ternary expressions to adapt display attributes based on guest presence: `reserverName = self.guest!isDefined() ? self.guest.name : self.owner.name`, `reserverCarId = self.guest!isDefined() ? self.guest.licensePlate : self.car.licensePlate`, `reserverEmail = self.guest!isDefined() ? self.guest.email : self.owner.email`. This creates a polymorphic "view" that shows guest info for guest reservations and owner info for regular reservations, without separate entity types.

## Trade-offs

- Pros: Security enforced at the model layer (not just UI), no custom code needed, declarative
- Cons: Limited to simple conditions in getter expressions, complex logic may need custom operations
- Prefer when: Data visibility depends on lifecycle state and must be enforced server-side

## Related Patterns

- [enum-state-machine](enum-state-machine.md)
- [derived-attribute-flattening](derived-attribute-flattening.md)
