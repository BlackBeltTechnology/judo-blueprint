---
id: organization-entity
title: Organization Entity with Contact Info and Membership
description: An Organization entity for a company or group in a multi-tenant platform, with contact fields, an ACTIVE/SUSPENDED/DEACTIVATED status, a composed address and membership data.
aliases: [organization, company, tenant organization]
keywords: [organization, contact, membership, status, tenant, address, capability]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: entity
status: single-project
projects: [mlszksz-platform]
evidence: [mlszksz-platform:model/MLSZKSZPlatform.model]
alternatives: []
fragment: organization-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---

## Intent

Model a company or group that uses a multi-tenant platform. The organization has a name and a contact email, a lifecycle status, an optional address, and membership information. Users belong to organizations, and organizations hold capabilities that describe what they offer.

### Status controls visibility and lifecycle

The status enumeration has three values: ACTIVE, SUSPENDED and DEACTIVATED. In the source project only ACTIVE organizations are listed to other users (project rule, not platform behaviour). Changing the status is a business action, so it belongs in custom operations with explicit transition rules, not in free editing. Interceptors fire only on built-in operations, so rules for custom operations live in the operations themselves.

## Structure

- **Organization** entity: required name, contactEmail and status; optional contact name and phone, city name, full address, membership start and description, user count, and two flags (isUserCountHidden, isAdminOrganization) that default to false.
- **OrganizationStatus** enumeration: ACTIVE (0), SUSPENDED (1), DEACTIVATED (2).
- **Address**: composed, 0..1. Deleted with the organization.
- **Invitation**: composed, 0..*. Deleted with the organization.
- **Capability** and **User**: associations, 0..*. They outlive the organization.

## Constraints

- The organization name and the contact email are required (model cardinality). Name uniqueness is a project rule enforced by a project service in the custom create operation (see backend.md); the platform does not enforce it.
- The status enumeration is the only state field. Do not add a second flag for the same state.
- Deleting an organization removes its composed address and invitations (composition cascades), but not its users or capabilities (associations do not cascade).
- Renaming an organization is restricted to platform administrators (project rule in a project service, see backend.md; not a platform rule).

## Variations

- **Without membership**: drop membership start and description.
- **Without address**: drop the composed address; keep the full address text if a single line is enough.
- **Single-tenant**: drop the status enumeration when every organization is active.

## When to use

- A multi-tenant platform needs a party entity that owns users and offers.
- Organizations need an active or suspended state that controls who sees them.

## When to avoid

- The party is a person. Use a person or user entity.
- The reference data is a fixed list that never changes at runtime. Use a lookup entity.

## Related

- [[organization-discovery-search-component]] — the card directory that lists ACTIVE organizations
- [[address-entity-with-location]] — the composed address the organization owns
- [[audit-log-entity]] — audit rows for status changes made by custom operations
