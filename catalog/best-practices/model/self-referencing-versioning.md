---
id: "self-referencing-versioning"
title: "Self-Referencing Association for Entity Versioning"
domain: "model"
category: "relation"
score: 73.2
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
alternatives:
  - snapshot-versioning-pattern
---
## Description

An entity maintains a version chain via a self-referencing association (`previousVersion -> Self [0..1]`) combined with a `lastVersion` boolean flag. When a new version is created, the previous version's `lastVersion` flag is set to `false`, and the new version links back to it. This creates a linked-list versioning history within a single entity table.

## Structure

- Entity has `previousVersion -> Self [0..1]` association (self-referencing)
- Entity has `lastVersion: Boolean, required, default: true`
- On version creation:
  1. Clone the current entity
  2. Set `clone.previousVersion = original`
  3. Set `original.lastVersion = false`
  4. Set `clone.lastVersion = true`
- Queries filter by `lastVersion = true` to get current versions
- Full history can be traversed by following `previousVersion` links

## Examples

### RackInspect
`Offer` has `previousVersion -> Offer [0..1]` and `lastVersion (default: true)`. The `generateNewVersion` operation creates a new offer version linked to the previous one. Combined with status (DRAFT -> DONE) and cost tracking fields, this provides full offer history with pricing snapshots.

## Trade-offs

- Pros: Simple linked-list versioning, no separate version table needed, full history preserved, easy to query current version
- Cons: Previous versions remain in the same table, potentially large table for heavily versioned entities, traversal requires multiple hops
- Prefer when: An entity needs version history with the ability to compare or rollback

## Related Patterns

- [enum-state-machine](enum-state-machine.md)
- [snapshot-versioning-pattern](snapshot-versioning-pattern.md) (alternative: clone child data into separate version entities)
