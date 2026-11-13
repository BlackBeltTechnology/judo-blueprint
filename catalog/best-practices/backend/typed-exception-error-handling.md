---
id: typed-exception-error-handling
title: Typed Exception with Error Code Enumeration
description: Business failures in custom operations are raised as a modeled fault, typically one general fault object carrying a code and a message, declared on every operation that can fail and created through a project factory.
aliases: [business error fault, modeled fault error handling, BusinessError fault, typed business exception, error code fault]
keywords: [modeled fault, fault, BusinessError, error code, exception, 422, X-Fault, custom operation, declared fault, ExceptionUtils, interceptor, InterceptorCallBusinessException]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:workflow-poc", "status:established"]
category: error
status: established
projects: [trivia, rackinspect, mlszksz-platform, ubives, park-here, indamedia-adtrack, workflow-poc]
evidence: ["trivia:unrecorded", "rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/EntityLifecycleServiceImpl.java", "rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/faultregistry/elementfault/ElementFaultUpdateInterceptor.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/utils/ExceptionUtils.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/post/impl/PostLifecycleServiceImpl.java", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "workflow-poc:unrecorded"]
alternatives: [validation-exception-hierarchy]
related: [state-lifecycle-operation, validation-exception-hierarchy, error-code-enum, safe-failure-pattern, interceptor-security-filter-validation, accept-reject-operations]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A business rule that refuses an operation (wrong state, missing permission, an external system that failed) needs a structured answer the client can show or branch on. In JUDO that answer is a modeled fault: a transfer object declared on the operation. Across applications the practice is to model one general fault with a code and a message, declare it on every operation that can fail, and raise it through one factory.

## Practice

### Platform base: modeled faults

