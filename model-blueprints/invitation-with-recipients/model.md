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
