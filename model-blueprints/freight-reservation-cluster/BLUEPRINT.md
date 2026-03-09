---
id: "freight-reservation-cluster"
title: "Freight Reservation Entity Cluster (Logistics Domain)"
score: 45.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - reserve-app
---
## Description

A domain-specific entity cluster for managing freight/logistics reservations at a warehouse or facility. The central FreightReservation entity connects a rich web of reference data entities to model a delivery event:

- **FreightReservation** -- the core booking with time slot (start, end), state lifecycle, vehicle details (numberPlate, driver, phone), loading details (machine, driver, phone), origin (fromLocation), partial delivery flag, and a technical identifier. It composes attachments (photos) and associates to all the reference entities below.
- **Gate** -- physical loading dock/gate at the facility
- **Spot** -- parking/staging area within the facility
- **Project** -- organizational grouping for reservations; scoped to users and spots
- **Partner** -- external delivery company (with name, address, contact, phone, externalIdentifier)
- **Company** -- internal receiving company
- **VehicleType** -- classification of vehicle (truck, van, etc.)
- **LoadingType** -- how goods are loaded/unloaded
- **LoadingTime** -- estimated duration for loading/unloading (name + minutes)
- **Item** -- line items on the reservation with quantity, product category, unit, and storage type
- **ProductCategory**, **Unit**, **StorageType** -- classification entities for items

The Item entity links a reservation to its cargo details: each item references a ProductCategory, Unit, and StorageType, enabling tracking of what is being delivered, in what quantities, using what measurement, and how it should be stored. A `deleted` flag on Item supports soft-removal of line items.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
