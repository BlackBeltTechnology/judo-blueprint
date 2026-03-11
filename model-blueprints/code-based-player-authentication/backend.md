## Overview

The code-based player authentication flow is implemented as two custom operation classes: Register generates a temporary code and sends it via email, while Activate validates the code and promotes it to the active access credential.

## Implementation Pattern

- `RegisterCustomImplementation` implements the generated `Register` operation interface as an OSGi `@Component`
- It injects `UserDao` (for user lookup/creation) and `EmailService` (for sending verification codes) via `@Reference`
- The register operation queries for an existing user by email using `StringFilter.equalTo()`, creates a new User if not found (or updates the existing one), generates a random 4-digit code stored in `tmpCode`, and sends the code via `EmailService.sendMessage()` with a plain-text template
- `ActivateCustomImplementation` implements the `Activate` operation interface as an OSGi `@Component`
- It injects only `UserDao` and validates the email+code combination by querying with both `filterByEmail()` and `filterByTmpCode()` simultaneously
- On successful match, it clears `tmpCode` and sets the permanent `code` attribute; on failure, it throws an `ErrorException` with `ErrorCode.INVALID_CODE`
- The error handling uses the actor-scoped Error TO and ErrorCode enum directly via builder pattern: `ErrorException(Error.builder().withCode(ErrorCode.INVALID_CODE).withMessage(...).build())`

## Examples

### trivia
- Key files: `custom/.../actors/player/application/RegisterCustomImplementation.java`, `custom/.../actors/player/application/ActivateCustomImplementation.java`
- Pattern: Register injects `UserDao` + `EmailService`, generates 4-digit code via `Random.nextInt(10000)`, stores in `tmpCode`, sends email with code and privacy notice; Activate injects `UserDao`, validates email+tmpCode combination, promotes to permanent `code`, throws `ErrorException(ErrorCode.INVALID_CODE)` on mismatch
- Notable: Registration is idempotent -- if a user with the given email already exists, it updates the name and regenerates the tmpCode rather than failing; the email template includes a full GDPR privacy notice as a static final string constant; the permanent `code` is set to the same value as the validated `tmpCode`
