---
id: operation-result-caching
title: Operation Result Caching in Entity Relations
description: "An entity stores operation results in a stored relation, effectively caching the output of an expensive or user-triggered computation."
aliases: []
keywords: [operation, result, caching, relations]
tags: ["domain:model", "layer:model", "project:skillmatrix-model", "status:single-project"]
category: operation
status: single-project
projects: [skillmatrix-model]
evidence: ["skillmatrix-model:unrecorded"]
alternatives: []
related: [mapped-operation-delegation, derived-relation-navigation]
fragment: pending
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

An entity stores operation results in a stored relation, effectively caching the output of an expensive or user-triggered computation. The operation clears previous results, computes new ones, and stores them back on the entity along with a timestamp. This allows the results to be viewed later without re-executing the operation.

## Structure

- Entity has a stored collection relation for results (e.g., `results -> TargetType [0..*]`)
- Entity has a timestamp attribute tracking last execution (e.g., `lastRun: Timestamp`)
- Operation body follows a clear-compute-store pattern:
  1. Clear previous results: `this.results -= this.results`
  2. Compute new results: `this.results += source.navigation`
  3. Update timestamp: `this.lastRun = Timestamp!now()`
- Results are persisted and available for subsequent reads without re-execution
- UI displays both the cached results and the last-run timestamp

## Examples

### SkillMatrix-Model
`Search` entity caches user search results. `Search.run()` operation: `this.results -= this.results; this.results += this.competences.users; this.results += this.tags.users; this.lastRun = Timestamp!now()`. Results are stored in `results -> User [0..*]` and displayed in a table. `Search.lastRun` tracks when the search was last executed. Similarly, `Definition.run()` (mapped) generates report results stored in `results -> Result [0..*]` with execution timestamp and Excel download URL.

## Trade-offs

- Pros: Avoids re-executing expensive queries, results available for pagination and display, timestamp provides audit context
- Cons: Cached results may become stale, clearing and re-populating may be costly for large result sets, consumes storage
- Prefer when: Operation results need to be persisted for later viewing, or the computation is expensive and should not run on every page load

## Related

- [[mapped-operation-delegation]]
- [[derived-relation-navigation]]

