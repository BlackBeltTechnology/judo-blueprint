## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%WorkStatus%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "WorkStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "IN_PROGRESS", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "DONE", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "WONT_FIX", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "NOT_STARTED", ordinal: 4
} }) { success fqn } }
```

## Examples

### rackinspect
- **Enum**: `rackinspect::entities::WorkStatus` -- IN_PROGRESS(1), DONE(2), WONT_FIX(3), NOT_STARTED(4)
- **JobSheet entity**: `rackinspect::entities::JobSheet` -- workStatus (req, default: IN_PROGRESS)
  - Relations: jobSheetItem (0..* COMPOSITION), workReport (0..1 ASSOC), offer (1..1 ASSOC), jobTaskFinishedDocuments (0..1 COMPOSITION)
  - Generalizes from a base document entity
- **WorkReport entity**: `rackinspect::entities::WorkReport` -- workStatus (req, default: IN_PROGRESS), startTime, endTime, numberOfWorkers
  - Relations: jobSheet (1..1 ASSOC), finishedJobSheetItems (0..* ASSOC), signedWorkReportDocument (0..1 COMPOSITION)
  - Generalizes from a base document entity
