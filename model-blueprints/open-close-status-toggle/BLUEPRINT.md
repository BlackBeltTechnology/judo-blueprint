---
id: "open-close-status-toggle"
title: "Open/Close Two-State Status Toggle with Operations"
score: 36.7
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
  - ams-model
  - skillmatrix-model
---
## Description

A two-state status enumeration with OPEN and CLOSED members, paired with `open` and `close` instance operations on the entity for toggling between states. The entity starts in the CLOSED state (default) and can be opened to allow participation/access, then closed again to stop it. In some variants, the entity defaults to OPEN instead of CLOSED. In some variants, the toggle uses a boolean `closed` attribute (default: false) instead of a status enum. This pattern models time-bounded or admin-controlled availability windows -- contests, registration periods, enrollment windows, campaigns, training plans, or any entity that needs to be explicitly activated and deactivated.

Unlike the DRAFT/DONE pattern (which is linear and terminal), the OPEN/CLOSED pattern is cyclical: the entity can be opened and closed repeatedly. Unlike the ACTIVE/SUSPENDED pattern (which implies user account management), OPEN/CLOSED is typically used for event or period entities where availability is the primary concern.

The transfer object exposes the open and close operations as MAPPED operations, and may add derived boolean attributes (e.g., `isClosed`, `isOpen`) to control UI visibility of the operations. Some variants add a `load` operation for bulk data import when the entity is in an empty state.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
