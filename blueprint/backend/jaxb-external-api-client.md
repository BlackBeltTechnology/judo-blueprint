---
id: "jaxb-external-api-client"
title: "JAXB-Based External API Client with Response Caching"
domain: "backend"
category: "integration"
score: 16.1
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - judo-partner
alternatives:
  - soap-client-integration
---
## Description

An external API client built with JAXB-generated classes from XSD schemas, deployed as a separate OSGi bundle. The client uses Java's `HttpClient` for HTTP communication (not CXF SOAP) with JAXB marshalling/unmarshalling for XML request/response bodies. Includes retry with exponential backoff, HTTP proxy support, and database-level response caching with a configurable TTL. API credentials are stored in a database entity rather than environment variables, allowing runtime configuration changes.

## Structure

```java
// Separate OSGi bundle with JAXB-generated classes from XSD
// navonline-client/src/main/xsd/*.xsd -> JAXB classes

// HTTP client with retry and proxy support
@Component(immediate = true, service = ApiUtils.class)
public class ApiUtils {
    HttpClient createClient() {
        HttpClient.Builder builder = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_1_1)
            .connectTimeout(Duration.ofSeconds(15));
        // Proxy support via system properties
        return builder.build();
    }

    Response queryApi(Request request) {
        // JAXB marshal request to XML
        // Send via HttpClient with 1-minute timeout
        // Retry up to 3 times with exponential backoff (1s, 2s, 4s)
        // JAXB unmarshal response
    }
}

// Caching service with TTL
@Component(immediate = true, service = CacheService.class)
public class CacheService {
    Optional<CachedResult> getCached(String key) {
        Optional<CacheEntry> entry = cacheDao.query()
            .filterByKey(StringFilter.equalTo(key))
            .selectOne();
        if (entry.isPresent() && isWithinTTL(entry.get(), Duration.ofHours(24))) {
            return Optional.of(entry.get().getResult());
        }
        // Delete stale entry, query external API, cache result
        return queryAndCache(key);
    }
}
```

## Examples

### judo-partner
NAV Online Invoice System (Hungarian Tax Authority) API v3.0 integration via dedicated `navonline-client` OSGi bundle with JAXB-generated classes from 6 XSD schemas (common, invoiceApi, invoiceBase, invoiceData, invoiceAnnulment, serviceMetrics). `TaxpayerServices` caches query results as `TaxpayerQuery` + `Taxpayer` entities with 24-hour TTL. Authentication uses SHA-512 password hash and SHA3-512 request signature with time-based keys. `NavUtils` handles HTTP communication with retry (3 attempts, exponential backoff) and proxy support. `ClearCacheCustomImplementation` provides manual cache invalidation by deleting all cached records in batches of 100.

## Trade-offs

- Pros: Type-safe XML handling via JAXB, separate bundle isolates generated code, database caching reduces external API calls, credentials managed at runtime via UI
- Cons: JAXB adds code generation complexity, XML is verbose compared to REST/JSON, cache invalidation requires manual operation, separate bundle adds deployment complexity
- Alternative: CXF SOAP client (see `soap-client-integration`) for WSDL-based services, REST API with JSON (simpler if available), in-memory caching (simpler but lost on restart)

## Related Patterns

- soap-client-integration
- external-api-adapter-pattern
- osgi-karaf-bundle-architecture
