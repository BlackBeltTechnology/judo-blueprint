## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Post" } }) {
  items { fqn name abstract
    attributes { items { name } }
    relations { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "PostStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostStatus", name: "DRAFT", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostStatus", name: "PUBLISHED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostStatus", name: "DELETED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "PostType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostType", name: "NEWS", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostType", name: "OFFER", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::PostType", name: "REQUEST", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Post",
  createable: true, updateable: true, deleteable: true, abstract: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "title"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "description"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "publishedAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Post", name: "postType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Post", name: "author",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Post", name: "organization",
  target: "{{NAMESPACE}}::Organization", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{SUBTYPE_NAME}}",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::{{SUBTYPE_NAME}}",
  target: "{{NAMESPACE}}::Post"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Abstract base**: `MLSZKSZPlatform::entities::Post` (abstract=true)
  - Attributes: title (req), description (req), status (req), createdAt (req), publishedAt, postType (req)
  - Relations: author (1..1 ASSOC to User), organization (1..1 ASSOC to Organization), inquiries (0..* COMPOSITION to Inquiry)
- **Concrete subtypes** (each generalizes Post):
  - `News` -- adds: image
  - `Offer` -- adds: validFrom (req), validUntil (req), price, isExpired; relation: capabilities (0..* ASSOC)
  - `Request` -- adds: deadline (req), isExpired; relation: capabilities (0..* ASSOC)
  - `Announcement` -- adds: isSensitive (default: false), isStrategic (default: false); relation: documents (0..* ASSOC)
- **Enums**: PostStatus (DRAFT, PUBLISHED, EXPIRED, DELETED, PENDING_REVIEW), PostType (NEWS, OFFER, REQUEST, ANNOUNCEMENT)
