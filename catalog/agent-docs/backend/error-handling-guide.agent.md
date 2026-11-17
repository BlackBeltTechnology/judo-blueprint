# error-handling-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/error-handling-guide.md.

## Overview
- Two kinds: platform error (`ValidationException` 400, `AccessDeniedException` 403, `AuthenticationRequiredException` 401, `NotFoundException` 404) and modeled fault (generated `<Fault>Exception`, HTTP 422 + `X-Fault`).
- Platform errors come from `judo-runtime-core`, package `hu.blackbelt.judo.runtime.core.exception`.
- Input problem (wrong, missing, out of range) → `ValidationException`. Typed business rule → modeled fault declared on the operation.
- Never throw a bare `RuntimeException` for user-facing problems: the dispatcher wraps it as `InternalServerException` → generic 500.
- Interceptors cannot throw a modeled fault; they throw `InterceptorCallBusinessException`.

## Platform Exceptions
- All live in `hu.blackbelt.judo.runtime.core.exception`; extend unchecked `ClientException` (extends `RuntimeException`).
- No no-arg constructor and no `ValidationException(String)` constructor. Use `new ValidationException(List<ValidationResult>)`.
- Gotcha: `InternalServerException("Operation failed", cause)` takes message and cause.

## Validation Results and Locations
- `ValidationResult` fields: `code`, `level`, `location` (type `Object`, optional), `details` map.
- Field errors carry the attribute or relation name as `location`.
- Platform results without location: `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `INVALID_IDENTIFIER`.
- A `ValidationException` may carry only a code (for example `SHIPPED_TIME_MUST_AFTER_ORDER_TIME`).
- Do not assume every error renders next to an input field.

## Modeled Faults
- A fault is a transfer object type in the model, attached to an operation as a fault.
- Generated class names are per project (`BusinessErrorException` is an example, not a fixed name).
- SDK generator emits checked `<Fault>Exception extends java.lang.Exception` with typed details.
- Operation must declare the fault. Without a declared fault the SDK interface has no `throws` clause and Maven fails with `not compatible with throws clause`.
- Wire: HTTP 422, header `X-Fault: <fault FQN>`, body `{ "<fault FQN>": { <details> }, "code": "<errorCode>" }`.
- Generated client catches platform `BusinessException`, matches `type` to declared faults.
- Frontend fault dialog translates keys `faults.<fault FQN>.<attribute>`.

## Exceptions Thrown from Interceptors
- `OperationCallInterceptor.preCall` and `postCall` declare `throws InterceptorCallBusinessException`.
- Constructor: `new InterceptorCallBusinessException(type, errorCode, details, cause, locale)`.
- Put the FQN of a modeled fault transfer object into `type`, so `faults.<type>.<attribute>` translates.
- Generated `<Fault>Exception` is checked and cannot be thrown from an interceptor.
- A checked service exception called from an interceptor: catch and rethrow as `InterceptorCallBusinessException`.
- Field-level problems may still use `ValidationException` (unchecked, compiles).

## How the Runtime Maps Exceptions to HTTP
- `BusinessException` (module `judo-dispatcher-api`) extends `RuntimeException`, not `ClientException`.
- Exceptions are not unwrapped recursively: a `ClientException` or `BusinessException` inside a cause chain is not mapped.
- CXF `FaultInterceptor` handles only exceptions that escape the mapper and sets only the HTTP status.
- Exposed operations validate input in a transaction that is rolled back; no interceptors run then.
- No `FeedbackItem` class exists; the equivalent is `ValidationResult`.

## Example Project Helpers (Not Platform API)
- Projects often write helpers such as `ExceptionUtils` (`createValidationResult`, `createValidationException`, `createBusinessException`). Not platform API.
- Translate helper calls to the platform mechanism (`new ValidationException(...)`, `BusinessException`).

## Best Practices
- Validate all inputs at the start of an operation.
- Collect all validation errors and throw them in one `ValidationException`.
- Declare faults on operations whose callers must handle a typed business error.
- Use the most specific exception type; use exceptions for errors, not normal control flow.
- Messages: clear, actionable, localized; never expose internal details or stack traces.
- Log errors with context.
- Validation strategy: `MISSING_REQUIRED_ATTRIBUTE`, `MISSING_REQUIRED_RELATION`, `__referenceId` appear in results.

## Testing Error Handling
- Use `assertThrows` to verify custom code throws the expected exception.

## API Error Code Reference
- Failed request body: `code` (from tables or own code), `location` (validation only, usually attribute or relation name), `details` (map).
- Platform errors: body is a list of results; modeled faults use the `X-Fault` form.
- 400: invalid input violating model constraints.
- 401 / 403 / 404: authentication, access denied, not found.
- 422: reserved for modeled business faults and `InterceptorCallBusinessException`; `X-Fault` carries the fault FQN.
- 500: unexpected server-side error (bug or misconfiguration).

## See Also
- Related: `internationalization-guide.md`, `interceptors.md`, `custom-operations.md`, `platform-behavior-reference.md`, `patterns-and-best-practices.md`.
