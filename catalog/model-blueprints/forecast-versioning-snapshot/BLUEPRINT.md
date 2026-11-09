---
id: forecast-versioning-snapshot
title: Forecast Versioning with Monthly Snapshot Composition
description: "A versioning pattern for periodic financial forecasts where a parent entity keeps its current monthly forecasts and archived forecast versions, each version holding a frozen monthly breakdown."
aliases: []
keywords: [forecast, versioning, monthly, snapshot, composition]
tags: [domain:model, layer:model, project:itracker, status:single-project]
category: pattern
status: single-project
projects: [itracker]
evidence: ["itracker:unrecorded"]
alternatives: []
fragment: forecast-versioning-snapshot
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Keep the current forecast and a history of archived forecast versions on one parent entity. Each archive freezes the monthly breakdown and its totals, so later comparisons show what was projected at each point against the realized values.

### Versions are frozen copies

An archive copies the current monthly forecasts into a new version. The version's monthly rows are separate entities, so later edits to the current forecast do not change an archived version.

### Monthly granularity is kept per version

Each version keeps the month-by-month breakdown, not only flat totals. The version's totals are stored with it.

## Structure

The parent entity composes two collections: the current monthly forecasts (0..*) and the archived forecast versions (0..*). It has an integer version counter and an instance operation that performs the archive.

A forecast version has a required timestamp and required totals of projected and realized savings. It composes its own monthly rows (0..*).

The monthly row for the current forecast has a required month, a required projected saving, an optional realized saving and an optional date. The monthly row inside a version has the same fields, with a required date, and is never edited after the version is created.

## Constraints

- The monthly rows of a version are composed by the version, not by the parent. The parent reaches them only through the versions.
- The month and projected saving are required on the current monthly row. The timestamp and both totals are required on the version.
- The archive operation copies the current monthly rows into a new version, sets the totals and the timestamp, and increments the version counter.
- The archive operation is an instance operation on the parent. Its body is a custom implementation placeholder.

## Variations

- **Flat totals only.** Store only the version totals and skip the monthly rows. This is cheaper, but it cannot compare months across versions. See [[entity-change-history-snapshot]].
- **Per-entity history entries.** Keep one history row per change instead of one version per archive. See [[history-audit-trail-entity]].
- **Shared audit table.** Record archive events in a general log. See [[audit-log-entity]].

## When to use

- A periodic forecast is revised and the earlier states must stay comparable.
- The comparison needs the monthly breakdown, not just totals.
- Each archive is a deliberate user action, not an automatic change log.

## When to avoid

- Only the value history of one flat attribute is needed. Use a snapshot entity instead.
- Forecasts change continuously and an archive per change would produce too many versions.
- Versions must be edited after creation. The version rows are frozen by design.

## Related

- [[entity-change-history-snapshot]] — flat attribute snapshots of one entity, without monthly granularity
- [[history-audit-trail-entity]] — per-entity history rows instead of versioned composition
- [[audit-log-entity]] — a shared audit table for who changed what
