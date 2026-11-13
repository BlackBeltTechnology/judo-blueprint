---
id: capacity-reservation-cluster
title: Capacity Reservation Entity Cluster
description: "An entity cluster for capacity reservations at a shared site: a central reservation linked to reference data, parties, time slots, attachments and line items."
aliases: [freight-reservation-cluster, freight reservation cluster, logistics reservation entities, site booking cluster]
keywords: [capacity, reservation, cluster, slot, resource, reference data, booking, domain]
tags: [domain:model, layer:model, layer:backend, project:reserve-app, status:single-project]
category: pattern
status: single-project
projects: [reserve-app]
evidence: ["reserve-app:unrecorded"]
alternatives: []
fragment: capacity-reservation-cluster
diagram: { kinds: [entity, enum, transfer], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model one scheduled use of a shared site as a reservation with a time slot, a lifecycle state, transport and handling details, and the line items it covers. The reservation links to reference data (docks, slots, resource types and handling types) and to the parties involved (a requester, a recipient company, projects).

### One reservation, many references

The reservation holds the event data itself. Reusable facts such as a dock, a slot, a resource type or a product category are separate entities that many reservations point to. Changing a reference record does not copy it into each reservation.

### Items are a line-item list

Each line item is an entity with a quantity, a product category, a unit and a storage type. A soft-delete flag removes a line without losing the history of the reservation.

## Structure

The reservation entity has:

- a time slot (start and end timestamps)
- a lifecycle state, one member of the `ShipmentState` enumeration
- transport details (identifier, driver, phone)
- handling details (machine, driver, phone, a partial-delivery flag, the origin location)
- a technical identifier
- an optional dock, slot, project and time window
- a partner (optional) and a recipient company (required)
- a required resource type and handling type
- two optional suspension links to users, one for each party that can suspend the reservation
- composed attachments (0..*) and associated items (0..*)

The reference entities are docks, slots, resource types, handling types, time windows, product categories, units and storage types. Most share a name and an active flag.

The partner and the recipient company are organization entities. The partner has contact details and an external identifier, and links to its contacts and reservations. A project groups users, slots and reservations.

## Constraints

- The reservation's state is one member of the `ShipmentState` enumeration.
- The recipient company and the resource and handling types are required on the reservation.
- The attachments are composed by the reservation. They are removed with it.
- A line item links to one reservation. Its product category, unit and storage type are optional.
- Reference entities share the name and active attributes. The name is required.
- Suspension links are set only by the party that suspends. The other party's link stays empty.

## Variations

- **Items as embedded values.** Store line items inside the reservation instead of as separate entities. This is simpler, but the items cannot be shared or queried on their own.
- **Shared project scope only.** Drop the partner and keep only projects for access control. This fits deployments with a single party type.
- **State as a plain status.** Replace the nine-member lifecycle with a simple status. See [[shipment-state-enum]] for the full lifecycle and [[active-suspended-deactivated-status-enum]] for a simpler form.

## When to use

- Reservations are booked in advance into time slots at a shared site.
- Several parties (a requester, an approver, a site operator) act on the same reservation.
- Reference data such as docks and resource types is maintained separately from the bookings.

## When to avoid

- Bookings have no time slot or no reference data to link.
- The line items are not tracked one by one.
- Only one party uses the system and no access scoping by project is needed.

## Related

- [[shipment-state-enum]]: the lifecycle enumeration used by the reservation
- [[identity-account-organization-cluster]]: the users and organizations that the reservation links to
- [[audit-log-entity]]: recording who changed a reservation
