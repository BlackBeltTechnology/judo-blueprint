---
id: "external-system-staging-entity"
title: "External System Staging Entity for Integration"
domain: "model"
category: "entity"
score: 49.2
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-client
  - indamedia-adtrack
  - judo-partner
---
## Description

A dedicated staging entity serves as a buffer for data received from external systems before it is validated and transformed into domain entities. The staging entity mirrors the external system's data format (often with English field names matching the external API), while the domain entities use the project's internal naming and structure. Separate operations handle creation from the staging data, including deduplication checks and organizational routing.

## Structure

- Staging entity with attributes matching external API field names (may use English names even when domain uses another language)
- Attributes are simple types (String, Timestamp, Text) without domain enums or relations
- No business logic on the staging entity itself
- Domain entity has dedicated operations for creating from staging data (e.g., `letrehozJarokeloBejelentes`)
- Operations include deduplication: `Entity!filter(e | e.externalId == input.externalId)!empty()` checks
- Operations include routing: filter by organizational identifier to determine which org unit handles the record
- The staging entity may also have a synchronization flag for tracking bidirectional sync status

## Examples

### KozutEugyfelClient
`JarokeloStaging` entity with English-named fields (`url`, `title`, `description`, `fullAddress`, `user`, `id`, `status`, `institution`, `ceated`, `updated`) mirroring the Jarokelo road inspector API. `Bejelentes.letrehozJarokeloBejelentes` operation receives `JarokeloBejelentes` DTO, checks `SzervezetAzonosito` for org routing and `Bejelentes!filter(b | b.jarokeloAzonosito == input.jarokeloAzonosito)` for deduplication before creating the domain entity with Hungarian-named fields.

### IndamediaAdTrack
`FetchedData` entity captures raw platform API data (`totalCost`, `dailyCost`, `fetchedUpdated`) with a required `trackedCampaign [1..1]` back-reference. `AvailableCampaign` similarly stages campaign metadata fetched from Google/Meta platforms (`id`, `name`, `start`, `end`). The `syncData` and `fetchAvailableCampaigns` operations create staging records from platform API responses, which are then processed into domain entities (`Cost`, `TrackedCampaign`). Both staging entities preserve the raw data for audit and reconciliation.

### judo-partner
NAV (Hungarian tax authority) integration uses a multi-entity staging subsystem: `Taxpayer` entity stores queried taxpayer data (name, validity, vatCode, countyCode), `TaxpayerQuery` tracks query metadata (timestamp, taxIdentifier, status), and `TaxpayerAddress` stores detailed Hungarian address data (streetName, publicPlaceCategory, building, staircase, floor, door, lotNumber). The `Partner.queryTaxpayer` operation queries NAV and stages results. `Taxpayer.updatePartner` and `TaxpayerAddress.addToPartner` operations transform staging data into domain Partner/Address records.

## Trade-offs

- Pros: Clean separation between external API format and domain model, deduplication at integration boundary, supports multiple external sources
- Cons: Additional entity to maintain, data transformation logic in operations, potential data staleness in staging
- Prefer when: Integrating with external systems that have different data formats or when deduplication/validation is needed before domain entity creation

## Related Patterns

- [initializer-operation](initializer-operation.md) (synchronization operations run periodically)
- [unmapped-transfer-dto](unmapped-transfer-dto.md) (input DTOs for external data)
- [category-enum-pattern](category-enum-pattern.md) (BejelentesTipus classifies source system)
