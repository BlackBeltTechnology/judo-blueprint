---
id: "business-error-vs-generic-operation-error"
title: "Business Error Fault for UI-Visible Failures (422 vs 500)"
domain: "backend"
category: "error"
score: 31.0
usage_count: 1
alternative_count: 1
first_seen: "2026-07-09"
last_updated: "2026-07-09"
projects:
  - rackinspect
alternatives:
  - typed-exception-error-handling
---
## Description

Only a **modeled business fault** reaches the frontend as a displayable message. JUDO maps exception types to HTTP status codes, and the generated React client treats them very differently:

| Thrown from custom op | HTTP | Frontend behavior |
| --- | --- | --- |
| `GenericOperationErrorException` | **500** | Generic "something went wrong" crash toast; `code`/`details` payload is **not** surfaced |
| modeled `BusinessErrorException` | **422** (+ `X-Fault` header) | Structured fault rendered to the user (code + message) |

**Rule:** if a custom operation's failure must be *shown to the user* (a business rule violation they can act on), the operation MUST declare a modeled business-error `fault` (e.g. `BusinessError`) and throw `BusinessErrorException`. `GenericOperationError` is only for truly internal/unexpected failures where a 500 is acceptable. This choice is made **in the model** (the operation's `faults` parameter target) and then regenerated — the operation interface's `throws` clause follows the model.

## Structure

```
# Model: set the operation fault target to the business-error TO (regenerate after)
update(fqn: "…::Rack.deleteRack/faults[fault]",
       input: { parameter: { target: "…::services::error_services::BusinessError" } })
```
```java
// Impl throws the modeled fault via the shared factory
throw ExceptionUtils.createBusinessErrorException("RACK_IN_USE", i18n.rack_in_use());
// -> new BusinessErrorException(BusinessError.builder().withCode(code).withMessage(msg).build())
```
Note: the 1-arg `BusinessErrorException(BusinessError)` leaves `getErrorCode()`/`getMessage()` null — the machine code lives in the body, so assert `ex.getDetails().getCode()` in tests.

## Examples

### RackInspect
`deleteRack`/`deleteWarehouse` were first modeled with `fault GenericOperationError` → the `RACK_IN_USE`/`WAREHOUSE_IN_USE` reason surfaced only as an opaque 500 and never appeared in the UI. Switching the operation fault to the modeled `BusinessError` (then regenerating) made the guard message render as a proper 422 business fault, matching the established `DeleteFaultRegistry` prior art and the app-wide `ExceptionUtils.createBusinessErrorException(code, i18nMessage)` idiom.

## Trade-offs

- Pros: users get actionable, localized business messages; type-safe, model-driven error contract; clean separation of "expected business failure" (422) vs "bug" (500).
- Cons: requires a modeled `BusinessError` transfer object and a model change + regen to switch an operation's fault.
- Prefer when: the failure is a business-rule violation the end user should see and act on.

## Related Patterns

- [typed-exception-error-handling](typed-exception-error-handling.md) — the broader modeled-fault mechanism
- [validation-exception-hierarchy](validation-exception-hierarchy.md) — field-level (400) validation errors
- [guarded-delete-with-deactivate-fallback](guarded-delete-with-deactivate-fallback.md) — a guard that relies on this
