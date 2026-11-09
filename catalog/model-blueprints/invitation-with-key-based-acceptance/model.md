## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Invitation%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { like: "%InvitationType%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "InvitationType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::InvitationType", name: "USER", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::InvitationType", name: "ACCOUNT", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "InvitationEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "invitationType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "expiration"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "inviteId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "invitePrivateKey"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "invitePublicKey"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "isApplicationFeatureSupported"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "isOrganizationFeatureSupported"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "acceptInvitation",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::InvitationEntity.acceptInvitation"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::InvitationEntity", name: "cancelInvitation",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::InvitationEntity.cancelInvitation"
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "AcceptInvitationLinkParameter"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AcceptInvitationLinkParameter", name: "userName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AcceptInvitationLinkParameter", name: "password"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AcceptInvitationLinkParameter", name: "passwordAgain"
} }) { success fqn } }
```

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
