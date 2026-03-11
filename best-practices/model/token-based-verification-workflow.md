---
id: "token-based-verification-workflow"
title: "Token-Based Verification Workflow Pattern"
domain: "model"
category: "operation"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

Entities that require email-based verification use a set of token-related attributes to implement a multi-step verification workflow. A temporary token is generated and sent via email; the user clicks a link to verify, progressing the entity through a state machine (PENDING -> VERIFIED -> APPROVED/REJECTED). Tokens have configurable expiry times and the workflow includes expiration handling.

## Structure

- Entity has token-related attributes:
  - `verificationToken` or `invitationToken`: String storing the random token
  - `verificationExpiresAt` or `expiresAt`: Timestamp for token expiry
  - `verifiedAt`: Timestamp recording when verification occurred
- Entity has a status enum that includes PENDING, VERIFIED, EXPIRED states
- Configuration entity stores expiry durations (e.g., `invitationExpiryDays`, `verificationExpiryMinutes`)
- Operations:
  - Submit/create: generates token, sets expiry, sends email
  - Verify: validates token, checks expiry, transitions to VERIFIED
  - Accept/Reject: admin action after verification
- Token validation is implemented as a custom backend operation

## Examples

### MLSZKSZPlatform
Three entities use token-based verification: **RegistrationRequest** (`verificationToken`, `verificationExpiresAt`, `verifiedAt` with `RegistrationRequestStatus`: PENDING -> VERIFIED -> APPROVED/REJECTED or EXPIRED), **InvitationRecipient** (`verificationToken`, `verificationExpiresAt`, `usedForSuccessfulRegistration` flag), and **UserInvitationRequest** (`invitationToken`, `expiresAt`, `verifiedAt` with `InvitationStatus`: PENDING -> VERIFIED -> APPROVED/REJECTED or EXPIRED). Configuration entity stores `invitationExpiryDays` and `verificationExpiryMinutes`. Custom operations: `RegistrationTransfer.registration` (generates token), `RegistrationTransfer.verifyUserInvitation` (validates token).

## Trade-offs

- Pros: Secure email verification without storing passwords, configurable expiry, clear state progression, supports multiple verification workflows
- Cons: Requires email service integration, token management adds complexity, expired tokens need cleanup
- Prefer when: External users need to verify their identity via email before gaining access (registration, invitation workflows)

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (status lifecycle for verification entities)
- [custom-implementation-placeholder](custom-implementation-placeholder.md) (token generation/validation in custom code)
- [singleton-entity](singleton-entity.md) (Configuration singleton stores expiry settings)
