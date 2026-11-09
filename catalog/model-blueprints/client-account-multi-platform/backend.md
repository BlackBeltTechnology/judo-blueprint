## Overview

The Client-Account-Campaign entity cluster is implemented through a layered service architecture: thin custom operation classes delegate to service interfaces (`ClientService`, `AccountService`, `AggregatedCampaignService`, `TrackedCampaignService`), which in turn use DAO classes for persistence and an `AdsBusinessApiProviderService` for external platform integration. Scheduler jobs automate recurring data synchronization and lifecycle management.

## Implementation Pattern

- **Thin custom operations**: Each `*CustomImplementation` class is an OSGi `@Component` that injects a domain service via `@Reference` and delegates to it in a single line (e.g., `accountService.setGoogleCredential(_this, input)`)
- **Service layer**: Domain services (`ClientService`, `AccountService`, `AggregatedCampaignService`, `TrackedCampaignService`) are interfaces with OSGi `@Component` implementations. They encapsulate business logic, entity creation, and cross-entity orchestration
- **Platform adapter abstraction**: An `AdsBusinessApi` interface defines platform-agnostic operations (isConnected, getAllCampaignForCustomer, getCampaignCostToDate). `AdsBusinessApiProviderService` acts as a factory, dispatching on the `Platform` enum to instantiate the correct adapter (e.g., `GoogleAdsApiImpl`)
- **DAO pattern**: Operations use both entity DAOs (for direct entity manipulation) and transfer DAOs (for mapped transfer objects). Entity lookup failures throw `BusinessErrorException` with specific `ErrorCode` values
- **Scheduler integration**: Three `Runnable` OSGi components handle automated tasks: fetching campaign costs, resetting daily attributes, and archiving expired campaigns. They inject the same service interfaces used by custom operations
- **Cascade operations**: Delete and untrack operations cascade through related entities (history, costs, fetched data) before removing the parent

## Examples

### indamedia-adtrack
- Key files: `custom/.../accounttransfer/SetGoogleCredentialCustomImplementation.java`, `custom/.../aggregatedcampaigntransfer/CreateTrackedCampaignCustomImplementation.java`, `common/impl/AccountServiceImpl.java`, `common/impl/TrackedCampaignServiceImpl.java`, `common/impl/AggregatedCampaignServiceImpl.java`, `common/AdsBusinessApiProviderService.java`
- Pattern: Custom operations delegate to service layer; `AccountServiceImpl` handles credential CRUD and campaign discovery via `AdsBusinessApiProviderService`; `TrackedCampaignServiceImpl` syncs costs from external APIs and manages Cost/FetchedData entities; `AggregatedCampaignServiceImpl` orchestrates budget recalculation across tracked campaigns
- Notable: The `syncAvailableCampaigns` operation discovers campaigns from the external platform and creates `AvailableCampaign` entities for campaigns not yet tracked. Budget recalculation aggregates `totalSpend` and `todaySumSpend` across all tracked campaigns within an aggregated campaign. Cascade delete removes history, costs, fetched data, and unlinks available campaigns before deleting the parent entity.
