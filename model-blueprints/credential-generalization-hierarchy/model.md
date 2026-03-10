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
