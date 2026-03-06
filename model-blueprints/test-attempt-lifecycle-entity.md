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

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%TestStatus%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Test" } }) {
  items { fqn name
    attributes { items { name defaultExpression } }
    relations { items { name lower upper relationKind memberType } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities with `start` and `submit` operations and a status attribute defaulting to CREATED.

## Creation Mutations

### TestStatus enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "TestStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TestStatus", name: "CREATED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TestStatus", name: "STARTED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TestStatus", name: "FINISHED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TestStatus", name: "FAILED", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::TestStatus", name: "EXCLUDED", ordinal: 5
} }) { success fqn } }
```

### Test entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Test",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "score"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "duration"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "timestampOfCreation"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "timestampOfStarted"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "timestampOfFinished"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "personalBest"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "playerEmail"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Test", name: "{{CONTEXT_RELATION}}",
  target: "{{NAMESPACE}}::{{CONTEXT_ENTITY}}", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Test", name: "player",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Test", name: "{{ITEMS_RELATION}}",
  target: "{{NAMESPACE}}::{{ITEM_ENTITY}}", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### State transition operations

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Test", name: "start",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Test"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Test", name: "submit",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Test"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Test", name: "exclude",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::Test"
} }) { success fqn } }
```

## Examples

### trivia
- **TestStatus enum**: `trivia::entities::TestStatus` -- CREATED(1), STARTED(2), FINISHED(3), FAILED(4), EXCLUDED(5)
- **Test entity**: `trivia::entities::Test` (non-CRUD)
  - Attributes (9): status (req, default: TestStatus#CREATED), score, duration, timestampOfCreation, timestampOfStarted, timestampOfFinished, personalBest (req, default: false), playerEmail, id (req)
  - Relations: contest (1..1 ASSOC to Contest), player (1..1 ASSOC to User), prompts (0..* COMPOSITION to Prompt)
  - Operations: start (INSTANCE), submit (INSTANCE), exclude (INSTANCE)
  - A test is created when a player enters a contest (Contest.enter operation), starts when the player begins answering, and finishes when they submit answers or the time runs out
- **Admin Test TO** (`trivia::actors::admin::Test`):
  - Attributes: status (req), result, duration, timestampOfCreation, timestampOfStarted, timestampOfFinished, personalBest (req), playerEmail, id (req), contest (denormalized string)
  - Operations: exclude (MAPPED) -- admin can exclude tests (e.g., for cheating)
  - Flattened view: contest name denormalized as a string attribute instead of a relation
- **Player Test TO** (`trivia::actors::player::Test`):
  - Attributes: title, playerEmail, playerName, id, responseTime -- minimal view with contest context
  - Operations: start (MAPPED), submit (MAPPED) -- player can start and submit their test
  - The submit operation takes an AnswerList input containing Answer items (number + choice pairs)
- **Prompt entity** (`trivia::entities::Prompt`): composed items within a test
  - Attributes: number (req), answer (req, default: Choice#NONE), correct (req, default: false)
  - Relations: question (1..1 ASSOC to Question)
  - Each prompt presents a question and records the player's answer choice and whether it was correct
- **Player Prompt TO** (`trivia::actors::player::Prompt`):
  - Attributes: question, category, choiceA, choiceB, choiceC, choiceD, number, answer, solution -- denormalized question content for display
