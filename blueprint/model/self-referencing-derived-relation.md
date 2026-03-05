---
id: "self-referencing-derived-relation"
title: "Self-Referencing Derived Relation"
domain: "model"
category: "relation"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

A transfer object defines a derived relation whose getter expression is `self`, creating a self-referencing relation. The target transfer type is a different projection of the same underlying entity, allowing the same entity to be viewed through multiple transfer lenses simultaneously (e.g., a Contest viewed as itself and also as a Scoreboard).

## Structure

- Transfer object has a derived relation with getter `self`
- Target type is a different transfer object mapped to the same entity
- Enables presenting the same entity data in different UI contexts without additional queries

## Examples

### Trivia
`player::Contest` has a derived relation `scoreboard -> player::Scoreboard (0..1)` with getter `self`. Both `player::Contest` and `player::Scoreboard` map to `entities::Contest`, but Scoreboard projects different attributes (title + personalBests filter). This lets the UI show contest info and scoreboard from the same entity.

## Trade-offs

- Pros: No additional queries needed, reuses entity data through different projections, clean separation of UI concerns
- Cons: May be confusing that a relation points to "the same thing", requires understanding of transfer projection model
- Prefer when: The same entity needs to be presented in multiple UI views simultaneously

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [derived-attribute-flattening](derived-attribute-flattening.md)
