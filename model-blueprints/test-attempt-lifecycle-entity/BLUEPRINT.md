---
id: "test-attempt-lifecycle-entity"
title: "Test/Attempt Lifecycle Entity with Status Tracking"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

A Test (or Attempt) entity that represents a user's participation in a timed activity, with a multi-stage lifecycle status enum tracking progress from creation through completion or failure. The entity carries:

- **Status attribute**: typed to a lifecycle enum with members like CREATED (not yet started), STARTED (in progress), FINISHED (completed successfully), FAILED (exceeded time or other failure), and EXCLUDED (administratively removed). The default is CREATED.
- **Timestamp tracking**: separate timestamps for each lifecycle stage (timestampOfCreation, timestampOfStarted, timestampOfFinished) rather than a single createdAt/updatedAt pair, enabling precise duration calculations.
- **Score and duration**: computed results stored as attributes (score, duration) after completion.
- **Player reference**: association (1..1) to the user who took the test, plus a denormalized `playerEmail` string for quick display.
- **Context reference**: association (1..1) to the contest/exam/activity that the test belongs to.
- **Composed items**: composition (0..*) to individual prompt/answer items within the test.
- **Personal best flag**: a boolean `personalBest` attribute (default: false) for marking the user's best score on this contest.
- **Identifier**: a unique `id` for external reference (e.g., sharing test results via URL).

State transition operations: `start` (CREATED -> STARTED), `submit` (STARTED -> FINISHED or FAILED based on results), `exclude` (admin operation to mark a test as EXCLUDED).

This pattern is suitable for any scenario where users take timed assessments, quizzes, exams, or challenges: the lifecycle tracks the full attempt from entry through completion, with administrative override capability.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
