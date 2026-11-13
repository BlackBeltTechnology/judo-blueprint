---
id: jaxb-external-api-client
title: JAXB-Based External API Client with Response Caching
description: "An external XML API client built from JAXB classes generated from the provider's XSD schemas, in its own OSGi bundle, using the JDK HttpClient with retry and proxy support and a database-backed response cache with a time-to-live; all local practice around platform OSGi components."
aliases: ["XSD client", "JAXB HTTP client", "external XML API cache"]
keywords: ["JAXB", "XSD", "HttpClient", "OSGi bundle", "retry", "backoff", "proxy", "cache", "TTL", "external API"]
tags: ["domain:backend", "layer:backend", "project:judo-partner", "status:single-project"]
category: integration
status: single-project
projects: [judo-partner]
evidence: ["judo-partner:unrecorded"]
alternatives: [soap-client-integration]
related: [soap-client-integration, external-api-adapter-pattern, osgi-karaf-bundle-architecture, custom-operation-osgi-component]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

An external provider publishes an XML API described by XSD schemas but not as a SOAP/WSDL service. The application needs type-safe access, resilience to transient failures and fewer calls to the provider. The practice isolates the generated JAXB classes in a dedicated OSGi bundle, calls the API with the JDK `HttpClient`, retries with backoff, and caches answers in the application database.

## Practice

### Platform: what the application provides

JUDO has no built-in client for external APIs. The application's own code runs as OSGi components in the runtime (custom operations and services are DS components that inject DAOs and other services with `@Reference`, see [custom operations](../../agent-docs/backend/custom-operations.md)). Everything below is a convention on top of that; [[osgi-karaf-bundle-architecture]] covers the bundle split and [[custom-operation-osgi-component]] the component model.

### Practice notes

```java
// Example code: all types are generated types
// Separate bundle: src/main/xsd/*.xsd  ->  JAXB classes at build time

@Component(immediate = true, service = ApiUtils.class)
public class ApiUtils {
    HttpClient createClient() {
        return HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(Duration.ofSeconds(15))
                .build();                                 // proxy taken from system properties if set
    }

    Response queryApi(Request request) {
        // JAXB marshal request -> POST with a request timeout
        // retry a few times with exponential backoff (1 s, 2 s, 4 s)
        // JAXB unmarshal the response; map error responses to a business error
    }
}

@Component(immediate = true, service = CacheService.class)
public class CacheService {
    @Reference CacheEntryDao cacheDao;

    Optional<CachedResult> get(String key) {
        Optional<CacheEntry> entry = cacheDao.query()
                .filterByKey(StringFilter.equalTo(key))
                .selectOne();
        if (entry.isPresent() && withinTtl(entry.get(), Duration.ofHours(24))) {
            return Optional.of(entry.get().getResult());
        }
        return queryAndCache(key);   // delete the stale entry, call the API, store the result
    }
}
```

- **Own bundle for generated classes.** The XSD-generated classes build in a separate bundle that the application bundle depends on, so regeneration of the schema does not touch application code, and the JAXB runtime dependencies stay out of the model bundle.
- **Cache in the database.** The cache is an entity (query record plus result records), read through the generated DAO with a filter ([[dao-fluent-query-filter]]) and a mask for the fields needed ([[mask-field-projection]]). Check the age on read; delete stale rows when refreshing.
- **Provide a manual invalidation operation** (a custom operation that deletes the cached records in batches), since entries otherwise live until their TTL passes.
- **Credentials in an entity**, not in environment variables, when operators must change them at runtime from the UI. Treat them as secrets: do not log them, restrict the entity's access, and keep signing or hashing steps required by the provider in one place.
- **Failures.** Convert transport and provider errors into the operation's modeled fault so the user sees a translated message; never let a raw exception from the client escape a custom operation (see [error handling](../../agent-docs/backend/error-handling-guide.md)).
- Do not call the external API from an interceptor `postCall` on a hot path: it runs inside the operation's transaction ([ordering and transactions](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).

## Rationale

- JAXB gives type-safe XML handling and a clear compile-time break when the provider changes a schema.
- The database cache cuts external calls and survives restarts, unlike an in-memory cache.
- Cost: code generation complexity, verbose XML, a separate bundle to deploy, and manual invalidation. A 24-hour TTL can serve stale data; pick a TTL per use.

## Example

An application validates tax identifiers against an external registry XML API. A dedicated client bundle holds JAXB classes generated from six XSD schemas. A lookup service caches each query as a query record with result records for 24 hours. The API authenticates with a password hash and a request signature derived from a timestamp. A utility class does the HTTP call with three attempts, exponential backoff and optional proxy, and a custom operation clears the cache in batches of 100.

## When to avoid

- When the provider offers a WSDL: use a SOAP client ([[soap-client-integration]]).
- When a simple JSON REST API exists: a plain HTTP client without code generation is lighter.
- When results must always be fresh or per-user private: do not cache, or key the cache by user.
- When one simple provider call is enough: skip the cache and the retry code.

## Related

- [[soap-client-integration]] — the WSDL-based alternative
- [[external-api-adapter-pattern]] — an adapter around several providers
- [[osgi-karaf-bundle-architecture]] — separate bundles for client modules
- [[custom-operation-osgi-component]] — the component model the client is called from
- [[dao-fluent-query-filter]] — querying the cache entity
- [[mask-field-projection]] — loading only needed cache fields
