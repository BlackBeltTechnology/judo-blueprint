---
id: "mutable-entity-update-pattern"
title: "Mutable Entity Update Pattern"
domain: "backend"
category: "data-access"
score: 61.8
usage_count: 9
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - alba
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
---
## Description

Entities returned by DAO queries are mutable objects. Updates are performed by modifying fields directly on the returned entity object via setter methods, then calling `dao.update(entity)` to persist. This is a simple but effective pattern for in-place modifications without needing a separate update DTO.

## Structure

```java
// Fetch entity
Entity entity = entityDao.getById(id).get();

// Modify fields
entity.setStatus(NewStatus.VALUE);
entity.setTimestamp(LocalDateTime.now());
entity.setField(null);  // Clear a field

// Persist changes
entityDao.update(entity);
```

Note: No mask is used in this pattern (updates all fields). For partial updates, use `entityDao.update(entity, EntityMask.entityMask().withField())`.

## Examples

### Trivia
Used extensively: `user.get().setTmpCode(null); user.get().setCode(input.getCode()); userDao.update(user.get())` in Activate. `_this.setStatus(TestStatus.FINISHED); _this.setDuration(duration); testDao.update(_this)` in Submit. Direct setter mutation followed by DAO update call.

### RackInspect
Toggle operations use masked updates: `thiss.setActive(!thiss.getActive()); addressDao.update(thiss, AddressMask.addressMask());`. Permission recalculation uses dirty-checking before update: compares `user.toMap()` before and after changes to avoid unnecessary writes.

### ALBA
State transitions use setter + masked update: `product.setState(ProductState.FINALIZED); productDao.update(product, ProductMask.productMask())`. Batch rollback in ApproveVersion iterates approved versions: `for (Product p : approved) { p.setState(ProductState.FINALIZED); productDao.update(p); }`.

### mlszksz-platform
User lastLogin update in interceptor: `user.setLastLogin(LocalDateTime.now()); userDao.update(user)`. Post lifecycle: `offer.setStatus(PostStatus.PUBLISHED); offer.setPublishedAt(LocalDateTime.now()); offerDao.update(offer)`. Configuration update: fetch single config entity, set fields from input (with null-safe Optional handling), then `configurationDao.update(config)`.

### Ubives
Organization registration toggle: `org.setIsRegistrationFeatureSupported(false); organizationDao.update(org, mask)`. Access role change: `access.setOrganizationAccessType(accessType); accessDao.update(access, mask)`. User enable/disable: `user.setEnabled(enabled); userDao.update(user, mask)`. All service methods follow the fetch-mutate-update cycle with masks.

### ParkHere
Reservation state changes: `reservation.setReservationStatus(ReservationStatus.EXPIRED); reservation.setEndTime(LocalTime.now()); reservation.setModified(LocalDateTime.now(Clock.systemUTC())); reservation.setModifiedBy(currentUser.getName()); reservationDao.update(reservation)`. Car archival: `car.setIsFavorite(false); car.setIsArchived(true); carDao.update(car)`. Holiday cancellation loops update each reservation's status to DELETED with masked update.

### Indamedia-AdTrack
Account updates: `account.setPlatform(input.getPlatform()); account.setIsActive(input.getIsActive()); accountTransferDao.update(account)`. Campaign updates: `campaign.setName(input.getName()); campaign.setTotalBudget(input.getTotalBudget()); campaign.setRemainingBudget(...); aggregatedCampaignTransferDao.update(campaign)`. Tracked campaign cost updates: `trackedCampaign.setTodaySpend(costInfo.getSpendToday()); trackedCampaign.setTotalCost(costInfo.getTotalSpendToDate()); trackedCampaignTransferDao.update(trackedCampaign)`.

### judo-partner
Partner soft delete: `partner.setTaxIdentifier(null); partner.setIsArchived(true); partnerDao.update(partner)`. Validation status updates: `partner.setValidationStatus(ValidationStatus.FAILED); partner.setValidationError(errorCode); partnerDao.update(partner)`. Batch duplicate detection: iterates all matching partners, sets `isDuplicateName` flag, then `partnerDao.updateAll(duplicates)` for batch persistence.

### workflow-poc
Context label update: `context.setLabel(input.getLabel().get()); contextDao.update(context)`. Event processing: `event.setProcessed(true); eventDao.update(event)`. Workflow version metadata: `workflowVersion.setModel(model); workflowVersion.setDiagram(diagramUtils.getDiagram(workflowVersion)); workflowVersion.setUploadTime(LocalDateTime.now()); workflowVersionDao.update(workflowVersion)`. Token timestamp: `_this.setTimestamp(LocalDateTime.now()); tokenDao.update(_this)`.

## Trade-offs

- Pros: Simple, intuitive, no separate update DTO needed, supports clearing fields via null
- Cons: Updates all fields (no partial update without mask), mutable objects can lead to accidental state changes
- Alternative: Masked updates via `dao.update(entity, mask)` for partial field updates (more performant)

## Related Patterns

- builder-pattern-entity-creation
- dao-fluent-query-filter
- mask-field-projection
