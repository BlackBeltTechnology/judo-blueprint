---
id: "event-log-entity"
title: "Event Log Entity with Type Enum and Actor Reference"
score: 51.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - alba
---
## Description

An Event entity that records domain-level events as a chronological log. Each event has a type attribute (typed to an EventType enum defining specific event kinds), a message string for human-readable details, a createdAt timestamp, a reference to the entity the event is about (e.g., product 0..1 ASSOC), and a reference to the user who performed the action (performedBy 0..1 ASSOC). The entity is non-CRUD, created by backend operations when significant state changes occur.

Unlike the full AuditLog pattern (which includes entityType/entityId string fields and denormalized userName), this is a lightweight, relation-based approach where the event directly links to the domain entity and actor via associations. The EventType enum defines the vocabulary of possible events (e.g., PRODUCT_CREATED, PRODUCT_FINALIZED, PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED).

This pattern is suitable when events need to be displayed on a specific entity's timeline (via the entity's events relation) rather than in a platform-wide audit dashboard.

Some variants (e.g., kozut-eugyfel-client) denormalize the actor information into string attributes on the event (kezdemenyezoNev/initiatorName, celFelhasznaloNev/targetUserName) rather than using a relation to the User entity, and add a subsidiary Ertesites (Notification) entity composed by each event for user notification delivery.

Some variants use a **generalization-based event hierarchy** instead of a type enum: an abstract base event entity with concrete subtypes (e.g., Forward, Close, Comment, Create) that each extend the base entity via generalization. In this variant, the event type is determined by the concrete subtype rather than an enum attribute, and subtypes can carry additional type-specific attributes and relations. The base entity provides shared attributes (text, timestamp) and a relation to the initiating user. This approach is used with static email-sending operations on the abstract base entity.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
