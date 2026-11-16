---
id: plan-versioning-snapshot
title: Plan Versioning with Period Snapshot Composition
description: "A versioning pattern for periodic plans where a parent entity keeps its current period plans and archived plan versions, each version holding a frozen period breakdown."
aliases: [forecast-versioning-snapshot, forecast versioning, monthly forecast snapshot, period plan versioning, versioned plan archive]
keywords: [plan, versioning, period, snapshot, composition, archive, projection]
tags: [domain:model, layer:model, project:itracker, status:single-project]
category: pattern
status: single-project
projects: [itracker]
evidence: ["itracker:unrecorded"]
alternatives: []
fragment: plan-versioning-snapshot
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep the current plan and a history of archived plan versions on one parent entity. Each archive freezes the period breakdown and its totals, so later comparisons show what was projected at each point against the realized values.

### Versions are frozen copies

An archive copies the current period plans into a new version. The version's period rows are separate entities, so later edits to the current plan do not change an archived version.

### Period granularity is kept per version

Each version keeps the period-by-period breakdown, not only flat totals. The version's totals are stored with it.

## Structure

The parent entity composes two collections: the current period plans (0..*) and the archived plan versions (0..*). It has an integer version counter and an instance operation that performs the archive.

A plan version has a required timestamp and required totals of projected and realized values. It composes its own period rows (0..*).

The period row for the current plan has a required period, a required projected value, an optional realized value and an optional date. The period row inside a version has the same fields, with a required date, and is never edited after the version is created.

## Constraints

- Every relation is a composition, so deleting the parent deletes its current rows, its versions and their rows.
- The period rows of a version are composed by the version, not by the parent. The parent reaches them only through the versions.
- The period and projected value are required on the current period row. The timestamp and both totals are required on the version.
- The archive operation copies the current period rows into a new version, sets the totals and the timestamp, and increments the version counter.
- The archive operation is an instance operation on the parent with a custom implementation. Interceptors run only for the platform's built-in operations, so the operation does the copy itself, in one transaction: a failure leaves no half-written version.

## Variations

- **Flat totals only.** Store only the version totals and skip the period rows. This is cheaper, but it cannot compare periods across versions. See [[entity-change-history-snapshot]].
- **Per-entity history entries.** Keep one history row per change instead of one version per archive. See [[history-audit-trail-entity]].
- **Shared audit table.** Record archive events in a general log. See [[audit-log-entity]].

## When to use

- A periodic plan is revised and the earlier states must stay comparable.
- The comparison needs the period breakdown, not just totals.
- Each archive is a deliberate user action, not an automatic change log.

## When to avoid

- Only the value history of one flat attribute is needed. Use a snapshot entity instead.
- Plans change continuously and an archive per change would produce too many versions.
- Versions must be edited after creation. The version rows are frozen by design.

## Related

- [[entity-change-history-snapshot]]: flat attribute snapshots of one entity, without period granularity
- [[history-audit-trail-entity]]: per-entity history rows instead of versioned composition
- [[audit-log-entity]]: a shared audit table for who changed what
