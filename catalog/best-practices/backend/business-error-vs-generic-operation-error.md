---
id: business-error-vs-generic-operation-error
title: Business Error Fault for UI-Visible Failures (422 vs 500)
description: "A failure the user must see and act on is raised as a modeled business fault (HTTP 422) declared on the operation; anything else surfaces as a generic 500 toast."
aliases: [422 vs 500, business fault, UI-visible error]
keywords: [fault, business error, 422, 500, X-Fault, custom operation, error code, throws]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: error
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [typed-exception-error-handling]
fragment: "none: backend-only"
first_seen: 2026-07-09
last_updated: 2026-11-10
---
## Intent

Only a failure that reaches the frontend as a structured fault is rendered as a message the user can act on. This practice decides, per custom operation, whether a failure is a modeled business fault (shown to the user) or an unexpected internal error (generic toast).

## Practice

### Platform base

- A modeled fault is a transfer object attached to an operation as a fault. The generator turns it into a checked `<Fault>Exception` with the constructors `(details)`, `(errorCode, details)` and `(errorCode, details, cause)`; the error code is the exception message ([error handling guide](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).
- The operation must declare the fault in the model. Without it the generated interface has no `throws` clause and the build fails when the implementation throws it.
- On the wire a modeled fault is HTTP 422 with header `X-Fault: <fault FQN>` and body `{ "<fault FQN>": {details}, "code": "<errorCode>" }`. Any other `RuntimeException` becomes a 500 with the fixed code `INTERNAL_SERVER_ERROR` and empty details ([HTTP mapping](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)).
- The generated React client shows a 500 as a generic internal-error toast; a 422 goes to the operation fault dialog, which translates attributes by `faults.<fault FQN>.<attribute>` ([frontend error handling](../../agent-docs/frontend/error-handling.md)).
- `BusinessErrorException` and `GenericOperationErrorException` are not platform classes. They exist only when the project's own model defines faults named `BusinessError` or `GenericOperationError`.

### Project practice: pick the fault by audience

This layer is project practice (rackinspect):

- If the failure is a business rule violation the user can act on, the operation declares a modeled business-error fault and the implementation throws its exception with a machine code and a localized message.
- A generic operation-error fault is only for truly internal failures where a 500 is acceptable.
- The choice is made in the model (the operation's fault target) and then regenerated; the `throws` clause of the operation interface follows the model.
- Project code, not platform API: a shared `ExceptionUtils.createBusinessErrorException(code, i18nMessage)` factory wrapped the generated exception.

```java
// Example project code: ExceptionUtils is a project helper, BusinessErrorException is generated from the project's BusinessError fault
throw ExceptionUtils.createBusinessErrorException("RACK_IN_USE", i18n.rack_in_use());
// which builds: new BusinessErrorException(BusinessError.builder().withCode(code).withMessage(msg).build())
```

- The one-argument constructor leaves `getErrorCode()` and the exception message null: the machine code lives in the details body, so tests should assert `ex.getDetails().getCode()` (observed in the project; *verify* against your generated class, the platform docs describe an `(errorCode, details)` constructor that sets the message).

## Rationale

- Users get actionable, localized business messages from a type-safe, model-driven error contract.
- Expected business failures (422) stay separate from bugs (500).
- Cost: a modeled `BusinessError` transfer object, plus a model change and regeneration to switch an operation's fault.

## Example

`deleteRack` and `deleteWarehouse` were first modeled with a generic operation-error fault. The `RACK_IN_USE` / `WAREHOUSE_IN_USE` reasons reached the client only as an opaque 500 and never appeared in the UI. Switching the operation fault to the modeled business error and regenerating rendered the guard message as a proper 422 fault, in line with the existing delete-fault registry and the app-wide factory idiom.

The old text states that the generic fault yields 500. The platform docs say any modeled fault is a 422, so that 500 most likely came from how the project's generic fault was thrown or declared: *verify* which of the two in your project.

## When to avoid

- Failures tied to an input field or addressable path: a `ValidationException` with machine-code prefixes renders at the field (400, see [[validation-exception-hierarchy]]).
- Interceptors: a generated checked fault exception cannot be thrown from an interceptor; use `InterceptorCallBusinessException` with the fault FQN as `type` instead ([error handling guide](../../agent-docs/backend/error-handling-guide.md#exceptions-thrown-from-interceptors)). Interceptors also never run around custom operations.
- Failures where a 500 is acceptable because the user cannot act on them.

## Related

- [[typed-exception-error-handling]] — the broader modeled-fault mechanism
- [[validation-exception-hierarchy]] — field-level (400) validation errors
- [[guarded-delete-with-deactivate-fallback]] — a guard that relies on this
