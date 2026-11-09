---
id: "null-safe-collection-aggregation"
title: "Null-Safe Collection Aggregation Pattern"
domain: "model"
category: "operation"
score: 38.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - mjsz
---
## Description

When aggregating collection values with `!sum()`, optional (nullable) fields are first filtered using `!filter(x | x.field!isDefined())` before the sum is applied. This prevents null values from breaking the aggregation. Required fields can be summed directly without the guard. A variant uses `!count() > 0 ? !sum(...) : 0` to guard against empty collections returning null.

## Structure

- **Required field aggregation** (no guard needed):
  ```
  self.collection!sum(x | x.requiredField)
  ```
- **Optional field aggregation** (null-safe):
  ```
  self.collection!filter(x | x.optionalField!isDefined())!sum(x | x.optionalField)
  ```
- **Empty collection guard** (null-safe):
  ```
  self.collection!count() > 0 ? self.collection!sum(x | x.field) : 0
  ```
- The `!isDefined()` check filters out items where the field is null
- The `!count() > 0` check prevents sum on empty collections
- This pattern applies to any collection aggregate: `!sum()`, `!avg()`, `!min()`, `!max()`

## Examples

### itracker
In `archiveForecast`, `sumOfSavingPotential` directly sums the required field: `this.monthlyForecasts!sum(f | f.savingPotential)`. But `sumOfSaving` uses the null-safe pattern because `saving` is optional: `this.monthlyForecasts!filter(f | f.saving!isDefined())!sum(f | f.saving)`. This handles months where actual savings have not yet been entered.

### MJSZ
`Team.points` uses the empty-collection guard variant: `self.homeMatches!count() > 0 ? 3 * self.homeMatches!sum(m | m.homeWin) + self.homeMatches!sum(m | m.draw) : 0`. Same pattern on `Team.goalsFor` and `Team.goalsAgainst`, guarding against teams with no home or visitor matches. The `Team.matches` attribute uses filter+count: `self.homeMatches!filter(hm | hm.homeScore!isDefined())!count()`.

## Trade-offs

- Pros: Prevents runtime errors from null values, explicit about null handling, composable with other collection operations
- Cons: Verbose compared to a built-in null-coalescing aggregate, easy to forget the guard on optional fields
- Prefer when: Aggregating over collections where some items may have null values in the aggregated field

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md)
- [derived-relation-navigation](derived-relation-navigation.md)
