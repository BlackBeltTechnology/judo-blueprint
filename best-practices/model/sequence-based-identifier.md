---
id: "sequence-based-identifier"
title: "Sequence-Based Identifier Pattern"
domain: "model"
category: "entity"
score: 39.4
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - itracker
  - mjsz
  - InterfaceRegister
  - workflow-poc
---
## Description

An entity attribute marked as an identifier uses a sequence-based default value expression to auto-generate unique sequential IDs. The expression `TypeName!getVariable("SEQUENCE", "EntityName")` produces an auto-incrementing value on creation.

## Structure

- Attribute is of numeric type (typically `Long` with precision 18, or `Integer` with precision 9) or String with formatted sequence
- Marked as an identifier field
- Default value uses: `TypeName!getVariable("SEQUENCE", "EntityName")`
- The attribute is typically made derived (read-only) in transfer projections
- Variant: String identifier with prefix and zero-padding for human-readable IDs
- Variant: Count-based expression `'PREFIX-' + ((Entity!count()+1)!asString())!lpad(N, "0")` for simpler sequential IDs

```
identifier: Long, required, identifier=true
  default: trivia::types::Long!getVariable("SEQUENCE", "Question")
```

## Examples

### Trivia
`Question.identifier` is a Long (precision 18) with default `trivia::types::Long!getVariable("SEQUENCE", "Question")`. In the admin transfer projection, `identifier` is exposed as a derived (read-only) attribute, preventing manual override.

### itracker
`Initiative.id` is an Integer (precision 9) with default `itracker::types::Integer!getVariable("SEQUENCE", "initiative")`. The `id` field is not exposed on the actor-level transfer, keeping it internal. Note: uses Integer instead of Long, showing the type can vary.

### MJSZ
`Player.identifier` is a String with default `"MJSZ" + mjsz::types::Long!getVariable("SEQUENCE", "MJSZID")!asString()!lpad(5, "0")`. This produces human-readable IDs like "MJSZ00001". Demonstrates a String-type variant with domain prefix and zero-padding for consistent width.

### InterfaceRegister
Uses count-based ID generation on transfer objects instead of the SEQUENCE variable: `ApplicationTransfer.id = 'APP-' + ((Application!count()+1)!asString())!lpad(4, "0")`, `VendorTransfer.id = 'VND-' + ((Vendor!count()+1)!asString())!lpad(4, "0")`, `InterfaceSpecification.id = 'IFS-' + ...`, `ConnectionDefinition.id = 'CON-' + ...`. Each entity type uses a unique 3-letter prefix. This variant uses `!count()` instead of `!getVariable("SEQUENCE", ...)`, making the ID transfer-level (default on creation form) rather than entity-level.

### workflow-poc
`Event.sequence` is a Long (required) with default `workflow::types::Long!getVariable("SEQUENCE", "Event")`. Used not as a business identifier but as an ordering sequence for event processing -- ensuring workflow events are processed in the correct order. Demonstrates using the SEQUENCE pattern for ordering rather than identification.

## Trade-offs

- Pros: Guaranteed uniqueness, auto-generated, human-readable sequential IDs
- Cons: Not suitable for distributed systems without coordination, sequential IDs may leak information about record counts
- Prefer when: You need simple, auto-incrementing numeric identifiers for an entity

## Related Patterns

- [default-value-patterns](default-value-patterns.md)
