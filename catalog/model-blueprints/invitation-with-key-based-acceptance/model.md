## Examples

### ubives
- **InvitationEntity**: `Ubives::entities::InvitationEntity` (non-CRUD)
  - Attributes: invitationType (req), email (req), expiration (req), userName (optional), invitePrivateKey (optional), invitePublicKey (optional), inviteId (optional), isApplicationFeatureSupported (req, default: false), isOrganizationFeatureSupported (req, default: false)
  - Relations: organization (0..1 DERIVED back to OrganizationEntity)
  - Operations: acceptInvitation (INSTANCE), cancelInvitation (INSTANCE)
  - Composed by OrganizationEntity via invitations (0..* COMPOSITION)
- **InvitationType enum**: `Ubives::entities::InvitationType` -- USER(1), ACCOUNT(2)
  - USER: invitation for a new user to be created in the organization
  - ACCOUNT: invitation for an existing platform account to join the organization
- **AcceptInvitationLinkParameter** TO (unmapped): userName (req), firstName (optional), lastName (optional), password (req), passwordAgain (req) -- used as input for the acceptInvitation operation when creating a new user account
- **Transfer objects:**
  - `Invitation` TO -- email, expiration, invitationType, inviteId; operations: cancelInvitation (MAPPED), inviteUser (STATIC), inviteAccount (STATIC)
  - `InviteLink` TO -- full invitation fields including keys; operations: acceptInvitation (MAPPED), cancelInvitation (MAPPED)
  - `InviteAccountParameter` (unmapped) -- email (req) -- input for inviting existing accounts
  - `InviteUserParameter` (unmapped) -- email (req) -- input for inviting new users
- Organization operations inviteAccount and inviteUser create InvitationEntity instances with the appropriate type
- The AnonymousActor accesses invitation acceptance via the InviteLink TO without authentication
