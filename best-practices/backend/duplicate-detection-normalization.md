---
id: "duplicate-detection-normalization"
title: "Duplicate Detection via Name Normalization and Similarity"
domain: "backend"
category: "operation"
score: 47.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - judo-partner
---
## Description

A pattern for detecting duplicate entities by normalizing string fields (removing punctuation, company form suffixes, and case variations) and computing similarity scores. Each entity stores a `normalizedName` alongside the display `name`. After any name change (create, update, import), the system queries all non-archived entities with the same normalized name and sets an `isDuplicateName` flag on all of them. Name validation against external sources uses Jaro-Winkler similarity with a configurable threshold.

## Structure

```java
// Name normalization utility
public static String normalizeCompanyName(String name) {
    // Strip legal form suffixes (Kft., Zrt., Bt., Nyrt., etc.)
    // Remove punctuation and special characters
    // Convert to uppercase for comparison
    return normalized;
}

// Name similarity calculation
public static double calculateSimilarity(String name1, String name2) {
    return new JaroWinklerSimilarity().apply(name1, name2);
}

// Duplicate flag recalculation
public void setIsDuplicate(String name) {
    List<Entity> duplicates = entityDao.query()
        .maskedBy(EntityMask.entityMask().withNormalizedName().withIsArchived())
        .filterByNormalizedName(StringFilter.equalTo(normalizeCompanyName(name)))
        .filterByIsArchived(BooleanFilter.isFalse())
        .selectList();

    for (Entity entity : duplicates) {
        entity.setIsDuplicateName(duplicates.size() > 1);
    }
    entityDao.updateAll(duplicates);
}
```

Key elements:
- `normalizedName` stored on entity (denormalized for query efficiency)
- `isDuplicateName` boolean flag recalculated after every name change
- Jaro-Winkler similarity (threshold 0.8) for external name validation
- Hungarian company form mapping (e.g., "KORLATOLT FELELOSSEGU TARSASAG" -> "Kft.")
- Batch update via `dao.updateAll()` for all affected entities

## Examples

### judo-partner
`PartnerUtils.normalizeCompanyName()` strips Hungarian legal form suffixes and normalizes for comparison. `PartnerUtils.correctCompanyName()` maps full company form names to abbreviations. `PartnerServices.setIsDuplicate()` queries all non-archived partners with the same normalized name using a masked query and sets `isDuplicateName` flag. Called from `createPartner()`, `validatePartner()`, `deletePartner()`, and `PartnerUpdateInterceptor`. Name validation against NAV uses `PartnerUtils.calculateSimilarity()` (Jaro-Winkler, threshold 0.8) comparing both the full name and short name from NAV data.

## Trade-offs

- Pros: Efficient duplicate detection via indexed normalized field, real-time flag updates on every change, external validation adds confidence, batch update minimizes queries
- Cons: Normalization logic is domain-specific (Hungarian company forms), recalculating flags across all duplicates on every change is O(n), Jaro-Winkler threshold may produce false positives/negatives
- Alternative: Database-level fuzzy matching (pg_trgm), phonetic matching (Soundex/Metaphone), manual duplicate review queue

## Related Patterns

- soft-delete-archive-pattern
- dao-fluent-query-filter
- mask-field-projection
