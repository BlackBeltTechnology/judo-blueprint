---
id: "external-api-adapter-pattern"
title: "External API Adapter with Factory Provider"
domain: "backend"
category: "integration"
score: 57.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - indamedia-adtrack
---
## Description

A multi-layer adapter pattern for integrating with external REST/gRPC APIs in a platform-agnostic way. Consists of: (1) a platform-agnostic business API interface defining operations, (2) platform-specific adapter implementations (e.g., Google Ads, Meta Ads), (3) a factory/provider service that selects the correct adapter based on configuration (e.g., account platform type), and (4) DTOs for transferring external data into the application domain. This cleanly separates external API concerns from business logic and supports adding new platforms without modifying existing code.

## Structure

```java
// 1. Platform-agnostic interface
public interface AdsBusinessApi {
    boolean isConnected(String customerId);
    List<CampaignInfo> getAllCampaignForCustomer(String customerId);
    CampaignCostInfo getCampaignCostToDate(String customerId, String campaignId, LocalDate upToDate);
}

// 2. Platform-specific implementation
public class GoogleAdsApiImpl implements AdsBusinessApi {
    public GoogleAdsApiImpl(String developerToken, String delegatedAccount,
                            Optional<String> loginCustomerId, String jsonKey) {
        // Initialize Google Ads client with credentials
    }

    @Override
    public List<CampaignInfo> getAllCampaignForCustomer(String customerId) {
        // Execute GAQL query, map to DTOs
    }
}

// 3. Factory/provider service
@Component(immediate = true, service = AdsBusinessApiProviderService.class)
public class AdsBusinessApiProviderServiceImpl implements AdsBusinessApiProviderService {
    @Reference FileStoreService fileStoreService;
    @Reference GoogleCredentialDao credentialDao;

    public AdsBusinessApi getAdsBusinessApi(Account account) throws BusinessErrorException {
        Platform platform = account.getPlatform();
        if (platform == Platform.GOOGLE) {
            // Retrieve credentials, create GoogleAdsApiImpl
            return new GoogleAdsApiImpl(developerToken, delegatedAccount, loginCustomerId, jsonKey);
        } else if (platform == Platform.META) {
            throw ExceptionUtils.createBusinessErrorException(PLATFORM_NOT_IMPLEMENTED, ...);
        }
    }
}

// 4. DTOs
public class CampaignCostInfo {
    String campaignId;
    BigDecimal totalSpendToDate;
    BigDecimal spendToday;
    LocalDateTime lastFetched;
}
```

## Examples

### Indamedia-AdTrack
`AdsBusinessApi` interface defines 7 methods for campaign discovery, connection testing, cost retrieval, and budget monitoring. `GoogleAdsApiImpl` implements it using Google Ads API v20 with GAQL queries, micro-currency conversion (`MICROS_IN_CURRENCY = 1_000_000L`), and streaming for large result sets. `AdsBusinessApiProviderServiceImpl` factory retrieves credentials from FileStore, creates `GoogleAdsApiImpl` instances, and returns platform-specific customer IDs. Supports Google (implemented) and Meta (placeholder with `PLATFORM_NOT_IMPLEMENTED` error). Three DTOs: `CampaignInfo`, `CampaignCostInfo`, `CampaignDailyInfo`.

## Trade-offs

- Pros: Clean separation of external API concerns, supports multiple platforms via single interface, testable (mock the interface), credential management isolated in provider
- Cons: Extra abstraction layers, new DTOs to maintain alongside model entities, provider factory grows with each platform
- Alternative: Direct API client usage in services (simpler but couples business logic to specific platform), OSGi service registry for automatic platform discovery

## Related Patterns

- service-delegation-pattern
- filestore-mediated-file-transfer
- facade-service-pattern
