---
id: user-holiday-absence-tracking
title: User Holiday and Absence Tracking
description: A Holiday entity composed by a User that stores the date ranges when the user is unavailable, with a check for overlapping ranges and a calendar that can override public days.
aliases: [absence tracking, leave tracking]
keywords: [user, holiday, absence, composition, date range, calendar, overlap]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:park-here, status:single-project]
category: pattern
status: single-project
projects: [park-here]
evidence: ["park-here:unrecorded"]
alternatives: [contact-info-composition-cluster]
related: [contact-info-composition-cluster, reservation-booking-entity]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Record when a user is not available, as date ranges owned by that user. A booking flow can then avoid those dates, and an administrator can see them in one place.

### A holiday belongs to its user

The user composes its holidays. A holiday has no meaning without its user, so deleting the user deletes the holidays. The holiday points back to its owner through a derived relation that navigates up the composition (`self!container(...)`), so the owner is found without a stored foreign key. See [[container-back-reference]].

### Overlaps are checked before a holiday is saved

A new range must not overlap an existing holiday of the same user. The check runs in the operation that creates the holiday, because interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

## Structure

The Holiday entity has a required start date and a required end date. The User entity composes zero or more holidays. A derived 0..1 relation `owner` on Holiday returns the owning User through the container navigation. The DayType enumeration (Work, Off) marks calendar overrides for single days, so a public holiday can be a working day or a weekday can be an off day. The Reservation entity stands next to the holiday because creating a holiday can affect existing bookings in the same range.

## Constraints

- The start date must not be after the end date.
- A holiday must not overlap another holiday of the same user.
- A holiday must not start in the past (the example enforces this in the creation logic).
- Deleting a user deletes its holidays, because the relation is a composition.
- Creating a holiday that overlaps reservations changes those reservations. The example cancels them. This side effect must be explicit in the operation and must be shown to the user before it is applied.
- Interceptors do not run for custom operations, so a platform write guard cannot protect them. The overlap check and the reservation change must be in the operation.

## Variations

- **Show affected reservations first.** A query returns the reservations inside the proposed range, so the user sees the effect before confirming. Use this when a holiday can cancel bookings.
- **Calendar overrides.** Single-day overrides (Work or Off) on top of a public calendar let an administrator correct the calendar. The example computes public holidays and then applies these overrides.
- **Holiday without reservation impact.** If the range cannot affect bookings, drop the reservation link and keep only the overlap check.

## When to use

- Users must mark the periods when they are unavailable, and other flows must respect those periods.
- Holidays belong to one user and disappear with the user.
- Booking or scheduling flows need a list of unavailable dates per user.

## When to avoid

- The unavailable period is shared by a team or a resource, not one user. Put it on the team or resource instead.
- The information is only a single flag, not a date range. A boolean on the user is enough.
- Periods must be shared by many owners with independent lifecycles. Use an association, not a composition.

## Related

- [[contact-info-composition-cluster]] — another user-owned composition, with the same ownership rules
- [[container-back-reference]] — the derived owner relation on the holiday
- [[reservation-booking-entity]] — the bookings that a holiday can affect
