---
id: entity-change-history-snapshot
title: "Entity Change History Snapshot"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---

## Description

A companion History entity that stores snapshots of a parent entity's key attributes each time significant changes occur. The history entity duplicates the parent's important fields (name, budget amounts, date ranges, etc.) and adds a `changed` timestamp recording when the snapshot was taken. The parent entity holds a 0..* association to its history records, creating a chronological audit trail of how the entity's attributes evolved over time. This is different from the simple History (whoDid/whatDid/whenDid) pattern in that it captures full attribute snapshots rather than textual descriptions of actions.

This pattern is useful for entities where configuration changes need to be tracked for reporting, billing, or compliance -- such as campaign budgets, pricing tiers, or contract terms.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%History%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper memberType } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{PARENT_ENTITY}}History",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}History", name: "{{SNAPSHOT_FIELD}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}History", name: "changed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}History", name: "{{PARENT_RELATION}}",
  target: "{{NAMESPACE}}::{{PARENT_ENTITY}}", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "history",
  target: "{{NAMESPACE}}::{{PARENT_ENTITY}}History", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### indamedia-adtrack
- **Entity**: `AdTrack::entities::AggregatedCampaignHistory` (non-CRUD)
  - Snapshot attributes: name (req), start (req), end (req), totalBudget (req), dailyBudget (req)
  - Timestamp: changed (req)
  - Relations: aggregatedCampaign (1..1 ASSOCIATION to AggregatedCampaign)
- **Parent entity**: `AdTrack::entities::AggregatedCampaign`
  - Has relation: history (0..* ASSOCIATION to AggregatedCampaignHistory)
  - When campaign budget/dates are modified, a history snapshot is created capturing the previous values
- **Transfer object**: `AdTrack::services::AggregatedCampaignHistoryTransfer` exposes all snapshot fields (name, start, end, totalBudget, dailyBudget, changed) as read-only
- The AggregatedCampaignTransfer has relation: aggregatedCampaignHistoryTransfer (0..*) for viewing history
