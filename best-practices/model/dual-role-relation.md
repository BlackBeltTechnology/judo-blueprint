---
id: "dual-role-relation"
title: "Dual-Role Relation Pattern for Same Entity Type"
domain: "model"
category: "relation"
score: 17.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mjsz
---
## Description

When an entity can participate in the same relationship type under different roles, two separate bidirectional relations are defined to the same target entity instead of a single generic relation with a role attribute. Each relation is named with a role prefix (e.g., `homeTeam`/`visitorTeam`) and the reverse side uses a role-suffixed collection name (e.g., `homeMatches`/`visitorMatches`). This enables role-specific navigation, filtering, and aggregation without additional discriminator fields.

## Structure

- Entity A defines two separate relations to Entity B, distinguished by role prefix:
  - `roleOneTarget -> EntityB [cardinality]` with reverse `roleOneCollection`
  - `roleTwoTarget -> EntityB [cardinality]` with reverse `roleTwoCollection`
- Both are two-way (bidirectional) associations
- The target entity navigates back through role-specific collections
- Aggregation expressions operate on each role collection independently
- Enables separate calculations per role (e.g., home vs visitor statistics)

```
Match.homeTeam -> Team [1..1] <-> Team.homeMatches [0..*]
Match.visitorTeam -> Team [1..1] <-> Team.visitorMatches [0..*]
```

## Examples

### MJSZ
`Match` has two mandatory relations to `Team`: `homeTeam [1..1]` and `visitorTeam [1..1]`, each as a bidirectional association. `Team` has reverse collections `homeMatches [0..*]` and `visitorMatches [0..*]`. This enables role-specific standings calculations: `Team.goalsFor = homeMatches!sum(homeScore) + visitorMatches!sum(visitorScore)`, `Team.goalsAgainst = homeMatches!sum(visitorScore) + visitorMatches!sum(homeScore)`. Points are calculated separately per role and then summed.

## Trade-offs

- Pros: Type-safe role semantics, clear navigation per role, enables separate per-role aggregations, no discriminator field needed
- Cons: More complex relation graph, more relations to maintain, entity appears multiple times in partner's relation list
- Prefer when: An entity participates in the same type of relationship under distinct, well-defined roles with different calculation needs

## Related Patterns

- [bidirectional-relation](bidirectional-relation.md)
- [derived-attribute-flattening](derived-attribute-flattening.md)
- [null-safe-collection-aggregation](null-safe-collection-aggregation.md)
