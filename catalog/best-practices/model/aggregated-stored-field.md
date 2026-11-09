---
id: "aggregated-stored-field"
title: "Aggregated Stored Field for Denormalized Collection Data"
domain: "model"
category: "entity"
score: 42.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
---
## Description

An entity stores pre-computed aggregated data from its collection relations in dedicated "*Aggregated" suffix fields. These stored (not derived) RichText or String fields contain concatenated or formatted summaries of related collection data. They are populated by custom business logic (triggers or operations) rather than being computed on every read, trading storage for read performance.

## Structure

- Entity has stored RichText or String attributes with "*Aggregated" suffix
- These fields correspond to 0..* collection relations on the same entity
- The fields are STORED (not DERIVED), meaning they must be explicitly updated
- Population mechanism is typically:
  - Custom backend operation code that runs when collections change
  - Trigger logic on collection modification
  - Batch update operations
- Provides fast read access to summarized collection data without joining

## Examples

### Alba
`Product` entity has three aggregated fields: `curriculumAggregated: RichText` (mirrors `curriculum [0..*] -> Curriculum`), `resultTypesAggregated: RichText` (mirrors `resultTypes [0..*] -> ResultType`), `audienceAggregated: RichText` (mirrors `audience [0..*] -> Audience`). All are STORED, not DERIVED. The exact update mechanism is in custom backend code, likely triggered when product is saved or when reference data changes.

## Trade-offs

- Pros: Fast read access without joins, good for display in lists/search, reduces query complexity
- Cons: Risk of stale data if update triggers fail, requires custom sync logic, unclear update contract, storage duplication
- Prefer when: Collection data needs to be displayed frequently in summarized form and read performance is prioritized over data freshness; consider derived attributes as an alternative when real-time accuracy is more important

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md) (alternative: compute on every read)
- [custom-implementation-placeholder](custom-implementation-placeholder.md) (update logic in custom code)
