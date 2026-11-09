## Examples

### mlszksz-platform
- **RegistrationRequest**: `MLSZKSZPlatform::entities::RegistrationRequest`
  - Token attributes: verificationToken, verificationExpiresAt, verifiedAt
  - Status: RegistrationRequestStatus (PENDING, VERIFIED, APPROVED, REJECTED, EXPIRED)
  - Additional: organizationName, contactName, contactEmail, contactPhone, companyAdminName, companyAdminEmail, fullAddress, rejectionReason
  - Transfer object exposes accept/reject operations
- **InvitationRecipient**: `MLSZKSZPlatform::entities::InvitationRecipient`
  - Token attributes: verificationToken, verificationExpiresAt
  - Additional: email, sentAt, usedForSuccessfulRegistration
- **UserInvitationRequest**: `MLSZKSZPlatform::entities::UserInvitationRequest`
  - Token attributes: invitationToken, expiresAt, verifiedAt
  - Status: InvitationStatus (PENDING, VERIFIED, APPROVED, REJECTED, EXPIRED)
  - Transfer object exposes accept/reject operations
- **InvitationStatus enum**: `MLSZKSZPlatform::types::InvitationStatus` -- same 5 members as RegistrationRequestStatus
