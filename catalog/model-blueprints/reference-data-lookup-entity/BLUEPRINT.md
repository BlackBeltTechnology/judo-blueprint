---
id: reference-data-lookup-entity
title: Reference Data Lookup Entity (Name + Active/Enabled)
description: "A minimal reference data entity with a `name` (required) attribute and optionally an `active` or `isEnabled` boolean attribute (default: true) for soft-enable/disable."
aliases: [lookup table, master data, classification entity]
keywords: [reference, data, lookup, name, active, enabled, dropdown, classification]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:reserve-app", "project:alba", "project:trivia", "project:itracker", "project:viterra_demo", "project:InterfaceRegister", "project:doors-model", "project:ams-model", "project:skillmatrix-model", "project:mlszksz-platform", "status:established"]
category: pattern
status: established
projects: [reserve-app, alba, trivia, itracker, viterra_demo, InterfaceRegister, doors-model, ams-model, skillmatrix-model, mlszksz-platform]
evidence: ["reserve-app:unrecorded", "alba:unrecorded", "trivia:unrecorded", "itracker:unrecorded", "viterra_demo:unrecorded", "InterfaceRegister:unrecorded", "doors-model:unrecorded", "ams-model:unrecorded", "skillmatrix-model:unrecorded", "mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: []
fragment: reference-data-lookup-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep a small managed list of options that other entities point to: vehicle types, categories, regions, units, countries, tags and similar. Administrators or a data-seeding step maintain the list. Core entities reference an entry through an association and users pick the entry from a drop-down or a multi-select.

### The lookup is minimal

A lookup carries a display name and, in many variants, one flag that retires an option without deleting the records that already use it. Some variants add one or two extra attributes, such as a numeric value, a description or a localized name.

### Lookups are shared, not owned

A core entity references a lookup entry. It does not own it. Removing the reference leaves the entry in the list.

## Structure

One lookup entity, called `Category` in the neutral example, with a required `name` that is the identifier. Optionally it has a required boolean flag that defaults to true. The flag is named `active`, `isActive` or `isEnabled` depending on the project, or is absent in the simplest variants. A core entity, `Order` in the example, holds an association to the lookup: 0..1 or 1..1 for a single choice, 0..* for a multi-select. The association is one-way in most projects. Some add the reverse collection, for example the orders of a category.

The lookup entity has all three CRUD flags (createable, updateable, deleteable) off. Writes go through transfer objects and access points that the project exposes to the administrator, or through seeding.

## Constraints

- The lookup is an association target and never a composition part of the referencing entity.
- The name is required. It is the identifier in most projects. Uniqueness of names is not a model rule; where it matters, a custom operation or service checks it (project practice).
- The flag, where present, defaults to true and hides an option from new choices. It does not remove existing references. Choice lists filter on it; read paths that show existing values do not. See [[soft-delete-active-flag]].
- The entity-level CRUD flags are all false, so the platform exposes no direct create, update or delete on the entity itself. Whether an actor may edit the list depends on the access and transfer object that the project defines for that actor. See [[entity-crud-at-service-layer]].
- Partner or end-user views usually get a name-only transfer object. The administrator gets the full one with the flag.

## Variations

- **Name only.** No flag. Use it for stable lists that are never retired.
- **Name plus active flag.** The flag name differs between projects (`active`, `isActive`, `isEnabled`).
- **Extra attribute.** One more field, such as minutes, address, website, description, a numeric rank or a classifier enumeration. See [[category-enum-pattern]] when the classifier is itself fixed.
- **Code plus name.** A short identifier (`code` or `identifier`) next to the display name, for lists such as countries, divisions or financial categories.
- **Localized or alternative name attribute.** The identifier attribute is called `title`, `code` or a local-language word instead of `name`.
- **Grouped lookup.** A lookup with a parent lookup or group, forming a two-level classification.
- **Many-to-many tags.** Several entities share the lookup through 0..* associations. See [[capability-lookup-entity]].
- **Derived count on the admin view.** The administrator's transfer object adds a derived attribute such as the number of related items.

## When to use

- A field must be chosen from a list that administrators change without a model change.
- Several entities share the same classification.
- Options must be retired without losing history on existing records.

## When to avoid

- The set is small, fixed and part of the domain vocabulary. Use an enumeration, see [[category-enum-pattern]].
- Each lookup entry has its own lifecycle, relations or permissions. Model a full entity instead.
- Records must own their list entries. Use a composition.

## Related

- [[capability-lookup-entity]] — a specialisation with an on/off flag and many-to-many tags
- [[category-enum-pattern]] — a fixed list as an enumeration instead of an entity
- [[soft-delete-active-flag]] — the retire-without-delete flag used by many variants
- [[entity-crud-at-service-layer]] — all CRUD flags off on the entity, writes through transfer objects
- [[initializer-entity-with-init-operation]] — seeding lookup rows at startup
