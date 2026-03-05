---
id: multiple-choice-question-entity
title: "Multiple-Choice Question Entity with Choice Enum"
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

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { eq: "Choice" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Question" } }) {
  items { fqn name
    attributes { items { name } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities with attributes named `choiceA`, `choiceB`, `choiceC`, `choiceD`, and `solution`.

## Creation Mutations

### Choice enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "Choice"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Choice", name: "A", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Choice", name: "B", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Choice", name: "C", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Choice", name: "D", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Choice", name: "NONE", ordinal: 5
} }) { success fqn } }
```

### QuestionStatus enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "QuestionStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::QuestionStatus", name: "REVIEW", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::QuestionStatus", name: "APPROVED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::QuestionStatus", name: "REJECTED", ordinal: 3
} }) { success fqn } }
```

### Question entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Question",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "question"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "choiceA"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "choiceB"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "choiceC"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "choiceD"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "solution"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "identifier"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Question", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Question", name: "category",
  target: "{{NAMESPACE}}::Category", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Moderation operations

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Question", name: "approve",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Question", name: "reject",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Question", name: "review",
  operationType: INSTANCE
} }) { success fqn } }
```

## Examples

### trivia
- **Choice enum**: `trivia::entities::Choice` -- A(1), B(2), C(3), D(4), NONE(5)
  - NONE serves as the default/unanswered sentinel value for the Prompt entity's answer attribute
- **QuestionStatus enum**: `trivia::entities::QuestionStatus` -- REVIEW(1), APPROVED(2), REJECTED(3)
- **Question entity**: `trivia::entities::Question` (non-CRUD)
  - Attributes (8): question (req), choiceA (req), choiceB (req), choiceC (req), choiceD (req), solution (req, Choice enum), identifier (req, default: getVariable("SEQUENCE", "Question")), status (req, default: QuestionStatus#REVIEW)
  - Relations: category (0..1 ASSOC to Category), upload (0..1 ASSOC to Upload)
  - Operations: approve (INSTANCE), reject (INSTANCE), review (INSTANCE)
- **Admin Question TO** (`trivia::actors::admin::Question`):
  - Attributes: question (req), choiceA-D (req), solution (req), identifier, status, categoryName (denormalized)
  - Relations: category (0..1 AGGREGATION)
  - Operations: upload (STATIC), approve (MAPPED), reject (MAPPED), review (MAPPED), download (STATIC)
  - Admin can bulk-upload questions via JSON and bulk-download, plus moderate individual questions
- **Player Prompt TO** (`trivia::actors::player::Prompt`):
  - Attributes: question, category, choiceA-D, number, answer, solution
  - The solution is only revealed in the PromptList returned after test submission; during the test, only question+choices are shown
- The question identifier uses a database sequence for unique numbering across bulk imports
