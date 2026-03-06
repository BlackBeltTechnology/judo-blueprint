---
id: "service-delegation-pattern"
title: "Service Delegation from Custom Operations"
domain: "backend"
category: "service"
score: 64.2
usage_count: 6
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
---
## Description

Custom operations act as thin OSGi wrappers that delegate all business logic to shared service classes. The custom operation handles only the SDK interface contract (method signature, exceptions), while complex logic lives in reusable, testable service implementations. This separation enables: (1) sharing logic across multiple operations, (2) unit testing without OSGi, (3) clean layered architecture.

## Structure

```java
@Component(immediate = true, service = OperationInterface.class)
public class OperationCustomImplementation implements OperationInterface {
    @Reference SharedService sharedService;

    @Override
    public ReturnType method(Entity _this, Input input) throws BusinessErrorException {
        return sharedService.doBusinessLogic(_this, input);
    }
}
```

Service implementation (in `common/` module):
```java
@Component(immediate = true, service = SharedService.class)
public class SharedServiceImpl implements SharedService {
    @Reference EntityDao entityDao;
    @Reference OtherService otherService;

    public ReturnType doBusinessLogic(Entity entity, Input input) {
        // Complex business logic here
    }
}
```

## Examples

### RackInspect
~80% of custom operations delegate to 12 shared services: `OfferService` (offer lifecycle), `FaultRegistryService` (registry CRUD), `ItemService` (item management), `PriceModifierService` (pricing), `JobTaskService` (job tasks), `ReportService` (document generation), `EmailSenderService` (emails), `WarehouseService` (racks). Example: `CloseOfferCustomImplementation` is one line: `offerService.closeOffer(_this);`.

### mlszksz-platform
65+ operations delegate to 15+ services: PostService (facade for creation+lifecycle), FeedService (feed management), UserService, InvitationService, RegistrationService, MasterDataService, AuditLogService, etc. Each operation is 5-10 lines: delegate to service, then log audit trail. Example: `postService.publishOffer(_this); auditLogService.log(...)`.

### Ubives
42 custom operations delegate to 7 services: OrganizationService, ApplicationService, InviteService, AccessService, UserService, AccountService, MailServices. Operations are pure one-liners: `applicationService.createApplication((UUID) _this.identifier().getIdentifier(), input.getName())`. Same operation repeated across multiple actor views (dashboardorganization, organization, partnerdashboard, profile).

### ParkHere
20 custom operations delegate to 7 services: ReservationService (validation + creation + modification), CarService (favorite logic), HolidayService (validation + creation + cancellation), ActorService (permission checks), ConfigurationService, DateService, EmailSenderService. Example: `ReservationCustomImplementation` is two lines: `reservationService.validateInput(input); reservationService.createReservation(input);`.

### Indamedia-AdTrack
17 custom operations delegate to 6 services: `AccountService` (credential management, campaign sync, connection testing), `AggregatedCampaignService` (budget tracking, spending aggregation), `TrackedCampaignService` (data sync from Google Ads), `ClientService` (CRUD), `AdsBusinessApiProviderService` (API client factory). All operations are 1-3 line delegates. Example: `UntrackCustomImplementation` calls `trackedCampaignService.untrackCampaign(_this)` then `aggregatedCampaignService.recalculateSpendings()`.

### judo-partner
15 custom operations delegate to 7 services: `PartnerServices` (partner CRUD, tax validation, duplicate detection), `TaxpayerServices` (NAV API caching), `ImportPartnerServices` (migration pipeline), `AddressServices`/`ContactServices` (set-as-primary logic), `ConfigServices` (cache clearing), `CountryServices` (country import). Example: `CreatePartnerCustomImplementation` calls `partnerServices.createPartner(input)` then logs the action via `PartnerLog`.

## Trade-offs

- Pros: Reusable business logic, testable without OSGi, clean separation of concerns, reduces code duplication
- Cons: Extra layer of indirection, service interfaces must be maintained, harder to trace call flow
- Alternative: Put all logic directly in custom operations (simpler for small projects, but does not scale)

## Related Patterns

- custom-operation-osgi-component
- test-data-builder-factory
