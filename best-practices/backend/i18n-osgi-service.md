---
id: "i18n-osgi-service"
title: "I18n Service with ThreadLocal Locale and OSGi Proxy"
domain: "backend"
category: "config"
score: 68.4
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
---
## Description

An internationalization infrastructure using: (1) an interface with `@MessageByKey` annotated methods for all translatable messages, (2) a properties file per locale, (3) an `InheritableThreadLocal` locale supplier for thread-safe locale resolution, and (4) an OSGi BundleActivator that registers a proxy-based i18n service. Services inject the i18n interface to get localized messages for error messages, document content, and UI labels.

## Structure

```java
// I18n interface
public interface AppI18n {
    @MessageByKey String error_not_found();
    @MessageByKey String validation_required_field();
    // 100+ methods
}

// ThreadLocal locale supplier
public class ThreadLocalLocaleSupplier {
    private static final InheritableThreadLocal<Locale> locale =
        new InheritableThreadLocal<>() {
            @Override protected Locale initialValue() { return new Locale("hu"); }
        };
}

// Usage in services
@Reference AppI18n i18n;
throw ExceptionUtils.createBusinessErrorException("NOT_FOUND", i18n.error_not_found());
```

## Examples

### RackInspect
`RackInspectI18n` interface with 100+ `@MessageByKey` methods. `RackInspectI18n_hu.properties` contains all Hungarian translations. `ThreadLocalLocaleSupplier` defaults to Hungarian locale. `RackInspectI18nActivator` (BundleActivator) registers the proxy service. Used throughout services for error messages and in `DimensionService` for boolean display values ("Igen"/"Nem").

### mlszksz-platform
`MLSZKSZPlatformI18n` interface with methods like `user_not_found()`, `post_not_draft()`, `entity_not_found(entityType, id)`, `invalid_date_range(from, to)`. Registered via `MLSZKSZPlatformI18nActivator`. Used across all services for BusinessErrorException messages. Mocked in integration tests with hardcoded English strings.

### ParkHere
`ParkHereI18n` interface with abstract methods including parameterized messages: `user_not_found()`, `too_many_active_reservations(long num)`, `reservation_doorman_notification_title(String formattedDate)`. Properties files for English (default) and Hungarian (`ParkHereI18n_hu.properties`). `ThreadLocalLocaleSupplier` injected into all 7 service implementations. Used for all error messages, email subjects, and notification content.

### Indamedia-AdTrack
`AdTrackI18n` interface with 8 message methods including parameterized: `logged_in_user_not_found()`, `client_not_found()`, `account_not_found()`, `campaign_not_found()`, `credential_not_set()`, `connection_failed_to_google_ads()`, `platform_not_supported(String)`, `platform_not_implemented(String)`. English and Hungarian (`AdTrackI18n_hu.properties`) bundles. Registered via `AdTrackI18nActivator`. Default locale: Hungarian. Used across all 6 service implementations for error messages.

## Trade-offs

- Pros: Type-safe message access (compile-time checked), thread-safe locale, standard ResourceBundle backend, inherited by child threads
- Cons: New message requires both interface method and properties entry, BundleActivator is manual wiring, no runtime language switching for existing threads
- Alternative: Direct ResourceBundle usage, Spring MessageSource, or external i18n library

## Related Patterns

- validation-exception-hierarchy
- osgi-karaf-bundle-architecture
