## Examples

### indamedia-adtrack
- **CampaignStatus enum**: `AdTrack::entities::CampaignStatus` -- ONGOING(1), FINISHED(2), DELETED(3)
- Used by: `AggregatedCampaign` entity (status attribute, default: `AdTrack::entities::CampaignStatus#ONGOING`)
- AggregatedCampaign has time-bounded attributes: start, end, remainingDays
- Transfer object `AggregatedCampaignTransfer` exposes status for display
- `AggregatedCampaignUpdateInput` includes status field for state transitions
- `TrackedCampaignUpdateInput` also has a status field
- `deleteAggregatedCampaign` operation soft-deletes by setting status to DELETED
