---
id: "snapshot-versioning-pattern"
title: "Snapshot Versioning via Clone-to-Version Entities"
domain: "model"
category: "entity"
score: 63.4
usage_count: 4
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
alternatives:
  - self-referencing-versioning
---
## Description

An entity maintains a history of snapshots by cloning its current data into separate "history" or "version" entities. The parent holds both the current working data (editable) and archived snapshots (read-only collection of version entities). An operation creates point-in-time copies with aggregate summaries or timestamped records of key field values at the time of change.

## Structure

- Parent entity has a composition or association to history/version entities (`0..*`)
- Version/history entity mirrors key attributes from the parent with additional metadata (timestamp)
- Version entity has a required `1..1` relation back to the parent
- An update operation:
  1. Creates a new history/version record with the current or previous field values
  2. Attaches it to the parent's history collection
  3. Updates the parent entity
- History records are immutable once created

## Examples

### itracker
`Initiative` has current data in `monthlyForecasts -> MonthlyForecast [0..*]` and history in `forecastVersions -> ForecastVersion [0..*]`. `ForecastVersion` holds `timestamp`, `sumOfSavingPotential`, `sumOfSaving` and its own `monthlyForecasts -> MonthlyForecastVersion [0..*]`. The `archiveForecast` operation creates a ForecastVersion, computes sums (with null-safe `!isDefined()` filtering), clones each MonthlyForecast into a MonthlyForecastVersion, and attaches everything to the initiative.

### IndamediaAdTrack
`AggregatedCampaign` has a `history [0..*]` association to `AggregatedCampaignHistory`. The history entity snapshots 5 key fields (`name`, `start`, `end`, `totalBudget`, `dailyBudget`) plus a `changed: Timestamp`. When `updateAggregatedCampaign` changes budget or dates, a new history record captures the previous values. Each history record has a required `aggregatedCampaign [1..1]` back-reference. Records are immutable and ordered by `changed` timestamp.

### judo-partner
`Record` entity has `versions -> RecordVersion [0..*]` (TWO-WAY) and `currentVersion -> RecordVersion [0..1]` (stored pointer to the latest version). `RecordVersion` captures `version: Integer`, `registrationTimestamp: Timestamp`, `changes: Text`, `recordNumber: String` (identifier), and `deliveryTimestamp`. The `currentVersion` stored pointer avoids the need for derived head/sort expressions to find the latest version.

### workflow-poc
`Workflow` maintains version tracking with `versions [0..*]` (all versions), `head [0..1]` (latest, possibly uncommitted), and `published [0..1]` (active production version). `WorkflowVersion` has `versionNumber`, `committed` (boolean), `commitComment`, `commitTime`, `uploadTime`, and `model`/`diagram` (YAML/Mermaid content). The `upload` operation creates new versions; `commit` marks them as finalized; `publish` promotes head to published. This dual-pointer (head/published) pattern enables draft editing without affecting production.

## Trade-offs

- Pros: Full history preserved with timestamps and aggregates, current data remains editable, each version is independent
- Cons: Data duplication (cloned entities), requires separate entity types for versions, more complex entity graph
- Prefer self-referencing-versioning when: The entire entity needs versioning (not just child data)
- Prefer snapshot-versioning when: Only a subset of child data needs periodic snapshots with aggregated summaries

## Related Patterns

- [self-referencing-versioning](self-referencing-versioning.md) (alternative: linked-list versioning of the entity itself)
- [composition-ownership](composition-ownership.md)
- [audit-event-entity](audit-event-entity.md) (related: event-based audit trail)
