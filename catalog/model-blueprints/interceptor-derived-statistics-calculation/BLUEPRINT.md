---
id: interceptor-derived-statistics-calculation
title: Interceptor-Based Derived Statistics Calculation
description: A statistics transfer object whose counts with relative date filters are filled in by an operation interceptor after built-in list and refresh operations.
aliases: [statistics interceptor, derived counts interceptor]
keywords: [interceptor, postCall, statistics, derived, count, date filter, transfer object]
tags: [domain:model, layer:model, layer:backend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model", "mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/StatisticsActiveUsersInterceptor.java"]
alternatives: [operation-call-logging-interceptor]
fragment: interceptor-derived-statistics-calculation
diagram: { kinds: [entity, transfer], members: types }
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Some statistics need counts with a relative date filter, such as "accounts that logged in during the last 30 days". The platform expression language (JQL) does have date functions (`Timestamp!now()`, `!plusDays(n)`), so a plain model-level derived attribute is the first choice and should be tried first. The platform docs name the cases it cannot cover: values that need a lookup outside the model, collection-valued context, or logic that nested JQL scopes cannot express. For those the platform's escape hatch is a transient transfer object attribute with no binding, filled by an operation interceptor's postCall hook. This entry applies that escape hatch to date-filtered counts; the choice of an interceptor for this case is the application's, not a platform requirement. The hook fills in the computed values on the response of a built-in list or refresh operation.

### The interceptor sees only built-in operations

The platform runs interceptors only for the built-in behaviour operations the runtime implements itself: create, update, delete, list/query, refresh, set/unset/add/remove reference, reference and input range, getTemplate, getMetadata, getPrincipal, upload token, export and validate. Custom (SDK-implemented), MAPPED and script operations never hit an interceptor, even when `getOperations` lists them or returns an empty collection (empty means all built-in calls only). The statistics fields are therefore available only on the built-in list and refresh operations of the statistics transfer object, not on a custom operation that returns the same data. A custom operation that needs the same numbers must compute them in its own implementation.

### The hook fills values in the payload

The postCall hook adds the computed values to the response payload that the built-in operation returns. The values are not stored, so each call recomputes them.

## Structure

The shape has a writable account entity with a stored timestamp (the last login), and a transfer object `Statistics` that carries transient count attributes. The count attributes are declared transient with no binding. The transfer object is not createable, updateable or deleteable. Its counts are filled in by the interceptor, not by the model. The interceptor is attached to the built-in list and refresh operations of the statistics transfer object.

## Constraints

- The interceptor applies only to the built-in list and refresh operations it is registered for. Custom operations get no interceptor around them.
- The interceptor may throw only `InterceptorCallBusinessException`. A modeled fault's generated exception is checked and cannot be thrown from an interceptor.
- When several interceptors apply to one operation, both preCall and postCall run in registration order (postCall is not reversed). Synchronous interceptors run inside the operation's transaction, so an exception rolls back the operation's write.
- The count attributes are transient. They are not stored and are not part of the entity's data.
- Date filters use a threshold that is computed from a clock passed into the interceptor, so tests can control it.
- Counts are recomputed on every call, so a heavy count query slows the list or refresh it is attached to.

## Variations

- **Global statistics.** The transfer object has counts over the whole system, attached to one list operation.
- **Per-parent statistics.** The transfer object is linked to a parent (for example an organization), and the interceptor counts only the rows under the parent identifier in the payload.
- **Pre-computed statistics.** A scheduled job stores the counts on an entity, when the numbers do not need to be current.

## When to use

- A dashboard or statistics page needs counts with a relative date filter.
- The numbers may be a little stale only if the list or refresh is cheap; otherwise use a stored value.
- The statistics are read through built-in list or refresh operations.

## When to avoid

- The count can be written as a plain model-level derived attribute, including date arithmetic with `!now()` and `!plusDays(n)`. Prefer that.
- A custom operation must return the statistics. The interceptor will not run for it.
- The counts must be exact at the moment of a write, or must be stored for audit.
- The count query is expensive and the page is called often. Pre-compute the numbers instead.

## Related

- [[operation-call-logging-interceptor]]: another postCall interceptor on built-in operations
- [[audit-log-entity]]: shows that audit rows for custom operations must be written by the operation, because interceptors skip them
- [[initializer-entity-with-init-operation]]: a custom static operation that interceptors do not wrap
