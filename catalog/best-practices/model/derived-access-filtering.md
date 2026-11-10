---
id: derived-access-filtering
title: Derived Access Point with Getter Filtering
description: Access points use the DERIVED access type with getter expressions to filter or restrict the data visible to an actor.
aliases: []
keywords: [derived, access, point, getter, filtering]
tags: ["domain:model", "layer:model", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:skillmatrix-model", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:ams-model", "project:park-here", "project:InterfaceRegister", "project:judo-partner", "project:workflow-poc", "project:reserve-app", "status:established"]
category: access
status: established
projects: [trivia, rackinspect, itracker, alba, skillmatrix-model, viterra_demo, judo-demo-miniworkflow, ams-model, park-here, InterfaceRegister, judo-partner, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "itracker:unrecorded", "alba:unrecorded", "skillmatrix-model:unrecorded", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "ams-model:unrecorded", "park-here:unrecorded", "InterfaceRegister:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
fragment: derived-access-filtering
diagram: { kinds: [entity, enum, transfer, actor], members: types }
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Restrict what an actor can reach by giving its access a `DERIVED` type and a getter expression, so visibility is enforced in the model.

## Practice

- An actor access has `accessType` `ALL` or `DERIVED`. `ALL` is fixed to `0..*` and has no getter; `DERIVED` has a configurable cardinality (`0..1` or `0..*`) and a getter ([accesspoint.md](../../agent-docs/model/esm_metamodel/accesspoint.md), *AccessType Behaviour*).
- Getter rules, all at once ([architectural patterns](../../agent-docs/backend/architectural-patterns.md), *Rules for `accesses[*].getterExpression`*):
  - the filter starts from the entity, not from the transfer object
  - `self` is not in scope inside an actor access getter; iterate from the entity with a lambda variable
  - a `DERIVED` access needs an expression that returns references; for "see everything" use `ALL` with no getter
  - `!getVariable(...)` returns a scalar; compare with `==`, and qualify the primitive type
- Typical shapes:
  - status filter: `Contest!filter(c | c.status == ContestStatus#OPEN)`
  - singleton: an expression ending in `!any()` with cardinality `0..1`
  - ownership: compare an entity field to the actor's own value, for example `!getVariable("ACTOR", "email")`
  - role-scoped: one `!filter` whose lambda disjuncts a role flag and the ownership clause; JQL has no if/else ([advanced modeling patterns](../../agent-docs/model/advanced-modeling-patterns.md), *Role-scoped access getters*)
- Inside a derived attribute on the principal's own transfer object, `self` is the actor's row (used for flags such as `isNotAdmin`); that is a different place from the access getter.
- Admin actors commonly use `ALL`.
- `isActiveExpression` on the actor decides whether the actor may log in, a separate switch from access filtering.

## Rationale

The filter runs in the generated query, so a client never receives rows outside it, and no custom code is needed. Limits: the expression language has restrictions (no nested lambda scopes, multi-value claims cannot be consumed, `!any()` at most once); when a rule does not fit, compute it in a backend interceptor into a transient attribute ([interceptors](../../agent-docs/backend/interceptors.md)). Access filtering is a model rule; it does not protect custom operations.

## Example

`Player` actor has two accesses to `ContestView`, a transfer object mapped to `Contest`: `allContests` of type `ALL` and `openContests` of type `DERIVED` with getter `Contest!filter(c | c.status == ContestStatus#OPEN)`, cardinality `0..*`.

Seen in 13 projects, mostly for status, ownership and singleton accesses.

## When to avoid

- When the actor should see everything: use `ALL`.
- When visibility depends on logic JQL cannot express: use a custom service or interceptor.
- Do not rely on a UI filter alone for security.

## Related

- [[actor-based-transfer-projection]] — what shape the actor receives
- [[singleton-entity]] — the singleton access shape
- [[range-expression-filtering]] — filtering choices for relation selectors
- [[container-back-reference]] — navigation used inside filters

## Structure diagram

<!-- mermaid:generated fragment=derived-access-filtering cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class Contest {
    <<Entity>>
    +ContestStatus status
    +String title
  }
  class ContestStatus {
    <<Enumeration>>
    OPEN
    CLOSED
  }
  class ContestView {
    <<Transfer>>
    +ContestStatus status
    +String title
  }
  class Player {
    <<Actor>>
  }
  class PlayerPrincipal {
    <<Transfer>>
    +String email
  }
  Contest ..> ContestStatus : status
  ContestView ..> Contest : maps
  ContestView ..> ContestStatus : status
  Player ..> PlayerPrincipal : principal
```
<!-- /mermaid:generated -->
