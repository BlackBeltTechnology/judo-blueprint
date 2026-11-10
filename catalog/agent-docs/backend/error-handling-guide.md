---
title: Backend Error Handling Guide
description: Platform exceptions versus modeled faults, what interceptors may throw, HTTP mapping and error codes.
---

# Backend Error Handling Guide

## Overview

JUDO has two distinct kinds of backend errors. Choosing the right one decides the HTTP status, what the frontend shows, and whether the code can be thrown from where you need it.

| Kind | Java type | Checked? | HTTP | Where it comes from |
| :--- | :--- | :--- | :--- | :--- |
| Platform error | `ValidationException` (400), `AccessDeniedException` (403), `AuthenticationRequiredException` (401), `NotFoundException` (404) | No (`ClientException` extends `RuntimeException`) | 400 / 403 / 401 / 404 | `judo-runtime-core` (`hu.blackbelt.judo.runtime.core.exception`) |
| Modeled fault | Generated `<Fault>Exception` | Yes (`extends java.lang.Exception`) | 422 + `X-Fault` header | Generated from a fault transfer object in your model, declared on an operation |

Rules of thumb:

- A **field or input problem** (a value is wrong, missing, out of range) is a `ValidationException`.
- A **business rule violation** that the client should handle as a typed fault is a **modeled fault** declared on the operation.
- Never throw a bare `RuntimeException` for a user-facing problem: the dispatcher wraps it as `InternalServerException` and the client gets a generic 500.
- **Interceptors cannot throw a modeled fault.** They throw `InterceptorCallBusinessException` (see [Interceptors](interceptors.md#throwing-a-business-error-from-an-interceptor)).

For localizing messages see the [Internationalization Guide](internationalization-guide.md).

## Table of Contents

- [Platform Exceptions](#platform-exceptions)
- [Validation Results and Locations](#validation-results-and-locations)
- [Modeled Faults](#modeled-faults)
- [Exceptions Thrown from Interceptors](#exceptions-thrown-from-interceptors)
- [How the Runtime Maps Exceptions to HTTP](#how-the-runtime-maps-exceptions-to-http)
- [Example Project Helpers (Not Platform API)](#example-project-helpers-not-platform-api)
- [Best Practices](#best-practices)
- [Testing Error Handling](#testing-error-handling)
- [API Error Code Reference](#api-error-code-reference)

---

## Platform Exceptions

All platform exceptions below live in `hu.blackbelt.judo.runtime.core.exception` and extend the abstract, unchecked `ClientException` (`getStatusCode()`, `getDetails()`).

| Exception | HTTP | Constructor | Typical use |
| :--- | :--- | :--- | :--- |
| `ValidationException` | 400 | `(Collection<ValidationResult>)` or `(String message, Collection<ValidationResult>)` | Input validation failures, possibly several at once |
| `AuthenticationRequiredException` | 401 | `(ValidationResult)` | Missing or invalid authentication |
| `AccessDeniedException` | 403 | `(ValidationResult)` | Permission failures |
| `NotFoundException` | 404 | `(ValidationResult)` | A required instance does not exist |

There is no no-arg constructor and no `ValidationException(String)` constructor: `new NotFoundException()` or `new ValidationException("text")` do not compile. Build a `ValidationResult` (`hu.blackbelt.judo.dao.api.ValidationResult`, a Lombok `@Builder`) and pass it in.

```java
import hu.blackbelt.judo.dao.api.ValidationResult;
import hu.blackbelt.judo.runtime.core.exception.ValidationException;

List<ValidationResult> errors = new ArrayList<>();

if (input.getTitle() == null || input.getTitle().isBlank()) {
    errors.add(ValidationResult.builder()
            .code("TITLE_REQUIRED")
            .level(ValidationResult.Level.ERROR)
            .location("title")                       // optional, see below
            .detail("message", i18n.field_is_required())
            .build());
}
if (!errors.isEmpty()) {
    throw new ValidationException(errors);           // all errors in one response
}
```

```java
throw new NotFoundException(ValidationResult.builder()
        .code("ENTITY_NOT_FOUND")
        .level(ValidationResult.Level.ERROR)
        .location("id")
        .build());
```

`ValidationResult` also exists with `Level.WARNING`. Other `RuntimeException`s are not mapped to a status: the dispatcher rethrows `ClientException` and `BusinessException` unchanged and wraps everything else in `InternalServerException("Operation failed", cause)`, which becomes a 500.

## Validation Results and Locations

A `ValidationResult` has `code`, `level`, `location` (type `Object`) and a `details` map. **`location` is optional and not always a model attribute.**

- Field errors carry the attribute or relation name as `location`.
- The platform itself emits results without location (`AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `INVALID_IDENTIFIER`) or with non-field locations such as `_mask` and `_identifier`.
- You may throw a `ValidationException` with only a code (the official documentation example uses `SHIPPED_TIME_MUST_AFTER_ORDER_TIME` with no location).

Do not assume every error can be rendered next to an input field, and do not assume a validation error maps to a model attribute.

Business-semantic failures that are tied to an input can be expressed as a `ValidationException` whose result `code` carries a machine-readable prefix (for example `ERR_QUOTA_EXCEEDED`); clients branch on the code. If the failure is a true business rule that deserves its own typed handling in the UI, model a fault instead.

## Modeled Faults

A modeled fault is a transfer object type in the ESM/JSL model that is attached to an operation as a fault (`<faults>` in the ESM model; `error` declarations with a `throws` clause in JSL).

- The SDK generator turns each fault into a checked `<Fault>Exception extends java.lang.Exception` with typed details and the constructors `(details)`, `(errorCode, details)` and `(errorCode, details, cause)`. The error code is the exception message.
- The operation must **declare the fault**. If a custom-implemented operation has no declared fault, the generated SDK interface has no `throws` clause and Maven fails with `... not compatible with throws clause` when you throw one.
- On the wire a modeled fault is HTTP **422** with header `X-Fault: <fault FQN>` and body `{ "<fault FQN>": { <details> }, "code": "<errorCode>" }`.
- The generated SDK client wrapper catches the platform `BusinessException`, matches its `type` against the declared faults and rethrows the typed `<Fault>Exception`; for an operation without declared faults the raw `BusinessException` passes through. The dispatcher itself never validates the fault type against the model.
- The frontend fault dialog translates attributes with keys `faults.<fault FQN>.<attribute>`.

Because the exception class is generated **per project**, names such as `BusinessErrorException` or `GenericOperationErrorException` exist only if your own model defines faults called `BusinessError` or `GenericOperationError`. They are not part of the platform. If you want such a generic fault, model it explicitly.

```java
// Custom operation implementation: declared fault, checked exception
@Override
public void accept(Entity _this) throws AlreadyShippedException {
    if (isShipped(_this)) {
        throw new AlreadyShippedException("ALREADY_SHIPPED", /* typed details */ details);
    }
}
```

## Exceptions Thrown from Interceptors

`OperationCallInterceptor.preCall` and `postCall` declare `throws InterceptorCallBusinessException` and nothing else.

- A generated `<Fault>Exception` is checked and **cannot** be thrown from an interceptor.
- Interceptors do not handle business problems themselves; a business error they raise is wrapped:
  `new InterceptorCallBusinessException(type, errorCode, details, cause, locale)`. The dispatcher converts it into a `BusinessException` and the client receives 422 with `X-Fault: <type>`.
- Put the **FQN of a modeled fault transfer object** into `type` so the frontend translation `faults.<type>.<attribute>` matches. Neither `type` nor `details` is validated against the model; a typo still returns 422 but the dialog falls back to raw attribute names. `details` must not be `null` (the exception mapper dereferences it).
- A service that you call from an interceptor may throw a checked `<Fault>Exception`; catch it and rethrow it wrapped in `InterceptorCallBusinessException`.
- Field-level problems may still be reported with a `ValidationException` (unchecked, so it compiles), but business refusals belong in `InterceptorCallBusinessException`.

Details and examples: [Interceptors](interceptors.md#throwing-a-business-error-from-an-interceptor).

## How the Runtime Maps Exceptions to HTTP

| Thrown | Status | Body |
| :--- | :--- | :--- |
| `ClientException` subclass | `getStatusCode()` (400 if null) | `getDetails()` as JSON (list of validation results) |
| `BusinessException` (incl. `InterceptorCallBusinessException`) | 422, header `X-Fault: <type>` | `{ "<type>": {details without keys starting with "_" and without nulls}, "code": "<errorCode>" }`; the cause is included only when `includeBusinessCause` is enabled |
| `InternalServerException` / any other `RuntimeException` | 500 | `{ "level": "ERROR", "code": "INTERNAL_SERVER_ERROR", "details": {} }`; the stack trace appears in `details.exception` only when `returnRuntimeExceptions` is enabled (never for `BusinessException`) |

Notes:

- `BusinessException` (module `judo-dispatcher-api`) extends `RuntimeException`, **not** `ClientException`. Fields: `type`, `errorCode`, `details`, `throwable`, `locale`.
- Exceptions are not unwrapped recursively: a `ClientException` or `BusinessException` buried in a cause chain surfaces as a generic 500.
- The CXF `FaultInterceptor` only handles exceptions that escape the mapper and sets just the HTTP status.
- Exposed operations validate their input in a transaction that is rolled back; no interceptors run during that validation.
- There is no `FeedbackItem` class; the equivalent structure is `ValidationResult`.

## Example Project Helpers (Not Platform API)

Many projects write a small helper class (for example an `ExceptionUtils` in the project's own common module) that builds `ValidationResult` objects and wraps their generated fault exceptions. **These helpers are project code, not platform API**: `ExceptionUtils.createValidationResult(...)`, `ExceptionUtils.createValidationException(...)`, `ExceptionUtils.createBusinessErrorException(...)` and `createBusinessException(...)` do not exist in any JUDO runtime module or template. Other agent docs in this directory use them only as examples of such project code; the shape is:

```java
// Example project code (put it in your own common module, not provided by JUDO)
public final class ExceptionUtils {
    public static ValidationResult createValidationResult(String location, String message) {
        return ValidationResult.builder()
                .code(message).level(ValidationResult.Level.ERROR)
                .location(location).build();
    }
    public static ValidationException createValidationException(Collection<ValidationResult> results) {
        return new ValidationException(results);
    }
}
```

When you read an example that calls such a helper, translate it to the platform mechanism above (`new ValidationException(List<ValidationResult>)`, or a modeled fault).

> [!IMPORTANT]
> **There is no `BusinessException` class in `runtime-core`.**
>
> Older docs and code comments sometimes refer to a `BusinessException` type — it does not exist as a Java class in the current JUDO runtime. The concrete type for generic business failures is **`GenericOperationErrorException`**, and `ExceptionUtils.createBusinessException(...)` is the factory that produces it.
>
> **Convention for business-semantic failures**: the idiomatic pattern is to throw a `ValidationException` whose `ValidationResult` entries carry a **machine-code prefix** in the code/message (e.g. `ERR_USER_INACTIVE`, `ERR_QUOTA_EXCEEDED`). Clients branch on the prefix; the 400 status and field-level rendering are a feature, not a bug, because the business cause is tied to an input or an addressable path.

> [!WARNING]
> **`NotFoundException` and `AccessDeniedException` require a `ValidationResult` constructor.**
>
> The current runtime-core does **not** provide a no-arg constructor on these exceptions. You must instantiate them with a `ValidationResult` (or collection thereof):
>
> ```java
> throw new NotFoundException(ExceptionUtils.createValidationResult(
>     "id", i18n.entity_not_found()));
>
> throw new AccessDeniedException(ExceptionUtils.createValidationResult(
>     "principal", i18n.access_denied()));
> ```
>
> `new NotFoundException()` / `new AccessDeniedException()` will not compile. Prefer `ExceptionUtils.createValidationResult(field, message)` so the message is localizable and the field path renders correctly client-side.

---

## Best Practices

### Error Handling Best Practices

✅ **DO:**
- Validate all inputs at the beginning of an operation.
- Collect all validation errors and throw them in a single `ValidationException`.
- Declare faults on operations whose callers must handle a typed business error.
- Provide clear, actionable, localized messages.
- Use the most specific exception type.
- Log errors with context.

❌ **DON'T:**
- Use exceptions for normal control flow.
- Expose internal details or stack traces in user-facing messages.
- Return `null` to signal an error.
- Swallow exceptions silently.
- Throw `RuntimeException` for user-facing errors (it becomes a 500).
- Wrap unexpected exceptions into a business fault; real bugs should stay 500.
- Throw a generated fault from an interceptor.

### Validation Strategy

Collect all errors, then throw once:

```java
List<ValidationResult> errors = new ArrayList<>();

if (entity.getTitle() == null) {
    errors.add(ValidationResult.builder().code("TITLE_REQUIRED")
            .level(ValidationResult.Level.ERROR).location("title").build());
}
if (entity.getAmount() != null && entity.getAmount() < 0) {
    errors.add(ValidationResult.builder().code("AMOUNT_NEGATIVE")
            .level(ValidationResult.Level.ERROR).location("amount").build());
}

if (!errors.isEmpty()) {
    throw new ValidationException(errors);
}
```

A `ValidationException` can carry many `ValidationResult`s. If a custom operation catches it and throws a single fault instead, the per-row result list is lost. Keep the multi-result shape when the client needs a list of row-level problems.

For required fields and relations declared in the model the runtime validator already reports `MISSING_REQUIRED_ATTRIBUTE` and `MISSING_REQUIRED_RELATION` (the latter with `__referenceId`); do not duplicate those checks in custom code.

---

## Testing Error Handling

Use `assertThrows` to verify that custom code throws the expected exception.

```java
@Test
void rejectsMissingTitle() {
    ValidationException ex = assertThrows(ValidationException.class,
            () -> implementation.accept(entityWithoutTitle));
    assertThat(ex.getDetails().toString()).contains("TITLE_REQUIRED");
}

@Test
void rejectsShippedOrder() {
    assertThrows(AlreadyShippedException.class,   // generated from the model fault
            () -> implementation.accept(shippedOrder));
}
```

---

## API Error Code Reference

### Error Response Structure

A failed request returns JSON containing:
- `code`: the error code from the tables below (or your own code).
- `location`: for validation errors, optional; usually the attribute or relation name.
- `details`: a map with additional parameters.

For platform errors the body is a list of such results; for modeled faults see [How the Runtime Maps Exceptions to HTTP](#how-the-runtime-maps-exceptions-to-http).

### HTTP 400 - Bad Request
Invalid input that violates model constraints.

| Error Code | Description |
| :--- | :--- |
| `MISSING_REQUIRED_ATTRIBUTE` | A mandatory attribute was not provided. |
| `MISSING_REQUIRED_RELATION` | A mandatory relation was not provided (carries `__referenceId`). |
| `MISSING_REQUIRED_PARAMETER` | A mandatory operation parameter was not provided. |
| `NOT_ACCEPTED_BY_RANGE` | The selected instance is not in the range of allowed values. |
| `MAX_LENGTH_VALIDATION_FAILED`| A string exceeds the `maxLength` defined in the model. |
| `PATTERN_VALIDATION_FAILED` | A string does not match the model `pattern`. |
| `ENTITY_NOT_FOUND` | An entity referenced by an ID in the request could not be found. |
| `INVALID_QUERY_MASK` | The query mask in the request could not be parsed. |

### HTTP 401 - Unauthorized

| Error Code | Description |
| :--- | :--- |
| `AUTHENTICATION_REQUIRED` | A non-public operation was called without a valid `Bearer` token. |
| `ACCESS_TOKEN_EXPIRED` | The JWT access token has expired. |

### HTTP 403 - Forbidden

| Error Code | Description |
| :--- | :--- |
| `ACCESS_DENIED` | The operation is not exposed to the current actor. |
| `ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION` | The signed instance of a bound operation was produced by a transfer object that is not exposed to the actor. |
| `AUTHENTICATED_ENTITY_NOT_FOUND` | The principal is authenticated but no actor entity exists for it (see [Authentication Guide](authentication-guide.md)). |
| `PERMISSION_DENIED` | The user lacks the required CRUD privileges on the `Access` link. |

### HTTP 404 - Not Found

| Error Code | Description |
| :--- | :--- |
| `BOUND_OPERATION_INSTANCE_NOT_FOUND`| The instance referenced by the signed ID of an `INSTANCE` operation could not be found. |

### HTTP 422 - Unprocessable Entity
Reserved for modeled **business faults** (and `InterceptorCallBusinessException`). The `X-Fault` header contains the fault type (the fault FQN) and the body contains the fault details.

### HTTP 500 - Internal Server Error
An unexpected server-side error (a bug or misconfiguration). See [How the Runtime Maps Exceptions to HTTP](#how-the-runtime-maps-exceptions-to-http).

---

## See Also
- [Internationalization Guide](internationalization-guide.md) - For localizing error messages.
- [Interceptors](interceptors.md) - For errors raised from interceptors.
- [Custom Operations](custom-operations.md) - For implementing operations that may throw these errors.
- [Platform Behavior Reference](platform-behavior-reference.md) - Signed identifiers, optimistic locking, reserved payload keys.
- [Patterns and Best Practices](patterns-and-best-practices.md) - Other common backend patterns.
