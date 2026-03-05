---
id: "factory-operation-with-prepopulation"
title: "Factory Operation with Child Pre-Population"
domain: "model"
category: "operation"
score: 26.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - judo-demo-miniworkflow
---
## Description

A static operation on the transfer layer acts as a factory that creates an entity along with a complete set of pre-populated child entities. The factory accepts an unmapped input DTO, resolves the current actor, constructs the parent entity, and then creates a fixed number of child entities based on business rules (e.g., 12 months for annual tracking).

## Structure

- Static operation on a transfer object (not entity-level)
- Input: unmapped DTO with creation parameters
- Operation body:
  1. Resolves current user via `ACTOR` context variable
  2. Creates parent entity from input fields
  3. Uses `mutable` keyword to convert transient input relations to stored references
  4. Creates child entities in a loop (or explicitly) and attaches via `+=` to parent composition
  5. Returns the created entity
- Output: the created entity (as transfer type)

## Examples

### itracker
`user::Initiative.createInitiative(input: InititativeInput) -> Initiative`: resolves current user via `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()`, creates an Initiative with all input fields plus `mutable input.region` and `mutable input.category`, then pre-populates 12 MonthlyForecast entries (months 0-11) with identical `monthlySavingPotential`. Returns the created initiative.

### judo-demo-miniworkflow
`DocumentTransfer.createDocument(input: NewDocument) -> DocumentTransfer`: resolves current user, creates a `DocumentTransfer` with `referenceNumber` from input and current user as `owner`, then creates an initial `DocumentHistoryEntry` with `toState = IN_PROGRESS` and `eventTime = Timestamp!now()`. Appends the history entry via `transfer.documentHistoryEntries += newHistoryEntry`. Returns the created document transfer.

## Trade-offs

- Pros: Complete entity graph created atomically, business rules enforced (e.g., always 12 months), clean API with single call
- Cons: Rigid pre-population (always same number of children), operation body can be verbose for many children
- Prefer when: Creating an entity requires a predefined set of child entities based on domain rules

## Related Patterns

- [unmapped-transfer-dto](unmapped-transfer-dto.md)
- [transient-relation-parameter](transient-relation-parameter.md)
- [actor-context-variable-lookup](actor-context-variable-lookup.md)
