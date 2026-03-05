---
id: "integer-boolean-for-aggregation"
title: "Integer Boolean Flags for Aggregation Support"
domain: "model"
category: "entity"
score: 15.0
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - mjsz
---
## Description

Derived attributes that represent boolean conditions (true/false) are typed as Integer (0 or 1) rather than Boolean. This enables direct use in arithmetic aggregation operations like `!sum()` for counting occurrences, computing points, or calculating statistics. The ternary expression `condition ? 1 : 0` converts a boolean condition to a summable integer flag.

## Structure

- Derived attribute with Integer type
- Getter expression uses ternary: `condition ? 1 : 0`
- Consuming derived attributes use `!sum(x | x.integerFlag)` for aggregation
- Avoids the need for `!filter(x | x.booleanFlag)!count()` pattern
- Particularly useful in scoring and standings calculations

```
// Define integer flag
homeWin: Integer = self.homeScore - self.visitorScore > 0 ? 1 : 0

// Use in aggregation
points: Integer = 3 * self.matches!sum(m | m.homeWin)
```

## Examples

### MJSZ
`Match` entity defines 3 integer boolean flags: `homeWin = self.homeScore - self.visitorScore > 0 ? 1 : 0`, `draw = self.homeScore - self.visitorScore == 0 ? 1 : 0`, `visitorWin = self.homeScore - self.visitorScore < 0 ? 1 : 0`. These are consumed by `Team.points = 3 * self.homeMatches!sum(m | m.homeWin) + self.homeMatches!sum(m | m.draw)` for standings calculation. Boolean type is available but deliberately not used.

## Trade-offs

- Pros: Enables direct summation for points/standings, avoids filter+count pattern, simplifies aggregation expressions
- Cons: Less type-safe than Boolean (any integer value possible), less semantic (0/1 less clear than true/false)
- Prefer when: Boolean-like attributes need to participate in arithmetic aggregations (scores, points, statistics)

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md)
- [null-safe-collection-aggregation](null-safe-collection-aggregation.md)
