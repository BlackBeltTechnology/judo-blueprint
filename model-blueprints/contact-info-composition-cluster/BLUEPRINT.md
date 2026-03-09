---
id: "contact-info-composition-cluster"
title: "Contact Info Composition Cluster (Email, Phone, Address)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A set of small, composable contact information entities that are owned by a parent entity through composition: EmailAddress (email, name, active), PhoneNumber (phone, name, active, isFax), and Address (streetName, city, postalCode, building, floor, door, fullAddress, active). Each contact entity carries an `active` boolean (default: true) and toggle operations: `toggleActive` (enable/disable) and `togglePrimary` (set as primary). The parent entity (Partner, CompanyData, or User) composes multiple instances of each (0..*) and maintains a separate "primary" association (0..1) pointing to the preferred instance. A derived `container` relation (0..1) provides back-navigation to the parent. This pattern allows entities to have multiple addresses, emails, and phones with one designated as primary.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
