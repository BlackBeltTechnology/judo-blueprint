## Overview

Implements a pluggable external API adapter pattern using separate Maven modules for the API interface, platform-specific implementations, and a factory/provider OSGi service. The provider service resolves the correct adapter at runtime based on entity state (e.g., platform enum) and supplies it with credentials loaded from the database.

## Implementation Pattern

**Module structure:**
```
application/
  adapters/
    ads-business-api/   -- API interface + DTOs (standalone OSGi bundle, no JUDO dependencies)
    google-ads/         -- Google Ads adapter implementation (depends on API module + Google SDK)
    meta-ads/           -- (future) Meta Ads adapter implementation
  common/
    XxxProviderService.java       -- Provider interface
    impl/XxxProviderServiceImpl.java  -- Factory that resolves adapter by platform
  app/custom/           -- Custom operations that @Reference the provider service
```

**API interface module:**
- A plain Java interface (e.g., `AdsBusinessApi`) with business-oriented methods returning DTOs
- DTO classes use the builder pattern (hand-written or Lombok) -- they are decoupled from JUDO transfer objects
- No OSGi annotations, no JUDO SDK dependencies -- this bundle is a pure API contract
- Packaged as an OSGi `bundle` with `maven-bundle-plugin`

**Adapter implementation module(s):**
- Each module implements the API interface using a specific external SDK (e.g., `GoogleAdsApiImpl implements GoogleAdsApi extends AdsBusinessApi`)
- The implementation class is a plain POJO (not an OSGi component) -- it is instantiated by the provider service with runtime credentials
- Constructor accepts credential parameters (tokens, keys, customer IDs) and initializes the SDK client
- Methods translate between external SDK types and the shared DTO types

**Provider service (factory):**
- An OSGi `@Component(service=XxxProviderService.class)` in the `common` module
- `@Reference` injects DAOs to load entity data (account, credentials) and `FileStoreService` for binary credentials (e.g., JSON key files)
- The `getApi(entityInstance)` method: (1) loads the entity, (2) reads the platform enum, (3) fetches platform-specific credentials, (4) constructs and returns the appropriate adapter instance
- Uses a `switch`/`if-else` on the platform enum to dispatch to the correct adapter constructor
- Throws `BusinessErrorException` with i18n error messages for unsupported or not-yet-implemented platforms

**Consumption pattern:**
- Custom operations and shared services `@Reference` the provider service (never the adapter directly)
- Typical usage: `AdsBusinessApi api = providerService.getApi(account); api.doSomething(customerId);`
- The provider service also provides helper methods (e.g., `getCustomerId()`) that extract platform-specific identifiers

**Error handling:**
- Connection failures are caught and wrapped in `BusinessErrorException` with i18n messages
- The API interface methods may throw platform-specific exceptions; callers wrap them in business errors

## Examples

### indamedia-adtrack
- Key files: `adapters/ads-business-api/AdsBusinessApi.java` (interface), `adapters/ads-business-api/dto/CampaignInfo.java`, `CampaignCostInfo.java`, `CampaignDailyInfo.java` (DTOs), `adapters/google-ads/GoogleAdsApiImpl.java` (Google Ads adapter), `common/AdsBusinessApiProviderService.java` (provider interface), `common/impl/AdsBusinessApiProviderServiceImpl.java` (provider factory)
- Pattern: `AdsBusinessApi` defines 7 methods (getAccountInformation, isConnected, getAllCampaignForCustomer, getCampaignBudgetAndUsage, getCampaignHistory, getCampaignCostToDate, getCampaignDetails). `GoogleAdsApiImpl` is a POJO constructed with developer token, delegated account, optional login customer ID, and JSON key. `AdsBusinessApiProviderServiceImpl` is an OSGi `@Component` that switches on `Platform` enum (GOOGLE/META) to construct the correct adapter.
- Notable: The Google Ads adapter uses `GoogleAdsClient` from the Google Ads Java SDK v20 with service account OAuth2 credentials. The provider loads the JSON key file via `FileStoreService` and converts it to a string for the adapter constructor. Meta platform is declared but throws a "not implemented" error -- demonstrating the extensibility point. A `GoogleAdServiceManagerTestActivator` component exists for manual API testing during development (disabled by default via `-1L` customer ID sentinel).
- DI wiring: `AdsBusinessApiProviderServiceImpl` `@Reference AccountDao`, `GoogleCredentialDao`, `AdTrackI18n`, `FileStoreService`. Custom operations and services `@Reference AdsBusinessApiProviderService` (never the adapter directly). `TrackedCampaignServiceImpl` and `AccountServiceImpl` both consume the provider service for API calls.
