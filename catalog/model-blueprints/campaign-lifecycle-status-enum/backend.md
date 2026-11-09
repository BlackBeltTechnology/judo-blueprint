## Overview

The CampaignStatus enum (ONGOING/FINISHED/DELETED) drives campaign lifecycle logic in both custom operations and scheduled jobs. Backend code uses the status to filter active campaigns, transition expired campaigns to FINISHED, and soft-delete campaigns by setting status to DELETED.

## Implementation Pattern

- A service layer class (e.g., `AggregatedCampaignService`) encapsulates all status transition logic, injected into both custom operations and scheduler jobs via OSGi `@Reference`
- **Soft-delete**: The `deleteAggregatedCampaign` operation performs a hard delete (cascading to history and tracked campaigns), but the `TrackedCampaignUpdateInput` allows setting status to DELETED for soft-delete at the tracked campaign level
- **Scheduled archival**: A `Runnable` OSGi component (e.g., `UpdateExpiredAggregatedCampaignStatus`) queries for ONGOING campaigns whose end date has passed, then sets their tracked campaigns' status to FINISHED
- **DAO filtering**: Uses `EnumerationFilter.equalTo(CampaignStatus.ONGOING)` combined with `DateFilter` to query only active, running campaigns
- **Daily reset**: Another scheduler resets daily spend attributes for ONGOING campaigns within their date range, using the same filter pattern
- Status is set on creation (defaults to ONGOING in model) and transitioned programmatically -- no explicit state machine, but status transitions are performed in service methods

## Examples

### indamedia-adtrack
- Key files: `common/impl/AggregatedCampaignServiceImpl.java`, `scheduler/UpdateExpiredAggregatedCampaignStatus.java`, `scheduler/ResetDailyAttributes.java`, `scheduler/FetchCampaignCost.java`
- Pattern: Service methods `dailyArchiveAggregatedCampaigns(date)` and `dailyResetAggregatedCampaigns(date)` filter by `CampaignStatus.ONGOING` and date ranges, then transition expired campaigns to FINISHED
- Notable: Three scheduler jobs operate on the status -- archival (ONGOING->FINISHED for expired), daily reset (recalculate spend for ONGOING), and fetch (sync external data for ONGOING). The `TrackedCampaign` inherits its initial status from its parent `AggregatedCampaign` on creation.
