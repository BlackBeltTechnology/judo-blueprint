## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%WorkflowVersion%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    operations { items { name operationType } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    relations { items { name lower upper } }
  }
} } }
```

Look for entities with both `head` (0..1) and `published` (0..1) relations pointing to the same version type, plus a `versions` (0..*) collection.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{DEFINITION_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "headVersionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "publishedVersionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "versions",
  target: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "head",
  target: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "published",
  target: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "upload",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{DEFINITION_NAME}}.upload"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}", name: "publish",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{DEFINITION_NAME}}.publish"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{DEFINITION_NAME}}Version",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "versionNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "model"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "committed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "commitComment"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "commitTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "commit",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version.commit"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{DEFINITION_NAME}}Version", name: "{{PARENT_RELATION}}",
  target: "{{NAMESPACE}}::{{DEFINITION_NAME}}", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### workflow-poc
- **Workflow entity**: `workflow::entities::Workflow` (non-CRUD)
  - Attributes: name (req), headVersionNumber, publishedVersionNumber
  - Relations: versions (0..* ASSOC to WorkflowVersion), head (0..1 ASSOC), published (0..1 ASSOC)
  - Operations: upload (INSTANCE), publish (INSTANCE), commit (INSTANCE)
- **WorkflowVersion entity**: `workflow::entities::WorkflowVersion` (non-CRUD)
  - Attributes: name, label, versionNumber (req), model, diagram, committed (req, default: false), commitComment, commitTime, uploadTime
  - Relations: states (0..* COMPOSITION to State), events (0..* COMPOSITION to Event), initialState (0..1 ASSOC), workflow (1..1 ASSOC back to Workflow), role (0..1 ASSOC), observers (0..* ASSOC to URL)
  - Operations: commit (INSTANCE)
- **Lifecycle flow**: upload YAML -> creates new head version (committed=false) -> commit (sets committed=true, records commitTime) -> publish (makes the version the active published version)
- **Admin Transfer Objects**: `workflow::transfers::admin::Workflow` (with upload operation and versions relation), `workflow::transfers::admin::WorkflowVersion` (with commit operation, exposes model/diagram/version metadata, adds uncommitted derived boolean)
- **Input TOs**: `workflow::transfers::admin::UploadInput` (yaml field), `workflow::transfers::admin::CommitInput` (comment field)
