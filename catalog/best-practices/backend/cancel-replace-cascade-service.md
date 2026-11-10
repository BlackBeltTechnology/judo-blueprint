---
id: "cancel-replace-cascade-service"
title: "Cancel-and-Replace Async Cascade Service (OSGi)"
domain: "backend"
category: "async"
score: 62.0
usage_count: 1
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - compsychletter
---
## Description

An OSGi `@Component` that manages per-entity background work queues with cancel-and-replace semantics. When a new trigger arrives for the same entity while a previous cascade is in-flight, the service cancels the in-flight futures (`Future.cancel(true)`, best-effort) and immediately starts a fresh cascade from the new state. Useful for re-translation cascades, re-computation pipelines, or any "latest-wins" background fan-out.

Precedent in this project: `ChatSessionStore` (sweep eviction pattern using `ScheduledExecutorService` + `ConcurrentHashMap` + `ScheduledFuture`).

## Structure

```java
@Component(service = TranslationCascadeService.class, immediate = true)
public class TranslationCascadeService {

    @Reference TemplateDao templateDao;
    @Reference LanguageVariantDao languageVariantDao;
    @Reference LlmProvider llmProvider;
    @Reference LlmAuditService llmAuditService;

    private ScheduledExecutorService executor;
    // Key: entity identifier; Value: active cascade with its in-flight futures
    private final ConcurrentHashMap<UUID, Cascade> active = new ConcurrentHashMap<>();

    @Activate
    void activate() {
        executor = Executors.newScheduledThreadPool(2);
    }

    @Deactivate
    void deactivate() {
        active.values().forEach(Cascade::cancelAll);
        executor.shutdownNow();
    }

    public void enqueue(Template template) {
        UUID id = template.identifier().getIdentifier();
        Cascade prev = active.remove(id);
        if (prev != null) prev.cancelAll();          // cancel-and-replace
        Cascade fresh = new Cascade(template.identifier());
        active.put(id, fresh);
        fresh.start(executor, templateDao, languageVariantDao, llmProvider, llmAuditService);
    }

    private class Cascade {
        final TemplateIdentifier templateId;
        final List<Future<?>> futures = new CopyOnWriteArrayList<>();

        Cascade(TemplateIdentifier id) { this.templateId = id; }

        void start(ScheduledExecutorService exec, ...) {
            // Load variants fresh from DB (template handle may be stale)
            // For each variant, submit a Future that:
            //   1. Set status=TRANSLATING; persist
            //   2. Call llmProvider.translateMarkdown(...)
            //   3. On success: body=translated, status=OK; persist; audit success
            //      On InterruptedException / cancellation: skip (do NOT persist FAILED)
            //      On other failure: status=FAILED; persist; audit failure
            //   4. On completion, remove from registry if this is still the active cascade
            futures.add(exec.submit(() -> { /* per-variant logic */ }));
        }

        void cancelAll() {
            futures.forEach(f -> f.cancel(true));
        }
    }
}
```

Key structural elements:
- `@Activate` / `@Deactivate`: lifecycle hooks manage the executor and cancel all in-flight work on bundle stop.
- `ConcurrentHashMap<EntityId, Cascade>`: per-entity registry; `remove` + `put` is the cancel-and-replace sequence (not `replace`; `remove` lets us call `cancelAll` on the displaced cascade before inserting the new one).
- `CopyOnWriteArrayList<Future<?>>`: safe iteration from the deactivate path while workers append.
- `Future.cancel(true)`: interrupts running threads; underlying HTTP/LLM calls may still complete server-side — the result is simply discarded.
- Cascade workers MUST check `Thread.interrupted()` or catch `InterruptedException` and exit cleanly — do NOT set `status=FAILED` on cancellation (the new cascade will overwrite the status).
- `immediate = true` on `@Component` ensures the service is available before the first operation fires.

## Examples

### compsychletter
`TranslationCascadeService` in `application/services/.../operations/templates/`. Triggered by `editOriginalBody` and `changeOriginalLanguage` operations. Each trigger re-translates all `LanguageVariant` rows of a `Template` from the new original body. Per-variant states: `OK → PENDING → TRANSLATING → OK / FAILED`. Cancel-and-replace: second `editOriginalBody` on the same template cancels any in-progress variant futures and starts fresh from the new body. Audit: `LlmAuditService.record(VARIANT_RETRANSLATE_CASCADE, ...)` per variant on completion (safe-failure wrapped).

## Trade-offs

- Pros: Prevents redundant LLM calls for superseded edits; user sees the latest edit's result as soon as possible; clean per-variant status surfacing
- Cons: `Future.cancel(true)` is best-effort — the underlying HTTP call may complete server-side even after cancellation; variants briefly show stale translated content from an in-progress cascade before being overwritten by the new one
- Prefer when: Background fan-out work is expensive (LLM calls, external API), entities are edited frequently, and only the latest state matters (last-edit-wins)
- Avoid when: All intermediate results must be preserved (use a proper queue/event-log instead); strict ordering guarantees needed across cascades

## Anti-Patterns

- **Setting `status=FAILED` on `InterruptedException`** — Cancellation is not failure; the new cascade will handle the variant. Setting FAILED on cancel creates a false failure state that the user sees before the new cascade completes.
- **Using `replace` instead of `remove`+`put`** — `ConcurrentHashMap.replace` does not allow the cancel-on-displacement action in between.
- **Sharing one executor across unrelated services** — Each cascade service should own its executor; `shutdownNow` in `@Deactivate` must not kill other services' work.
- **Not declaring `immediate = true`** — Without it the OSGi container may delay instantiation until the service is first looked up; the first operation invocation may race with component activation.

## Related Patterns

- [safe-failure-pattern](safe-failure-pattern.md)
- [custom-operation-osgi-component](custom-operation-osgi-component.md)
- [quartz-scheduled-job](quartz-scheduled-job.md)
