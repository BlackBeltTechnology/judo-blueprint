---
id: "address-entity-with-location"
title: "Address Entity with Geolocation"
score: 71.0
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - doors-model
---
## Description

An Address entity that captures structured address fields (street, building, floor, door, postal code) along with a composed Location entity for geographic coordinates (latitude, longitude). The address references a City and PostalCode via associations, and a Location via composition. A computed `fullAddress` attribute provides a concatenated display string. This pattern is common in platforms that need to store physical addresses with map-pinning capability. Variants include type-flags (isBilling, isHeadquarters, isPostal, isDelivery) with corresponding toggle operations, and a Country association instead of (or in addition to) City/PostalCode references. Simpler variants store city, country, street, and zipCode as direct string attributes rather than referencing lookup entities, with a derived `fullAddress` computed from the concatenation of these fields.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
