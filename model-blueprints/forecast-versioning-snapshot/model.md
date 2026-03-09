## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%ForecastVersion%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    relations { items { name lower upper relationKind memberType } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities with both `monthlyForecasts` (0..* COMPOSITION) and `forecastVersions` (0..* COMPOSITION) relations, plus an `archiveForecast` operation.

## Creation Mutations

### MonthlyForecast entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "MonthlyForecast",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecast", name: "month"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecast", name: "savingPotential"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecast", name: "saving"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecast", name: "date"
} }) { success fqn } }
```

### MonthlyForecastVersion entity (immutable snapshot copy)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "MonthlyForecastVersion",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecastVersion", name: "date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecastVersion", name: "savingPotential"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::MonthlyForecastVersion", name: "saving"
} }) { success fqn } }
```

### ForecastVersion entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "ForecastVersion",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ForecastVersion", name: "timestamp"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ForecastVersion", name: "sumOfSavingPotential"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ForecastVersion", name: "sumOfSaving"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::ForecastVersion", name: "monthlyForecasts",
  target: "{{NAMESPACE}}::MonthlyForecastVersion", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### Parent entity (container for forecasts and versions)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

### Parent entity relations and operation

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "monthlyForecasts",
  target: "{{NAMESPACE}}::MonthlyForecast", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "forecastVersions",
  target: "{{NAMESPACE}}::ForecastVersion", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "archiveForecast",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{PARENT_ENTITY}}#archiveForecast"
} }) { success fqn } }
```

## Examples

### itracker
- **Initiative entity** (`itracker::entities::Initiative`): the parent entity for cost-saving initiatives
  - Relations: monthlyForecasts (0..* COMPOSITION to MonthlyForecast), forecastVersions (0..* COMPOSITION to ForecastVersion)
  - Operations: archiveForecast (INSTANCE) -- snapshots the current monthly forecasts into a new ForecastVersion
  - Also has: version attribute (integer, tracks a version counter incremented on each archive)
- **MonthlyForecast entity** (`itracker::entities::MonthlyForecast`): non-CRUD
  - Attributes: month (req), savingPotential (req), saving, date
  - No relations, no operations
  - Represents a single month's forecast within the current (active) forecast plan
- **ForecastVersion entity** (`itracker::entities::ForecastVersion`): non-CRUD
  - Attributes: timestamp (req), sumOfSavingPotential (req), sumOfSaving (req)
  - Relations: monthlyForecasts (0..* COMPOSITION to MonthlyForecastVersion)
  - Each version captures the aggregate totals and a complete copy of the monthly breakdown at the time of archiving
- **MonthlyForecastVersion entity** (`itracker::entities::MonthlyForecastVersion`): non-CRUD
  - Attributes: date (req), savingPotential (req), saving
  - No relations, no operations
  - Immutable copy of MonthlyForecast data frozen within a ForecastVersion
- **Transfer objects**:
  - `itracker::actors::user::ForecastVersion` (mapped): exposes timestamp, sumOfSavingPotential, sumOfSaving, monthlyForecasts (0..* AGGREGATION)
  - `itracker::actors::user::MonthlyForecast` (mapped): exposes month, savingPotential, saving, date
  - `itracker::actors::user::MonthlyForecastVersion` (mapped): exposes date, savingPotential, saving
  - `itracker::actors::user::Initiative` (mapped): exposes forecastVersions (0..* AGGREGATION) and monthlyForecasts (0..* AGGREGATION), plus archiveForecast (MAPPED) operation
