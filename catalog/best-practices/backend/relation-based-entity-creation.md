---
id: relation-based-entity-creation
title: Relation-Based Child Entity Creation
description: Create a child entity through the generated create method of the parent DAO for the relation, instead of calling the child DAO, so the child is created and linked in one call.
aliases: [create through parent, parent DAO create relation, composition child creation, createChildren]
keywords: [relation, child, creation, parent DAO, composition, ForCreate, containment, create per relation]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:ubives", "project:park-here", "project:judo-partner", "project:workflow-poc", "status:established"]
category: data-access
status: established
projects: [trivia, ubives, park-here, judo-partner, workflow-poc]
evidence: ["trivia:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Create the rows of a parent's contained collection (answers of a test, addresses of a partner, states of a workflow version) through the parent's DAO, so the link to the parent is part of the call.

## Practice

### Platform: per-relation create methods

- The generated DAO of a mapped, non-abstract type has per-relation `create`, `set`, `unset`, `add`, `remove` and range methods, subject to the relation's allowed-operation flags (the create method exists only if the relation allows creation) ([which types get a full DAO](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)). The method for a relation takes the parent entity and the child's `<Child>ForCreate` payload (or a list) and returns the persisted child; the exact names follow the relation names, so read them from the generated DAO interface.
- Child payloads are built with the generated builder ([[builder-pattern-entity-creation]]). A single-valued relation setter in a builder needs a real object, never `null`; clearing is `unset<Relation>` ([clearing a relation](../../agent-docs/backend/data-access-guide.md#clearing-a-relation-unset-not-setnull)).
- The same parent DAO has query methods for the relation. Multi-valued ones return a customizer (`filterBy...`, `maskedBy`, `selectList()`), single-valued ones return the entity directly, so adding `.selectOne()` does not compile ([relationship navigation](../../agent-docs/backend/data-access-guide.md#query-result-methods)).
- Interceptors fire only for built-in behaviour operations, never for custom ones ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Whether a DAO call made from Java triggers the create interceptors of the child is not described in the docs; do not rely on it, and repeat any logic such an interceptor would run.

### Project practice: use the parent DAO when the relation is containment

```java
// Example project code: Parent, Child, ParentDao and the relation name "Children" are generated types
Child child = parentDao.createChildren(parent, ChildForCreate.builder()
    .withNumber(i + 1)
    .withText(text)
    .build());

List<Child> all = parentDao.queryChildren(parent).selectList();   // multi-valued
Owner owner = childDao.queryOwner(child);                         // single-valued, no selectOne
```

- Five projects use this for composition children created in loops or batches: numbered prompts of a test, applications, invitations and users of an organization, cars and holidays of a user, addresses and contacts of a partner, events, states and transitions of a workflow version, log entries of a context.
- The parent must already be persisted.
- Lists are passed as a collection where the generated method accepts one (users of an organization, doormen of a configuration).
- When the child is not a contained part (an independent entity that merely references the parent), create it with its own DAO and set the relation in the builder, as in [[builder-pattern-entity-creation]].

## Rationale

- The link to the parent is established by the call itself, so no relation can be forgotten in the builder, and the call is type-checked.
- The parent DAO stays the single place for the contained collection (create and query).
- Cost: the parent must exist and the relation must allow creation; the method is not available for relations whose create flag is off in the model.

## Example

A contest entry creates a test and then, in a loop, one prompt per question through the test DAO's prompt-creating method; an import step creates an import record's partner rows through the import DAO. Reading them back is the matching query method of the same DAO.

## When to avoid

- When the relation is an association to independent entities: use the child DAO and set or add the reference ([[builder-pattern-entity-creation]]).
- When the relation is not creatable in the model (the method is not generated); change the model flags or create the child through its own DAO if it has a full DAO.
- When thousands of children are created in one operation: the whole operation is one transaction, so batch it or use a list-taking method.

## Related

- [[builder-pattern-entity-creation]] — the `ForCreate` builder used for the child payload
- [[dao-fluent-query-filter]] — query methods for reading the children back
- [[relation-traversal-validation]] — walking the same relations to validate
