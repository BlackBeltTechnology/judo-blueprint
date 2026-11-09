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
