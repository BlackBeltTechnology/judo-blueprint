---
id: "upsert-create-or-update"
title: "Upsert Pattern (Create or Update)"
domain: "backend"
category: "operation"
score: 64.6
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - park-here
  - indamedia-adtrack
  - judo-partner
---
## Description

A custom operation that checks whether a singleton or unique entity exists and either creates it (if absent) or updates it (if present). This implements the upsert (update-or-insert) semantic for configuration entities or other singletons that may not yet exist on first access. The pattern uses `dao.query().selectOne()` to check existence, then branches to `dao.create()` or `entity.setXxx() + dao.update()`.

## Structure

```java
@Override
public void accept(Context _this, Input input) {
    Optional<Configuration> existing = configurationDao.query().selectOne();
    if (existing.isEmpty()) {
        configurationDao.create(ConfigurationForCreate.builder()
            .withField1(input.getField1())
            .withField2(input.getField2())
            .build());
    } else {
        existing.get().setField1(input.getField1());
        existing.get().setField2(input.getField2());
        configurationDao.update(existing.get());
    }
}
```

## Examples

### ParkHere
`ConfigurationCustomImplementation` upserts a singleton Configuration entity storing email templates (doorman, deletion, modification, reminder), contact email, and sender email. On first invocation it creates the config; on subsequent calls it updates the existing record.

### Indamedia-AdTrack
`TrackedCampaignServiceImpl.updateOrCreateCosts()` upserts daily `Cost` records for tracked campaigns. Queries existing cost by date filter, updates amount if found or creates new `CostForCreate` if absent. Called during data sync to maintain day-by-day spending records without duplicates. Also used for `FetchedData` snapshots -- each sync creates a new snapshot while cost records are upserted.

### judo-partner
`CountryServices.importCountries()` upserts countries from an ISO 3166 JSON file. For each country, queries by name; if not found, creates a new `Country` record. This ensures idempotent country data imports -- running the import multiple times does not create duplicates.

## Trade-offs

- Pros: Safe for first-time setup, idempotent, handles both initial and subsequent invocations cleanly
- Cons: Not atomic (race condition if two requests arrive simultaneously), no optimistic locking
- Alternative: Database-level upsert (INSERT ON CONFLICT), or Init operation for initial seeding

## Related Patterns

- init-data-seeding
- mutable-entity-update-pattern
- builder-pattern-entity-creation
