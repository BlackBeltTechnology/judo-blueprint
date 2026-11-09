---
id: client-account-multi-platform
title: Client-Account-Campaign Multi-Platform Integration Cluster
description: A cluster where a client owns platform accounts and budget groups, and tracks campaigns found on several ad platforms.
aliases: [multi-platform campaign tracking, client account cluster]
keywords: [client, account, campaign, multi, platform, integration, cluster, budget, adapter]
tags: [domain:model, layer:model, layer:backend, project:indamedia-adtrack, status:single-project]
category: pattern
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: [external-api-adapter-provider-pattern]
fragment: client-account-multi-platform
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Let one client connect several external ad platforms, follow the campaigns found on them, and group those campaigns under budgets that are watched over time. The platform differences stay behind one adapter, so the model does not change when a platform is added.

### The client owns its accounts and budgets

Accounts and budget groups belong to the client and are removed with it. Campaigns are read through the accounts they were found on, so they are associations and not owned parts.

### Budgets follow their campaigns

A budget group sums the spend of its tracked campaigns. The sum is recalculated in the service whenever a child changes.

## Structure

The Client entity has a required name identifier and a required isActive flag. It owns Account and AggregatedCampaign through compositions (0..*). Account has a required platform enumeration and a 0..* association to TrackedCampaign. AggregatedCampaign groups tracked campaigns through a 0..* aggregation. TrackedCampaign has a required name and total cost.

## Constraints

- A composition has one owner. Accounts and budget groups belong to one client.
- A bidirectional association cannot be a composition on either side. Keep the campaign link one-way.
- The platform is a required enumeration. Adding a platform adds an enumeration value and an adapter, not a new entity.
- Budget totals are derived from the tracked campaigns in the service, not entered by hand.

## Variations

- **Owned cost history.** Daily cost rows owned by each tracked campaign give a time series for budgets.
- **Discovered but not tracked.** A separate entity for campaigns found on a platform but not yet followed lets a user select which to track.
- **Credential entity.** A protected entity holds the platform credential for an account, so it is never shown on the account's form.
- **Single platform.** Drop the enumeration when only one platform is connected.

## When to use

- A client connects several external advertising or reporting platforms.
- Campaigns from those platforms must be grouped under shared budgets.
- Spend must be watched against budget over time.

## When to avoid

- Only one external source exists and no grouping is needed. A simple synchronised list is enough.
- The external platform is a plain rate or price feed without accounts. Use the external-adapter pattern alone.
- Campaigns must be owned by one account and never shared. Use a composition instead of an association.

## Related

- [[external-api-adapter-provider-pattern]] — the adapter and factory that hide each platform's API
- [[bank-account-entity]] — another client-owned child set, shown with a composition
- [[campaign-lifecycle-status-enum]] — the status enumeration for time-bounded campaigns in the same domain
- [[contact-info-composition-cluster]] — a composed cluster of owned children under one parent
