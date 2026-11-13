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
- Operations become thin controllers: validate input, call service, map result. Interceptors do not run for custom operations (platform), so write rules and permission checks in the service or operation
- Multiple operations across different actors can share the same service (e.g., both admin and company-admin publish operations call `FeedService.createFeedEntry()`)

**Service layering:**
- Services can reference other services: `FeedServiceImpl` references `PlatformEmailService` and `PushNotificationService`
- Services reference DAOs from the generated SDK: `@Reference UserDao`, `@Reference NotificationDao`
- External integration services (Keycloak, Firebase) are behind stable interfaces, making them swappable for testing

**i18n sub-pattern:**
- A method-per-message interface (e.g., `<Project>I18n`) registered via `I18nService` with a `ThreadLocalLocaleSupplier` for request-scoped locale
- Services `@Reference` the i18n interface to produce localized messages for modeled faults and validation errors (the fault exception class is generated per project; helpers such as `ExceptionUtils` are example project code, not platform API)
- An activator component (`@Component(immediate=true)`) calls `i18nService.register(I18nInterface.class, localeSupplier)` on activation and `unregister()` on deactivation

## Examples

### Example (project code)
- Pattern: one shared service package with an interface and an implementation per concern, covering push notifications, feeds, posts, registration, invitations, organizations, users, master data, validation, audit logs, configuration templates, email and identity-provider access.
- Notable: Post operations are decomposed into three services: creation (creates the entity and assigns it to an organization), lifecycle (publish, delete and expire transitions), and user-initiated requests. The feed service uses strategy objects for targeting rules.
- DI wiring: Custom operations in the app custom package `@Reference` service interfaces -> service implementations `@Reference` DAOs and other services -> external modules implement specific interfaces

### Example (project code)
- Pattern: shared utility services in one package and domain calculation services in another, with cross-cutting services such as reporting, email, document conversion, PDF watermarking, configuration templates, history, pricing, offers, registry and jobs.
- Notable: Services are organized in two tiers, utility services (each with interface and implementation) and domain calculation services (some are static utility classes). The report service orchestrates a document generation pipeline that references many DAOs and other services. An `i18n` sub-package provides a method-per-message interface registered via `I18nService` with `ThreadLocalLocaleSupplier` for request-scoped locale.
- DI wiring: Custom operations `@Reference` service interfaces -> report service implementation `@Reference` configuration, document and history services plus multiple DAOs -> an external-rate service in a separate SOAP client module, consumed by scheduler jobs

### Example (project code)
- Pattern: shared service interfaces in one package with matching implementations. Custom operations in the app custom package are thin one-liner delegators (for example, a connection test calls the account service). Services reference other services and an external API provider.
- Notable: The provider service acts as a factory for external API adapters (see `external-api-adapter-provider-pattern` blueprint). An exception helper (project code, not platform API) wraps the project's generated fault exception and the platform `ValidationException`. The i18n interface uses a `@MessageByKey` annotation for a generic `getMessage(key, params)` method alongside method-per-message methods. Properties files provide an English default and further locale translations.
- DI wiring: Custom operations `@Reference` service interfaces (e.g., an account service). Service implementations `@Reference` DAOs, the i18n interface, a file store service, the API provider service, and other services. The actor service `@Reference`s `VariableResolver` to resolve the current authenticated user's email.
