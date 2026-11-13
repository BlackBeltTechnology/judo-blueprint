---
id: cancel-replace-cascade-service
title: Cancel-and-Replace Async Cascade Service (OSGi)
description: "An OSGi component keeps one background cascade per entity and cancels the in-flight one when a newer trigger arrives, so only the latest state is processed."
aliases: [latest-wins background work, cancel and replace, async cascade]
keywords: [cascade, Future.cancel, ConcurrentHashMap, executor, OSGi component, Activate, Deactivate, latest wins]
tags: ["domain:backend", "layer:backend", "project:compsych-letter-demo", "status:single-project"]
category: async
status: single-project
projects: [compsych-letter-demo]
evidence: ["compsychletter:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-05-13
last_updated: 2026-11-10
---
## Intent

When a new trigger arrives for an entity while background work for the same entity is still running, cancel the in-flight work and start a fresh cascade from the new state ("latest wins"). Fits re-processing cascades, re-computation pipelines and any expensive fan-out where only the newest input matters.

## Practice

### Platform base

- The service is an ordinary OSGi Declarative Services component; custom operations call it by injecting it with `@Reference` ([OSGi component registration](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern), [injecting DAOs and services](../../agent-docs/backend/data-access-guide.md#injecting-daos-and-services)).
- Code on other threads runs outside the operation's transaction and without request context variables ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). The cascade workers therefore cannot rely on the caller's transaction or actor; the docs do not describe the DAO transaction behaviour of a plain executor thread, so open and manage the transaction in the worker (*verify*, see [[quartz-scheduled-job]]).
- Interceptors never run around custom operations, so none of them guards the trigger operation.

### Practice notes: per-entity cascade registry

This layer is a convention built on the platform, not a platform feature. Example code:

```java
// Example code: DocumentDao, DocumentVariantDao, ExternalProvider are generated types
@Component(service = RefreshCascadeService.class, immediate = true)
public class RefreshCascadeService {

    @Reference DocumentDao documentDao;
    @Reference DocumentVariantDao documentVariantDao;
    @Reference ExternalProvider externalProvider;

    private ScheduledExecutorService executor;
    // Key: entity identifier; Value: active cascade with its in-flight futures
    private final ConcurrentHashMap<UUID, Cascade> active = new ConcurrentHashMap<>();

    @Activate
    void activate() { executor = Executors.newScheduledThreadPool(2); }

    @Deactivate
    void deactivate() {
        active.values().forEach(Cascade::cancelAll);
        executor.shutdownNow();
    }

    public void enqueue(Document document) {
        UUID id = document.identifier().getIdentifier();
        Cascade prev = active.remove(id);
        if (prev != null) prev.cancelAll();          // cancel-and-replace
        Cascade fresh = new Cascade(document.identifier());
        active.put(id, fresh);
        fresh.start(executor);
    }

    private class Cascade {
        final List<Future<?>> futures = new CopyOnWriteArrayList<>();
        void start(ScheduledExecutorService exec) {
            // Load variants fresh from the DB (the document handle may be stale).
            // For each variant submit a Future that:
            //  1. sets status PROCESSING and persists
            //  2. calls the external provider
            //  3. success: store body, status OK, audit; interruption/cancel: skip, do NOT persist FAILED;
            //     other failure: status FAILED, audit
            //  4. on completion removes itself from the registry if still the active cascade
            futures.add(exec.submit(() -> { /* per-variant logic */ }));
        }
        void cancelAll() { futures.forEach(f -> f.cancel(true)); }
    }
}
```

- `@Activate` / `@Deactivate` own the executor and cancel in-flight work when the bundle stops.
- A `ConcurrentHashMap` holds one cascade per entity. Use `remove` then `put`, not `replace`: `remove` returns the displaced cascade so it can be cancelled before the new one is inserted.
- `CopyOnWriteArrayList<Future<?>>` lets the deactivate path iterate while workers append.
- `Future.cancel(true)` is best effort: the thread is interrupted, but an HTTP/external call may still finish server side and its result is simply discarded.
- Workers check for interruption and exit cleanly. They never write `FAILED` on cancellation, because the new cascade overwrites the status.
- `immediate = true` makes the service available before the first operation fires.

## Rationale

- Avoids redundant expensive calls (external API calls) for superseded edits; the user sees the newest edit's result as early as possible; per-variant status stays visible.
- Cost: cancellation is best effort, and variants may briefly show stale content from an in-progress cascade until the new one overwrites it.
- Do not set `FAILED` on `InterruptedException` (a false failure the user would see), do not use `replace` instead of `remove` + `put`, do not share one executor across unrelated services (`shutdownNow` would kill other work), and do not omit `immediate = true` (the first operation can race with activation).

## Example

The `RefreshCascadeService` is triggered by the `editSourceBody` and `changeSourceLocale` operations. Each trigger re-processes every `DocumentVariant` of a `Document` from the new source body. Variant states move `READY → PENDING → PROCESSING → READY / FAILED`. A second `editSourceBody` on the same document cancels the running variant futures and starts again from the new body. Each completed variant writes an audit record (`VARIANT_REFRESH_CASCADE`), wrapped so audit failure never breaks the cascade ([[safe-failure-pattern]]). A session store uses the same scheduled-executor + concurrent-map idiom for sweep eviction.

## When to avoid

- Every intermediate result must be preserved: use a proper queue or event log.
- Strict ordering across cascades is required.
- Work is cheap enough that cancelling gains nothing.

## Related

- [[safe-failure-pattern]] — audit and side effects that must not break the cascade
- [[custom-operation-osgi-component]] — the operation that triggers the service
- [[quartz-scheduled-job]] — other background work outside the request transaction
