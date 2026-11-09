## Examples

### indamedia-adtrack
**Entity cluster:**
- **Client**: `AdTrack::entities::Client` -- name (req), isActive (req, default: true); relations: accounts (0..*), aggregatedCampaigns (0..*)
- **Account**: `AdTrack::entities::Account` -- platform (req, Platform enum), isActive (req, default: true); relations: client (1..1), credential (0..1 to Credential), trackedCampaigns (0..*), availableCampaings (0..*)
- **TrackedCampaign**: `AdTrack::entities::TrackedCampaign` -- id (req), name (req), status (req), totalCost (req), todaySpend (req), lastUpdated (req); relations: account (0..1), costs (0..*), aggregatedCampaign (1..1), fetchedData (0..*), availableCampaign (0..1)
- **AggregatedCampaign**: `AdTrack::entities::AggregatedCampaign` -- name (req), totalBudget (req), totalSpend (req, default: 0), dailyBudget (req), todaySumSpend (req, default: 0), remainingBudget (req, default: 0), remainingAverageDailySpend (req, default: 0), start (req), end (req), remainingDays (req), status (req, default: ONGOING), lastUpdated (req); relations: client (1..1), trackedCampaigns (0..*), history (0..*)
- **Cost**: `AdTrack::entities::Cost` -- dailyCost (req), spendToDate (req), date (req); relation: trackedCampaign (1..1)
- **FetchedData**: `AdTrack::entities::FetchedData` -- totalCost (req), dailyCost (req), fetchedUpdated (req); relation: trackedCampaign (1..1)
- **AvailableCampaign**: `AdTrack::entities::AvailableCampaign` -- id (req), name (req), start (req), end; relations: account (1..1), trackedCampaign (0..1)

**Transfer objects:**
- `ClientPanel` -- access point with clients collection and createClient operation
- `ClientTransfer` -- mapped; operations: updateClient, newAccount, createAggregatedCampaign
- `AccountTransfer` -- mapped; operations: setGoogleCredential, testConnection, fetchAvailableCampaigns, updateAccount
- `TrackedCampaignTransfer` -- mapped; operations: updateCampaign, syncData, syncCostByDate, syncCosts, untrack
- `AggregatedCampaignTransfer` -- mapped; operations: createTrackedCampaign, updateAggregatedCampaign, syncData, deleteAggregatedCampaign
- Multiple unmapped input TOs: ClientInput, ClientUpdateInput, AccountInput, AccountUpdateInput, GoogleCredentialInput, AggregatedCampaignCreateInput, AggregatedCampaignUpdateInput, TrackedCampaignUpdateInput, CostInput
