---
id: "literal-derived-attribute"
title: "Literal Constant Derived Attribute"
domain: "model"
category: "transfer"
score: 49.9
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - alba
  - park-here
---
## Description

A derived attribute on a transfer object uses a literal constant string (or value) as its getter expression, always returning the same fixed value regardless of the underlying entity state. This is used for application-level constants like application names or version strings, and also for boolean constants that serve as UI control flags.

## Structure

- Transfer attribute with `memberType="DERIVED"`
- Getter expression is a literal value: `"Constant String"`, `true`, or `false`
- The underlying entity may have no corresponding attribute
- Boolean constants are often used with `hiddenBy`/`enabledBy` to permanently enable or disable UI elements

## Examples

### Trivia
`player::Application.name` has getter expression `"BlackBelt Trivia"` -- always returns this literal string. The underlying `Application` entity has no `name` attribute; the value exists only in the transfer layer.

### Alba
`AuthorProduct.fixNotEnabled` has getter expression `false` -- always returns false, used to permanently disable a UI control. `PublicAuthorProfile.isTrue` has getter expression `true` -- used as an always-true flag for UI enablement. These boolean constants serve as fixed UI control drivers without entity-level storage.

### ParkHere
`User.trueFlag` has getter expression `true` -- always returns true. Used as an always-enabled flag for UI conditional logic (e.g., `enabledBy` or as the opposite of `hiddenBy` conditions). This is defined at the entity level rather than the transfer level, making the constant available to all transfer projections of User.

## Trade-offs

- Pros: Simple way to expose constants through the API, no database storage needed
- Cons: Value is hardcoded in the model, requires model change to update
- Prefer when: A fixed label or constant needs to be exposed to clients through the transfer layer

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md)
- [ui-control-transfer-fields](ui-control-transfer-fields.md)
