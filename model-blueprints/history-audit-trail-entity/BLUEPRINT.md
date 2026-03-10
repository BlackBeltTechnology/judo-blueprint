---
id: "history-audit-trail-entity"
title: "History Audit Trail Entity (Who/What/When)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A minimal History entity that records an audit trail of actions with three attributes: whoDid (the user who performed the action), whatDid (description of the action), and whenDid (timestamp of the action). The entity is non-CRUD and composed by a parent entity (typically a Task or work item) via a history (0..*) composition relation. Unlike the full AuditLog pattern which uses enums and entity references, this is a lightweight, denormalized approach where the actor and action are stored as plain text strings. This is suitable when a simple chronological log of human-readable events is sufficient.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
