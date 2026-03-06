---
id: "invitation-with-recipients"
title: "Invitation Entity with Recipient Tracking"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

An Invitation entity representing a batch invitation with a message, createdAt timestamp, and a createdBy relation to the User who sent it. A recipientCount attribute denormalizes the number of recipients. The Invitation has a one-to-many association to InvitationRecipient entities, each tracking: email address, sentAt timestamp, verificationToken, verificationExpiresAt, and a boolean flag usedForSuccessfulRegistration. The Invitation is owned by an Organization (via composition). This pattern supports bulk user invitations with individual tracking of each recipient's verification status.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Invitation%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Invitation",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Invitation", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Invitation", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Invitation", name: "recipientCount"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Invitation", name: "createdBy",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Invitation", name: "recipients",
  target: "{{NAMESPACE}}::InvitationRecipient", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "InvitationRecipient",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationRecipient", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationRecipient", name: "sentAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationRecipient", name: "verificationToken"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InvitationRecipient", name: "verificationExpiresAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::InvitationRecipient", name: "invitation",
  target: "{{NAMESPACE}}::Invitation", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

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
