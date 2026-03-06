---
id: "typed-exception-error-handling"
title: "Typed Exception with Error Code Enumeration"
domain: "backend"
category: "error"
score: 61.7
usage_count: 7
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - workflow-poc
alternatives:
  - validation-exception-hierarchy
---
## Description

Custom operations throw typed exceptions using JUDO's modeled fault mechanism. An `ErrorException` wraps a structured `Error` transfer object containing an enumerated error code and human-readable message. This provides a structured, model-driven error contract between backend and frontend.

## Structure

```java
// Define error codes as model enumeration
// ErrorCode: INVALID_CODE, CONTEST_NOT_OPEN, TEST_CLOSED, TEST_ALREADY_STARTED, TEST_NOT_STARTED

// Throw typed exception
throw new ErrorException(
    Error.builder()
        .withCode(ErrorCode.INVALID_CODE)
        .withMessage("Invalid activation code.")
        .build()
);

// Operation signature declares the exception
public TestId apply(Contest _this, Credential input) throws ErrorException {
```

## Examples

### Trivia
5 error codes used across 4 operations: `INVALID_CODE` (Activate, Enter), `CONTEST_NOT_OPEN` (Enter, Start, Submit), `TEST_CLOSED` (Start, Submit), `TEST_ALREADY_STARTED` (Start), `TEST_NOT_STARTED` (Submit). Each builds an Error with code + message string.

### RackInspect
Uses `BusinessErrorException` (modeled fault) instead of `ErrorException`. Operations declare `throws BusinessErrorException`. Error creation is centralized via `ExceptionUtils.createBusinessErrorException(code, message)` with i18n messages from `RackInspectI18n`.

### mlszksz-platform
Uses `BusinessErrorException` via centralized `ExceptionUtils.createBusinessErrorException(code, message)`. Error codes like "FORBIDDEN_ROLE_INVITATION", "USER_NOT_FOUND", "POST_NOT_DRAFT". Messages sourced from `MLSZKSZPlatformI18n` interface. Services re-throw BusinessErrorExceptions but wrap unexpected errors.

### Ubives
Uses `BusinessErrorException` with `ErrorCode` enum and `BusinessError.builder()`. 12+ error codes: `PASSWORD_DOES_NOT_MATCH`, `ORGANIZATION_DOES_NOT_EXISTS`, `ACCOUNT_IS_ALREADY_IN_ORGANIZATION`, `APPLICATION_ALREADY_EXISTS_IN_ORGANIZATION_WITH_THIS_NAME`, `KEYCLOAK_USER_ALREADY_EXISTS_WITH_THIS_NAME`, `IDM_DOES_NOT_EXISTS`. Validation in custom operations (e.g., password match) and service layer (e.g., uniqueness checks).

### ParkHere
Uses `BusinessErrorException` with `ErrorCode` enum (USER_NOT_FOUND, CAR_NOT_FOUND, PERMISSION_DENIED, NOT_VALID_DATA, TOO_MANY_RESERVATION, MISSING_REQUIRED_DATA, RESERVATION_NOT_FOUND). All creation centralized via `ExceptionUtils.createBusinessErrorException(code, message)` with i18n messages from `ParkHereI18n`. Comprehensive validation in `ReservationService.validateInput()` (280+ lines) covering 9 validation categories.

### Indamedia-AdTrack
Uses `BusinessErrorException` with 10 error codes: `USER_NOT_FOUND`, `CLIENT_NOT_FOUND`, `ACCOUNT_NOT_FOUND`, `CAMPAIGN_NOT_FOUND`, `CREDENTIAL_NOT_FOUND`, `CONNECTION_FAILD`, `PLATFORM_NOT_SUPPORTED`, `PLATFORM_NOT_IMPLEMENTED`, `TRACKED_CAMPAIGN_NOT_FOUND`, `TRACKED_CAMPAIGN_UNFETCHABLE`. Centralized via `ExceptionUtils.createBusinessErrorException(code, message)` with i18n from `AdTrackI18n`. Covers entity-not-found, external API failures, and platform support validation.

### workflow-poc
Uses `DeclarationErrorException` with `DeclarationErrorCode` enum and `DeclarationError.builder()`. `UploadCustomImplementation` validates YAML workflow definitions with 6 validation categories: workflow name mismatch, missing state/role/event references, empty transition targets, missing database roles. Each throws `DeclarationErrorException(DeclarationError.builder().withCode(DeclarationErrorCode.INVALID_REFERENCE).withMessage("Role does not exist:" + name).build())`.

## Trade-offs

- Pros: Structured error contract, enumerated codes enable frontend-specific handling, model-driven, type-safe
- Cons: Requires modeled fault type in ESM, error messages are hardcoded strings (not i18n), some operations use RuntimeException instead (gap)
- Alternative: `ValidationException` for field-level errors, `RuntimeException` for unrecoverable errors (less structured)

## Related Patterns

- state-lifecycle-operation
- validation-exception-hierarchy
