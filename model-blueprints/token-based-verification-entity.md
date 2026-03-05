---
id: token-based-verification-entity
title: "Token-Based Verification Entity"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---

## Description

An entity that implements a token-based verification workflow with attributes: a verification/invitation token (string), an expiration timestamp (verificationExpiresAt or expiresAt), a verified-at timestamp (verifiedAt), and a status enum following the PENDING -> VERIFIED -> APPROVED/REJECTED lifecycle. This pattern supports email verification, invitation acceptance, and registration approval flows. The entity is typically non-CRUD (created only through custom operations) and carries a rejectionReason for denied requests. A corresponding status enum has members: PENDING, VERIFIED, APPROVED, REJECTED, EXPIRED.

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
