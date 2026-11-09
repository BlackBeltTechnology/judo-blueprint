## Overview

The Invitation/InvitationRecipient entities are created by backend services that handle bulk invitation workflows. An `AdminInvitationService` manages admin-level bulk invitations (CSV-based), while the `UserService.inviteUser()` handles individual user invitations within an organization. Both generate hashed verification tokens with expiry for each recipient and send invitation emails.

## Implementation Pattern

- The `AdminInvitationServiceImpl` handles bulk invitations via `inviteBulk()`: parses a CSV file of email addresses, creates an `Invitation` entity with a `recipientCount` denormalized field, and creates `InvitationRecipient` entities for each email
- Each `InvitationRecipient` gets a securely generated token (`TokenUtils.generateSecureToken()`), hashed before storage (`TokenUtils.hashToken()`), with an expiry timestamp computed from `Configuration.invitationExpiryDays`
- Invitation emails are sent via `PlatformEmailService` with the plain (unhashed) token for verification links
- The `RegistrationServiceImpl.submitRegistration()` validates the invitation token by hashing the incoming token and querying `InvitationRecipientDao.filterByVerificationToken()`, then checks expiry and reuse status
- After successful registration submission, `InvitationRecipient.usedForSuccessfulRegistration` is set to `true` to prevent code reuse
- Custom operations: `InviteBulkCustomImplementation` (AdminDashboard), `InviteUserCustomImplementation` (OrganizationAdminPanel)

## Examples

### mlszksz-platform
- Key files: `common/services/impl/AdminInvitationServiceImpl.java`, `common/services/impl/RegistrationServiceImpl.java`, `custom/.../admindashboard/InviteBulkCustomImplementation.java`, `custom/.../organizationadminpanel/InviteUserCustomImplementation.java`
- Pattern: Bulk CSV parsing creates Invitation + InvitationRecipient entities; tokens are hashed (SHA-256) before storage; verification validates hash match + expiry + reuse flag
- Notable: Supports both admin bulk invitations (CSV file with emailList) and company-admin single invitations; both use the same `TokenUtils` for token generation and hashing
