---
id: facade-service-pattern
title: Facade Service Pattern for Domain Operations
description: "A project-level facade service gives a domain one interface for its operations and delegates internally to focused sub-services; custom operations inject only the facade."
aliases: [domain facade, service facade]
keywords: [facade, service, domain, operations, delegation, osgi]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "status:emerging"]
category: service
status: emerging
projects: [mlszksz-platform, park-here, indamedia-adtrack]
evidence: ["mlszksz-platform:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: [service-delegation-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A domain with many operations (create, publish, delete, edit) gets one facade interface. Custom operation classes inject only that facade, and the facade dispatches to sub-services that each own one concern. This keeps the operation classes thin and the dependency graph of each operation small.

## Practice

### Platform base: thin operation, handwritten service

The platform docs describe the base pattern: the generated custom-operation class stays thin and delegates to a handwritten service class that holds the business logic and injects DAOs (see [custom service layer](../../agent-docs/backend/architectural-patterns.md) and [custom operations](../../agent-docs/backend/custom-operations.md)). Operations and services are OSGi components wired with `@Reference`.

### Project practice: add a facade on top of the services

The facade layer itself is project practice, not a platform concept. Where one service would grow too large, split it and put a facade in front:

- The facade interface lists the domain operations in domain terms.
- The facade implementation is an OSGi component whose methods are pure delegation to sub-services.
- Sub-services inject the DAOs and other services they need. Operations never inject sub-services directly.

```java
// Example project code: PostService, PostCreationService, PostLifecycleService are project classes
public interface PostService {
    News createNews(NewsInput input, Organization org);
    void publishNews(News news);
}

@Component(immediate = true, service = PostService.class)
public class PostServiceImpl implements PostService {
    @Reference PostCreationService creationService;
    @Reference PostLifecycleService lifecycleService;

    public News createNews(NewsInput input, Organization org) {
        return creationService.createNews(input, org);
    }
    public void publishNews(News news) {
        lifecycleService.publishNews(news);
    }
}

@Component(immediate = true, service = PostCreationService.class)
public class PostCreationServiceImpl implements PostCreationService {
    @Reference ActorService actorService;   // project helper
    @Reference NewsDao newsDao;             // generated DAO
    // creation logic with validation and author assignment
}
```

## Rationale

- Callers see one small interface, so operation classes need one `@Reference`.
- Sub-services stay focused and testable in isolation (see [[integration-test-reflection-injection]]).
- Cost: an extra indirection layer, pass-through methods, and a facade interface to maintain next to the sub-service interfaces.

## Example

- mlszksz-platform: a `PostService` facade delegates to a creation service (validation, author assignment) and a lifecycle service (publish, delete, expire, edit, feed management). Custom operations such as the publish implementation inject only `PostService`, which decomposes a 20+ method domain into two services.
- park-here: `ReservationService` acts as a large facade (validation, creation for four reservation types, modification, cancellation) with about a dozen injected dependencies. Custom operations are two- or three-line delegates.
- indamedia-adtrack: `AggregatedCampaignService` orchestrates campaign lifecycle, delegates to `TrackedCampaignService` for per-campaign data sync, and runs scheduled work. Operations inject only the aggregate service.

## When to avoid

- Small domains: inject the one service directly ([[service-delegation-pattern]]).
- When the facade would only forward every call one-to-one to a single service: it adds indirection without decomposition.

## Related

- [[service-delegation-pattern]] — the base pattern: operation delegates to a service
- [[custom-operation-osgi-component]] — how operations and services are registered as OSGi components
- [[state-lifecycle-operation]] — lifecycle operations that a lifecycle sub-service typically serves
- [[integration-test-reflection-injection]] — wiring services in tests
