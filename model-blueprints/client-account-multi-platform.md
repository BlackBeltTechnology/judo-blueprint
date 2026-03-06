---
id: "client-account-multi-platform"
title: "Client-Account-Campaign Multi-Platform Integration Cluster"
score: 57.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---
## Description

A multi-tier entity cluster for managing external platform integrations on behalf of clients. The structure consists of:
- **Client** -- the customer/tenant entity with a name and isActive flag, owning multiple Accounts and AggregatedCampaigns.
- **Account** -- represents a connection to a specific external platform (typed by a Platform enum). Each account holds a credential (0..1) for API authentication and tracks campaigns discovered on that platform.
- **TrackedCampaign** -- a campaign from an external platform being monitored, with cost/spend tracking attributes and a link to fetched data snapshots.
- **AggregatedCampaign** -- a client-defined budget wrapper that groups multiple TrackedCampaigns across platforms, with budget management attributes (totalBudget, dailyBudget, remainingBudget, totalSpend).
- **Cost** -- daily cost records per tracked campaign with date and cumulative spend.
- **FetchedData** -- raw data snapshots from external API fetches with timestamps.
- **AvailableCampaign** -- campaigns discovered on a platform but not yet tracked, enabling campaign selection.

This pattern enables a single client to connect to multiple ad platforms (Google, Meta, etc.), discover available campaigns, select which to track, aggregate them into budget groups, and monitor spend against budgets over time.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Campaign%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Account%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Client",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Client", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Client", name: "isActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Account",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Account", name: "platform"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Account", name: "isActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Account", name: "client",
  target: "{{NAMESPACE}}::Client", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Account", name: "credential",
  target: "{{NAMESPACE}}::Credential", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Client", name: "accounts",
  target: "{{NAMESPACE}}::Account", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "TrackedCampaign",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "totalCost"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "todaySpend"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "lastUpdated"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "account",
  target: "{{NAMESPACE}}::Account", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::TrackedCampaign", name: "costs",
  target: "{{NAMESPACE}}::Cost", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "AggregatedCampaign",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "totalBudget"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "dailyBudget"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "totalSpend"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "remainingBudget"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "start"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "end"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "client",
  target: "{{NAMESPACE}}::Client", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::AggregatedCampaign", name: "trackedCampaigns",
  target: "{{NAMESPACE}}::TrackedCampaign", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Cost",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Cost", name: "dailyCost"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Cost", name: "spendToDate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Cost", name: "date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Cost", name: "trackedCampaign",
  target: "{{NAMESPACE}}::TrackedCampaign", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

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
