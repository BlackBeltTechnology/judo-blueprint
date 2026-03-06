---
id: "credential-generalization-hierarchy"
title: "Credential Generalization Hierarchy (Platform-Specific API Credentials)"
score: 57.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---
## Description

An abstract or minimal Credential base entity that serves as a common reference point for API credentials, with platform-specific concrete subtypes inheriting from it via generalization. The base Credential entity typically has no data attributes of its own (or very few), and carries only a back-reference relation to the parent entity it authenticates (e.g., Account). Each platform-specific subtype (e.g., GoogleCredential, MetaCredential) adds the fields required by that platform's API: API keys, tokens, customer IDs, key files, delegated accounts, etc. The parent entity (Account) holds a single 0..1 association to the base Credential type, which polymorphically resolves to whichever platform subtype was created. A Platform enum discriminates which platform an Account belongs to.

This pattern enables a single Account entity to work with different external API providers while keeping credential schemas cleanly separated. It is the model-layer analog of the Strategy pattern.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Credential%" } }) {
  items { fqn name abstract
    attributes { items { name } }
    relations { items { name } }
    generalizations { items { fqn } totalCount }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Credential",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Credential", name: "account",
  target: "{{NAMESPACE}}::Account", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PLATFORM_NAME}}Credential",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::{{PLATFORM_NAME}}Credential",
  target: "{{NAMESPACE}}::Credential"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PLATFORM_NAME}}Credential", name: "{{CREDENTIAL_FIELD}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "Platform"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::Platform", name: "{{PLATFORM_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

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
