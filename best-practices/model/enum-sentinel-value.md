---
id: "enum-sentinel-value"
title: "Enum Sentinel Value Pattern"
domain: "model"
category: "enum"
score: 39.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - InterfaceRegister
---
## Description

Enumerations include a sentinel member (like `NONE`) that represents the absence of a meaningful value. This is used as a default value for attributes where "no selection" is a valid state, and in conditional getter expressions where the real value must be hidden.

## Structure

- Enum includes a dedicated sentinel member (e.g., `NONE`, `UNKNOWN`)
- Sentinel is typically the last ordinal in the enum
- Used as default value for attributes: `answer = Choice#NONE`
- Used as hidden value in conditional getters: `condition ? realValue : Choice#NONE`

## Examples

### Trivia
`Choice` enum has members A, B, C, D, and `NONE` (ordinal 5). `Prompt.answer` defaults to `Choice#NONE` (no answer yet). `player::Prompt.answer` returns `Choice#NONE` when the test is not finished, hiding the real answer from players during gameplay.

### InterfaceRegister
`DevelopmentType` enum has 4 members: COTS, COTS_WITH_ADDITIONAL_DEVELOPMENTS, CUSTOM_DEVELOPMENT, and `UNKNOWN` (ordinal 4). The UNKNOWN sentinel serves as a fallback classification when the development type of an application or specification is not yet determined, avoiding the need for nullable enum attributes.

## Trade-offs

- Pros: Type-safe "no value" representation, works in both defaults and conditional logic, no nulls needed
- Cons: Sentinel must be handled in business logic (not a "real" value), adds an extra enum member
- Prefer when: An enum-typed attribute needs to represent "not yet set" or "hidden" states

## Related Patterns

- [conditional-visibility-getter](conditional-visibility-getter.md)
- [enum-state-machine](enum-state-machine.md)
- [default-value-patterns](default-value-patterns.md)
