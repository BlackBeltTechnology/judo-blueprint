---
id: "bulk-json-import-export"
title: "Bulk JSON Import/Export via FileStore"
domain: "backend"
category: "operation"
score: 28.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - judo-partner
---
## Description

Admin operations for bulk import and export of entity data using JSON files mediated through the FileStore service. Import reads JSON from FileStore, deserializes with Jackson, processes each record (with dedup/validation), and creates entities. Export queries all entities, serializes to JSON, stores in FileStore, and returns a file reference.

## Structure

```java
// Import: inner POJO for JSON deserialization
public static class Q {
    @JsonProperty(required = true) private String field1;
    @JsonProperty private String optionalField;
}

// Read from FileStore + deserialize
InputStream stream = fsService.get(input.getFile().getId());
List<Q> items = new ObjectMapper().readValue(stream, new TypeReference<List<Q>>() {});

// Process with dedup
for (Q item : items) {
    if (entityDao.query().filterByName(StringFilter.equalTo(item.name)).count() == 0) {
        entityDao.create(EntityForCreate.builder()...build());
        count++;
    }
}

// Export: serialize + store in FileStore
byte[] json = new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsBytes(items);
String fileId = fsService.put(new ByteArrayInputStream(json), "export.json", "application/json");
```

## Examples

### Trivia
Upload/Download operations for bulk question management. Upload reads JSON from FileStore, deserializes to inner `Q` class, skips duplicates by question text, shuffles answer positions for anti-cheating, creates Question entities with category resolution. Download exports all questions as pretty-printed JSON.

### judo-partner
`PartnerImportCustomImplementation` reads partner JSON from FileStore, parses using Jackson `JsonUtils` with Hungarian-format `@JsonProperty` annotations, creates staged `Import` and `ImportPartner` records for a multi-phase migration pipeline. `ImportCountriesCustomImplementation` imports ISO 3166 country data from JSON. Data files (partners.json 1.2MB, countries.json 65KB, banks.json) stored in `migration/` directory.

## Trade-offs

- Pros: Handles bulk data efficiently, FileStore decouples from REST layer, Jackson inner class keeps serialization contained
- Cons: Loads entire JSON into memory (no streaming), IOException swallowed in trivia Upload, N+1 category lookups in Download
- Alternative: CSV import/export, streaming JSON parser for large datasets, database-level bulk operations

## Related Patterns

- filestore-mediated-file-transfer
- builder-pattern-entity-creation
