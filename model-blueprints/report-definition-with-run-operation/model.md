## Detection Query

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    operations { items { name customImplementation } }
    relations { items { name relationKind } }
  }
} } }
```

Look for entities named Definition or Report with a `run` operation and COMPOSITION relations to Result entities.

## Creation Mutations

### Report package and entities

```graphql
mutation { create(input: { package: {
  container: "{{ROOT_NAMESPACE}}", name: "report"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{ROOT_NAMESPACE}}::report", name: "Definition",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{ROOT_NAMESPACE}}::report", name: "Result",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

### Report Definition members

```graphql
mutation { create(input: { dataMember: {
  container: "{{ROOT_NAMESPACE}}::report::Definition", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{ROOT_NAMESPACE}}::report::Definition", name: "results",
  target: "{{ROOT_NAMESPACE}}::report::Result", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{ROOT_NAMESPACE}}::report::Definition", name: "run",
  operationType: "INSTANCE", binding: "{{ROOT_NAMESPACE}}::report::Definition.run"
} }) { success fqn } }
```

### Report Result members

```graphql
mutation { create(input: { dataMember: {
  container: "{{ROOT_NAMESPACE}}::report::Result", name: "time"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{ROOT_NAMESPACE}}::report::Result", name: "excel"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{ROOT_NAMESPACE}}::report::Result", name: "createExcel",
  operationType: "INSTANCE", customImplementation: true,
  binding: "{{ROOT_NAMESPACE}}::report::Result.createExcel"
} }) { success fqn } }
```

## Examples

### skillmatrix-model
- **report::Definition entity**: `SkillMatrix::report::Definition`
  - Attributes: name (req)
  - Relations: selectedUnits (0..* OneWay ASSOC Unit), results (0..* COMPOSITION Result), selectedUsers (0..* OneWay ASSOC User)
  - Operations: run (INSTANCE) -- executes the report and creates a new Result entry

- **report::Result entity**: `SkillMatrix::report::Result`
  - Attributes: time (Timestamp), excel (Binary), reportName (DERIVED: `self!container(SkillMatrix::report::Definition).name`)
  - Relations: users (0..* OneWay ASSOC User)
  - Operations: createExcel (INSTANCE, customImplementation=true) -- generates an Excel export file from the report data
  - The `reportName` derived attribute navigates up to the parent Definition via `!container()` to display the report name

- **Report transfer objects**:
  - report::ReportDefinition TO -- name (MAPPED) + executions (0..* ASSOC ReportResult), units (0..* AGGREGATION Unit), professionals (0..* AGGREGATION Professional); operations: run (MAPPED)
  - report::ReportResult TO -- time (DERIVED), reportName (MAPPED), excel (DERIVED)
  - report::ResultHelper TO -- time (MAPPED), reportName (MAPPED), excel (MAPPED) + competences (0..* AGGREGATION Competence), users (0..* AGGREGATION ReportedUser); operations: createExcel (MAPPED)
  - report::ReportedUser TO -- fullName (MAPPED), unitName (DERIVED) + skills (0..* AGGREGATION Skill)
  - report::Skill TO -- competenceName (MAPPED), competenceScore (MAPPED), approvedLevelName (MAPPED), userFullName (MAPPED), unitName (MAPPED) + tags (0..* AGGREGATION Tag)
  - report::Competence TO -- user (TRANSIENT), unit (TRANSIENT), competence (TRANSIENT), tag (TRANSIENT), score (TRANSIENT), level (TRANSIENT) -- all transient attributes for tabular flattening

- **Report data flow**:
  1. HR Employee creates a report::Definition, selecting units and/or users
  2. HR Employee runs the report (Definition.run operation)
  3. The run operation creates a Result, snapshots the matching users, and stores a timestamp
  4. The createExcel operation (custom Java implementation) generates an Excel file from the result data
  5. The report::Competence TO with all-transient attributes serves as a flattened row structure for Excel generation
