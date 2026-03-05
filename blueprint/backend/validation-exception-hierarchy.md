---
id: "validation-exception-hierarchy"
title: "Validation Exception Hierarchy (Field-Level and Business-Level)"
domain: "backend"
category: "error"
score: 74.2
usage_count: 5
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
  - judo-partner
alternatives:
  - typed-exception-error-handling
---
## Description

A structured exception hierarchy for different error scenarios, centralized via a static `ExceptionUtils` factory class. Three exception types: (1) `ValidationException` for field-level errors shown on specific form fields (with location parameter), (2) `BusinessErrorException` for business-rule violations shown as toast/dialog messages (with error code), (3) `GenericOperationErrorException` for general operation failures. This provides more granularity than a single typed exception approach.

## Structure

```java
// Field-level validation (shown on form field)
throw ExceptionUtils.createValidationException("accountNumber",
    "Bank account number format is invalid");

// Business-level error (shown as toast/dialog)
throw ExceptionUtils.createBusinessErrorException("OFFER_NOT_FOUND",
    i18n.offer_not_found());

// Generic operation error
throw ExceptionUtils.createGenericOperationErrorException(
    "Unexpected error during processing");
```

Interceptors typically use `ValidationException` in `preCall`, while services use `BusinessErrorException` for rule violations.

## Examples

### RackInspect
`ExceptionUtils` provides static factories for all three types. `BankAccountCreateAndUpdateInterceptor` throws `ValidationException("accountNumber", ...)` for format errors. `OfferService` throws `BusinessErrorException("OFFER_NOT_FOUND", i18n.offer_not_found())` for business rules. `HistoryService` catches all exceptions silently (silent failure pattern).

### mlszksz-platform
Primarily uses `BusinessErrorException` via `ExceptionUtils.createBusinessErrorException(code, message)` with i18n messages. Error codes like "FORBIDDEN_ROLE_INVITATION", "USER_NOT_FOUND", "POST_NOT_DRAFT". Services re-throw business exceptions but catch unexpected errors: `catch (BusinessErrorException e) { throw e; } catch (Exception e) { throw ExceptionUtils.createBusinessErrorException("UNEXPECTED", i18n.operation_not_implemented_yet()); }`.

### ParkHere
Uses both `BusinessErrorException` and `ValidationException` in different contexts. Services throw `BusinessErrorException` for business rules (permission denied, too many reservations, user not found). Interceptors throw `ValidationException` for field-level errors (user not present, car not available). `CarService.setFavoriteCarWithValidationException()` translates `BusinessErrorException` to `ValidationException` for interceptor contexts. `ExceptionUtils` provides factories for both: `createBusinessErrorException(ErrorCode, message)` and `createValidationException(location, code)`.

### Indamedia-AdTrack
`ExceptionUtils` provides three static factories: `createBusinessErrorException(ErrorCode, String)` for business errors, `createValidationException(String, String)` for field-level validation, and `createValidationResult(String, String)` for building validation results. BusinessErrorException used throughout all 6 services. ValidationException available but not actively used -- services rely on DAO-level validation. Error codes are strongly typed via `ErrorCode` enum.

### judo-partner
`ExceptionUtils` provides `newValidationException(location, message)` and `newBusinessException(exceptionMessage, operation, errorMessage)`. Primarily uses `ValidationException` with field-level targeting (e.g., `taxNumber`, `name`, `taxNumberType`, `addressCity`). `ValidationErrorCode` enum (NAME_MISMATCH, INVALID_TAX_ID, UNDER_DISSOLUTION, UNDER_LIQUIDATION, DUPLICATE_TAX_ID) categorizes errors. `BusinessException` used for NAV connection failures with Hungarian locale.

## Trade-offs

- Pros: Fine-grained error targeting (field vs business vs generic), i18n-ready messages, centralized factory avoids inconsistency
- Cons: Three exception types to choose from (can cause confusion), Hungarian hardcoded strings in some interceptors bypass i18n
- Alternative: Single modeled `ErrorException` with error codes (simpler but less granular)

## Related Patterns

- typed-exception-error-handling
- interceptor-crud-lifecycle
- i18n-osgi-service
