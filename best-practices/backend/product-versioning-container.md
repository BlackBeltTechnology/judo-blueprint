---
id: "product-versioning-container"
title: "Version Container Pattern for Entity Versioning"
domain: "backend"
category: "operation"
score: 42.2
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
alternatives:
  - data-snapshot-versioning
---
## Description

A versioning pattern using a dedicated container entity to group all versions of a product/document. Each version is a full copy of the entity (not a diff), stored with an incrementing version number. The container enforces the business rule that only one version can be in APPROVED state at any time. When a new version is approved, all previously approved versions are rolled back. New versions are created by cloning the current entity's data and relations into a new entity linked to the same container.

## Structure

```
Entity Model:
- ProductVersions (container) --> versions[] --> ProductVersion (version=0,1,2...)
- ProductVersions (container) --> allProducts[] --> Product (each version is a Product)
- Product --> productVersions --> ProductVersions (back-reference to container)
- Product --> version --> ProductVersion (current version info)
- ProductVersion --> origin --> Product (the product this version represents)

Operations:
- DraftNewVersion: clone current product, increment version, link to same container
- ApproveVersion: rollback all other approved versions, approve current
```

```java
// DraftNewVersion operation
Product current = productDao.getById(id).orElseThrow();
ProductVersion currentVersion = productDao.queryCurrentVersion(current).orElseThrow();
ProductVersions container = productDao.queryProductVersions(current);

// Clone product with new DRAFT state
Product newProduct = productDao.create(ProductForCreate.builder()
    .withTitle(current.getTitle())
    // ... copy all fields
    .withState(ProductState.DRAFT)
    .withProductVersions(container)  // Same container
    .build());

// Increment version
ProductVersion newVersion = productVersionDao.create(
    ProductVersionForCreate.builder()
        .withVersion(currentVersion.getVersion().orElse(0) + 1)
        .withOrigin(newProduct).build());
productVersionsDao.addVersions(container, newVersion);
```

## Examples

### ALBA
`ProductVersions` container groups all product versions. `DraftNewVersion` clones all product data (title, extent, goal, audiences, curriculums, result types, attachments, aggregated fields) and creates version N+1 in DRAFT state. `ApproveVersion` queries all approved products in the container via `productVersionsDao.queryAllProducts(versions).filterByState(EnumerationFilter.equalTo(ProductState.APPROVED))`, rolls them back to FINALIZED, then approves the current version.

## Trade-offs

- Pros: Full version history preserved, clear container grouping, single-approved-version enforcement, supports concurrent draft while approved version is published
- Cons: Full entity cloning is expensive and creates data duplication, relation cloning must be done manually for each relation type, container entity adds model complexity
- Alternative: Data snapshot versioning (immutable history copies -- see `data-snapshot-versioning`), event sourcing, or temporal table patterns

## Related Patterns

- data-snapshot-versioning
- state-lifecycle-operation
- builder-pattern-entity-creation
