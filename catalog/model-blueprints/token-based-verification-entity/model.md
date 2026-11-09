## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Registration%" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "{{REQUEST_TYPE}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{REQUEST_TYPE}}Status", name: "PENDING", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{REQUEST_TYPE}}Status", name: "VERIFIED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{REQUEST_TYPE}}Status", name: "APPROVED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{REQUEST_TYPE}}Status", name: "REJECTED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{REQUEST_TYPE}}Status", name: "EXPIRED", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{REQUEST_TYPE}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "verificationToken"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "verificationExpiresAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "verifiedAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "rejectionReason"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{REQUEST_TYPE}}", name: "createdAt"
} }) { success fqn } }
```

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
