---
id: idm-realm-keycloak-integration
title: "IDM/Realm Keycloak Integration Entity Cluster"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---

## Description

A pair of entities that model external Identity Management (IDM) system integration, specifically for Keycloak or similar OIDC providers. The structure consists of:

- **IdmEntity** -- represents an external identity management server instance with a URL (the Keycloak server address) and an optional name. It holds a one-to-many association to Realm entities, since one IDM server can host multiple realms.
- **RealmEntity** -- represents a Keycloak realm (a security namespace) with a name attribute and a back-reference to its IDM server (0..1 ASSOCIATION). A realm is composed by an Organization (0..1 COMPOSITION), meaning each organization can have its own dedicated authentication realm.

This pattern enables multi-tenant authentication where each organization gets its own Keycloak realm for user registration, while the platform manages the IDM server connection centrally. The Initializer entity has an `initDefaultIdm` operation to seed the default IDM server configuration on first startup. Application entities (composed by Organization) carry applicationId and applicationToken fields for Keycloak client registration.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Idm%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Realm%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "IdmEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::IdmEntity", name: "url"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::IdmEntity", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::IdmEntity", name: "realm",
  target: "{{NAMESPACE}}::RealmEntity", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "RealmEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::RealmEntity", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::RealmEntity", name: "idm",
  target: "{{NAMESPACE}}::IdmEntity", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "ApplicationEntity",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ApplicationEntity", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ApplicationEntity", name: "applicationId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ApplicationEntity", name: "applicationToken"
} }) { success fqn } }
```

## Examples

### ubives
- **IdmEntity**: `Ubives::entities::IdmEntity` (non-CRUD)
  - Attributes: url (req), name (optional)
  - Relations: realm (0..* ASSOC to RealmEntity)
  - Represents a Keycloak server instance; initialized by Initializer.initDefaultIdm
- **RealmEntity**: `Ubives::entities::RealmEntity` (non-CRUD)
  - Attributes: name (req)
  - Relations: idm (0..1 ASSOC to IdmEntity)
  - Composed by OrganizationEntity via realm (0..1 COMPOSITION); each org gets its own realm
- **ApplicationEntity**: `Ubives::entities::ApplicationEntity` (non-CRUD)
  - Attributes: name (req), applicationId (req), applicationToken (req)
  - Relations: organization (0..1 DERIVED back to OrganizationEntity)
  - Operations: deleteApplication (INSTANCE)
  - Represents a Keycloak client registered within an organization's realm
- **FaceIdentifierEntity**: `Ubives::entities::FaceIdentifierEntity` (non-CRUD)
  - Attributes: recognitionId (optional)
  - Linked from IdentityEntity (0..* ASSOC) for biometric authentication support
- **Transfer objects:**
  - `Idm` TO -- url, name; relation: realm (0..* ASSOC)
  - `Realm` TO -- name; relation: idm (0..1 ASSOC)
  - `Application` TO -- name, applicationId, applicationToken; operations: newApplication (STATIC), deleteApplication (MAPPED)
  - `FaceIdentifier` TO -- recognitionId
- Organization.realmName derived attribute provides quick display of the associated realm's name
