---
id: actor-resolution-variable-resolver
title: Actor Resolution via VariableResolver Pattern
description: Resolve the current authenticated user in a custom operation by reading ACTOR variables through VariableResolver and loading the user entity, usually wrapped once in a project service.
aliases: [current user resolution, getCurrentUser, actor lookup]
keywords: [actor, variable resolver, getVariable, current user, authentication, ownership, audit]
tags: ["domain:backend", "layer:backend", "project:alba", "project:mlszksz-platform", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:reserve-app", "project:doors-model", "project:rackinspect", "status:established"]
category: auth
status: established
projects: [alba, mlszksz-platform, judo-demo-miniworkflow, ubives, park-here, indamedia-adtrack, judo-partner, reserve-app, doors-model, rackinspect]
evidence: ["alba:unrecorded", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/ActorServiceImpl.java", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "reserve-app:unrecorded", "doors-model:unrecorded", "rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/ActorServiceImpl.java"]
alternatives: [keycloak-jit-user-provisioning]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Custom operations and interceptors often need to know who is calling: for authorization checks, ownership of created records and audit entries. The caller's identity is read from the request context with `VariableResolver`, and the application's user entity is then loaded from it.

## Practice

### Platform: variables of the ACTOR category

- Java: inject `hu.blackbelt.judo.dispatcher.api.VariableResolver` with `@Reference` and call `variableResolver.resolve(String.class, "ACTOR", "email")`. This is the Java equivalent of the model/JQL expression `!getVariable('ACTOR', 'email')` ([accessing the logged-in user](../../agent-docs/backend/patterns-and-best-practices.md#4-pattern-accessing-user--request-context)).
- Variable categories include `SYSTEM`, `ENVIRONMENT`, `REQUEST`, `ACTOR`, `PRINCIPAL` and `SEQUENCE` ([variable providers](../../agent-docs/backend/platform-behavior-reference.md#variable-providers)). `ACTOR` values come from the actor the runtime resolved for the request; the actor row is read from the database on every request that carries a principal, and a missing row gives `AUTHENTICATED_ENTITY_NOT_FOUND` ([principal-to-actor resolution](../../agent-docs/backend/authentication-guide.md#principal-to-actor-resolution-and-multi-client-mapping)).
- In model expressions the same value is available without Java: `Type!filter(u | u.email == types::Email!getVariable('ACTOR', 'email'))!any()`; primitive types must be fully qualified ([getVariable rules](../../agent-docs/backend/architectural-patterns.md#rules-for-accessesgetterexpression)).

### Practice notes: look up the user entity, then wrap it once

Which actor attributes exist (`email`, `userName`, `identifier`) depends on the model's actor type. Typical code queries the user entity with the resolved value:

```java
// Example code: User and UserDao are generated types
@Reference VariableResolver variableResolver;
@Reference UserDao userDao;

String email = variableResolver.resolve(String.class, "ACTOR", "email");
User user = userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .selectOne()
    .orElseThrow(() -> new IllegalStateException("Current user not found: " + email));
```

- `selectOne()` returns an `Optional` ([query result methods](../../agent-docs/backend/data-access-guide.md#query-result-methods)); decide explicitly what a missing user means instead of `.orElse(null)`, which only moves the failure to a later NullPointerException.
- Do not paste this block into every operation. Several applications wrap it in one service (`ActorService` / `Variables`, example helpers) with `getCurrentUser()`, which throws a business error when the user is missing; operations inject only that service.
- Interceptors use the same lookup, for example to resolve the caller's account for ownership on create or to check an admin flag. Remember that interceptors do not protect custom operations, so the check must also sit in the operation or its service ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- When a Keycloak user may exist without a database row, provisioning is a separate concern ([[keycloak-jit-user-provisioning]]).

### Variation: shared actor service

One variant wraps the ACTOR variable lookup in a shared `ActorService` that every operation injects, instead of repeating the lookup per operation.

## Rationale

- The identity comes from the authenticated request, not from client-supplied input, so it cannot be spoofed by an operation parameter.
- One wrapper removes the duplicated lookup, gives one place for the not-found handling, and makes operations easier to unit test with a mocked service.
- Cost: one extra database query per operation for the user entity (the runtime already read the actor row, but your user entity is a separate load); a wrapper may cache per request.

## Example

Typical uses: setting the author or owner on a created record, recording who performed a state transition, writing a log entry with the acting user, and gating admin-only features. One variant resolves the actor purely in the model with an expression (`!getVariable('ACTOR', 'email')` filtered over the user entity) in its transition operations, and another variant injects a thin wrapper with a model-name target filter so it binds to the right model.

## When to avoid

- When a model expression can do the work: a derived attribute or an access filter using `getVariable` needs no Java at all.
- When the operation only needs the actor's identifier or email and not the entity, skip the user query and use the resolved value directly.
- Authorization decisions belong in the model's access control where possible; this pattern only supplies identity.

## Related

- [[keycloak-jit-user-provisioning]] — creates the user row this lookup expects
- [[custom-operation-osgi-component]] — where the lookup is called from
- [[dao-fluent-query-filter]] — the query used to load the user
