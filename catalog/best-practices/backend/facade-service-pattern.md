---
id: facade-service-pattern
title: Facade Service Pattern for Domain Operations
description: "A facade service gives a domain one interface for its operations and delegates internally to focused sub-services; custom operations inject only the facade."
aliases: [domain facade, service facade]
keywords: [facade, service, domain, operations, delegation, osgi]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "status:emerging"]
category: service
status: emerging
projects: [mlszksz-platform, park-here, indamedia-adtrack]
evidence: ["mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/PostServiceImpl.java", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
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

### Practice notes: add a facade on top of the services

The facade layer itself is a convention, not a platform concept. Where one service would grow too large, split it and put a facade in front:

- The facade interface lists the domain operations in domain terms.
- The facade implementation is an OSGi component whose methods are pure delegation to sub-services.
- Sub-services inject the DAOs and other services they need. Operations never inject sub-services directly.

```java
// Example code: OrderService, OrderCreationService, OrderLifecycleService are classes
public interface OrderService {
    Notice createNotice(NoticeInput input, Account org);
    void publishNotice(Notice notice);
}

@Component(immediate = true, service = OrderService.class)
public class OrderServiceImpl implements OrderService {
    @Reference OrderCreationService creationService;
    @Reference OrderLifecycleService lifecycleService;

    public Notice createNotice(NoticeInput input, Account org) {
        return creationService.createNotice(input, org);
    }
    public void publishNotice(Notice notice) {
        lifecycleService.publishNotice(notice);
    }
}

@Component(immediate = true, service = OrderCreationService.class)
public class OrderCreationServiceImpl implements OrderCreationService {
    @Reference ActorService actorService;   // helper
    @Reference NoticeDao noticeDao;             // generated DAO
    // creation logic with validation and author assignment
}
```

## Rationale

- Callers see one small interface, so operation classes need one `@Reference`.
- Sub-services stay focused and testable in isolation (see [[integration-test-reflection-injection]]).
- Cost: an extra indirection layer, pass-through methods, and a facade interface to maintain next to the sub-service interfaces.

## Example

- One application: an `OrderService` facade delegates to a creation service (validation, author assignment) and a lifecycle service (publish, delete, expire, edit, feed management). Custom operations such as the publish implementation inject only `OrderService`, which splits a large domain into two services.
- One application: `BookingService` acts as a large facade (validation, creation for several booking types, modification, cancellation) with many injected dependencies. Custom operations are short delegates.
- Another application: `GroupService` orchestrates item lifecycle, delegates to `ItemSyncService` for per-item data sync, and runs scheduled work. Operations inject only the group service.

## When to avoid

- Small domains: inject the one service directly ([[service-delegation-pattern]]).
- When the facade would only forward every call one-to-one to a single service: it adds indirection without decomposition.

## Related

- [[service-delegation-pattern]] — the base pattern: operation delegates to a service
- [[custom-operation-osgi-component]] — how operations and services are registered as OSGi components
- [[state-lifecycle-operation]] — lifecycle operations that a lifecycle sub-service typically serves
- [[integration-test-reflection-injection]] — wiring services in tests
