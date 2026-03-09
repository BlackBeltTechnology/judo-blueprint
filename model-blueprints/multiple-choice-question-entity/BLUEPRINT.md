---
id: "multiple-choice-question-entity"
title: "Multiple-Choice Question Entity with Choice Enum"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

A Question entity representing a multiple-choice question with fixed answer options. The entity carries the question text, individual choice text attributes (choiceA, choiceB, choiceC, choiceD), and a `solution` attribute identifying the correct answer. The answer options are defined by a Choice enum with members A, B, C, D, and NONE (for unanswered). The question has a sequence-based identifier (auto-generated via getVariable("SEQUENCE")) and a moderation status attribute (typed to a status enum with REVIEW/APPROVED/REJECTED members) with operations to transition between states (approve, reject, review).

The question is classified via a `category` association (0..1) to a Category lookup entity, and may reference an `upload` batch (0..1) indicating which bulk import produced it. The entity is non-CRUD -- questions are created by backend operations (bulk import or generation) rather than direct CRUD.

Transfer objects provide different views: an admin view with full editing capability and moderation operations, and a player view (via Prompt) showing only the question text and choices (without revealing the solution until after submission).

This pattern is suitable for quiz, exam, survey, and assessment applications where questions have a fixed set of labeled answer choices.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
