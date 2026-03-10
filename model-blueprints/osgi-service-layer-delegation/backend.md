## Overview

Implements a multi-module service layer where custom operations delegate to shared OSGi service interfaces defined in a `common` module. Service implementations live in the module closest to their concern (common, keycloak-client, firebase), and OSGi Declarative Services wires them together at runtime.

## Implementation Pattern

**Module structure:**
```
application/
  common/          -- service interfaces + implementations for core business logic
  keycloak-client/ -- implementations for Keycloak-specific services
  firebase/        -- implementations for Firebase-specific services
  adapters/        -- external API adapter interfaces + implementations
  app/custom/      -- custom operation classes that @Reference service interfaces
  scheduler/       -- scheduled jobs that @Reference service interfaces
  interceptors/    -- interceptors that @Reference service interfaces
```

**Interface definition (common module):**
- Service interfaces are plain Java interfaces in the `common` module (e.g., `PushNotificationService`, `KeycloakUserService`, `PlatformEmailService`, `FeedService`, `AuditLogService`, `ValidationService`)
- No OSGi annotations on the interface -- only the implementation carries `@Component(service=...)`
- Methods are coarse-grained business operations, not CRUD (e.g., `sendPostPublishedNotification()`, not `createNotification()`)

**Implementation (various modules):**
- `@Component(immediate=true, service=<Interface>.class)` with `@Reference` to DAOs, other services, and external clients
- Implementation location follows the "closest concern" principle: `PushNotificationServiceImpl` in common (uses Firebase + DAOs), `KeycloakUserServiceImpl` in keycloak-client (uses RealmManager), `FirebaseMessagingService` in firebase (wraps Firebase SDK)

**Custom operation consumption:**
- Custom operation classes `@Reference` the service interface (never the implementation)
- Operations become thin controllers: validate input, call service, map result
- Multiple operations across different actors can share the same service (e.g., both admin and company-admin publish operations call `FeedService.createFeedEntry()`)

**Service layering:**
- Services can reference other services: `FeedServiceImpl` references `PlatformEmailService` and `PushNotificationService`
- Services reference DAOs from the generated SDK: `@Reference UserDao`, `@Reference NotificationDao`
- External integration services (Keycloak, Firebase) are behind stable interfaces, making them swappable for testing

**i18n sub-pattern:**
- A method-per-message interface (e.g., `AdTrackI18n`, `RackInspectI18n`) registered via `I18nService` with a `ThreadLocalLocaleSupplier` for request-scoped locale
- Services `@Reference` the i18n interface to produce localized error messages for `BusinessErrorException`
- An activator component (`@Component(immediate=true)`) calls `i18nService.register(I18nInterface.class, localeSupplier)` on activation and `unregister()` on deactivation

## Examples

### mlszksz-platform
- Key files: `common/services/` (15 service interfaces), `common/services/impl/` (15 implementations), `keycloak-client/osgi/KeycloakUserServiceImpl.java`, `firebase/FirebaseMessagingService.java`
- Pattern: 15+ shared service interfaces in `common/services/`: `PushNotificationService`, `FeedService`, `PostService`, `PostLifecycleService`, `PostCreationService`, `RequestPostService`, `RegistrationService`, `InvitationService`, `AdminInvitationService`, `OrganizationService`, `UserService`, `MasterDataService`, `InquiryService`, `ValidationService`, `AuditLogService`, `ConfigurationTemplateService`, `PlatformEmailService`, `KeycloakUserService`, `MagicLinkService`, `ForgotPasswordService`
- Notable: Post operations are decomposed into three services: `PostCreationService` (creates entity + assigns to organization), `PostLifecycleService` (publish/delete/expire transitions), `RequestPostService` (user-initiated post requests). The `FeedService` uses strategy objects (`AllActiveOrganizationsTargetingStrategy`, `RequestTargetingStrategy`) for feed targeting rules.
- DI wiring: Custom operations in `app/custom/` `@Reference` service interfaces -> service implementations `@Reference` DAOs and other services -> external modules (`keycloak-client`, `firebase`) implement specific interfaces

### rackinspect
- Key files: `common/utils/services/` (13 service interfaces), `common/utils/services/impl/` (13 implementations), `common/services/` (5 additional service interfaces), `mnb-soap-client/` (external SOAP integration module)
- Pattern: 18+ shared service interfaces split across two packages: `common/utils/services/` for cross-cutting utilities (`ReportService`, `EmailSenderService`, `DocumentConversionService`, `PdfWatermarkService`, `ConfigurationTemplateService`, `HistoryService`, `CostPriceService`, `PriceService`, `PriceModifierService`, `OfferService`, `OfferItemService`, `FaultRegistryService`, `RegistryService`, `JobTaskService`, `ItemService`, `ActorService`) and `common/services/` for domain-specific calculation services (`DimensionService`, `DimensionInterceptorService`, `WarehouseService`, `RackService`, `AddressService`).
- Notable: Services are organized in two tiers -- utility services in `common/utils/services/` (each with interface + impl) and domain calculation services in `common/services/` (some are static utility classes). The `ReportService` orchestrates a complex document generation pipeline referencing 10+ DAOs and 4 other services. An `i18n` sub-package provides `RackInspectI18n` (method-per-message interface registered via `I18nService`) with `ThreadLocalLocaleSupplier` for request-scoped locale.
- DI wiring: Custom operations `@Reference` service interfaces -> `ReportServiceImpl` `@Reference` `ConfigurationTemplateService`, `PdfWatermarkService`, `DocumentConversionService`, `HistoryService`, `RegistryService` + multiple DAOs -> `ExchangeRateService` in `mnb-soap-client` module consumed by scheduler jobs

### indamedia-adtrack
- Key files: `common/AccountService.java`, `ActorService.java`, `AggregatedCampaignService.java`, `ClientService.java`, `TrackedCampaignService.java`, `AdsBusinessApiProviderService.java` (6 service interfaces), `common/impl/` (6 implementations), `common/i18n/AdTrackI18n.java`, `common/i18n/AdTrackI18nActivator.java`, `common/i18n/ThreadLocalLocaleSupplier.java`, `common/utils/ExceptionUtils.java`
- Pattern: 6 shared service interfaces in `common/` with matching implementations in `common/impl/`. Custom operations in `app/custom/` are thin one-liner delegators (e.g., `TestConnectionCustomImplementation` calls `accountService.testConnection(_this)`). Services reference other services (e.g., `AggregatedCampaignServiceImpl` references `TrackedCampaignService`) and the external API provider (`AdsBusinessApiProviderService`).
- Notable: The `AdsBusinessApiProviderService` acts as a factory for external API adapters (see `external-api-adapter-provider-pattern` blueprint). `ExceptionUtils` is a static utility interface with factory methods for `BusinessErrorException` and `ValidationException`. The `AdTrackI18n` interface uses `@MessageByKey` annotation for a generic `getMessage(key, params)` method alongside method-per-message methods. Properties files provide English default and Hungarian (`_hu`) translations.
- DI wiring: Custom operations `@Reference` service interfaces (e.g., `AccountService`, `TrackedCampaignService`). Service implementations `@Reference` DAOs, `AdTrackI18n`, `FileStoreService`, `AdsBusinessApiProviderService`, and other services. `ActorServiceImpl` `@Reference VariableResolver` to resolve the current authenticated user's email.
