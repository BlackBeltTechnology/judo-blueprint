---
id: address-entity-with-location
title: Address Entity with Geolocation
description: "An Address entity that captures structured address fields (street, building, floor, door, postal code) along with a composed Location entity for geographic coordinates (latitude, longitude)."
aliases: []
keywords: [address, geolocation, location]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:mlszksz-platform", "project:rackinspect", "project:doors-model", "status:emerging"]
category: pattern
status: emerging
projects: [mlszksz-platform, rackinspect, doors-model]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "doors-model:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

An Address entity that captures structured address fields (street, building, floor, door, postal code) along with a composed Location entity for geographic coordinates (latitude, longitude). The address references a City and PostalCode via associations, and a Location via composition. A computed `fullAddress` attribute provides a concatenated display string. This pattern is common in platforms that need to store physical addresses with map-pinning capability. Variants include type-flags (isBilling, isHeadquarters, isPostal, isDelivery) with corresponding toggle operations, and a Country association instead of (or in addition to) City/PostalCode references. Simpler variants store city, country, street, and zipCode as direct string attributes rather than referencing lookup entities, with a derived `fullAddress` computed from the concatenation of these fields.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
