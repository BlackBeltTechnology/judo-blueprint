---
id: "invitation-with-key-based-acceptance"
title: "Invitation Entity with Key-Based Acceptance Flow"
score: 44.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---
## Description

An Invitation entity that implements an invitation workflow using cryptographic keys (public/private key pair) rather than simple verification tokens. The invitation carries:

- **invitationType** -- an enum (USER/ACCOUNT) distinguishing whether the invitation is for a new organization-scoped user or an existing platform account to join an organization
- **email** -- the invitee's email address
- **expiration** -- when the invitation expires
- **inviteId** -- a unique identifier for the invitation link
- **invitePrivateKey / invitePublicKey** -- a cryptographic key pair for secure invitation verification
- **Feature support flags** -- isApplicationFeatureSupported, isOrganizationFeatureSupported (with defaults of false) that determine what the invitee can access after joining

The invitation is composed by an Organization (0..* COMPOSITION) and has a derived back-reference to it. Operations include acceptInvitation (triggered when the invitee clicks the link and provides credentials) and cancelInvitation (for revoking pending invitations). The accept operation takes an AcceptInvitationLinkParameter unmapped TO with userName, firstName, lastName, password, and passwordAgain fields for account creation.

An InvitationType enum (USER/ACCOUNT) discriminates the two invitation flows: USER invitations create a new user scoped to the organization, while ACCOUNT invitations grant an existing platform account access to the organization.

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
