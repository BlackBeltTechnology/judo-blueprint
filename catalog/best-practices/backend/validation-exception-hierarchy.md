---
id: validation-exception-hierarchy
title: Validation Exception Hierarchy (Field-Level and Business-Level)
description: Pick the error type by what failed. Field problems are platform validation exceptions with an attribute location, business refusals are modeled faults, and a project factory creates both so call sites stay uniform.
aliases: [field vs business error, validation vs business exception, ExceptionUtils factory, error type choice]
keywords: [ValidationException, ValidationResult, location, modeled fault, business error, factory, ExceptionUtils, interceptor, i18n, 400, 422]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "status:established"]
category: error
status: established
projects: [rackinspect, mlszksz-platform, park-here, indamedia-adtrack, judo-partner]
evidence: ["rackinspect:unrecorded", "mlszksz-platform:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded"]
alternatives: [typed-exception-error-handling]
related: [typed-exception-error-handling, interceptor-crud-lifecycle, i18n-osgi-service, error-code-enum, safe-failure-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Backend code reports two different kinds of problems and the client treats them differently. A wrong value belongs next to a form field; a refused business rule is shown as a message. Using the right error type for each, and creating them through one factory, keeps behaviour and wording consistent.

## Practice

### Platform base

(See the [Error Handling Guide](../../agent-docs/backend/error-handling-guide.md#platform-exceptions).)

- `ValidationException` (HTTP 400) is unchecked and built from a collection of `ValidationResult` objects (`code`, `level`, optional `location`, `details`). There is no constructor taking a plain string. Several results can be thrown at once.
- `location` is optional and not always a model attribute. The frontend maps a 400 to form fields only when the first result has a `location`; results without one produce only a generic toast, and only a few validation codes have default translations ([Validation Errors Without Location](../../agent-docs/frontend/error-handling.md#validation-errors-without-location)).
- A business refusal is a modeled fault (HTTP 422, `X-Fault`) declared on the operation ([Modeled Faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults), [[typed-exception-error-handling]]). From an interceptor use `InterceptorCallBusinessException` ([Interceptors](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- Any other runtime exception becomes a 500 ([How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)).

### Project layer: choose by what failed

| Failure | Type | Shown as |
| :--- | :--- | :--- |
| A value of one input is invalid | `ValidationException`, result `location` = attribute name | message on the form field |
| A business rule refuses the action | modeled fault (general business error with a code) | toast or dialog |
| General operation failure | a second, generic fault if the model has one | dialog |

In the projects, interceptors mostly validate in `preCall` and throw `ValidationException`, because a field rule fits a create or update payload ([[interceptor-crud-lifecycle]]). Services raise the business fault for rule violations. Where an interceptor needs to report a service's business fault, it must translate it, since a generated fault cannot be thrown from an interceptor; one project translates the business error into a validation exception for interceptor contexts.

### The factory

A static helper class in the project's common module (`ExceptionUtils`, example project code, not part of JUDO) offers:

- `createValidationResult(location, code)` and `createValidationException(location, code)` or `(List<ValidationResult>)`
- `createBusinessErrorException(code, message)` for the project's own business fault
- optionally a generic-operation-error factory

```java
// field level, shown on the field (example project helper)
throw ExceptionUtils.createValidationException("accountNumber", "ACCOUNT_NUMBER_INVALID");

// business level, shown as a message (generated fault type of the project)
throw ExceptionUtils.createBusinessErrorException("OFFER_NOT_FOUND", i18n.offer_not_found());
```

Both calls go through the helper, so a code constant and a translated message are always used and no call site builds exceptions by hand. Put the message in the translation service ([[i18n-osgi-service]]), not into a literal.

### Collect, then throw

When several fields can be wrong, gather all results and throw one `ValidationException` with the whole list ([Validation Strategy](../../agent-docs/backend/error-handling-guide.md#validation-strategy)). Only throw one result when it is the only rule.

### Do not rewrap everything

A catch-all that turns every exception into a business error hides real bugs that should stay 500s. Catch known fault types, wrap known external failures with the cause logged, and let the rest propagate.

## Rationale

- Fine-grained targeting: field versus business versus generic, i18n-ready messages, and a factory that prevents drift.
- Three types to choose from can confuse; the table above is the rule.
- Alternative: a single modeled fault with error codes is simpler but gives no field-level feedback.
- Known gaps in the original projects: hardcoded (for example Hungarian) strings in some interceptors bypass i18n, and a silent-catch service hides failures ([[safe-failure-pattern]]).

## Example

- RackInspect: the factory has static methods for all three kinds. A bank-account create/update interceptor throws a validation exception on the account number location for format errors. An offer service throws the business error for "offer not found".
- mlszksz-platform: mostly the business fault via the factory with i18n messages and codes such as forbidden role invitation or post not draft. Services re-throw business exceptions and wrap anything unexpected as a generic business error.
- ParkHere: services throw the business fault for rules (permission denied, too many reservations, user not found); interceptors throw the validation exception for field-level problems such as an unavailable car. A service method translates the business error into a validation exception for interceptor use.
- Indamedia-AdTrack: the factory has business, validation and validation-result creators. The business error is used throughout the services; the validation exception exists but is rarely used because DAO-level validation covers most cases. Codes come from a model enumeration.
- judo-partner: mostly validation exceptions that target fields (tax number, name, address city) with a validation code enumeration (name mismatch, invalid tax id, duplicate tax id); a business exception with a Hungarian locale for failures of the tax-authority connection.

## When to avoid

- Only one kind of failure exists in the application: use that single type directly ([[typed-exception-error-handling]]).
- The code runs in an interceptor and needs a business refusal: use `InterceptorCallBusinessException` rather than the generated fault.
- The failure is unexpected: let it propagate as a 500.

## Related

- [[typed-exception-error-handling]] — the business-fault side in detail
- [[interceptor-crud-lifecycle]] — where field validation usually runs
- [[i18n-osgi-service]] — message source for the factory
- [[error-code-enum]] — the code vocabulary
- [[safe-failure-pattern]] — deliberate swallowing of failures
