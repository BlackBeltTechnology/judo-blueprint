---
id: external-api-adapter-provider-pattern
title: External API Adapter with Provider Service Pattern
description: "Isolates each external platform API behind one interface and a factory service that picks the right adapter at runtime, so a new platform is added without changing the callers."
aliases: [adapter provider, external api factory]
keywords: [external, api, adapter, provider, factory, platform, credentials, interface]
tags: ["domain:model", "layer:backend", "project:indamedia-adtrack", "project:park-here", "status:emerging"]
category: pattern
status: emerging
projects: [indamedia-adtrack, park-here]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: []
fragment: none: backend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Let the business code call one API interface, whatever external platform sits behind it. Each platform is an adapter behind that interface. A factory service picks the adapter for an entity and supplies its credentials, so adding a platform does not change the callers.

### One interface, many adapters

The API interface is a plain contract with business-oriented methods and its own data objects. Each platform adapter implements it with that platform's SDK. Callers see only the interface.

### The factory decides, the caller does not

The provider service reads the platform of an entity, loads its credentials, and returns a ready client. Callers never construct an adapter or read a credential.

## Structure

Three layers. The API module is a standalone bundle with the interface and its data objects, with no dependency on the model or on any platform SDK. Each adapter module depends on the API module and on one platform SDK. The provider service is a component in the common module. It loads the entity and its credentials, dispatches on the platform, and returns the adapter. Custom operations and services reference the provider service, never an adapter. The provider and the callers are OSGi components of the application (common practice).

## Constraints

- The API module has no dependency on the model or on any platform SDK.
- Adapters are plain objects built by the provider with runtime credentials, not components of their own.
- Callers reference the provider service, never an adapter class.
- A platform with no adapter yet fails with a modeled business fault declared on the calling operation (HTTP 422), not with a bare runtime exception (which the client sees as a generic 500). The calling operation must declare the fault.
- Credentials that are files (for example a key file) are read through the application's file store service, not from a path.

## Variations

- **Dispatch on an enumeration.** The provider switches on the platform enumeration of the entity. A new platform adds one enum member and one branch.
- **Declared but not implemented.** Declare a platform in the enumeration before its adapter exists. The provider raises a clear "not implemented" business fault, which marks the extension point.
- **Lookup by configuration.** Choose the adapter from a configuration entry instead of an enumeration. This suits tenants that use different providers for the same platform.
- **Helper methods on the provider.** The provider exposes helpers that extract platform-specific identifiers from the entity, so callers do not know the platform's id format.

## When to use

- The application integrates with two or more external platforms that offer the same kind of data.
- The platform is chosen per entity, and each entity holds its own credentials.
- Adding a platform later should touch only a new module and one branch.

## When to avoid

- There is one external service and no plan for another. A direct client is simpler.
- The platforms differ so much that a shared interface would hide the important differences. Keep them as separate services.
- The external calls are simple HTTP calls with no SDK. A small client class is enough.

## Related

- [[exchange-rate-entity]]: an entity whose automatic fetch calls an external rate source
- [[external-api-adapter-pattern]]: the best-practice version of this pattern, without the bundle layout
- [[osgi-service-layer-delegation]]: how the provider and other services are wired together
- [[safe-failure-pattern]]: when a failing external call must not break the business operation
