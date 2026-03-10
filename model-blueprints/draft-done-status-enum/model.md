## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with exactly two members: DRAFT and DONE.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DRAFT", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DONE", ordinal: 2
} }) { success fqn } }
```

## Examples

### rackinspect
- **FaultRegistryStatus**: `rackinspect::entities::FaultRegistryStatus` -- DRAFT(1), DONE(2)
  - Used by: FaultRegistry entity (status attribute, default: DRAFT)
  - FaultRegistry transitions from DRAFT to DONE when the fault inspection is completed
- **OfferStatus**: `rackinspect::entities::OfferStatus` -- DRAFT(1), DONE(2)
  - Used by: Offer entity (status attribute)
  - Offer transitions from DRAFT to DONE when the pricing offer is finalized
