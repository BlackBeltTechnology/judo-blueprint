---
id: "personal-best-tracking"
title: "Boolean Flag Personal Best Tracking with Recalculation"
domain: "backend"
category: "operation"
score: 39.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
---
## Description

Tracking a "best" record among a set of related entities using a boolean flag rather than a computed view. When a new candidate appears (e.g., new test submission), the system compares it against the current best using a multi-criteria comparison (primary score, tiebreaker). If the current best is removed/excluded, all candidates are re-evaluated to find the new best. The comparison logic is duplicated across creation and removal operations.

## Structure

```java
// On new submission: compare with existing PB
Optional<Test> existingPB = contestDao.queryTests(contest)
    .filterByPersonalBest(BooleanFilter.isTrue())
    .filterByPlayerEmail(StringFilter.equalTo(email))
    .selectOne();

if (existingPB.isEmpty()) {
    _this.setPersonalBest(true);  // First entry is PB
} else if (score > existingPB.get().getScore()
        || (score == existingPB.get().getScore() && duration < existingPB.get().getDuration())) {
    existingPB.get().setPersonalBest(false);
    _this.setPersonalBest(true);   // New PB: better score or same score + faster
}

// On exclusion: recalculate PB from remaining candidates
if (excluded.getPersonalBest()) {
    // Iterate all FINISHED tests, find new best by score then duration
}
```

## Examples

### Trivia
Submit operation sets PB when new score > existing PB score, or same score with shorter duration. Exclude operation recalculates PB by iterating all FINISHED tests for same player/contest when excluded test was the PB. Comparison logic (score + duration tiebreaker) is duplicated in both operations.

## Trade-offs

- Pros: Fast reads (just filter by boolean flag), no computed view needed
- Cons: Duplicated comparison logic, in-memory iteration for recalculation (could use DB sort), flag can become inconsistent if not updated atomically
- Alternative: Computed view/query that always calculates best on read, or centralized PB service

## Related Patterns

- state-lifecycle-operation
- dao-fluent-query-filter
