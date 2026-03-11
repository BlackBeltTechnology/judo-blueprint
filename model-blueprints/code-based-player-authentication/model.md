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
