---
id: "data-snapshot-versioning"
title: "Data Snapshot Versioning (Immutable History Records)"
domain: "backend"
category: "operation"
score: 54.4
usage_count: 3
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - indamedia-adtrack
  - workflow-poc
alternatives:
  - product-versioning-container
---
## Description

An audit/versioning pattern where the current state of a collection of child entities is copied into immutable snapshot records before a significant state transition. A version entity is created with a timestamp and aggregated summary values, and each child entity is duplicated into a version-specific copy. The snapshots are appended to a versions collection on the parent entity, enabling historical tracking of how data evolved over time.

## Structure

```
// Pseudocode for snapshot creation
var version = new VersionEntity(
    timestamp = Timestamp!now(),
    summaryField1 = this.children!sum(c | c.field1),
    summaryField2 = this.children!filter(c | c.field2!isDefined())!sum(c | c.field2)
)

for (child in this.children) {
    var copy = new ChildVersionEntity(
        field1 = child.field1,
        field2 = child.field2,
        field3 = child.field3
    )
    version.children += copy
}

this.versions += version
```

Entity structure:
- `Parent` -> `children[]` (current mutable data)
- `Parent` -> `versions[]` -> `Version` (immutable snapshots)
- `Version` -> `childCopies[]` -> `ChildVersion` (point-in-time copies)

## Examples

### itracker
`ArchiveForecast` operation creates a `ForecastVersion` with timestamp and summed saving potentials/savings from current `MonthlyForecast` records. Each `MonthlyForecast` is copied into a `MonthlyForecastVersion` with savingPotential, date, and saving fields. Called automatically by `Approve` before status transition to APPROVED, creating an immutable record of forecast state at approval time.

### Indamedia-AdTrack
`AggregatedCampaignService.updateAggregatedCampaign()` creates an `AggregatedCampaignHistory` snapshot on every update, recording name, start, end, totalBudget, dailyBudget, remainingBudget, and remainingDays at the time of the change. History entries track how campaign configuration evolved over time. Used for budget change audit and reporting.

### workflow-poc
`WorkflowVersion` entities represent versioned snapshots of a workflow definition. Each upload creates a new `WorkflowVersion` with an incremented version number, containing states, transitions, events, and role assignments. Uncommitted head versions are replaced on re-upload. Published versions become the active definition. The `Workflow` entity maintains a `head` reference to the latest version and a `published` reference to the active one.

## Trade-offs

- Pros: Complete audit trail, immutable history, enables comparison between versions, simple to query historical state
- Cons: Data duplication grows with each snapshot, no delta/diff storage (full copies), aggregation must be recalculated or stored redundantly
- Alternative: Version container pattern with full entity cloning (see `product-versioning-container`), event sourcing, temporal database tables

## Related Patterns

- state-lifecycle-operation
- builder-pattern-entity-creation
- product-versioning-container
