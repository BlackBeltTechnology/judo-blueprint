---
id: "code-based-player-authentication"
title: "Code-Based Player Authentication with Registration Flow"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

A lightweight authentication pattern for anonymous or semi-anonymous users (players, participants) where access is controlled via a temporary code rather than a full username/password authentication flow. The User entity carries a `code` attribute (the active access code) and a `tmpCode` attribute (a pending code awaiting activation). A separate Admin entity represents the privileged actor with email and active attributes.

The registration flow uses unmapped transfer objects:
1. **RegisterInput** TO: email (req) + name -- the player provides their email and optional name
2. The backend generates a temporary code and stores it in `tmpCode` on the User entity
3. **Credential** TO: email (req) + code (req) -- the player provides their email and the code they received
4. **Application.activate** operation validates the code against tmpCode and promotes it to the active `code`
5. The User entity has a `reset` operation to regenerate the code (e.g., if forgotten)

The Player actor accesses the system through an Application transfer object with `register` (STATIC) and `activate` (STATIC) operations. This pattern avoids the complexity of OAuth/Keycloak integration for simple consumer-facing applications where email-based code verification is sufficient.

This is similar to the token-based verification pattern but simpler: there is no dedicated Token entity, no expiry tracking, and no email template system. The code is stored directly on the User entity.

## Detection Query

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

Look for entities with both `code` and `tmpCode` attributes.

```graphql
{ esm { transferobjecttypes(where: { name: { eq: "Credential" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%RegisterInput%" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

### User entity with code attributes

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "User",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "active"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "code"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::User", name: "tmpCode"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::User", name: "reset",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::User.reset"
} }) { success fqn } }
```

### Registration input TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "RegisterInput"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::RegisterInput", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::RegisterInput", name: "name"
} }) { success fqn } }
```

### Credential TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "Credential"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Credential", name: "code"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Credential", name: "email"
} }) { success fqn } }
```

### Application TO with register/activate

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "Application"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Application", name: "register",
  operationType: "STATIC", binding: "{{SERVICE_NAMESPACE}}::Application.register"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::Application", name: "activate",
  operationType: "STATIC", binding: "{{SERVICE_NAMESPACE}}::Application.activate"
} }) { success fqn } }
```

## Examples

### trivia
- **User entity** (`trivia::entities::User`): non-CRUD
  - Attributes: email (req), name (req), active (req, default: true), code (optional), tmpCode (optional)
  - Relations: tests (0..* ASSOC to Test)
  - Operations: reset (INSTANCE) -- regenerates the access code
- **Admin entity** (`trivia::entities::Admin`): non-CRUD
  - Attributes: email (req), active (req, default: true)
  - Separate entity for admin actors (not the same as User)
- **RegisterInput TO** (`trivia::actors::player::RegisterInput`): unmapped
  - Attributes: email (req), name (optional)
  - Used as input for the register operation
- **Credential TO** (`trivia::actors::player::Credential`): unmapped
  - Attributes: code (req), email (req)
  - Used as input for the activate operation -- validates the code sent to the player's email
- **Player Application TO** (`trivia::actors::player::Application`):
  - Attributes: name (optional)
  - Operations: register (STATIC), activate (STATIC)
  - Entry point for the player registration/authentication flow
- **Admin User TO** (`trivia::actors::admin::User`):
  - Attributes: email (req), name (req), active (req), code, tmpCode
  - Operations: reset (MAPPED) -- admin can reset a player's code
- **Two actor types**: Admin (`trivia::actors::admin::Admin`) and Player (`trivia::actors::player::Player`)
  - Admin manages questions, contests, users; Player registers, enters contests, takes tests
- **AdminPrincipal TO** (`trivia::actors::admin::AdminPrincipal`): email (req), active (req) -- the logged-in admin's identity
