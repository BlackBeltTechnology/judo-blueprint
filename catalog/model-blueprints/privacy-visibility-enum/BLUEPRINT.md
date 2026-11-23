---
id: privacy-visibility-enum
title: Privacy Visibility Enum (Expanding Visibility Levels)
description: "A closed enumeration of four expanding visibility scopes (peers, team, unit, everyone) that user-data fields use to state who may see them."
aliases: [visibility level enum, privacy scope enum]
keywords: [privacy, visibility, enum, ordinal, scope, user data]
tags: [domain:model, layer:model, project:sanctuary-backend, status:single-project]
category: pattern
status: single-project
projects: [sanctuary-backend]
evidence: ["sanctuary-backend:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let a user choose, field by field, how widely a piece of personal data is visible. The choices form an ordered scale, so a viewer's relationship to the user can be compared against the field's level.

### The scale is ordered by ordinal

The four members widen in order. Enumerations travel and persist as integer ordinals, so the order of the members is the order of the scale. A rule such as "visible when the field's level is at least the viewer's level" is project logic; compare the ordinals in code, and check in your platform version that a model expression can compare enumeration values before relying on it in a query.

## Structure

One enumeration, `PrivacyVisibility`, with four members: PUBLIC_FOR_PEERS (ordinal 1), PUBLIC_FOR_TEAM (ordinal 2), PUBLIC_FOR_UNIT (ordinal 3) and PUBLIC_FOR_EVERYONE (ordinal 4). Each privacy-controlled attribute of a settings entity is typed to this enumeration. The settings entity is composed by the user entity through an optional one-to-one composition, so a user has at most one settings record.

## Constraints

- The enumeration is closed. A new scope is a model change, not a data change.
- Ordinals must be unique and within 0 to 9999 (the model build rejects others). They are persisted and must stay ordered from narrowest to widest. Do not renumber members.
- The generated DAO method `query<Attribute>()` on an enumeration attribute can fail with a ClassCastException (the runtime delivers the ordinal); read the value through the transfer object instead.
- Every privacy-controlled attribute uses the enumeration type, so no free-text visibility value can be stored.

## Variations

- **Per-field enumeration.** Use one enumeration for all fields (this entry). Split only when two fields need different scales.
- **Scope as an entity.** When scopes need their own attributes, such as a label or a rule, model them as entities. See [[category-enum-pattern]].
- **Settings as an entity with one row per field.** Use this when fields are added often. The enumeration stays the same.

## When to use

- Users control who sees personal fields such as contact details or badges.
- The levels are a small, stable, ordered set.
- Queries compare visibility levels rather than match exact labels.

## When to avoid

- The scopes are user-defined or change often. Use an entity.
- The levels are unordered categories. Use a plain enumeration such as [[active-inactive-status-enum]] or a category enumeration.
- A field needs an exception list of named viewers. An enumeration cannot express that.

## Related

- [[category-enum-pattern]] — choosing between an enumeration and an entity for a fixed set of values
- [[environment-enum]] — another closed enumeration with persisted ordinals
- [[active-inactive-status-enum]] — a two-value status enumeration
