---
id: "reference-data-lookup-entity"
title: "Reference Data Lookup Entity (Name + Active/Enabled)"
score: 50.0
usage_count: 9
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - reserve-app
  - alba
  - trivia
  - itracker
  - viterra_demo
  - InterfaceRegister
  - doors-model
  - ams-model
  - skillmatrix-model
---
## Description

A minimal reference data entity with a `name` (required) attribute and optionally an `active` or `isEnabled` boolean attribute (default: true) for soft-enable/disable. These entities serve as lookup/classification tables referenced by core domain entities via association. They are non-CRUD (managed by admin operations or data seeding), and each represents a configurable option category: vehicle types, loading types, storage types, units of measurement, product categories, gates, spots, audiences, curricula, result types, question categories, regions, commodities, brands, vendors, roles, banks, legal groups, financial categories, applications (IT systems), counties, organizational unit types, job roles, countries, languages, jobs, tags, skill levels, and similar. The pattern is characterized by its extreme simplicity: just a name for display and optionally an active/enabled flag for filtering. Some variants add a single extra attribute (e.g., LoadingTime adds `minutes`, Institution adds `address` and `website`, Commodity adds `hun` for a localized name, BusinessDataType adds `businessDomain` as an enum classifier, Vendor adds `id` and `address`, Bank adds `giroCode` as an identifier, SkillLevel adds `score` as a numeric ranking). The simplest variants have only a `name` attribute with no active/enabled flag. Some variants use `identifier` + `name` or `code` + `name` as a composite identifier (e.g., Division, LegalCategory, FinancialCategory, Application, Country, Language). Some variants use a localized field name like `megnevezes` (Hungarian for "name/designation") as the primary identifier attribute instead of `name`.

This pattern enables administrators to configure dropdown options and classification values without code changes, while the active/enabled flag (when present) allows retiring options without deleting historical references. The flag name varies by project: `active` (reserve-app, skillmatrix-model) vs `isEnabled` (alba) vs absent (trivia, itracker, viterra_demo, InterfaceRegister, doors-model, ams-model, kozut-eugyfel-client).

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
