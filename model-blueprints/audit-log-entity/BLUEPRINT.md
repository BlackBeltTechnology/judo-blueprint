---
id: "audit-log-entity"
title: "Audit Log Entity"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

An AuditLog entity that records system events with a timestamp, action type (typically an enum), the entity type and ID being acted upon, a details text field, and an optional association to the User who performed the action. Denormalized fields like userName and organizationName allow audit records to remain readable even after the referenced user or organization is modified. The entity is typically non-CRUD (createable=false, updateable=false, deleteable=false), created only through backend operations.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
