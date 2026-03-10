---
id: "active-suspended-deactivated-status-enum"
title: "Active/Suspended/Deactivated Status Enum"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A three-state lifecycle enumeration with members ACTIVE, SUSPENDED, and DEACTIVATED. This pattern models entities that can be temporarily suspended (reversible) or permanently deactivated (typically irreversible). It is commonly applied to both User and Organization entities in platforms that require administrative account management. The corresponding transfer objects expose activate/suspend/deactivate operations to transition between states.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
