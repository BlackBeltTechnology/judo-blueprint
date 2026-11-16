---
id: relation-traversal-validation
title: Relation Traversal for Cross-Entity Validation
description: Validate an operation against the current state of related entities by navigating relations with DAO query methods (for example the status of the parent event) instead of keeping a denormalized copy on the child.
aliases: [validate through parent, navigate relation to validate, parent state check, cross-entity validation]
keywords: [relation, traversal, validation, cross-entity, DAO query, parent state, normalized, precondition]
tags: ["domain:backend", "layer:backend", "project:trivia", "status:single-project"]
category: operation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A custom operation on one entity often depends on the state of a related one (a result may only be submitted while its group is open). Read that state through the relation at the moment of the check, so the data stays normalized and cannot drift.

## Practice

### Platform: relation queries and error types

- The DAO query methods navigate relations. A single-valued relation query returns the entity directly (adding `.selectOne()` does not compile); a multi-valued one returns a customizer with `filterBy...`, `maskedBy` and `selectList()` ([relationship navigation](../../agent-docs/backend/data-access-guide.md#query-result-methods)). Mask the traversal to the fields the check reads ([using masks](../../agent-docs/backend/data-access-guide.md#using-masks-projections)).
- A refusal is a typed error: a field or input problem is a `ValidationException` (400); a business rule violation the client should handle is a modeled fault declared on the operation (422 with `X-Fault`); a bare `RuntimeException` becomes a generic 500 ([error handling guide](../../agent-docs/backend/error-handling-guide.md)). A custom operation that throws a modeled fault must declare it in the model, or the build fails ([rules for custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).
- The check runs in the operation's transaction, so the state read is a consistent view for that call, but the platform does not lock the related row: another request can change the group between the check and the write. Optimistic locking guards a row only when its `__version` is part of the update ([optimistic locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)).
- The same rule can often live in the model as a derived value or an operation precondition, which the UI can use to hide buttons; a UI rule alone does not protect an operation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

### Practice notes: traverse, then refuse

```java
// Example code: Result, Group, ResultDao and the fault/error types are generated types
Group group = resultDao.queryGroup(_this);       // single-valued: entity returned directly
if (group.getStatus() != GroupStatus.OPEN) {
    throw new ErrorException(Error.builder()
        .withCode(ErrorCode.GROUP_NOT_OPEN)
        .withMessage("Group is not open.")
        .build());                                    // modeled fault, see typed-exception-error-handling
}

Category category = itemDao.queryCategory(item);   // further hops work the same way
```

- Start, submit and enter operations of the observed implementation all check the group status through the result-to-group relation before doing anything else.
- Enter filters the user by email, code and active flag with the DAO query filters ([[dao-fluent-query-filter]]).
- Each hop is a query; in a loop over many parents, load once outside the loop or use a masked relation query.
- Reload the entity before the check when an earlier step may have changed it ([[entity-re-fetch-pattern]]).

## Rationale

- The check always uses the current state; there is no copied status column that can drift.
- The data model stays free of denormalized fields and the rule sits next to the operation.
- Costs: an extra query per hop and per check, an N+1 risk inside loops, and no caching. The check is repeated in every operation that needs it, so put it in one helper.

## Example

Submitting a result: the operation loads the result's group, sees it has been closed, and refuses with a coded error that the client shows, without writing anything. Starting a result of an open group passes the same check and proceeds.

## When to avoid

- When the check must hold under concurrent writes to the related entity: add a version check or a lock-like model design, since a read does not stop later changes.
- When the same status is needed in list screens or filters: expose a derived attribute in the model ([[derived-attribute-flattening]]) rather than traversing in Java.
- When many children are checked at once: query the parent once, not per child.

## Related

- [[entity-re-fetch-pattern]] — reload before checking when state may be stale
- [[typed-exception-error-handling]] — the refusal raised after the check
- [[dao-fluent-query-filter]] — filters used for the checks on lists
- [[relation-based-entity-creation]] — the creating side of the same relations
