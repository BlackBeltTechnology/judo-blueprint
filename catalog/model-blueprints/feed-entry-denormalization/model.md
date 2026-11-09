## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Feed%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "FeedEntry",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "entryType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "contentId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "title"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "summary"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "organizationName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "authorName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "post",
  target: "{{NAMESPACE}}::Post", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "ownerOrganization",
  target: "{{NAMESPACE}}::Organization", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::FeedEntry", name: "targetOrganizations",
  target: "{{NAMESPACE}}::Organization", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::FeedEntry`
  - Attributes: entryType (req), contentId (req), createdAt (req), title, summary, organizationName, capabilities, authorName, validUntil, isSensitive, validFrom
  - Relations: post (0..1 ASSOC), ownerOrganization (1..1 ASSOC), targetOrganizations (0..* ASSOC)
  - Non-CRUD; populated by backend syncFeed operation
- **Transfer Object**: `MLSZKSZPlatform::services::feed::FeedEntryTO`
  - Adds relations to specific content type TOs: request (0..1), offer (0..1), news (0..1), announcement (0..1), organization (1..1)
- Organization has both ownedFeedEntries and feedEntries relations for owned vs targeted content
