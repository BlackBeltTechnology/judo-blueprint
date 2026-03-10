## Overview

The AggregatedCampaignHistory entity is created as a snapshot whenever an AggregatedCampaign is created or updated. The service layer duplicates key attribute values (name, budget, dates) into a new history record with a timestamp, creating an audit trail of configuration changes over time.

## Implementation Pattern

- **Snapshot on create**: When the parent entity is first created, a history record is immediately created capturing the initial attribute values. This establishes a baseline in the audit trail
- **Snapshot on update**: When the parent entity is updated, a new history record is created with the updated values and the current timestamp before returning the updated entity. Both create and update follow the same `HistoryForCreate.builder().withName(...).withTotalBudget(...).withChanged(LocalDateTime.now()).withAggregatedCampaign(parent).build()` pattern
- **Cascade delete**: When the parent entity is deleted, all associated history records are deleted first by iterating over `parentDao.queryHistory(parent).selectList()` and deleting each one
- **DAO injection**: The history DAO (e.g., `AggregatedCampaignHistoryDao`) is injected via `@Reference` alongside the parent entity DAO in the same service class
- **No separate service**: History creation is embedded directly in the parent entity's service methods (create/update/delete) rather than extracted into a separate history service or interceptor

## Examples

### indamedia-adtrack
- Key files: `common/impl/AggregatedCampaignServiceImpl.java`
- Pattern: `createAggregatedCampaign()` and `updateAggregatedCampaign()` both call `aggregatedCampaignHistoryDao.create(AggregatedCampaignHistoryForCreate.builder()...build())` after the parent entity is persisted; `deleteAggregatedCampaign()` iterates and deletes all history records before deleting the parent
- Notable: History captures name, start, end, totalBudget, and dailyBudget -- all the fields a user can modify. The `changed` timestamp uses `LocalDateTime.now()`. The `adaptTo(AggregatedCampaign.class)` call converts the transfer object back to the entity type for the history record's relation.
