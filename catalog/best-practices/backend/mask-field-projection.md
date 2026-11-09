---
id: "mask-field-projection"
title: "Mask Pattern for Field Projection"
domain: "backend"
category: "data-access"
score: 77.5
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - alba
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
---
## Description

The Mask pattern controls which fields and nested relations are loaded from the database when querying or updating entities. Generated `EntityMask` builder classes allow specifying exactly which attributes and relation depths to include. This reduces data transfer and avoids loading unnecessary relation graphs. Masks can be used with `getById()`, `query().maskedBy()`, `update()`, and relation queries.

## Structure

```java
// Simple mask - specific fields only
PartnerMask.partnerMask()
    .withGenericValid()
    .withName();

// Nested mask - include relations with their own field selection
PartnerMask.partnerMask()
    .withAddresses(AddressMask.addressMask().withIsBilling().withCity())
    .withBillingAddress(AddressMask.addressMask())
    .withPartnerErrors(PartnerErrorMask.partnerErrorMask());

// Usage with getById
partnerDao.getById(id, PartnerMask.partnerMask().withGenericValid());

// Usage with relation query
partnerDao.queryAddresses(partner)
    .maskedBy(AddressMask.addressMask().withIsBilling())
    .selectList();

// Usage with update (partial update)
addressDao.update(entity, AddressMask.addressMask());
```

## Examples

### RackInspect
Extensive mask usage across all services. `RackService.createStandardRackMask()` builds a deeply nested mask spanning 5+ levels (rack -> elements -> dimension groups -> parameters -> selectable values + templates). Toggle operations use empty masks on update: `dao.update(entity, EntityMask.entityMask())`. `queryContainer()` uses masks to load only needed parent fields.

### ALBA
Masks used for performance optimization in every operation. `ProductMask.productMask().withState().withOwnVersion()` fetches only state for validation. `UserMask.userMask().withEmail().withIsActive()` for authentication checks. `ResultTypeMask.resultTypeMask().withName()` when bulk-fetching related entities for aggregation. Mask also used in `update()` calls: `productDao.update(product, ProductMask.productMask())`.

### mlszksz-platform
`UserMask.userMask().withEmail()` used in `LogAuthenticationInterceptor` for efficient user lookup during authentication. Minimal field loading in interceptors for performance-sensitive paths. Used across the 5 interceptors to load only the fields needed for their specific logic.

### Ubives
`AccountMask.accountMask().withUserName()` used in authentication interceptor for efficient user lookup. `AccountEntityMask.accountEntityMask()` used in init operations for existence checks. `OrganizationEntityMask.organizationEntityMask().withName()` for organization lookups. `InvitationEntityMask.invitationEntityMask()` for invitation queries. Consistent mask usage across all 7 services.

### ParkHere
`UserMask.userMask()` used in authentication interceptor and actor resolution. `ReservationMask.reservationMask().withReservationStatus()` for efficient status-only queries during holiday cancellation. `UserReservationMask` with specific fields (date, startTime, endTime, reserverName, parkingSlotInformation, reservationType, owner) for holiday conflict preview queries. Masks used consistently in `getById()` calls and `update()` calls across services.

### Indamedia-AdTrack
`UserMask.userMask().withEmail()` used in `LogAuthenticationInterceptor` for efficient user existence check during JIT provisioning. Minimal mask ensures only the email field is loaded from database when checking if user already exists before creation. Consistent with the pattern seen in other projects for authentication-path optimization.

### judo-partner
`PartnerMask.partnerMask().withNormalizedName().withIsArchived()` used in duplicate detection queries to minimize data transfer when scanning all partners with the same normalized name. `TaxpayerMask.taxpayerMask()` (empty mask) used in batch cache clearing to load only identifiers for deletion. Demonstrates combining mask with multi-filter queries for efficient bulk operations.

## Trade-offs

- Pros: Reduces data transfer, controls relation depth, type-safe field selection, prevents N+1 for nested relations
- Cons: Must explicitly include every needed field (easy to miss), empty mask behavior may be unintuitive, deeply nested masks are verbose
- Alternative: Load full entity without mask (simpler but less performant), GraphQL-style automatic field selection

## Related Patterns

- dao-fluent-query-filter
- mutable-entity-update-pattern
