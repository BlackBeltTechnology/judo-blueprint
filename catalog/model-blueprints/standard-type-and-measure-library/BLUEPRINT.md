---
id: standard-type-and-measure-library
title: Standard Type and Measure Library (Shared Type System)
description: "A shared types package (string, numeric, temporal primitives with fixed limits) and a measures package (SI measures and units) that every entity of a JUDO model draws its attribute types from."
aliases: []
keywords: [standard, type, measure, unit, library, shared, primitive, precision, maxLength]
tags: ["domain:model", "layer:model", "project:bhs-global-operation", "project:viterra_demo", "project:InterfaceRegister", "project:mjsz", "project:sanctuary-backend", "project:doors-model", "project:ams-model", "project:skillmatrix-model", "status:established"]
category: pattern
status: established
projects: [bhs-global-operation, viterra_demo, InterfaceRegister, mjsz, sanctuary-backend, doors-model, ams-model, skillmatrix-model]
evidence: ["bhs-global-operation:unrecorded", "viterra_demo:unrecorded", "InterfaceRegister:unrecorded", "mjsz:unrecorded", "sanctuary-backend:unrecorded", "doors-model:unrecorded", "ams-model:unrecorded", "skillmatrix-model:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give every project attribute the same vocabulary of types and units. One `types` package fixes string lengths and numeric precision. One `measures` package supplies physical measures and units for measured quantities. Entities reference these and never define their own primitives.

### One place for limits

String length, numeric precision and scale are decided once in the types package. A change applies to every attribute of that type. The platform requires `maxLength` on strings and `precision` / `scale` on numerics ([type reference](../../agent-docs/model/esm_metamodel/type.md#behaviour-rules)). The concrete values here are an organization convention, not platform defaults.

### Units are modelled, not stored as text

A physical quantity is a numeric attribute of a measured type with a stored unit. Conversion between units of one measure is done by the platform from the unit rates ([Measures](../../agent-docs/model/model-validation-and-transformation.md#measures)).

## Structure

Two packages under the model root. `types` holds the primitives: several string types with different limits (general, long text, phone, URL, e-mail), numeric types of different precision (integer, long, double, float), boolean, date, timestamp and optionally time. `measures` holds about 28 measures, each with its units and conversion rates. Application models add measured types and entities that point at these. The library is either a stand-alone model imported by other models, or a pair of packages embedded in the application model.

## Constraints

- Entities use only types from the `types` package. No inline primitives.
- Every string type has a maximum length; every numeric type a precision and scale.
- A measure has exactly one base unit; other units convert to it with rates.
- A measured type names its stored unit. Values are stored in that unit.
- Keep one definition per name. When a library is imported and also embedded, the two copies drift.

## Variations

- **Stand-alone library model.** Imported by application models, so the whole organization shares one copy.
- **Embedded copy.** The packages sit inside each application model. Simpler to build, but copies drift.
- **Project-specific string types.** Network addresses, identifier formats or code types are added next to the standard ones.
- **Different long-text limit.** `Text` limits of 250, 1000, 2000 or 4000 are all in use. Choose one per organization.
- **Without `Time`.** Several projects omit the time type.

## When to use

- Any JUDO model with more than a handful of attributes.
- Several models of one organization that should agree on limits.
- A domain with physical quantities that need unit conversion.

## When to avoid

- A tiny throw-away model where the default types are enough.
- A model that never uses measured quantities and does not want the unused measures package. It can be left out or trimmed.

## Related

- [[standard-type-library]] — the best-practice version of the type rules
- [[active-inactive-status-enum]] — a typical enumeration used alongside the types
