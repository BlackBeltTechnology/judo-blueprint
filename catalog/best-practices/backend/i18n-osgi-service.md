---
id: i18n-osgi-service
title: I18n Service with ThreadLocal Locale and OSGi Proxy
description: "A type-safe backend i18n interface with one method per message, a properties file per locale, a thread-local locale supplier and an OSGi-registered proxy service, injected into services and operations for localized messages."
aliases: [backend i18n, localized messages, MessageByKey, locale supplier]
keywords: [i18n, service, threadlocal, locale, osgi, proxy]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "status:established"]
category: config
status: established
projects: [rackinspect, mlszksz-platform, park-here, indamedia-adtrack]
evidence: ["rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/i18n/RackInspectI18nActivator.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/i18n/MLSZKSZPlatformI18nActivator.java", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Error messages, validation messages, email subjects and document text must come out in the user's language. A typed i18n interface has one method per message. A properties file per locale holds the text, and services inject the interface instead of hard-coding strings.

## Practice

### Platform base

The platform docs describe the backend i18n service ([backend i18n guide](../../agent-docs/backend/internationalization-guide.md)): an i18n interface with one method per translation key (parameters allowed), injected into custom operations with `@Reference`, resolving the text at runtime for the user's language, with translations in properties files per locale. The runtime also localizes bean-validation messages through its `I18nService` and a `LocaleProvider` (falling back to the configured default locale). The docs advise: no hard-coded English strings, descriptive keys, parameters for dynamic values, messages organized by category.

The docs do not say how the interface is turned into a registered service or how the locale is chosen per request; they say the interface is "typically defined in your common utilities".

### Practice notes: annotation proxy plus thread-local locale

The examples add this wiring on top (all of it application code):

- The interface methods carry a message-by-key annotation and a proxy implementation reads the properties bundle for the current locale.
- A bundle activator registers the proxy as an OSGi service, so services receive it by `@Reference`.
- A locale supplier backed by an `InheritableThreadLocal<Locale>` holds the current locale (default set per application, for example a regional language). Child threads inherit it. Services that build text outside a request, such as email jobs, read it directly.
- Messages with parameters are methods with arguments.

```java
// Example code
public interface AppI18n {
    @MessageByKey String error_not_found();
    @MessageByKey String too_many_active_bookings(long num);
}

@Reference AppI18n i18n;
// ExceptionUtils is a helper of the example, not platform API
throw ExceptionUtils.createBusinessException(i18n.status_change_failed(), i18n.entity_must_be_active());
```

How the message reaches the client depends on the mechanism: field errors are `ValidationException` (HTTP 400) and business faults are modeled faults (HTTP 422), see [error handling](../../agent-docs/backend/error-handling-guide.md). An interceptor cannot throw a modeled fault ([interceptors](../../agent-docs/backend/interceptors.md)).

## Rationale

- Compile-time-checked message access and one place for all texts.
- The thread-local locale needs no locale argument on every service method, and child threads inherit it.
- Cost: a new message needs an interface method and a properties entry per locale; the activator is manual wiring; the locale of an already running thread is not switched; integration tests usually replace the service with a mock (see [[integration-test-reflection-injection]]).

## Example

- One application: an interface with many methods, a properties file for a second locale, a default locale supplier and an activator that registers the proxy. It is used for error messages and for boolean display values.
- One application: a platform-specific interface with parameterized methods (not-found messages, invalid date range) used for business error messages. Tests mock it with fixed English strings.
- One application: English default and a second-language bundle, parameterized messages, the locale supplier injected into several services, used for errors, email subjects and notifications.
- One application: a few messages in English and a second language, that language as default, used by several services for error messages.

## When to avoid

- Messages that only the frontend displays: use the frontend translation files instead.
- A single-language application with few messages.

## Related

- [[validation-exception-hierarchy]] — exceptions that carry the localized messages
- [[osgi-karaf-bundle-architecture]] — bundle activators and OSGi service registration
- [[integration-test-reflection-injection]] — mocking the i18n service in tests
