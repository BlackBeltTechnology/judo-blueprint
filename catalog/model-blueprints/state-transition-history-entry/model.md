## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%HistoryEntry%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

Look for entities with `fromState`, `toState`, and `eventTime` attributes.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}HistoryEntry",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "fromState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "toState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "eventTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", name: "user",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "{{HISTORY_RELATION_NAME}}",
  target: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntry", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### Transfer object with denormalized user representation

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}HistoryEntryTransfer"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "fromState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "toState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "eventTime"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}HistoryEntryTransfer", name: "userRepresentation"
} }) { success fqn } }
```

## Examples

### judo-demo-miniworkflow
- **Entity**: `MiniWorkflow::DocumentHistoryEntry` (non-CRUD)
  - Attributes: fromState (optional), toState (req), eventTime (req), message (optional)
  - Relations: user (1..1 ASSOC to User)
  - Composed by Document via `documentHistoryEntries` (0..* COMPOSITION)
- **Transfer Object**: `MiniWorkflow::DocumentHistoryEntryTransfer`
  - Attributes: fromState, toState (req), eventTime (req), message, userRepresentation (denormalized user name)
  - Relations: user (1..1 ASSOC)
- When a Document state transition occurs (requestReview, accept, reject, close), a new DocumentHistoryEntry is created recording fromState (previous state), toState (new state), eventTime (when), message (optional reason), and user (who)
- The message field is populated when a reject operation includes a reason via the Message input TO
- DocumentTransfer exposes `documentHistoryEntries` (0..* AGGREGATION) for viewing the full state transition timeline on the document detail page
