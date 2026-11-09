## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "History" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "History",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whoDid"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whatDid"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whenDid"
} }) { success fqn } }
```

## Examples

### rackinspect
- **Entity**: `rackinspect::entities::History` (non-CRUD)
  - Attributes: whoDid (req), whatDid (req), whenDid (req)
  - No relations on the entity itself
- Composed by Task entity via `history` (0..* COMPOSITION)
- Task entity also has: created (default: now()), modified (default: now()), registryNumber; relations: documents (0..* COMPOSITION to Document), lastDocument (0..1 ASSOC), assignedTo (1..1 ASSOC to User)
- Provides a simple chronological audit log per task without structured enum-based action types
