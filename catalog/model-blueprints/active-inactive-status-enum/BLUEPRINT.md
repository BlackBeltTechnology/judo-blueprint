---
id: active-inactive-status-enum
title: Active/Inactive Two-State Status Enum
description: A minimal two-state status enumeration with ACTIVE and INACTIVE (or semantically equivalent) members.
aliases: []
keywords: [active, inactive, two, state, status, enum]
tags: ["domain:model", "layer:model", "project:viterra_demo", "project:sanctuary-backend", "status:emerging"]
category: pattern
status: emerging
projects: [viterra_demo, sanctuary-backend]
evidence: ["viterra_demo:unrecorded", "sanctuary-backend:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A minimal two-state status enumeration with ACTIVE and INACTIVE (or semantically equivalent) members. This is the simplest form of a status lifecycle enum, representing entities that are either currently in use (ACTIVE) or no longer in use (INACTIVE/ARCHIVED). Unlike the three-state ACTIVE/SUSPENDED/DEACTIVATED pattern, this enum has no intermediate state -- entities are either on or off. Unlike a simple boolean `active` flag, using an enum provides extensibility (additional states can be added later) and clearer semantics in queries and UI.

Variants include:
- **ACTIVE/INACTIVE** -- the classic binary toggle, used when entities are simply enabled or disabled
- **active/archived** -- a softer variant where the second state implies the entity is preserved for historical reference but no longer actively used
- **AKTIV/LEZART** -- a Hungarian-language variant meaning ACTIVE/CLOSED, used for ticket/case lifecycle where a case is either open for processing or closed after resolution

This enum is typically used as a `status` attribute on entities that need lifecycle management, such as users, reference data entries, configuration items, or service tickets.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
