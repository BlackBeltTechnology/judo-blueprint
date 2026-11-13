---
id: mask-field-projection
title: Mask Pattern for Field Projection
description: "Use the generated Mask classes to say which attributes and relations a DAO read or update touches: minimal masks for existence checks, lists and loops, nested masks for detail views, and masks on update for partial writes."
aliases: ["mask pattern", "DAO projection", "partial update mask"]
keywords: ["mask", "projection", "DAO", "getById", "maskedBy", "partial update", "N+1", "performance", "nested mask"]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "status:established"]
category: data-access
status: established
projects: [rackinspect, alba, mlszksz-platform, ubives, park-here, indamedia-adtrack, judo-partner]
evidence: ["rackinspect:application/interceptors/src/main/java/hu/blackbelt/rackinspect/interceptors/user/management/UserDeleteInterceptor.java", "alba:unrecorded", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/PushNotificationServiceImpl.java", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded"]
alternatives: []
related: [dao-fluent-query-filter, mutable-entity-update-pattern, entity-re-fetch-pattern, dirty-check-before-update]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

Every DAO read and update takes a mask that names the attributes and relations to load or write. Using the smallest mask that serves the code reduces data transfer, avoids loading relation graphs and N+1 reads, and makes updates touch only what changed.

## Practice

### Platform: what masks are and how they behave

- Every entity has a generated `<Entity>Mask` with a static factory `<Entity>Mask.<entity>Mask()` and fluent `.withAttribute()` methods; `.withRelation(<Related>Mask...)` takes a nested mask ([mask basics](../../agent-docs/backend/data-access-guide.md#mask-basics)).
- Masks apply to `getById`, `query().maskedBy(...)`, relation queries (`queryRelation(entity).maskedBy(...)`), `create` and `update` ([common mask patterns](../../agent-docs/backend/data-access-guide.md#common-mask-patterns)).
- The platform guide's rules: always mask queries; an **empty mask** loads only the identifier and is the cheapest existence check; use minimal masks in loops; chain nested masks to control relation depth; use masks in updates for partial writes ([mask best practices](../../agent-docs/backend/data-access-guide.md#mask-best-practices)).
- Do not read a field you did not include; it is `null` (same section). In generated getters an optional attribute is an `Optional`, a required one a plain value, and a key absent from the payload differs from a key present with `null` ([absent, null and empty](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)).
- A list call without an explicit seek returns all matching rows, so a mask limits columns, not rows; use a seek for paging ([pagination](../../agent-docs/backend/data-access-guide.md#pagination)).

### Practice notes: how the examples use them

```java
// Example code: Account, Address and their DAOs and masks are generated types
// existence check: identifier only
boolean exists = accountDao.getById(id, AccountMask.accountMask()).isPresent();

// list: only the displayed columns
accountDao.query().maskedBy(AccountMask.accountMask().withName().withIsArchived()).selectList();

// detail: nested masks control depth
accountDao.getById(id, AccountMask.accountMask()
        .withName()
        .withAddresses(AddressMask.addressMask().withCity().withIsBilling()));

// relation query
accountDao.queryAddresses(account).maskedBy(AddressMask.addressMask().withIsBilling()).selectList();

// partial update: only these fields are written
account.setName(newName);
accountDao.update(account, AccountMask.accountMask().withName());
```

- Build one named helper for a deep mask used in several places (one example has a standard nested mask five levels deep) instead of repeating the chain.
- Use the empty mask for toggle operations and batch deletes that need only the identifiers: `dao.update(entity, EntityMask.entityMask())` and loading ids before deleting in batches.
- In authentication and per-request paths (user lookup by e-mail) use the smallest mask: the check runs on every login or call ([[keycloak-jit-user-provisioning]]).
- On update, mask what you set. A wider mask than the changed fields rewrites values you loaded, which can overwrite concurrent changes; compare before writing ([[dirty-check-before-update]], [[mutable-entity-update-pattern]]).
- After a write, re-read with the mask the next step needs rather than reusing an object loaded with a smaller one ([[entity-re-fetch-pattern]]).
- Masks are for the DAO. Which fields a REST client receives is decided by the transfer object in the model; to hide fields from a response see [[interceptor-template-postcall]].

## Rationale

- Smaller reads: fewer columns and no hidden relation loads, which matters most in lists, loops and per-request code.
- Type-safe field selection checked at compile time.
- Cost: you must list every needed field; a forgotten field is `null` at runtime and reads like missing data; deeply nested masks are verbose.

## Example

Several applications use masks throughout. A duplicate check loads only the normalized name and archived flag of accounts with the same normalized name. A validation step loads only the state of a product. A calendar cancellation reads only the status of bookings. A cache clearing job loads ids with an empty mask and deletes in batches. A catalog service builds a five-level nested mask once and reuses it. Authentication interceptors load only the e-mail of the user.

## When to avoid

- When the entity is tiny and used once: the full read is no cost, though it is still cheap to write the mask.
- When you need every attribute, for example copying an entity; then name them explicitly rather than assume a default.
- Do not use a mask to try to secure data: the field is still reachable through other operations; use access rules in the model.

## Related

- [[dao-fluent-query-filter]] — queries that the mask is attached to
- [[mutable-entity-update-pattern]] — update with a mask
- [[entity-re-fetch-pattern]] — reading again after a write
- [[dirty-check-before-update]] — compare before writing
- [[interceptor-template-postcall]] — shaping responses
- [[keycloak-jit-user-provisioning]] — minimal mask on a per-login path
