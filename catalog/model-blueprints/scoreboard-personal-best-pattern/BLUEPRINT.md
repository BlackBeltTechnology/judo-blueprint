---
id: scoreboard-personal-best-pattern
title: Scoreboard with Personal Best Ranking Pattern
description: A Scoreboard transfer object that aggregates ranked results (personal bests) for a competitive activity.
aliases: [leaderboard, personal best ranking, high score list]
keywords: [scoreboard, personal, best, ranking, leaderboard, flag, tiebreak]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:trivia", "status:single-project"]
category: pattern
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: scoreboard-personal-best-pattern
diagram: { kinds: [entity, enum, transfer], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Show a ranked leaderboard of each participant's best result without a separate ranking service. A flag on the result entity marks the best attempt per participant and contest. The scoreboard is a transfer object that exposes only the flagged attempts.

### The flag is materialized

Ranking is not computed on every read. The flag is updated when an attempt is submitted (and when one is excluded). The scoreboard simply lists the attempts where the flag is true.

### The scoreboard is a read model

Two transfer objects carry the view: a personal-best row and a scoreboard that holds a title and the list of rows. Neither owns data.

## Structure

- `Attempt` (the result entity, for example a test attempt) has `score`, `duration`, `finishedAt`, a required boolean `personalBest` that defaults to false, and associations to its `Contest` and `Player`.
- `Contest` has a `title` and a collection of its attempts.
- `PersonalBest` is a transfer object mapped to `Attempt`. It exposes score, duration and finished-at, plus a derived `playerName` that reads the name through the player relation. It lists only flagged attempts through the relation that feeds it.
- `Scoreboard` is a transfer object mapped to `Contest`: a mapped `title` and a derived aggregation `personalBests` (0..*) to `PersonalBest`. The derived expression filters the contest's attempts on the flag.
- The player's contest view reaches the scoreboard through a relation (0..1) and may also reach the player's own bests through another relation (0..*).

## Constraints

- Exactly one attempt per player and contest carries the flag. The model does not enforce this; the submit operation maintains it (project practice). See the backend guidance.
- The flag is stored, so it can go stale if attempts are changed outside the submit and exclude operations.
- Ranking order (score descending, then duration ascending, then finish time ascending) is applied by the client when it requests the list, or by the query. It is not part of the model.
- The scoreboard and row transfer objects are read-only; they have no create, update or delete.
- Derived expressions are JQL. Keep them on the transfer object and check them with the model validation. See [model development](../../agent-docs/model/model-development.md).

## Variations

- **Computed ranking.** Skip the flag and rank on read with a query. Simpler to keep correct, slower on large result sets.
- **Several scopes.** Add a flag or a relation per scope (contest, season, overall).
- **Top-N only.** Return the first N rows from the list call.
- **Tiebreak rules.** Higher score wins; the shorter duration breaks a tie in the source project. Change the rule in the submit operation.

## When to use

- A competitive feature needs a leaderboard of best results per participant.
- Results arrive one at a time and the best must be known cheaply at read time.

## When to avoid

- Rankings must be exact at all times and attempts change often outside the submit path. Compute on read.
- The leaderboard needs complex ranking logic or large-scale aggregation. Use a purpose-built ranking store.

## Related

- [[dashboard-transfer-object]] — a read-model transfer object over entity data
- [[aggregated-stored-field]] — another stored value kept for cheap reads
