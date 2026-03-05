---
id: "collection-holder-entity"
title: "Collection Holder Entity (No Attributes)"
domain: "model"
category: "entity"
score: 12.3
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - alba
---
## Description

An entity with no stored attributes of its own exists solely to hold a collection of related entities. The parent references it via a mandatory 1..1 relation, and the holder contains a 0..* collection. This pattern ensures the parent always has a stable container for its collection items, separating the collection lifecycle from the parent entity. It enables derived relations like "get the latest item" to have a stable anchor point.

## Structure

- Holder entity has zero stored attributes
- Holder has a 0..* relation to the item entity type
- Parent has a 1..1 stored association to the holder (always exists)
- Derived relations on the parent can navigate through the holder (e.g., `self.holder.items!head(i | i.version desc)`)
- The holder may also have derived relations aggregating data (e.g., `allProducts = self.versions.origin`)

## Examples

### Alba
`ProductVersions` entity has no stored attributes. It holds `versions [0..*] -> ProductVersion` (stored association) and `allProducts [0..*] -> Product` (derived: `self.versions.origin`). `Product` references it via `productVersions [1..1]` (always exists). `Product.currentVersion` derives through it: `self.productVersions.versions!head(p | p.version desc)` to get the latest version.

## Trade-offs

- Pros: Enables 1..1 cardinality to a collection, provides stable anchor for derived navigation, separates version collection lifecycle
- Cons: Additional entity with no data, could be replaced with a direct 0..* relation in simpler cases, adds complexity to the entity graph
- Prefer when: A parent needs a guaranteed collection container that supports complex derived navigation; consider direct 0..* relation as a simpler alternative

## Related Patterns

- [derived-relation-navigation](derived-relation-navigation.md) (uses holder for navigation expressions)
- [collection-lower-bound-zero](collection-lower-bound-zero.md)
