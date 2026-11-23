---
id: application-vendor-integration-registry
title: Application-Vendor Integration Registry
description: "An enterprise registry of applications and the vendors that provide them, with a category per application, for tracking the integration landscape."
aliases: [application registry, vendor registry, integration landscape]
keywords: [application, vendor, registry, integration, enterprise architecture, category]
tags: [domain:model, layer:model, project:InterfaceRegister, status:single-project]
category: pattern
status: single-project
projects: [InterfaceRegister]
evidence: ["InterfaceRegister:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep one record per application and one record per vendor, so that an architect can see what software is in use, who provides it and what category it belongs to. Connections between applications, and where they run, can be modelled on top of this core.

### Each application has one vendor

An application is provided by exactly one vendor. The vendor is a shared record, so several applications from the same vendor point to one entry.

### Category is an enumeration

The application category is a fixed set of values. A new category is a model change, which keeps reports consistent.

## Structure

The Application entity has a required name (an identifier), a required version and a required category, which is an enumeration. It has a required association to one Vendor. The Vendor entity has a required name (an identifier) and a required address. The category enumeration has one value per application type, plus a catch-all value.

Connections between applications, deployment instances and network interfaces are separate entities that refer back to Application. They are not part of this core shape.

## Constraints

- An application has exactly one vendor.
- Name is an identifier for both the application and the vendor. The identifier flag marks the name as the natural key of a stored attribute on an entity. Uniqueness of names within the entity is intended; the runtime enforces uniqueness of an identifier attribute on each create and update, so a duplicate name fails with `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION` ([structure](../../agent-docs/model/esm_metamodel/structure.md)).
- The category must be one of the enumeration values. A catch-all value is used when no other value fits.
- The version is required. An unknown version is recorded with an explicit placeholder, not left empty.

## Variations

- **Vendor as a text field.** The vendor is a text attribute on the application. Simpler, but the vendor cannot be shared or renamed in one place.
- **Connections between applications.** A connection entity refers to a sender and a receiver application. Use this for interface tracking.
- **Deployment instances.** Each application is deployed as instances in environments. Each instance refers back to its application.
- **Network interfaces.** Servers, provided interfaces and client interfaces refer to the connection specification. Use this for technical detail.

## When to use

- An architecture team must know which applications exist and who provides them.
- Applications from the same vendor must be reported together.
- The category is used in reports or filters.

## When to avoid

- Only a list of application names is needed. A text list is enough.
- Connections and network details are the main need. Model them as a connection cluster first.
- Vendors change often and the history of each change matters. Use a history entry instead.

## Related

- [[organization-entity]]: a similar entity that holds a name and an address
- [[reference-data-lookup-entity]]: a lookup entity for shared reference values
- [[partner-with-contact-details]]: a partner record that holds contact details
