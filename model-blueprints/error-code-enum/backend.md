## Overview

The ErrorCode enum and BusinessError transfer object provide structured error handling across all custom operations. An `ExceptionUtils` utility class provides factory methods to create `BusinessErrorException` instances from an error code and message. Every custom operation's method signature declares `throws BusinessErrorException`, and operations throw these structured errors for entity-not-found checks, authorization failures, integration errors, and business rule violations.

## Implementation Pattern

- An `ExceptionUtils` utility (interface with static methods or class) provides `createBusinessErrorException(...)` to build `BusinessError` instances and wrap them in `BusinessErrorException`
- **Enum variant**: `createBusinessErrorException(ErrorCode errorCode, String message)` uses the model-defined `ErrorCode` enum for type-safe error identification. The `BusinessError` is built with `.withErrorCode(errorCode).withMessage(message)`
- **String variant**: `createBusinessErrorException(String code, String message)` uses free-form string codes without a companion enum. The `BusinessError` is built with `setCode(code)` and `setMessage(message)`
- **Direct builder variant**: Service layer classes construct `BusinessError` directly via `BusinessError.builder().withCode(ErrorCode.SOME_CODE).build()` and throw `new BusinessErrorException(...)` without a utility class
- **Domain-scoped variant**: The error code enum and error TO are scoped to a specific domain (e.g., `DeclarationErrorCode` for workflow validation) rather than application-wide, with a domain-specific exception class (e.g., `DeclarationErrorException`)
- **Actor-scoped inline variant**: The error code enum and error TO live in a specific actor namespace (e.g., `actors.player`), and custom operations throw the actor-scoped `ErrorException` directly via `Error.builder().withCode(ErrorCode.SOME_CODE).withMessage(...).build()` without a utility class
- All custom operation method signatures declare `throws BusinessErrorException`
- The same `ExceptionUtils` often also provides `createValidationException()` for field-level validation errors using JUDO's `ValidationResult` API
- Service layer classes (OSGi `@Component`) use `@Reference` to inject DAO classes and an i18n service, then call `ExceptionUtils.createBusinessErrorException(...)` in orElseThrow lambdas for entity lookups
- Error codes typically cover: entity lookup failures (*_NOT_FOUND), authorization (PERMISSION_DENIED), external integration issues (CONNECTION_FAILED, CREDENTIAL_NOT_SET), and platform support (PLATFORM_NOT_SUPPORTED)

## Examples

### mlszksz-platform
- Key files: `common/utils/ExceptionUtils.java`, `custom/.../offer/ModerationDeleteCustomImplementation.java` (authorization check), `custom/.../feedpanel/RegisterDeviceCustomImplementation.java` (validation)
- Pattern: `ExceptionUtils.createBusinessErrorException("CODE", message)` used in custom operations for both authorization and validation failures
- Notable: This project uses string-typed error codes without a companion ErrorCode enum -- the simplest variant of the pattern; errors are raised in custom operations like ModerationDelete (role check) and RegisterDevice (empty token check)

### indamedia-adtrack
- Key files: `common/utils/ExceptionUtils.java`, `common/impl/AccountServiceImpl.java`, `common/impl/AggregatedCampaignServiceImpl.java`, `common/impl/AdsBusinessApiProviderServiceImpl.java`
- Pattern: `ExceptionUtils.createBusinessErrorException(ErrorCode.CAMPAIGN_NOT_FOUND, i18n.campaign_not_found())` -- uses the model-defined `ErrorCode` enum with an i18n service for localized messages
- Notable: Enum variant with 12 error codes covering entity lookups (CLIENT_NOT_FOUND, ACCOUNT_NOT_FOUND), credential issues (CREDENTIAL_NOT_SET, CREDENTIAL_NOT_FOUND), integration failures (CONNECTION_FAILD), and platform support (PLATFORM_NOT_SUPPORTED, PLATFORM_NOT_IMPLEMENTED). The `AdsBusinessApiProviderService` dispatches on `Platform` enum and raises platform-specific errors.

