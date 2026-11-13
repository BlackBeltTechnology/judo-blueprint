---
id: product-versioning-container
title: Version Container Pattern for Entity Versioning
description: Practice for versioning a product or document with a container entity that groups full-copy versions, creates a new version by cloning, and keeps exactly one version approved.
aliases: [version container, full-copy versioning, draft new version, single approved version]
keywords: [version, container, versioning, product, clone, draft, approve, rollback, state]
tags: ["domain:backend", "layer:backend", "project:alba", "status:single-project"]
category: operation
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: [data-snapshot-versioning]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Keep every version of a product (or document) as a full, editable copy, grouped by a container entity, with a rule that only one version is approved at a time. This is a convention built on the platform; the platform offers no versioning feature, only the DAO calls the operations use.

## Practice

### Platform: the DAO calls the operations are built from

- Creation uses the generated `<Entity>ForCreate` builder and `dao.create`; relations to existing entities are set in the builder, and a single-relation setter needs a real object, never `null` ([builder pattern](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao), [[builder-pattern-entity-creation]]).
- Multi-valued relations are read with the DAO relation queries (`xDao.queryY(x)`), which return a customizer with `filterBy...`, `maskedBy` and `selectList()`; single-valued relation queries return the entity directly ([relationship navigation](../../agent-docs/backend/data-access-guide.md#query-result-methods)). Enumeration attributes are filtered with `EnumerationFilter`.
- The generated DAO has per-relation `create`, `set`, `unset`, `add` and `remove` methods, subject to the relation's allowed-operation flags ([which types get a full DAO](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)); attaching an existing entity to a collection relation of its parent is the relation's `add` method (as used below). Check the generated DAO interface for exact names.
- State changes of existing versions are ordinary entity updates ([[mutable-entity-update-pattern]]), and all steps of an operation run in that operation's transaction.
- Custom operations are not intercepted, so a rule enforced only in an interceptor would not apply here; the "one approved version" rule lives in the operations themselves ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

### Practice notes: container, full copies, two operations

Model shape (described in prose; the platform part is plain entities and relations): a container entity holds a collection of version-info records and a collection of all product copies; each product points back to its container and to its current version-info; each version-info has a version number and points to the product it represents.

- `DraftNewVersion` clones the current product with all attributes and relations into a new product in state DRAFT, linked to the same container, and creates a version-info with number + 1:

```java
// Example code: Product, ProductVersion(s) and their DAOs are generated types
Product current = productDao.getById(id).orElseThrow();
ProductVersion currentVersion = productDao.queryCurrentVersion(current).orElseThrow();
ProductVersions container = productDao.queryProductVersions(current);

Product copy = productDao.create(ProductForCreate.builder()
    .withTitle(current.getTitle())
    // ... every other attribute and relation is copied explicitly
    .withState(ProductState.DRAFT)
    .withProductVersions(container)
    .build());

ProductVersion next = productVersionDao.create(ProductVersionForCreate.builder()
    .withVersion(currentVersion.getVersion().orElse(0) + 1)
    .withOrigin(copy)
    .build());
productVersionsDao.addVersions(container, next);
```

- `ApproveVersion` queries all approved products of the container, sets them back to FINALIZED, then approves the current one:

```java
List<Product> approved = productVersionsDao.queryAllProducts(container)
    .filterByState(EnumerationFilter.equalTo(ProductState.APPROVED))
    .selectList();
for (Product p : approved) {
    p.setState(ProductState.FINALIZED);
    productDao.update(p);
}
```

- Relations are cloned by hand, relation type by relation type (for example tags, categories, attachments and aggregated fields); a new relation on the product means a code change in the clone.
- A draft can exist while the approved version stays published.

## Rationale

- The full history stays queryable and every version is an ordinary, editable entity, so no special read path is needed.
- The container makes the single-approved-version rule a single query.
- Costs: cloning duplicates data and is slow for large products, every relation must be copied explicitly, and the container adds model complexity. Two concurrent approvals of different versions are not serialized by the platform, so the single-approved rule can be broken under a race.

## Example

A product with version 2 approved: an editor calls draft, a version 3 copy appears in DRAFT linked to the same container. After review, approval sets version 2 to FINALIZED and version 3 to APPROVED. A query over the container for APPROVED products always returns at most one row.

## When to avoid

- When history is read-only and rarely needed: store immutable snapshots instead ([[data-snapshot-versioning]]).
- When the entity has many relations or large attachments, since cloning cost and maintenance grow with them.
- When only the audit of changes matters, not usable older versions ([[audit-event-trail]]).

## Related

- [[data-snapshot-versioning]] — alternative: immutable snapshots instead of editable copies
- [[state-lifecycle-operation]] — the draft, approved and finalized transitions
- [[builder-pattern-entity-creation]] — how the clone is created
- [[workflow-versioning-pattern]] — a model blueprint for versioned definitions
