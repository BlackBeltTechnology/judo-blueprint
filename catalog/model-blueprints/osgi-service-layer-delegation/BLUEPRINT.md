---
id: osgi-service-layer-delegation
title: OSGi Service Layer Delegation (Shared Business Services)
description: A backend pattern where custom operations, jobs and interceptors delegate business logic to shared OSGi service interfaces, with implementations split across Maven modules by concern.
aliases: [service layer, shared services, delegation pattern]
keywords: [osgi, service, layer, delegation, shared, business, services, interface, implementation]
tags: [domain:model, layer:backend, project:mlszksz-platform, project:rackinspect, project:indamedia-adtrack, project:park-here, status:established]
category: pattern
status: established
projects: [mlszksz-platform, rackinspect, indamedia-adtrack, park-here]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "indamedia-adtrack:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: none: backend-only
related: [osgi-scheduled-background-jobs, identity-account-organization-cluster]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Keep custom operation logic out of the app module: put it in services of a dedicated common module and let the operation classes only delegate. Keep custom operations thin. The operation validates input, calls a shared service and maps the result. The business rules live in the service, so several operations, jobs and interceptors can reuse them and the service can be tested without the JUDO dispatcher.

### Operations depend on interfaces, not implementations

A custom operation references the service interface. The OSGi runtime picks the implementation. Integrations such as an identity provider or a push provider sit behind their own interface, so they can be replaced in tests.

## Structure

The service interface is a plain Java interface in a shared common module, with no OSGi annotations. Its implementation carries the component annotation and references the generated DAOs and other services. Methods are coarse business operations (for example, "publish a notification"), not CRUD wrappers.

Implementations are placed in the module closest to their concern: a service that needs only the core model sits in the common module, a service that wraps a vendor SDK sits in that vendor's module. Operations, jobs and interceptors each live in their own module and reference only interfaces.

## Constraints

- The interface carries no OSGi annotations. Only the implementation is a component.
- Custom operations reference the interface, never the implementation class.
- A business rule violation is a modeled fault declared on the operation (HTTP 422); its exception class is generated per project, so names such as `BusinessErrorException` exist only when the project models such a fault. Helpers like `ExceptionUtils` are example project code, not platform API. Field-level input errors are validation exceptions (HTTP 400).
- An interceptor may only throw `InterceptorCallBusinessException`. Interceptors run only for built-in operations, so a service called from a custom operation must enforce its rules itself.
- Services may reference other services, but the reference graph must stay acyclic.

## Variations

- **Shared service across actors.** Two operations from different actors call the same service method. The actor-specific checks stay in the operation.
- **Strategy objects inside a service.** A feed or targeting service delegates a rule to a strategy class it references. Use this when a rule varies by type.
- **Message catalog as a service.** A method-per-message interface, registered with the platform's i18n service and read through a request-scoped locale, gives localized business messages. The interface and the registration are project code.
- **Adapter behind a service.** Wrap an external system in an adapter interface and let the service call only that interface. See [[external-api-adapter-provider-pattern]].

## When to use

- Several operations or jobs need the same business rule.
- Integrations (identity, push, mail, file storage) must be swappable or mockable.
- Operations would otherwise grow large with logic that is hard to test.

## When to avoid

- The logic is a single field copy or a trivial lookup. A service adds indirection without value.
- The rule must run on every built-in create, update or delete. Use an interceptor, and keep the service for custom code.
- The team cannot maintain the module split. A single module with the same interface discipline is enough for a small app.

## Related

- [[osgi-scheduled-background-jobs]] — scheduled jobs call the same service layer
- [[i18n-osgi-service]] — the message-catalog sub-pattern in detail
- [[identity-account-organization-cluster]] — an identity model whose custom operations delegate to services
