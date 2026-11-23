---
id: multi-platform-external-account-cluster
title: Multi-Platform External Account Cluster
description: A cluster where a parent organization owns external platform accounts and groups, and tracks activities found on several external platforms.
aliases: [client-account-multi-platform, client-account-campaign-multi-platform-integration-cluster, multi-platform campaign tracking, client account cluster]
keywords: [organization, account, activity, multi, platform, external, integration, cluster, totals, adapter]
tags: [domain:model, layer:model, layer:backend, project:indamedia-adtrack, status:single-project]
category: pattern
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: [external-api-adapter-provider-pattern]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let one organization connect several external platforms, follow the activities found on them, and group those activities under groups whose totals are watched over time. The platform differences stay behind one adapter, so the model does not change when a platform is added.

### The organization owns its accounts and groups

Accounts and groups belong to the organization and are removed with it. Activities are read through the accounts they were found on, so they are associations and not owned parts.

### Totals follow their activities

A group sums the spend of its tracked activities. The sum is recalculated in the service whenever a child changes.

## Structure

The Organization entity has a required name identifier and a required isActive flag. It owns Account and AggregatedActivity through compositions (0..*). Account has a required platform enumeration and a 0..* association to TrackedActivity. AggregatedActivity groups tracked activities through a 0..* association (reference only, no cascade). TrackedActivity has a required name and total cost.

## Constraints

- A composition has one owner and deletes its children with the parent. Accounts and groups belong to one organization. Associations carry no cascade.
- A bidirectional association cannot be a composition on either side. Keep the activity link one-way.
- The platform is a required enumeration. Adding a platform adds an enumeration value and an adapter, not a new entity.
- Group totals are derived from the tracked activities in the service, not entered by hand.

## Variations

- **Owned cost history.** Daily cost rows owned by each tracked activity give a time series for totals.
- **Discovered but not tracked.** A separate entity for activities found on a platform but not yet followed lets a user select which to track.
- **Credential entity.** A protected entity holds the platform credential for an account, so it is never shown on the account's form.
- **Single platform.** Drop the enumeration when only one platform is connected.

## When to use

- An organization connects several external reporting platforms.
- Activities from those platforms must be grouped under shared groups.
- Spend must be watched against a total over time.

## When to avoid

- Only one external source exists and no grouping is needed. A simple synchronised list is enough.
- The external platform is a plain rate or price feed without accounts. Use the external-adapter pattern alone.
- Activities must be owned by one account and never shared. Use a composition instead of an association.

## Related

- [[external-api-adapter-provider-pattern]]: the adapter and factory that hide each platform's API
- [[bank-account-entity]]: another organization-owned child set, shown with a composition
- [[ongoing-finished-deleted-status-enum]]: the status enumeration for time-bounded activities in the same domain
- [[contact-info-composition-cluster]]: a composed cluster of owned children under one parent
