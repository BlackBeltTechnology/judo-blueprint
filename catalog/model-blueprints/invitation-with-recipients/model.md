## Examples

### mlszksz-platform
- **Invitation entity**: `MLSZKSZPlatform::entities::Invitation`
  - Attributes: message, createdAt (req), recipientCount
  - Relations: createdBy (1..1 ASSOC to User), recipients (0..* ASSOC to InvitationRecipient)
  - Non-CRUD; created by backend via custom operations (inviteBulk, inviteUser)
- **InvitationRecipient entity**: `MLSZKSZPlatform::entities::InvitationRecipient`
  - Attributes: email (req), sentAt, verificationToken, verificationExpiresAt, usedForSuccessfulRegistration
  - Relations: invitation (1..1 ASSOC back to Invitation)
- Organization owns Invitations via composition (0..*)
- Bulk invitation supported via BulkInvitationInput TO (emailList, csvFile)
