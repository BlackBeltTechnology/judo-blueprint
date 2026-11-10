---
id: personal-best-tracking
title: Boolean Flag Personal Best Tracking with Recalculation
description: Project practice for marking the best record among related records with a stored boolean flag, set by comparing a new record with the current best and recalculated when the best is excluded.
aliases: [personal best flag, best record flag, high score flag]
keywords: [boolean, flag, personal best, tracking, recalculation, score, tiebreaker, leaderboard]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: operation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Find the best record per owner (for example a player's best test result in a contest) with a plain boolean filter instead of computing the best on every read. This is project practice (trivia); the platform has no "best record" concept.

## Practice

### Platform: what the pattern builds on

- Multi-valued relation queries on a DAO (for example `contestDao.queryTests(contest)`) return a query customizer that supports `filterBy...`, `maskedBy` and `selectList()`/`selectOne()`; `selectOne()` returns an `Optional` ([relation queries and result methods](../../agent-docs/backend/data-access-guide.md#query-result-methods)). Boolean attributes are filtered with `BooleanFilter.isTrue()` / `isFalse()`, not `equalTo(true)`.
- Relation query customizers have no ordering methods; to order candidates, sort in Java after fetching ([common query mistakes](../../agent-docs/backend/data-access-guide.md#common-query-mistakes)).
- The flag changes are plain entity updates ([[mutable-entity-update-pattern]]). All changes of one operation run in that operation's transaction, so the old best is cleared and the new one set together; two concurrent submissions by the same owner are not serialized by the platform, so the flag can still end up wrong under a race (the docs do not describe locking for this case).

### Project practice: compare on create, recalculate on exclusion

The record carries a `personalBest` boolean and the compared values (score, duration).

```java
// Example project code: Test, Contest, TestDao and ContestDao are generated types
Optional<Test> best = contestDao.queryTests(contest)
    .filterByPersonalBest(BooleanFilter.isTrue())
    .filterByPlayerEmail(StringFilter.equalTo(email))
    .selectOne();

if (best.isEmpty()) {
    current.setPersonalBest(true);                 // first entry is the best
} else if (score > best.get().getScore()
        || (score == best.get().getScore() && duration < best.get().getDuration())) {
    best.get().setPersonalBest(false);
    testDao.update(best.get());
    current.setPersonalBest(true);                 // higher score, or same score and faster
}
testDao.update(current);
```

- On submit: compare the new record with the owner's current best; the primary criterion is the score, the tiebreaker is the shorter duration.
- On exclusion of the current best: load the owner's remaining finished records, pick the new best with the same comparison, and set the flag. This runs in memory over all candidates of that owner.
- Keep the comparison in one helper used by both operations; the project duplicated it, which is the main weakness.

## Rationale

- Reading the best records is a flag filter, so leaderboards and profile screens stay cheap.
- Cost: the flag is a copy that must be maintained in every code path that creates, changes or removes a candidate, including paths without interceptors (custom operations are never intercepted, see [[interceptor-crud-lifecycle]]); recalculation on exclusion iterates all candidates.

## Example

A player submits a test with score 80 in 120 s; the earlier best had 80 in 150 s, so the earlier flag is cleared and the new record is flagged. An administrator then excludes the new record: the operation reloads the player's other finished tests in the contest and flags the best of them.

## When to avoid

- When the number of candidates is small or reads are rare: compute the best on read with a query or derived value so there is no flag to keep in sync.
- When candidates can be changed by many code paths; the flag drifts.
- When several submissions per owner can arrive concurrently and an inconsistent flag is not acceptable.

## Related

- [[state-lifecycle-operation]] — the finish transition that triggers the comparison
- [[dao-fluent-query-filter]] — the typed filters used to find the current best
- [[mutable-entity-update-pattern]] — how the flags are written
