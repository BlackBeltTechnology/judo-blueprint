## Examples

### indamedia-adtrack
- **Base entity**: `AdTrack::entities::Credential` (non-CRUD)
  - No data attributes
  - Relations: account (1..1 ASSOCIATION to Account)
- **Subtypes** (each generalizes Credential):
  - `GoogleCredential` -- customerId (req), delegatedAccount (req), jsonKeyFile (req), developerToken (req)
  - `MetaCredential` -- no additional attributes (placeholder for future Meta/Facebook API fields)
- **Platform enum**: `AdTrack::entities::Platform` -- META(1), GOOGLE(2)
- **Account entity**: `AdTrack::entities::Account` -- platform (req), isActive (req, default: true); relation: credential (0..1 ASSOC to Credential)
- Transfer object `AccountTransfer` exposes `setGoogleCredential` and `testConnection` operations
- `GoogleCredentialInput` unmapped TO provides the credential fields for the set operation
