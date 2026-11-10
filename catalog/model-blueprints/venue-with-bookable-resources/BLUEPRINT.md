---
id: venue-with-bookable-resources
title: Venue with Bookable Resource Slots
description: "A two-level resource hierarchy for bookable venues: a venue entity containing individually bookable slot entities, with per-member venue access and a preferred slot."
aliases: [bookable slots, venue and slots, parking garage with slots]
keywords: [venue, bookable, resource, slot, reservation, access, preferred slot, exclusive]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:park-here", "status:single-project"]
category: pattern
status: single-project
projects: [park-here]
evidence: ["park-here:unrecorded"]
alternatives: [reservation-booking-entity]
fragment: venue-with-bookable-resources
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model a physical place that is split into individually bookable units, and control who may book where. A venue contains slots, slots hold reservations, and members are linked to the venues they may use.

### Venue, slot and reservation form three tiers

The venue carries the shared settings (name, an active flag, an optional notification template). Each slot carries the physical descriptors (floor, next to a wall, a plan image) and two flags: active and exclusive. A reservation belongs to exactly one slot.

## Structure

A Venue entity has a required name, a required active flag and an optional notification template (text). A Slot entity has a required label, floor (integer), nextToWall, active and exclusive flags and an optional floorPlan reference. Venue and Slot are linked by one bidirectional pair: Venue.slots (0..*) and Slot.venue, both association kind. Slot and Reservation are linked by a second bidirectional pair: Slot.reservations (0..*) and Reservation.slot. Reservation has required startsAt and endsAt timestamps. A Member entity has two unidirectional associations: accessedVenues (0..*) and preferredSlot (0..1).

## Constraints

### Slots exist only inside a venue

A slot has exactly one venue. Both ends of the venue-slot pair are associations; the platform validator rejects composition on a bidirectional pair, so the pair is not a composition (see [[bidirectional-relation]]).

### Exclusive and inactive slots must be filtered by the backend

The exclusive flag and the member's venue access only matter if the backend enforces them. Selection of a slot is a reference range, and range interceptors are the boundary that fires on it. Hiding a slot in the UI does not protect it (see [backend.md](backend.md)).

### Free-slot logic depends on the reservation model

Whether a slot is free for a day or a date range is a query over its reservations. The blueprint does not fix the reservation shape; see [[reservation-booking-entity]].

## Variations

- Replace the venue-level access list with a role or permission enumeration when access is by role, not by venue.
- Make the venue-slot pair unidirectional (Venue to Slot) when slots never need to find their venue; then composition is allowed if the slot has no other owner.
- Add a derived attribute on Slot for the display name instead of a stored copy of the venue name.

## When to use

- Physical spaces are divided into units that members book one at a time (parking, desks, rooms, lockers).
- Members are limited to a subset of venues, with an optional favourite slot.

## When to avoid

- The bookable thing has no containing venue; use the plain reservation entity.
- Resources are fungible and only a count matters (stock level), not a named slot.

## Related

- [[reservation-booking-entity]] — the booking entity that hangs off a slot
- [[bidirectional-relation]] — how the two-way pairs are declared
- [[interceptor-range-override]] — narrow the slot range for the current member
- [[derived-access-filtering]] — alternative: derive the visible venues in the model
