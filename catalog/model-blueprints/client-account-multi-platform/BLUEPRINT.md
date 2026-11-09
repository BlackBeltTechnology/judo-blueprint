---
id: "client-account-multi-platform"
title: "Client-Account-Campaign Multi-Platform Integration Cluster"
score: 63.0
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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