### park-here
- Key files: `common/utils/ExceptionUtils.java`, `common/impl/ReservationServiceImpl.java`, `common/impl/HolidayServiceImpl.java`, `common/impl/ActorServiceImpl.java`, `common/impl/ConfigurationServiceImpl.java`
- Pattern: `ExceptionUtils.createBusinessErrorException(ErrorCode.USER_NOT_FOUND, parkHereI18n.user_not_found())` -- uses the model-defined `ErrorCode` enum with an i18n service (`ParkHereI18n`) for localized messages
- Notable: Enum variant with 8 error codes. The `ExceptionUtils` interface also provides `createValidationException()` for field-level validation using JUDO's `ValidationResult` API. Error codes are used extensively across all services: `ReservationServiceImpl` alone uses 6 different error codes (MISSING_REQUIRED_DATA, USER_NOT_FOUND, PERMISSION_DENIED, NOT_VALID_DATA, RESERVATION_NOT_FOUND, TOO_MANY_RESERVATION) for comprehensive reservation validation covering time checks, slot availability, permission checks, and per-type quota enforcement.

### ubives
- Key files: `services/AccountService.java`, `services/InviteService.java`, `services/ApplicationService.java`, `services/AccessService.java`, `services/OrganizationService.java`
- Pattern: Direct builder variant -- no `ExceptionUtils` utility class. Service layer classes construct errors inline via `new BusinessErrorException(BusinessError.builder().withCode(ErrorCode.SOME_CODE).build())` in `orElseThrow` lambdas and guard clauses
- Notable: 20 error codes covering identity management: uniqueness violations (ORGANIZATION_ALREADY_EXISTS_WITH_THIS_NAME, KEYCLOAK_USER_ALREADY_EXISTS_WITH_THIS_NAME), entity lookups (ACCOUNT_DOES_NOT_EXISTS, ORGANIZATION_DOES_NOT_EXISTS, INVITATION_DOES_NOT_EXISTS), Keycloak integration failures (KEYCLOAK_COULD_NOT_CREATE_USER, IDM_DOES_NOT_EXISTS), authentication (PASSWORD_DOES_NOT_MATCH), and validation (MISSING_REQUIRED_ATTRIBUTE at ordinal 10000)
- The BusinessError TO uses `code` field (not `errorCode`) and lives in the `entities` package; messages are not set in most cases -- the error code alone identifies the failure, making this a code-only variant without i18n

### workflow-poc
- Key files: `custom/.../entities/workflow/UploadCustomImplementation.java`
- Pattern: Domain-scoped direct builder variant -- `DeclarationError.builder().withCode(DeclarationErrorCode.INVALID_REFERENCE).withMessage(...)` constructed inline and thrown as `DeclarationErrorException` during workflow YAML upload validation
- Notable: Minimal single-member enum (`INVALID_REFERENCE`) scoped to workflow declaration validation. No `ExceptionUtils` utility; errors are built directly in validation guard methods (`checkWorkflowName`, `checkCrossReferences`, `checkStateExist`, `checkRoleExist`, `checkEventExist`). The upload operation performs 5 distinct cross-reference validations: workflow name match, initial state existence, transition from/to state existence, role existence, and event existence -- all raising the same INVALID_REFERENCE code with context-specific messages.

### trivia
- Key files: `custom/.../actors/player/application/RegisterCustomImplementation.java`, `custom/.../actors/player/application/ActivateCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/SubmitCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/test/StartCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/contest/EnterCustomImplementation.java`
- Pattern: Actor-scoped inline variant -- `ErrorException(Error.builder().withCode(ErrorCode.INVALID_CODE).withMessage(...).build())` constructed directly in custom operations without a utility class. The ErrorCode enum and Error TO live in the `trivia.actors.player` namespace rather than shared entities.
- Notable: 5 error codes all related to quiz workflow state preconditions (INVALID_CODE, CONTEST_NOT_OPEN, TEST_NOT_STARTED, TEST_ALREADY_STARTED, TEST_CLOSED). Used across 5 custom operation classes -- every player-facing operation validates preconditions and throws structured errors. No ExceptionUtils utility and no i18n; messages are hardcoded English strings.
