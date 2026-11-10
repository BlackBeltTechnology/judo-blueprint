---
id: interface-specification-generalization-hierarchy
title: Interface Specification Generalization Hierarchy
description: A generalization hierarchy of interface specifications, one base entity with synchronous and asynchronous protocol subtypes that each add only their own attributes.
aliases: [protocol type registry, interface specification hierarchy]
keywords: [interface, specification, generalization, hierarchy, protocol, subtype, polymorphic]
tags: [domain:model, layer:model, project:InterfaceRegister, status:single-project]
category: pattern
status: single-project
projects: [InterfaceRegister]
evidence: ["InterfaceRegister:unrecorded"]
alternatives: [credential-generalization-hierarchy]
fragment: interface-specification-generalization-hierarchy
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let an integration registry hold many kinds of interface in one place. A base entity carries what every interface shares. Each protocol is a subtype that adds only what its protocol needs. A reader can list all interfaces through one polymorphic view, and still get the protocol-specific fields.

### One base entity, many subtypes

The base entity is not createable or editable. Concrete protocols are subtypes of it. A protocol without extra fields is still a subtype, so the registry can tell the protocols apart.

### Asynchronous protocols share a grouping subtype

Email, file transfer and message queue share one intermediate subtype. The grouping is for navigation and shared typing. It adds no attributes.

## Structure

The base entity InterfaceSpecification has a required identifier name, a description, a link to the specification, a binary specification document, and a required direction of transmission (an enumeration). Six subtypes generalize it, directly or through AsynchronCommunication: Rest, Soap and DbLink directly; Email, FileTransfer and MessageQueue through AsynchronCommunication. Email composes zero or more EmailRecipient elements. FileTransfer carries a required transfer method and a required character encoding, both enumerations.

## Constraints

- Every subtype inherits the base attributes. A subtype adds only its own.
- The base entity is non-CRUD. Create and edit happen on the concrete subtypes.
- The recipients of an Email are composed. A recipient cannot exist without its Email.
- The direction of transmission is required on the base, so every subtype has one.
- Generalization is a platform feature between entity types only. Inheritance between transfer object types is not supported, so every transfer object (the read-only polymorphic one and each typed one) is declared on its own and maps its own entity.
- A transfer object used as a create target must not map to an abstract entity and must bind every required feature of the mapped entity. In the reference project the base is a concrete entity type that is simply not createable; making it abstract would be an alternative the project did not use.

## Variations

- **Flat list of subtypes.** All protocols generalize the base directly. Simple, but no shared grouping.
- **Grouped asynchronous subtypes.** Asynchronous protocols generalize an intermediate subtype, as in the reference project.
- **Polymorphic read, typed write.** A read-only transfer object over the base lists everything. Each subtype has its own writable transfer object.
- **Platform-managed polymorphic creation.** When an access links to a collection of an abstract base, the generated Create button offers the concrete subtypes, with no custom operation. The reference project did not model this; it creates on the subtype pages.

## When to use

- A registry holds several kinds of one thing, and each kind has its own fields.
- Users need one list across all kinds, plus typed editing of each kind.
- The kinds share a core of attributes.

## When to avoid

- The kinds share almost no attributes. Separate entities are clearer.
- Only one kind exists. A plain entity is enough.
- The kinds need to be switched at runtime. A type enumeration on one entity may be simpler.

## Related

- [[credential-generalization-hierarchy]] — the same polymorphic base-and-subtypes pattern for platform credentials
- [[post-generalization-hierarchy]] — an abstract base with concrete content subtypes
- [[partner-generalization-hierarchy]] — a generalization hierarchy for partners
