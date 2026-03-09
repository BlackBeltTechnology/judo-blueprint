---
id: "entity-change-history-snapshot"
title: "Entity Change History Snapshot"
score: 63.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---
## Description

A companion History entity that stores snapshots of a parent entity's key attributes each time significant changes occur. The history entity duplicates the parent's important fields (name, budget amounts, date ranges, etc.) and adds a `changed` timestamp recording when the snapshot was taken. The parent entity holds a 0..* association to its history records, creating a chronological audit trail of how the entity's attributes evolved over time. This is different from the simple History (whoDid/whatDid/whenDid) pattern in that it captures full attribute snapshots rather than textual descriptions of actions.

This pattern is useful for entities where configuration changes need to be tracked for reporting, billing, or compliance -- such as campaign budgets, pricing tiers, or contract terms.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