(Platform facts, see the [Error Handling Guide](../../agent-docs/backend/error-handling-guide.md#modeled-faults).)

- A fault is a transfer object attached to an operation as a fault. The generator produces a checked `<Fault>Exception` with typed details and the constructors `(details)`, `(errorCode, details)` and `(errorCode, details, cause)`.
- The operation must declare the fault. Without it the generated interface has no `throws` clause and the build fails when you throw one.
- The client receives HTTP 422 with the header `X-Fault: <fault FQN>` and the details plus `code` in the body. The frontend fault dialog translates the attributes with keys `faults.<fault FQN>.<attribute>` ([fault dialog](../../agent-docs/frontend/error-handling.md#operation-fault-dialog-http-422)).
- The exception class is generated per application. `BusinessErrorException` or `GenericOperationErrorException` exist only because an application modeled faults of those names; they are not platform API.
- Interceptors cannot throw a generated fault. They throw `InterceptorCallBusinessException` with the fault FQN as `type` ([Throwing a Business Error from an Interceptor](../../agent-docs/backend/interceptors.md#throwing-a-business-error-from-an-interceptor)).
- Field and input problems are `ValidationException` (400), not faults. A bare `RuntimeException` becomes a 500 ([How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)).

### Layer notes: one general fault

Applications converged on this shape. It is a modelling convention, not something the platform requires:

- One fault transfer object with a required `code` (a String) and a `message`. In the largest application this fault is declared on many operations (deletes, workflow steps, and document operations). Two more faults exist for special needs: a generic operation error with an operation name and details (mostly on toggle operations), and a bulk-upload error that also carries row locations so a bulk upload can report per-row problems.
- Codes are plain strings held as constants in application code, or an enumeration in the model (see [[error-code-enum]] for the trade-off). An enumeration gives the client a closed list; strings avoid a model change for each new code. Either way the code is the key for the frontend translation and for client branching.
- A factory (an `ExceptionUtils` class in the application's common module, example code) creates every exception: `createBusinessErrorException(code, message)` for the general fault, plus helpers for `ValidationResult` and `ValidationException`. The rule is to never `new` an exception inline. The code is a named constant and the message comes from the i18n service ([[i18n-osgi-service]]).

```java
// factory, example code; the exception type is generated from the model's own fault
public Entity accept(Entity _this) throws BusinessErrorException {
    Entity entity = dao.getById(_this.identifier(), EntityMask.entityMask()).orElseThrow();
    if (entity.getStatus() != Status.OPEN) {
        throw ExceptionUtils.createBusinessErrorException(
            Codes.ENTITY_NOT_OPEN, i18n.entity_not_open());
    }
    // ...
}
```

### Choosing the error type

| Situation | Use |
| :--- | :--- |
| A value of an input is wrong, tied to an attribute | `ValidationException` with the attribute as `location` |
| A permission, state, cross-entity or external-system failure | the general business fault (code + message), not a location-less validation result |
| Failure raised in an interceptor | `InterceptorCallBusinessException`, fault FQN as `type` |
| Readiness or completeness checks that should not abort | return the results as data instead of throwing |

The platform allows a validation result without location. The rule keeps validation results for attributes, so every location in a result is a model attribute name and the form can show it. Everything else becomes a business fault.

### Fail loudly, wrap on purpose

- Do not turn a missing precondition into a silent no-op. Raise a business fault with its own code (for example an "AI processing switched off" code) so the user sees why nothing happened.
- A known failure mode of an external system (connection refused, quota) is wrapped into the business fault and the cause is logged.
- Unexpected exceptions are real bugs and should stay 500. A catch-all that rewrites every exception to a generic business error hides them, as some implementations do; avoid it ([Error Handling Best Practices](../../agent-docs/backend/error-handling-guide.md#error-handling-best-practices)).

### Anti-patterns seen in practice

- Catching the generated fault and rethrowing a `RuntimeException`: the client then sees a 500 instead of the 422 fault. This happened in interceptors and a user-management service.
- Letting a database failure surface as "forbidden", or catching `Exception` and silently returning `allowed = false` without a log.
- Using `IllegalStateException` for business invariants: it becomes a 500.
- Passing a translated message as the `code` argument for not-found cases: the code should be a stable constant and the message separate.

## Rationale

- Structured, model-driven contract: a typed fault with a stable code lets the frontend translate and branch.
- One general fault keeps the model small and the factory simple; the cost is that the type does not tell the client which rule failed, only the code does.
- Hardcoded message strings in some implementations bypass i18n; use the translation service.
- Alternative: `ValidationException` only, simpler but with no typed fault handling in the UI ([[validation-exception-hierarchy]]).

## Example

- One application: a few codes (invalid code, group not open, result closed, result already started, result not started) in a model enumeration, built into an error object with code and message and thrown from several operations.
- One application: a general business error fault with string codes, created through the factory with messages from the i18n interface. It is declared on many operations; the two special faults cover generic operation errors and bulk upload.
- Another application: the same fault and factory, codes such as forbidden role invitation, user not found and post not draft. Services re-throw the fault and wrap unexpected errors, a catch-all that this entry advises against.
- A third application: the fault with an error-code enumeration of several codes (password mismatch, account missing, name already used, identity user exists), checked in custom operations and in the service layer.
- Two applications: the fault with an enumeration (not found, permission denied, too many bookings, external connection failed, platform unsupported), created through the common factory. One of them has a long input validation service that raises these.
- A workflow example: a domain-scoped declaration error with its own code enumeration for the YAML workflow validation, one code per category of reference problem.

## When to avoid

- The failure is a wrong input value: use `ValidationException` ([[validation-exception-hierarchy]]).
- The failure is a bug or an unexpected infrastructure error: let it be a 500.
- You are in an interceptor: use `InterceptorCallBusinessException`.
- The client never reacts to the failure other than showing a generic error.

## Related

- [[validation-exception-hierarchy]] — field-level counterpart and the factory
- [[error-code-enum]] — model blueprint for the code vocabulary and fault object
- [[state-lifecycle-operation]] — state checks that raise the fault
- [[safe-failure-pattern]] — where failures are deliberately swallowed
- [[interceptor-security-filter-validation]] — raising errors from interceptors
- [[accept-reject-operations]] — operations that declare the fault
