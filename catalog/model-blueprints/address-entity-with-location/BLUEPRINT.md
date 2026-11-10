---
id: address-entity-with-location
title: Address Entity with Location
description: "An address entity with structured street fields, a required city and postal code, and an optional composed location holding latitude and longitude for map use."
aliases: [address with coordinates, geolocated address, address location]
keywords: [address, location, latitude, longitude, geolocation, postal code, city]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, project:rackinspect, project:doors-model, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, rackinspect, doors-model]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "doors-model:unrecorded"]
alternatives: [address-field-auto-composition]
fragment: address-entity-with-location
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Store a physical address in structured parts, and optionally attach a geographic point to it. The street parts are kept apart so that the address can be edited and searched by field. The point is kept in its own entity so that an address without coordinates needs no empty values.

### Structured parts, not one string

The address keeps street name, building, floor, door and similar parts as separate attributes. A full-address text is computed from them, not typed in by hand.

### Location is a composed part

The location with latitude and longitude is a composed entity. It is owned by the address, so it is created and removed with it. The address does not need coordinates to exist.

## Structure

The Address entity has a required street name and optional building, floor and door attributes, a derived full-address text, and required associations to a City and a PostalCode, both of which are lookup entities. It has one optional composed Location (0..1). The Location has a required latitude and a required longitude, both decimal values. City has a name. PostalCode has a code. The Address entity is flagged not createable, updateable or deleteable, so the generated actions do not offer those operations on it in the reference shape; the owning entity creates it.

## Constraints

- The street name is required. The location is optional, and its latitude and longitude are both required when it exists.
- The city and the postal code are required lookup associations. They are references to existing entities, not text.
- The full-address text is derived. It is not stored and must not be edited by hand.
- A location belongs to one address. The location relation is a composition, so deleting the address deletes its location (composition cascades; an aggregation or association would not).
- A city and a postal code are checked against each other by the service that writes the address. The model does not enforce that pairing.

## Variations

- **Lookup references.** City and postal code are associations to lookup entities. This is the form in the reference shape.
- **Flat strings.** City, country, street and zip code are plain text attributes with a derived full address. No lookup entities are needed. This is simpler, but it cannot enforce a valid city and postal code pairing.
- **Type flags.** Flags such as billing, headquarters, postal and delivery mark the purpose of an address on its owner. Each flag has an operation that sets it.
- **Country association.** A country association replaces or adds to the city and postal code references.

## When to use

- Addresses are shown on a map or used for routing, so coordinates are needed.
- Address fields must be searched or validated separately.
- A few addresses per owner are kept, and each has a clear purpose.

## When to avoid

- Only a single free-text address is needed. Use one text attribute.
- Coordinates are never used. Leave out the location entirely.
- The address must be validated against an external postal service on each change. That validation is outside this model.

## Related

- [[address-field-auto-composition]] — computes the address text and the address line from the parts
- [[organization-entity]] — an owner that commonly composes an address
- [[partner-with-contact-details]] — an owner that holds addresses and contact data
- [[contact-info-composition-cluster]] — contact data composed on the same owner
