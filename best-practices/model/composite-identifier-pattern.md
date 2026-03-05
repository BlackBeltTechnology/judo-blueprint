---
id: "composite-identifier-pattern"
title: "Composite Identifier (Multiple Identifier Attributes)"
domain: "model"
category: "entity"
score: 35.8
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - InterfaceRegister
  - judo-partner
---
## Description

An entity uses multiple attributes marked as `identifier=true` to form a composite identifier. This means the entity is uniquely identified by the combination of two or more fields rather than a single primary key. This pattern is useful for entities that have both a system-generated code and a human-readable name, where either could serve as a lookup key.

## Structure

- Two or more attributes on the same entity have `identifier="true"`
- Both attributes are typically required (`required="true"`)
- Common combination: `id` (system code) + `name` (human-readable)
- Both identifier attributes use String type
- Transfer objects may expose both identifiers for display and lookup

## Examples

### InterfaceRegister
Four entities use composite identifiers with dual `id + name` identifier fields: `Application` (id: "APP-0001", name: "SalesForce"), `Vendor` (id: "VND-001", name: "Vendor 1"), `Server` (id + name), `InterfaceSpecification` (id: "IFS-0001", name: human-readable spec name), `HighLevelConnection` (id + name). Both fields are String type, required, and marked `identifier=true`. The `id` field uses count-based auto-generation while `name` is user-provided.

### judo-partner
`Country` entity has 4 identifier attributes: `code`, `name`, `alpha2`, `alpha3` -- each a different representation of the same country entity. `Partner` has 2 identifiers: `partnerCode` (system-generated) and `taxIdentifier` (optional, derived). Most other entities use single natural-key identifiers (e.g., `Register.registerCode`, `Case.caseCode`, `Record.recordNumber`).

## Trade-offs

- Pros: Supports both programmatic lookup (by code) and human-friendly lookup (by name), enforces uniqueness on both dimensions
- Cons: More complex uniqueness constraints, both fields must be provided and unique, may complicate relation references
- Prefer when: Entities need both a stable system identifier and a unique human-readable name

## Related Patterns

- [sequence-based-identifier](sequence-based-identifier.md)
- [naming-conventions](naming-conventions.md)
