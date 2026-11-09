---
id: "toggle-active-operation"
title: "Toggle Active Boolean Operation Pattern"
score: 75.2
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-09"
projects:
  - rackinspect
  - mlszksz-platform
---
## Description

A pervasive pattern where entities carry an `active` or `isActive` boolean attribute (default: true) and a toggle operation (named `toggleActive`, `activateToggle`, or similar) that flips the flag. This provides soft-enable/disable semantics without deletion. The toggle operation is an INSTANCE-type operation. Many entities in the same model apply this identical pattern, making it a cross-cutting concern. Some entities extend the pattern with additional toggle operations (togglePrimary, toggleBilling, toggleHeadquarters, togglePostal, toggleDelivery) for multi-flag management. In some projects, the toggle operation lives on the transfer object rather than the entity, and may be named `activateToggle` instead of `toggleActive`.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
