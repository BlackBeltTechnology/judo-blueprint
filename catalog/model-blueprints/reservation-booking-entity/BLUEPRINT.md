---
id: reservation-booking-entity
title: Reservation/Booking Entity with Time Slots and Status
description: A Reservation (or Booking) entity that models time-bounded resource reservations.
aliases: [booking entity, time slot reservation, appointment]
keywords: [reservation, booking, time, slots, status, quota, guest, reminder]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:park-here", "project:reserve-app", "status:emerging"]
category: pattern
status: emerging
projects: [park-here, reserve-app]
evidence: ["park-here:unrecorded", "reserve-app:unrecorded"]
alternatives: []
fragment: reservation-booking-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model a time-bounded claim on a resource: who reserved what, for which time slot, in which state. The entity carries the slot, a lifecycle status, a type that selects the booking rules, and the audit fields. Users create and change reservations through custom operations, not through generic edit forms.

### Status is a lifecycle, not a delete

A reservation is never removed in normal use. Cancelling ends it early (status expired, end time set to now). Deleting marks it deleted. Modifying marks the old one deleted and creates a new one. History stays readable.

### The type selects the rules

A type enumeration (normal, quick, guest, long) decides how a booking is created, which fields apply and which quota counts it. The rules sit in project code; the model only records the type.

## Structure

- `Reservation` with `date`, `startTime`, `endTime` (timestamps), `reservationStatus` (required enumeration: ACTIVE, DELETED, EXPIRED) and `reservationType` (required enumeration: NORMAL, QUICK, GUEST, LONG).
- Audit attributes: `created`, `createdBy`, `modified`, `modifiedBy`.
- Reminder flags: `hasToNotify`, `remindedBeforeStart`, `remindedBeforeEnd`. A scheduled job reads them to send reminders.
- Associations: `owner` (1..1 to the user entity), `resource` (1..1 to the reserved thing, for example a bookable slot) and optionally a vehicle or asset reference (0..1).
- `guest`: a composition (0..1) to a `Guest` part for bookings made for a third party. The guest is owned by the reservation.
- Denormalized display attributes (reserver name, e-mail, vehicle id) may be kept on the reservation so lists need no joins. They are project practice; see [[aggregated-stored-field]].
- The entity's createable, updateable and deleteable flags are off. Transfer objects and custom operations do the writing.

## Constraints

- The slot must be valid: not in the past, end after start, a minimum length. The model has no such rule; the creating operation validates it (project practice).
- Overlap detection per resource and per-user quotas per type are project logic, done with DAO query filters inside the service behind the operations. See [data access guide](../../agent-docs/backend/data-access-guide.md) and [[token-based-quota-limit]].
- Custom operations are not intercepted by the platform. Permission checks and validation belong in the operation or its service, not in an interceptor. See [interceptors](../../agent-docs/backend/interceptors.md).
- Status values persist as ordinals. Do not renumber them.
- Audit fields are set by the operations, using a UTC clock and the acting user.

## Variations

- **Capacity or logistics booking.** A longer lifecycle: not submitted, submitted, approved or rejected, arrived, finished, with delay states, and associations to gates, spots, loading types and vehicle types instead of one slot. See [[shipment-state-enum]]. Interceptors on the built-in create can wire the acting partner into the new reservation instead of a custom operation.
- **Long booking.** One reservation per working day in a date range, created together.
- **Copy-on-write modify.** Modify keeps the old row as deleted and adds a new row.
- **Guest booking.** The composed guest holds the third party's name and vehicle data.

## When to use

- Resources are booked for time slots and a booking has a lifecycle.
- Several booking types follow different rules and quotas.
- Users must see history and changes must be audited.

## When to avoid

- Bookings never change after creation and need no lifecycle. A plain dated record is enough.
- Booking is open-ended with no slot and no conflict check.
- The workflow is a multi-step approval. Use a state machine, see [[workflow-engine-state-machine-cluster]].

## Related

- [[shipment-state-enum]] — the richer status enumeration for logistics bookings
- [[token-based-quota-limit]] — limit how many active bookings a user may hold
- [[platform-email-template-service]] — e-mail on create, delete, modify and reminder
- [[audit-log-entity]] — a separate audit trail instead of audit attributes
- [[active-inactive-status-enum]] — a simpler two-state status
