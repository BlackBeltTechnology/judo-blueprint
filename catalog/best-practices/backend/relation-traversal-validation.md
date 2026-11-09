---
id: relation-traversal-validation
title: Relation Traversal for Cross-Entity Validation
description: Validating entity state by navigating relationships via DAO query methods rather than storing denormalized copies.
aliases: []
keywords: [relation, traversal, cross, validation]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: operation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [entity-re-fetch-pattern, typed-exception-error-handling]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Validating entity state by navigating relationships via DAO query methods rather than storing denormalized copies. For example, checking if a contest is open by traversing from Test to Contest: `testDao.queryContest(_this).getStatus()`. This keeps data normalized but requires relationship traversal for each validation check.

## Structure

```java
// Navigate relation and validate
Contest contest = testDao.queryContest(_this);
if (contest.getStatus() != ContestStatus.OPEN) {
    throw new ErrorException(Error.builder()
        .withCode(ErrorCode.CONTEST_NOT_OPEN)
        .withMessage("Contest is not open.")
        .build());
}

// Multi-hop validation
Category category = questionDao.queryCategory(question);
// Validate category properties...
```

Single-valued relations return the entity directly (not a query builder).
Collection-valued relations return a query builder with `selectList()`.

## Examples

### Trivia
Start, Submit, and Enter operations all validate contest status by traversing Test->Contest via `testDao.queryContest(_this).getStatus()`. Enter validates user by querying with email+code+active filters. Exclude traverses Test->Contest to find sibling tests for PB recalculation.

## Trade-offs

- Pros: Always validates against current state, no denormalization drift, clean separation of concerns
- Cons: Additional DB queries per validation, N+1 risk if done in loops, no caching
- Alternative: Denormalize status onto child entity, or use model-level derived attributes

## Related

- [[entity-re-fetch-pattern]]
- [[typed-exception-error-handling]]

