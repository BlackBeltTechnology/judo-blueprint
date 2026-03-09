---
id: "toggle-active-operation"
title: "Toggle Active Boolean Operation Pattern"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A pervasive pattern where entities carry an `active` boolean attribute (default: true) and a `toggleActive` instance operation with custom implementation that flips the flag. This provides soft-enable/disable semantics without deletion. The toggle operation is an INSTANCE-type custom operation. Many entities in the same model apply this identical pattern, making it a cross-cutting concern. Some entities extend the pattern with additional toggle operations (togglePrimary, toggleBilling, toggleHeadquarters, togglePostal, toggleDelivery) for multi-flag management.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
