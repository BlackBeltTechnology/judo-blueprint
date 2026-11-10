---
id: organization-discovery-search-component
title: Organization Discovery Search Component
description: A custom organization directory that replaces the generated discovery table with a filterable, infinite-scrolling card list; frontend only.
aliases: []
keywords: [organization, discovery, search, component, directory, filter, infinite scroll]
tags: [domain:model, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: [mlszksz-platform:unrecorded]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---

## Intent

Replace the generated data grid of an organization discovery panel with a card-based directory. Users filter by name, address and capability, and the list loads more rows as they scroll. The directory shows only organizations whose status is ACTIVE.

### The generated table is replaced, not extended

The generated panel is a table. The custom component is a visual element: the model must expose the panel as a custom implementation element, and the frontend registers a component for the key generated for it (see `frontend.md`). The generated query, paging and filter state still come from the platform, and the custom component reuses them.

## Structure

- A container component wires the filters, the seek-based pagination and the infinite scroll.
- Each organization is a card: logo avatar, name, address, contact details and capability tags.
- A filter bar offers three filters: organization name, address and capability. Filters apply in one batch.
- The pagination query always adds the status filter for ACTIVE organizations.
- Filter state persists for the session.

## Constraints

- The ACTIVE-only status filter is added by the frontend query builder, so the user cannot clear it in this UI. It is not a security rule: a client can call the generated query without it. To enforce it on the server, limit the actor's access with a getter expression in the model (project practice).
- Logos are binary attributes, carried as tokens. The project downloads them through its own access service and shows blob URLs, with a letter avatar as fallback. The service is example project code.
- Pagination is seek-based: the page size plus one row tells whether a next page exists. Offset paging is not used.
- Registration keys are generated per element in the container's `customization.ts`, and the scaffold `register<Container>CustomImplementations.tsx.default` contains the register function. Do not hard-code keys from another project.

## Variations

- **Card list without filters**: keep the container and cards, drop the filter bar.
- **Filter by capability only**: keep the capability autocomplete and drop name and address.
- **Non-ACTIVE organizations**: drop the status filter only if the platform's access rules already limit visibility.

## When to use

- The generated table for a discovery or directory panel is hard to read, and users browse by card.
- The entity has a logo and a short list of tags, such as capabilities.

## When to avoid

- Administrators need to sort and bulk-edit rows. Keep the generated table.
- The directory is small and fixed. A plain list is enough.

## Related

- [[organization-entity]] — the entity and its fields that the cards show
- [[address-entity-with-location]] — the address fields used by the address filter
