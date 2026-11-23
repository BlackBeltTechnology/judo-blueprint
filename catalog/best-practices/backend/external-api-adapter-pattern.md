---
id: external-api-adapter-pattern
title: External API Adapter with Factory Provider
description: Call an external REST or gRPC API behind a platform-neutral Java interface with one adapter per provider and a provider service that picks the adapter from configuration.
aliases: [API adapter, provider factory, third-party API client, ads API adapter]
keywords: [adapter, external API, factory, provider, interface, DTO, credentials, filestore, OSGi service, REST client, fault]
tags: ["domain:backend", "layer:backend", "project:indamedia-adtrack", "status:single-project"]
category: integration
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: []
related: [service-delegation-pattern, filestore-mediated-file-transfer, facade-service-pattern]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An application talks to several external services that do the same job (several advertising platforms, several payment providers). Business code should not know which one. Define one Java interface in business terms, write one adapter per provider, and let a provider service return the right adapter for an entity's configuration.

## Practice

### Four parts

1. An interface in business terms (connection check, list items, read cost to date). It uses plain DTOs, not provider types and not generated entity types.
2. One adapter class per provider. It is the only place with provider SDK calls, query languages, unit conversions (for example micro-currency) and paging or streaming of big results.
3. A provider service, an OSGi component, that reads the entity's platform attribute (an enumeration), loads the credentials and returns a new adapter instance.
4. DTOs for the data crossing the boundary, mapped to entities by the calling service.

The interface, adapters and provider service are application code. The platform only supplies the OSGi wiring (`@Reference`, `@Component`) used to reach the provider service from a custom operation (see [Example 3: External Service Integration](../../agent-docs/backend/custom-operations.md#example-3-external-service-integration) and [The Custom Service Layer](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer)).

### Keep credentials out of code

Credentials live in entities or files, not constants. The source application kept the provider key as a stored file and read it through the file store (see [[filestore-mediated-file-transfer]]); an entity row can hold the other settings. Protect the entities with actor access and do not return them through any transfer object that an ordinary actor can read.

### Map failures on purpose

An external failure is a runtime exception to the platform and becomes a generic 500 (see [How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)). Catch provider errors in the adapter, then raise one of:

- a modeled fault declared on the operation, if the UI should show a typed message (declare it on the model operation or the generated interface has no `throws` clause, see [Modeled Faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults));
- a `ValidationException` with a code, for an input-related failure;
- a clear "platform not implemented" fault for a provider that has no adapter yet.

Helpers such as an `ExceptionUtils.createBusinessErrorException` in the source application are application code, not platform API.

### Time, money and idempotency

Convert provider currency units once in the adapter. Use one clock for stored and compared timestamps (see [Time and Time Zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones)). Calls from a scheduled sync should be repeatable: query what exists with typed filters before creating (see [SDK Query Filters Reference](../../agent-docs/backend/data-access-guide.md#sdk-query-filters-reference)).

### Do not call out from inside an interceptor

Interceptors run in the transaction of the operation. A slow external call holds the transaction open, and an exception rolls back the write. A call from an `async()` interceptor is outside the transaction but loses its exceptions (see [The Interceptor Contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). Call the provider from a custom operation.

## Rationale

- Business code stays the same when a provider is added: a new adapter and one more branch in the provider service.
- The interface can be mocked in tests.
- Limit: more layers and DTOs, and the provider service grows with each platform.

## Example

One application: an ads interface with a few methods covers item discovery, connection testing, cost retrieval and budget monitoring. A search-ads adapter uses the provider's query language, converts micro-currency units and streams large result sets. The provider service loads the stored key through the file store and returns the adapter for the account's platform. A second provider is a placeholder that raises a "platform not implemented" error. A few DTOs carry item data.

## When to avoid

- Only one provider exists and will ever exist: call it from a service directly.
- The integration is a one-off file exchange: use a plain operation.
- The calls must be part of the same transaction as the data change: an outbox entity and a separate job fit better.

## Related

- [[service-delegation-pattern]] — thin operations calling services
- [[filestore-mediated-file-transfer]] — stored credential files
- [[facade-service-pattern]] — a single facade over several services
- [[cloud-drive-uploader-adapter]] — single-provider upload case with an unconfigured outcome
