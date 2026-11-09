## Overview

The token-based verification pattern is implemented across RegistrationRequest and UserInvitationRequest entities. The `RegistrationService` and `UserService` handle token generation, hashed storage, verification, and the PENDING -> VERIFIED -> APPROVED/REJECTED lifecycle. A `RegistrationCleanupJob` scheduler removes expired and processed requests.

## Implementation Pattern

- Token generation uses `TokenUtils.generateSecureToken()` (UUID-based) and `TokenUtils.hashToken()` (SHA-256 hash) -- the plain token is sent via email while only the hash is stored in the database
- Submission flow: create entity with PENDING status, hashed verificationToken, and computed expiresAt from `ConfigurationTemplateService.getVerificationExpiryMinutes()`
- Verification flow: hash the incoming token, query by hashed token, validate status==PENDING, validate token match, validate not expired, then transition to VERIFIED
- Approval flow: validate status==VERIFIED, create Organization + User + Keycloak account, request magic link for one-click login, send approval email, transition to APPROVED
- Rejection flow: validate status==VERIFIED, transition to REJECTED
- The `RegistrationCleanupJob` scheduler periodically removes: expired PENDING requests (verificationExpiresAt < now), and completed APPROVED/REJECTED requests
- UserInvitationRequest follows the same pattern but with `invitationToken`/`expiresAt` field names and `InvitationStatus` enum
- Custom operations: `RegistrationCustomImplementation`, `ValidateCustomImplementation`, `VerifyUserInvitationCustomImplementation` (registration actor), `AcceptCustomImplementation`, `RejectCustomImplementation` (admin and companyadmin)

## Examples

### mlszksz-platform
- Key files: `common/services/impl/RegistrationServiceImpl.java`, `common/services/impl/UserServiceImpl.java`, `common/utils/TokenUtils.java`, `scheduler/RegistrationCleanupJob.java`, `custom/.../registrationtransfer/RegistrationCustomImplementation.java`
- Pattern: SHA-256 hashed tokens stored in DB; plain tokens sent via email; verification validates hash match + expiry + status; approval creates Organization + User + Keycloak + magic link
- Notable: Two parallel verification workflows (RegistrationRequest for new organizations, UserInvitationRequest for new users in existing organizations) share the same `TokenUtils` and follow identical hash-and-verify logic
