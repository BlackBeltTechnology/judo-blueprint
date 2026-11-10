---
id: multiple-choice-question-entity
title: Multiple-Choice Question Entity with Choice Enum
description: "A non-CRUD Question entity with four fixed answer choices, a Choice enumeration for the correct answer and a review status."
aliases: [quiz question, multiple choice item]
keywords: [question, choice, enum, quiz, solution, status]
tags: [domain:model, layer:model, layer:frontend, project:trivia, status:single-project]
category: pattern
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: multiple-choice-question-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Store a question with a fixed set of labeled answers and one correct answer, so a quiz or assessment app can grade it. Questions are made by backend code (bulk import or generation), not by direct CRUD.

### Answers are fixed letters

The entity has exactly four choice texts (A to D) and a Choice enumeration for the correct one. The enumeration has a NONE member that means "not answered" and is used as the default for a player's answer.

### Questions are created by the backend

The entity sets its createable, updateable and deleteable flags to false, so the generated UI shows no create button, no editable fields and no delete button. Admin tools import and moderate questions through custom operations.

## Structure

The Question entity has a required question text, four required choice texts, a required solution (a Choice value), a required integer identifier and a required status (QuestionStatus: REVIEW, APPROVED, REJECTED). It has two optional associations, to a Category and to an Upload batch (each 0..1). The Choice enumeration lists A, B, C, D and NONE.

## Constraints

- Createable, updateable and deleteable are all false on Question.
- The question text and all four choice texts are required.
- The solution must be one of A, B, C, D. NONE is not a valid correct answer.
- The identifier gets its value from a sequence default expression (see [[sequence-based-identifier]]), so numbers stay unique across imports.
- A question's category and upload are optional. Deleting either one keeps the question.

## Variations

- **Admin view with moderation.** The admin projection exposes the full question, including the solution, and the status actions. Use it for editors.
- **Player view without the solution.** A player projection shows the question and choices only. The solution appears after the answers are submitted, so the test does not reveal it early.
- **Status-free bank.** If questions do not need review, drop the status enumeration and keep Choice.

## When to use

- A quiz, exam or survey has questions with a fixed set of labeled answers.
- Exactly one answer is correct and the correct letter must be stored.

## When to avoid

- Questions have a variable number of answers. Use a relation to an answer entity instead of four fixed attributes.
- More than one answer can be correct. A single Choice value cannot hold several answers.
- Answers are free text that the player types. Use a text attribute, not an enumeration.

## Related

- [[multi-actor-role-based-projections]] — the admin and player views of the same question are separate projections
- [[open-close-status-toggle]] — a two-state status enumeration, compared with the review status here
- [[sequence-based-identifier]] — the sequence default used for the identifier
- [[notification-entity]] — another entity with status and type enumerations
