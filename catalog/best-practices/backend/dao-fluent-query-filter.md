---
id: dao-fluent-query-filter
title: Fluent DAO Query with Type-Safe Filters
description: "Read data through generated DAOs: chain typed filterBy calls (AND-combined), then selectOne, selectList or count; use filterBy(String) JQL for OR logic and relation query methods for navigation."
aliases: [DAO query, typed filters, fluent query, StringFilter]
keywords: [dao, query, filter, StringFilter, BooleanFilter, selectOne, selectList, count, jql, mask]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:workflow-poc", "project:reserve-app", "status:established"]
category: data-access
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, ubives, park-here, indamedia-adtrack, judo-partner, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "alba:unrecorded", "mlszksz-platform:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Query entities in backend code with the generated DAO's fluent query builder: type-safe filters per attribute, chained with AND, ended by a terminal call. This is the default way to read data in custom operations, services and interceptors.

## Practice

### Platform: the fluent query API

The platform documents this API in the [data access guide](../../agent-docs/backend/data-access-guide.md#query-patterns). Key points:

- `dao.query()` returns a builder; `filterBy<Attribute>(Filter)` calls chain with **AND** logic ([combining filters](../../agent-docs/backend/data-access-guide.md#combining-multiple-filters)). Terminals: `selectOne()` (an `Optional`), `selectList()` and `count()` ([query result methods](../../agent-docs/backend/data-access-guide.md#query-result-methods)).
- Filter classes live in `hu.blackbelt.judo.sdk.query`: `StringFilter` (`equalTo`, `notEqualTo`, `like`, `ilike`), `NumberFilter`, `DateFilter`, `TimestampFilter` (equal, not equal, greater/less, with or-equal variants), `BooleanFilter` (`isTrue()` / `isFalse()`, not `equalTo(boolean)`) and `EnumerationFilter` (`equalTo`, `notEqualTo`) ([filters reference](../../agent-docs/backend/data-access-guide.md#sdk-query-filters-reference)).
- OR logic and anything a typed filter cannot express go through `filterBy(String)` with a JQL expression such as `this.isAdmin == true or this.isCoordinator == true`; use `==`, and `(this.f)!like('%x%')` for patterns; navigation (`this.relation.field`) is not supported there ([OR logic](../../agent-docs/backend/data-access-guide.md#or-logic-with-custom-filter-expressions)).
- Relation queries are generated per relation. Multi-valued ones (`countyDao.querySettlements(county)`) return a query customizer that supports filters, masks and `selectList()` but not `orderBy`; single-valued ones return the entity directly, so `.selectOne()` on them does not compile ([relationship navigation](../../agent-docs/backend/data-access-guide.md#relationship-navigation-queries)). Sort multi-valued results in Java.
- `maskedBy(...)` limits the loaded fields and avoids N+1 loading ([masks](../../agent-docs/backend/data-access-guide.md#using-masks-projections), [[mask-field-projection]]).
- Pagination is opt-in: a list call without a seek returns all matching rows ([pagination](../../agent-docs/backend/data-access-guide.md#pagination)).
- Known issues: querying an enumeration attribute with `query<Attribute>()` can throw a `ClassCastException`; and "not set" on an optional boolean needs `filterBy("this.x!isUndefined()")` ([known issues](../../agent-docs/backend/data-access-guide.md#known-issues-of-the-generated-dao)). For calls the SDK cannot express, the low-level `DAO` takes a `QueryCustomizer`.

```java
// Example project code (generated DAO types)
Optional<User> user = userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .filterByActive(BooleanFilter.isTrue())
    .selectOne();

List<Test> tests = contestDao.queryTests(contest)
    .filterByStatus(EnumerationFilter.equalTo(TestStatus.STARTED))
    .selectList();

long correct = testDao.queryPrompts(_this)
    .filterByCorrect(BooleanFilter.isTrue())
    .count();
```

### Project practice

- Duplicate detection before creation: `count() > 0` on the business key ([[upsert-create-or-update]]); existence checks combine `count()` with an empty or small mask.
- Where the query is a user lookup, wrap it once in a service ([[actor-resolution-variable-resolver]]).
- Several projects use `TimeFilter` for time-overlap queries (parking availability) and paged `selectList(offset, limit)` loops for batch validation or migration, and `findAllById` for bulk fetches by identifier list. These calls are not described in the platform docs; verify against the generated DAO of your model.
- Use one clock when a timestamp filter is compared with values written by Java code ([time zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones)).

## Rationale

- Compile-time checked attribute names and filter types, readable chained calls, and no query strings for the common cases.
- Cost: AND-only chaining (OR needs a JQL string, which is unchecked until runtime), no ordering on relation queries, and boolean filters that differ from the other filter classes.

## Example

Trivia filters by status, email and correctness flags in about fifteen query shapes across eight operations. ParkHere combines date, enumeration and two time filters into an availability query. workflow-poc fetches the next unprocessed event with a string filter, a boolean filter and an ordering. Ubives uses `count()` with a mask for username existence checks before creating organizations or applications.

## When to avoid

- When the condition needs OR, navigation or a function: use `filterBy(String)` with JQL, or a model-side derived attribute.
- When the data needs native SQL (for example a join table): there is no DAO method; isolate it in one service with a `DataSource`.
- To create or change data: see [[builder-pattern-entity-creation]] and [[mutable-entity-update-pattern]].

## Related

- [[builder-pattern-entity-creation]] — creating entities
- [[relation-based-entity-creation]] — creating children through a parent
- [[mask-field-projection]] — limiting the fields loaded
- [[upsert-create-or-update]] — query then create or update
- [[actor-resolution-variable-resolver]] — user lookup built on this query
