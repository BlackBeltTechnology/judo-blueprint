---
id: freight-reservation-cluster
title: Freight Reservation Entity Cluster (Logistics Domain)
description: "An entity cluster for freight and logistics reservations at a facility: a central reservation linked to reference data, parties, resource slots, attachments and cargo items."
aliases: []
keywords: [freight, reservation, cluster, logistics, domain]
tags: [domain:model, layer:model, layer:backend, project:reserve-app, status:single-project]
category: pattern
status: single-project
projects: [reserve-app]
evidence: ["reserve-app:unrecorded"]
alternatives: []
fragment: freight-reservation-cluster
diagram: { kinds: [entity, enum, transfer], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Model one delivery event at a facility as a reservation with a time slot, a lifecycle state, vehicle and loading details, and the cargo it carries. The reservation links to reference data (gates, spots, vehicle and loading types) and to the parties involved (partner, recipient company, projects).

### One reservation, many references

The reservation holds the event data itself. Reusable facts such as a gate, a spot, a vehicle type or a product category are separate entities that many reservations point to. Changing a reference record does not copy it into each reservation.

### Cargo is a line-item list

Each cargo line is an item entity with a quantity, a product category, a unit and a storage type. A soft-delete flag removes a line without losing the history of the reservation.

## Structure

The reservation entity has:

- a time slot (start and end timestamps)
- a lifecycle state, one member of the freight state enumeration
- vehicle details (number plate, driver, phone)
- loading details (machine, driver, phone, a partial-delivery flag, the origin location)
- a technical identifier
- an optional gate, spot, project and loading time
- a partner (optional) and a recipient company (required)
- a required vehicle type and loading type
- two optional suspension links to users, one for each party that can suspend the reservation
- composed attachments (0..*) and associated items (0..*)

The reference entities are gates, spots, vehicle types, loading types, loading times, product categories, units and storage types. Most share a name and an active flag.

The partner and the recipient company are organization entities. The partner has contact details and an external identifier, and links to its contacts and reservations. A project groups users, spots and reservations.

## Constraints

- The reservation's state is one member of the freight state enumeration.
- The recipient company and the vehicle and loading types are required on the reservation.
- The attachments are composed by the reservation. They are removed with it.
- A cargo item links to one reservation. Its product category, unit and storage type are optional.
- Reference entities share the name and active attributes. The name is required.
- Suspension links are set only by the party that suspends. The other party's link stays empty.

## Variations

- **Items as embedded values.** Store cargo lines inside the reservation instead of as separate entities. This is simpler, but the items cannot be shared or queried on their own.
- **Shared project scope only.** Drop the partner and keep only projects for access control. This fits deployments with a single party type.
- **Freight state as a plain status.** Replace the nine-member lifecycle with a simple status. See [[freight-logistics-state-enum]] for the full lifecycle and [[active-suspended-deactivated-status-enum]] for a simpler form.

## When to use

- Deliveries are booked in advance into time slots at a shared facility.
- Several parties (a partner, a logistician, a doorman) act on the same reservation.
- Reference data such as gates and vehicle types is maintained separately from the bookings.

## When to avoid

- Bookings have no time slot or no reference data to link.
- The cargo is not tracked item by item.
- Only one party uses the system and no access scoping by project is needed.

## Related

- [[freight-logistics-state-enum]] — the lifecycle enumeration used by the reservation
- [[identity-account-organization-cluster]] — the users and organizations that the reservation links to
- [[audit-log-entity]] — recording who changed a reservation
