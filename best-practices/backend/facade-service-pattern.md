---
id: "facade-service-pattern"
title: "Facade Service Pattern for Domain Operations"
domain: "backend"
category: "service"
score: 68.6
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
---
## Description

A Facade service that provides a unified interface for a domain's operations while delegating to specialized sub-services internally. Custom operations inject only the facade, which dispatches to the appropriate sub-service (e.g., PostCreationService or PostLifecycleService). This simplifies the dependency graph for operations while allowing complex domains to be decomposed into focused, testable services.

## Structure

```java
// Facade interface
public interface PostService {
    News createNews(NewsInput input, Organization org);
    void publishNews(News news);
    void deleteNews(News news);
    void editNews(News news, NewsInput input);
    // ... similar methods for Offer, Request
}

// Facade implementation delegates to sub-services
@Component(immediate = true, service = PostService.class)
public class PostServiceImpl implements PostService {
    @Reference PostCreationService creationService;
    @Reference PostLifecycleService lifecycleService;

    @Override
    public News createNews(NewsInput input, Organization org) {
        return creationService.createNews(input, org);
    }

    @Override
    public void publishNews(News news) {
        lifecycleService.publishNews(news);
    }
}

// Sub-service handles specific concern
@Component(immediate = true, service = PostCreationService.class)
public class PostCreationServiceImpl implements PostCreationService {
    @Reference ActorService actorService;
    @Reference ValidationService validationService;
    @Reference NewsDao newsDao;
    // Creation logic with validation and author assignment
}
```

## Examples

### mlszksz-platform
`PostService` facade delegates to `PostCreationService` (creation with validation, author assignment, capability handling) and `PostLifecycleService` (publish/delete/expire/edit with status transitions and feed management). Custom operations like `PublishCustomImplementation` inject only `PostService`. This decomposes a 20+ method domain into two focused sub-services while presenting a single interface to callers.

### ParkHere
`ReservationService` acts as a large facade with 280+ lines of validation logic, creation for 4 reservation types (NORMAL, QUICK, GUEST, LONG), modification, cancellation, and deletion. Coordinates between 12 injected dependencies (UserDao, ParkingSlotDao, EmailSenderService, DoormanDao, ReservationDao, FileStoreService, ConfigurationDao, ActorService, DateService, ParkHereI18n, ThreadLocalLocaleSupplier). Custom operations are 2-3 line delegates: `reservationService.validateInput(input); reservationService.createReservation(input);`.

### Indamedia-AdTrack
`AggregatedCampaignService` acts as a facade orchestrating campaign lifecycle. Delegates to `TrackedCampaignService` for individual campaign data sync, coordinates spending recalculation across all tracked campaigns, manages history snapshots, and handles scheduled operations (daily reset, daily archive, periodic fetch). Custom operations inject only `AggregatedCampaignService` for campaign group operations. Example: `SyncDataCustomImplementation` calls `aggregatedCampaignService.fetchSpendings()` which internally iterates all tracked campaigns via `TrackedCampaignService`.

## Trade-offs

- Pros: Simplified dependency graph for callers, focused sub-services with single responsibility, testable in isolation, clean API surface
- Cons: Extra indirection layer, facade methods are pure pass-through, facade interface must be maintained alongside sub-service interfaces
- Alternative: Direct injection of sub-services by callers (simpler but more coupling), single monolithic service (simpler but harder to maintain)

## Related Patterns

- service-delegation-pattern
- custom-operation-osgi-component
- state-lifecycle-operation
