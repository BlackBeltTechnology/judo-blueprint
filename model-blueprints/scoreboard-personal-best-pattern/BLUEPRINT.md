---
id: "scoreboard-personal-best-pattern"
title: "Scoreboard with Personal Best Ranking Pattern"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

A Scoreboard transfer object that aggregates ranked results (personal bests) for a competitive activity. The pattern consists of:

- A **PersonalBest** transfer object: a denormalized view of the best result per participant, containing score, duration, playerName, and timestampOfFinished. This is mapped from the underlying Test/Attempt entity filtered to only those flagged as personal bests.
- A **Scoreboard** transfer object: a container with a title attribute and a `personalBests` aggregation relation (0..*) to PersonalBest TOs, providing a ranked leaderboard view.
- The underlying Test entity carries a `personalBest` boolean attribute (default: false) that is set to true when a result is the user's best for that contest. This flag acts as a filter criterion for the scoreboard query.

The scoreboard is accessed from a Contest/Event transfer object via a `scoreboard` relation (0..1 ASSOC) and/or a `personalBests` relation (0..* ASSOC), giving players both a contest-scoped leaderboard and their own best results.

This pattern enables competitive features (leaderboards, rankings) without a separate ranking service: the personal best flag on the test entity combined with derived/query relations produces the ranked view at the transfer object level.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
