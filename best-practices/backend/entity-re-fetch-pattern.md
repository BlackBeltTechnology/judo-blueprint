---
id: "entity-re-fetch-pattern"
title: "Entity Re-fetch at Operation Start"
domain: "backend"
category: "operation"
score: 61.8
usage_count: 8
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - alba
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
---
## Description

In bound custom operations, the `_this` parameter is re-fetched from the database at the very start of the method. This ensures the operation works with the latest persisted state rather than potentially stale data from the caller. This is a recurring pattern across every bound operation in the trivia project.

## Structure

```java
@Override
public ReturnType apply(EntityType _this, InputType input) {
    // Re-fetch from DB to get fresh data
    _this = entityDao.getById(_this.identifier()).get();
    // ... proceed with business logic on fresh entity
}
```

The pattern always appears as the first line of bound operations. It uses `identifier()` to extract the entity's ID and `getById()` to load the full current state.

## Examples

### Trivia
All 4 bound operations (Enter, Start, Submit, Exclude) re-fetch at start: `_this = testDao.getById(_this.identifier()).get()` or `contest = contestDao.getById(contest.identifier()).get()`. EnterCustomImplementation re-fetches the Contest; Start/Submit/Exclude re-fetch the Test.

### RackInspect
All 24 toggle operations re-fetch with `orElseThrow()`: `Address thiss = addressDao.getById(_this.identifier()).orElseThrow();`. RackInspect prefers `orElseThrow()` over `.get()`, providing a safer null-handling approach compared to Trivia's `.get()`.

### ALBA
All bound product operations re-fetch with mask and `adaptTo()`: `productDao.getById(_this.identifier().adaptTo(ProductIdentifier.class), ProductMask.productMask().withState()).orElseThrow()`. Combines re-fetch with identifier adaptation and mask projection in a single call for efficiency.

### mlszksz-platform
Organization lookups use `organizationDao.getById(_this.identifier().getIdentifier()).orElseThrow()`. Post operations use `_this.adaptTo(Offer.class)` to convert transfer objects for service delegation. The re-fetch is often done inside the delegated service rather than in the custom operation itself, as part of the service-delegation pattern.

### ParkHere
Re-fetch done at service level: `reservationDao.getById(preservation.identifier().getIdentifier()).orElseThrow()` in `ReservationService.reservationIsCancelable()`, `reservationIsDeletable()`, and `reservationIsModifiable()`. `userDao.getById(_this.identifier().getIdentifier()).orElseThrow()` in `CreateCarCustomImplementation`. All use `.orElseThrow()` with typed `BusinessErrorException` for safe null handling.

### Indamedia-AdTrack
Re-fetch done at service level: `accountTransferDao.getById(accountInstance.identifier().getIdentifier()).orElseThrow()` in `AccountServiceImpl.getAccount()`. `clientTransferDao.getById(clientInstance.identifier().getIdentifier()).orElseThrow()` in `ClientServiceImpl`. All service methods re-fetch entities and throw `BusinessErrorException` with localized i18n messages on not-found via `ExceptionUtils.createBusinessErrorException()`.

### judo-partner
Re-fetch done in service methods: `partnerDao.getById(partner.identifier()).get()` in `PartnerServices.deletePartner()`. `taxpayerDao.getById(taxpayer.identifier().getIdentifier()).orElseThrow()` in `PartnerServices.getPartnerByTaxpayer()`. `taxpayerAddressDao.getById(taxpayerAddress.identifier()).orElseThrow()` in `addAddressToPartner()`. Also in interceptor: `partnerDao.getById(UUID.fromString(payload.get("__identifier").toString())).orElseThrow()` in `PartnerUpdateInterceptor.postCall()`.

### workflow-poc
Re-fetch used in multiple contexts: `workflowDao.getById(_this.identifier()).get()` in `UploadCustomImplementation` (twice -- once at start and once after version deletion to refresh state). `tokenDao.getById(_this.identifier()).get()` in `TriggerCustomImplementation` before processing events. `workflowVersionDao.getById(_this.identifier()).get()` in `DiagramUtils` at start of diagram generation. All use `.get()` rather than `.orElseThrow()`.

## Trade-offs

- Pros: Guarantees fresh data, prevents stale-state bugs, simple one-liner
- Cons: Adds an extra database round-trip per operation call, `.get()` on Optional without guard can throw NoSuchElementException
- Alternative: Trust the dispatcher-provided data (risky if other operations mutate concurrently)

## Related Patterns

- dao-fluent-query-filter
- state-lifecycle-operation
