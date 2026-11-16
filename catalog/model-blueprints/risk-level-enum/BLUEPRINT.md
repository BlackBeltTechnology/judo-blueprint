---
id: risk-level-enum
title: Risk Level Enum (LOW/MEDIUM/HIGH)
description: "A three-level risk classification enumeration with members LOW, MEDIUM and HIGH, used as an attribute for triage and filtering."
aliases: [risk rating enum, severity scale]
keywords: [risk, level, enum, low, medium, high, triage, ordinal]
tags: ["domain:model", "layer:model", "project:itracker", "status:single-project"]
category: pattern
status: single-project
projects: [itracker]
evidence: ["itracker:unrecorded"]
alternatives: []
fragment: risk-level-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Classify an item by risk exposure with a small, closed, ordered scale: low, medium or high. The scale is deliberately coarse. Three levels are enough for quick triage, filtering and dashboard grouping without a debate over fine gradations.

## Structure

One enumeration, `RiskLevel`, with three members: LOW (ordinal 1), MEDIUM (ordinal 2) and HIGH (ordinal 3). A domain entity (for example an initiative or an issue) carries an attribute of this enumeration type. The attribute has no default value, so the user sets it explicitly when creating the item.

## Constraints

- The enumeration is closed. Adding a level is a model change, not a data change.
- Member ordinals are unique and must stay within the platform range for enumerations (0 to 9999, see [JSL language notes](../../agent-docs/model/jsl-language-notes.md)). They are the persisted form and they travel as integers on the wire, so existing members are never renumbered or reordered. See [platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md).
- Ordinals 1, 2, 3 follow the severity order. Sorting by the attribute therefore sorts by risk, which is a project convention and not something the platform guarantees for display labels.
- Leave the attribute without a default when "not yet assessed" must be distinguishable from a real level. Make it required only when every item must be rated at creation.

## Variations

- **Add a level (for example CRITICAL).** Add one member with the next free ordinal. Existing rows keep their values.
- **Risk as a reference entity.** When levels need their own attributes (colour, SLA, owner), model them as an entity with a relation. See [[category-enum-pattern]] for the choice.
- **Combined classification.** Use the enumeration beside other classification enumerations on the same entity (for example saving type and action type in the source project). Each is independent.

## When to use

- Items need a simple, stable risk or severity rating.
- The rating is used to filter, group or prioritize in lists and dashboards.
- The vocabulary changes rarely and is part of the domain language.

## When to avoid

- The levels are user-maintained or change often. Use an entity with a relation.
- Risk needs a numeric score, weighting or history. Use numeric attributes or a separate assessment entity.
- A finer or domain-specific scale is required.

## Related

- [[category-enum-pattern]] — choosing between an enumeration and an entity for a fixed set of values
- [[environment-enum]] — another small closed enumeration with persisted ordinals
- [[active-inactive-status-enum]] — a two-member status enumeration
