---
id: dual-role-relation
title: Dual-Role Relation Pattern for Same Entity Type
description: "When an entity can participate in the same relationship type under different roles, two separate bidirectional relations are defined to the same target entity instead of a single generic relation with a role attribute."
aliases: [first second role, role relation, two relations same target]
keywords: [dual role, two-way relation, role prefix, reverse collection, aggregation per role, same target]
tags: ["domain:model", "layer:model", "project:mjsz", "status:single-project"]
category: relation
status: single-project
projects: [mjsz]
evidence: ["mjsz:unrecorded"]
alternatives: []
related: [bidirectional-relation, derived-attribute-flattening, null-safe-collection-aggregation]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An entity sometimes relates to the same target entity type in two distinct roles (a pairing has a first and a second participant). Model each role as its own named two-way relation instead of one generic relation plus a role discriminator.

## Practice

### One named relation per role, each with its own reverse collection

- The owning entity declares two relations to the same target, named by role (`firstParticipant`, `secondParticipant`), each `1..1` when the role is mandatory.
- Each relation is a two-way relation: the target gets a reverse member per role (`firstPairings`, `secondPairings`, both `0..*`). Both ends of a two-way relation point at each other through `partner` ([structure reference](../../agent-docs/model/esm_metamodel/structure.md)).
- The reverse end needs a role-specific name. A single shared reverse collection would merge the roles again.
- Keep the relation kind `ASSOCIATION` on both ends. The model validator rejects a two-way relation declared as composition, and requires that at least one end has lower bound 0; the `0..*` reverse end satisfies this ([advanced modeling patterns](../../agent-docs/model/advanced-modeling-patterns.md)).

### Aggregate per role on the target

Derived members of the target navigate each role collection on its own and combine them where needed, for example the total of a score across both roles: `self.firstPairings!sum(m | m.firstScore) + self.secondPairings!sum(m | m.secondScore)`. `!sum` accepts integer and decimal selectors only ([JQL collection functions](../../agent-docs/model/model-development.md)). For optional score fields see [[null-safe-collection-aggregation]].

## Rationale

- Role semantics are in the model, so navigation and aggregation need no filter on a discriminator value.
- Each role collection can be summed, counted or filtered independently, which a single generic relation cannot do without an extra `!filter`.
- Practice note (not platform behaviour): the role prefix on the forward name and the role suffix on the reverse name keep generated pages and expressions readable.
- Cost: more relations on the owning entity and more reverse members on the target.

## Example

`Pairing` has two mandatory relations to `Participant`: `firstParticipant` and `secondParticipant`. `Participant` has `firstPairings` and `secondPairings`. The derived `Participant.scoreFor` sums the first score over first-role pairings plus the second score over second-role pairings; `scoreAgainst` swaps the two scores. The entities and names are neutral stand-ins for the original model.

## When to avoid

- The roles are not fixed or there may be many of them: use a link entity that carries a role attribute.
- Only one role ever matters: a single relation is enough.
- No per-role reverse navigation or aggregation is needed: a one-way relation per role is simpler than a two-way pair.

## Related

- [[bidirectional-relation]] — the two-way relation this pattern repeats per role
- [[derived-attribute-flattening]] — derived members that read the role collections
- [[null-safe-collection-aggregation]] — safe sums over optional fields

## Structure diagram

```mermaid
classDiagram
  class Pairing {
    <<Entity>>
    +Integer firstScore
    +Integer secondScore
  }
  class Participant {
    <<Entity>>
    +Integer /scoreFor
    +Integer /scoreAgainst
  }
  Pairing "*" -- "1" Participant : firstParticipant / firstPairings
  Pairing "*" -- "1" Participant : secondParticipant / secondPairings
```
