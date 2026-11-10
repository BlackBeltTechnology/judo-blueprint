---
id: operation-call-logging-interceptor
title: Operation Call Logging Interceptor (Debug Logger for Built-in Operations)
description: An OperationCallInterceptor that logs built-in operation calls for debugging; it does not see custom operations, which must log explicitly.
aliases: []
keywords: [operation, call, logging, interceptor, debug, logger, built-in]
tags: [domain:model, layer:backend, project:rackinspect, project:park-here, status:emerging]
category: pattern
status: emerging
projects: [rackinspect, park-here]
evidence: [rackinspect:unrecorded, park-here:unrecorded]
alternatives: []
fragment: none: backend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---

## Intent

Log the fully qualified name of built-in operation calls as they pass through the JUDO dispatcher, without changing the request or the response. It is a debugging and monitoring aid, and a base for an operation audit trail.

### Interceptors see only built-in operations

An `OperationCallInterceptor` runs only around built-in operations (create, update, delete, list and similar generated operations). It never runs around custom (SDK-implemented), MAPPED or script operations, even if `getOperations` lists them. The built-in set also includes refresh, reference set/add/remove, reference range, input range, getTemplate, getMetadata and export. A call to a custom operation produces no interceptor log line. Custom operations that must be logged log explicitly, inside their own implementation.

## Structure

- One class implements `OperationCallInterceptor` and is bound to the model with a `judo.model.name` component property.
- `preCall` receives the `EOperation` and the parameter payload, logs the operation name, and returns the payload unchanged.
- `postCall` may be added to log the result or error status. All interceptors for an operation run `preCall` and `postCall` in registration order; `postCall` is not reversed.
- Scope: without an override of `getOperations`, the interceptor is attached to all built-in operations. Overriding `getOperations` narrows it to a named set of built-in operations.

## Constraints

- An interceptor is not a global logger. Do not rely on it for custom operations.
- The interceptor may only throw `InterceptorCallBusinessException`. Other exceptions are not business faults.
- Do not block or slow the call: logging only, no service calls that can fail the request. A synchronous interceptor runs inside the operation's transaction, and an exception (with the default `terminateOnException` true) ends the call and rolls back its write. An `async()` interceptor runs outside the transaction, but its exceptions are lost.
- Log names and identifiers, not request payloads that may contain personal data.

## Variations

- **All built-in operations**: no `getOperations` override. Simplest debug view.
- **Named built-in operations**: override `getOperations` and resolve the operations once, then cache them.
- **Duration and status**: add `postCall` to log the elapsed time and whether the call failed.

## When to use

- You want a trace of built-in operation calls during development or in a test environment.
- You need an audit foundation for generated create, update and delete calls.

## When to avoid

- You need a complete audit trail. Custom operations are not intercepted, so add explicit logging to them as well (see [[audit-log-entity]]).
- The check or logging must fail a request. Use a validating interceptor with a business exception instead (see [[interceptor-derived-statistics-calculation]] for a postCall example).

## Related

- [[audit-log-entity]] — the persisted audit rows; custom operations write their own row
- [[interceptor-derived-statistics-calculation]] — a postCall interceptor that fills computed values on built-in list responses
