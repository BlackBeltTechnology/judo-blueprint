---
id: forecast-versioning-snapshot
title: "Forecast Versioning with Monthly Snapshot Composition"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - itracker
---

## Description

A versioning pattern for periodic financial forecasts where a parent entity (e.g., Initiative) maintains both current monthly forecasts and archived forecast versions. The structure has three levels:

1. **Parent entity** (e.g., Initiative) -- composes both:
   - `monthlyForecasts` (0..* COMPOSITION) -- the current/active monthly breakdown
   - `forecastVersions` (0..* COMPOSITION) -- archived snapshots of previous forecast states

2. **MonthlyForecast entity** -- represents a single month's forecast data with:
   - `month` (required) -- month identifier or label
   - `savingPotential` (required) -- projected value
   - `saving` -- actual realized value
   - `date` -- specific date reference

3. **ForecastVersion entity** -- a timestamped snapshot that captures:
   - `timestamp` (required) -- when the snapshot was taken
   - `sumOfSavingPotential` (required) -- aggregated total of projected values
   - `sumOfSaving` (required) -- aggregated total of actual values
   - `monthlyForecasts` (0..* COMPOSITION to MonthlyForecastVersion) -- the frozen monthly breakdown

4. **MonthlyForecastVersion entity** -- an immutable copy of monthly data within a version:
   - Same fields as MonthlyForecast (date, savingPotential, saving)
   - Composed by ForecastVersion, not directly by the parent

An `archiveForecast` instance operation on the parent entity triggers the snapshot: it copies the current monthly forecasts into a new ForecastVersion with their aggregated sums and a timestamp.

This pattern enables tracking how forecasts evolve over time -- comparing what was projected at different points against actual outcomes. It differs from simple entity-change-history-snapshot by maintaining structured monthly granularity within each version rather than flat attribute snapshots.

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
  relationKind: COMPOSITION
} }) { success fqn } }
```

### Parent entity relations and operation

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "monthlyForecasts",
  target: "{{NAMESPACE}}::MonthlyForecast", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "forecastVersions",
  target: "{{NAMESPACE}}::ForecastVersion", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "archiveForecast",
  operationType: INSTANCE
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
