---
id: "venue-with-bookable-resources"
title: "Venue with Bookable Resource Slots"
score: 61.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
---
## Description

A two-level resource hierarchy for bookable venues: a Venue/Facility entity (e.g., ParkingGarage) containing multiple bookable Resource/Slot entities (e.g., ParkingSlot). The venue has a name, isActive flag, and optional email template for notifications. It maintains associations to authorized users (accessedUsers) and users with special access (usersWithIdCard). Each resource slot has an identifier (id), physical descriptors (floor, nextToWall, floorPlan), an isActive flag, an isExclusive flag, and a denormalized venue name. The slot links back to its venue (1..1 ASSOC) and has a collection of reservations (0..*). Users have a preferredSlot (0..1) association for default booking, and an accessedVenues (0..*) association listing which venues they can book in. This pattern models any domain where physical spaces are divided into individually bookable units with access control.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
