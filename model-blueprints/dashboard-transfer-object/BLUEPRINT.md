---
id: "dashboard-transfer-object"
title: "Dashboard Transfer Object with Statistics"
score: 62.7
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - InterfaceRegister
---
## Description

A dashboard transfer object that serves as the main access point for an actor, aggregating multiple entity collections via relations and providing summary attributes or operations for common actions. The dashboard TO maps to a user entity and provides a personalized landing page view. In full implementations, it aggregates multiple entity collections via relations and provides a statistics sub-object with computed counts. In minimal implementations, it provides a derived welcome text and operations for creating key domain entities. The dashboard is accessed as a 0..1 access point on the actor type.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
