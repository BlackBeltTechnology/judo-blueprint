---
id: "state-based-transfer-partitioning"
title: "State-Based Transfer Object Partitioning"
domain: "model"
category: "transfer"
score: 37.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - viterra_demo
---
## Description

The same entity is exposed through multiple transfer objects where each transfer is filtered by the entity's lifecycle state. Instead of a single transfer showing all records with the status as a column, the access layer creates separate entry points per state group, each targeting a different transfer object with appropriate CRUD permissions. This enforces that editable and read-only views are structurally distinct.

## Structure

- One entity with a status enum attribute
- Multiple transfer objects mapping to the same entity, each for a different state group
- Access points use derived getter expressions with status filters:
  - `Entity!filter(e | e.status == Status#OPEN and ...)` -> editable transfer
  - `Entity!filter(e | e.status != Status#OPEN and ...)` -> read-only transfer
- Editable transfer allows CRUD on composed children
- Read-only transfer disables all CRUD
- Different derived attributes and operations per transfer (e.g., submit on open, no operations on closed)

## Examples

### Viterra Demo
`Report` entity has `ReportStatus` (PENDING, SUBMITTED, REVIEW, ACCEPTED). Partner actor has two partitioned access points: `openReports` filters `status == PENDING` and targets `PartnerOpenReportTransfer` (stocks updateable, submit operation available), while `closedReports` filters `status != PENDING` and targets `PartnerClosedReportTransfer` (read-only, no operations). The submit operation returns `PartnerClosedReportTransfer`, moving the report from the open to the closed partition.

## Trade-offs

- Pros: Clear separation of editable vs read-only states, prevents accidental edits on finalized records, distinct UI pages per state
- Cons: More transfer objects to maintain, state transitions require returning the correct transfer type for navigation
- Prefer when: An entity has a clear mutable/immutable lifecycle boundary where different states need fundamentally different UI experiences

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [enum-state-machine](enum-state-machine.md)
- [derived-access-filtering](derived-access-filtering.md)
- [operation-return-type-navigation](operation-return-type-navigation.md)
