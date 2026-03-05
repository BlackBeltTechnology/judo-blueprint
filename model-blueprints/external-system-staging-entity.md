---
id: external-system-staging-entity
title: "External System Staging Entity for API Data Import"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - kozut-eugyfel-client
---

## Description

A staging entity that mirrors the data structure of an external system's API response, serving as a temporary landing zone for imported data before it is transformed into domain entities. The staging entity has flat, loosely-typed attributes (all strings, few required) matching the external API's field names (often in a different language or naming convention than the domain model). The entity has no relations, no operations, and is not CRUD-managed -- it is populated by a synchronization operation and then consumed by domain entity creation logic.

This pattern enables clean separation between the external system's data format and the internal domain model. The staging entity acts as a data transfer buffer: the sync operation fetches data from the external API, writes it to staging entities, and then a separate transformation step creates or updates domain entities from the staged data. This two-phase approach makes it easy to add validation, deduplication, and error handling between import and domain creation.

The companion domain entity typically carries an external system identifier attribute (e.g., jarokeloAzonosito) to link back to the external system's record, plus a static synchronization operation (szinkronizal) that orchestrates the import pipeline.

## Detection Query

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name required memberType } totalCount }
    relations { totalCount }
    operations { totalCount }
  }
} } }
```

Look for entities with many string attributes (5+), no relations, no operations, and attribute names suggesting external API field mapping (e.g., camelCase English names mixed with domain-language names, or generic names like `id`, `status`, `url`, `title`, `description`).

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{EXTERNAL_SYSTEM}}Staging",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{EXTERNAL_SYSTEM}}Staging", name: "{{FIELD_NAME}}"
} }) { success fqn } }
```

## Examples

### kozut-eugyfel-client
- **JarokeloStaging entity**: `e_ugyfelszolgalat::entities::JarokeloStaging`
  - Attributes (all optional strings): url, title, description, fullAddress, user, id, status, institution, ceated (sic -- typo of "created"), updated
  - No relations, no operations
  - Mirrors the response format of the Jarokelo (Hungarian public complaint portal) API
  - Used by the `Bejelentes.szinkronizal` (synchronize) static operation which fetches open complaints from Jarokelo, stages them in JarokeloStaging entities, and then creates or updates Bejelentes (Report) domain entities
  - The Bejelentes entity carries `jarokeloAzonosito` (Jarokelo identifier) to track which domain records originated from the external system
  - Additional static operations on Bejelentes support the integration: `letrehozJarokeloBejelentes` (create report from Jarokelo data), `letezikJarokeloBejelentes` (check if a Jarokelo report already exists), `nyitottJarokeloBejelentesek` (list open Jarokelo reports)
  - The SzervezetAzonosito (Organization Identifier) entity provides `azonosito` (identifier) + `megnevezes` (name) mapping for external organization codes, managed by Admin actor via `szinkronizaltSzervezetek` access point
