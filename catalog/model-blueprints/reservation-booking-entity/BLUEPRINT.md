---
id: "reservation-booking-entity"
title: "Reservation/Booking Entity with Time Slots and Status"
score: 62.2
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
  - reserve-app
---
## Description

A Reservation (or Booking) entity that models time-bounded resource reservations. It captures a date, startTime, endTime for the time slot, a reservationStatus enum (ACTIVE/DELETED/EXPIRED) for lifecycle management, and a reservationType enum to distinguish different booking categories (e.g., NORMAL, QUICK, GUEST, LONG). The entity carries audit trail attributes (created, createdBy, modified, modifiedBy) for tracking who made and last changed the booking. It associates to an owner User (1..1), the reserved resource (e.g., ParkingSlot 1..1), and optionally to a guest entity (0..1 COMPOSITION) for third-party bookings and a vehicle/asset reference (0..1). Denormalized display fields (reserverName, reserverEmail, reserverCarId) enable quick display without joining. Reminder tracking fields (hasToNotify, reminderTimer, remindedBeforeStart, remindedBeforeEnd) support notification workflows. The entity is typically non-CRUD, managed entirely through custom operations on transfer objects.

Some variants model freight/logistics reservations with richer status lifecycles (NOT_SUBMITTED -> SUBMITTED -> APPROVED/REJECTED -> ARRIVED -> FINISHED with delay states) and associations to logistics resources (gates, spots, loading types, vehicle types) instead of simple parking slots.

The ReservationStatus enum follows a lifecycle from active through completion or cancellation. The ReservationType or state enum categorizes bookings by their nature, privilege level, or workflow stage.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
