---
id: scheduled-data-sync-pipeline
title: Scheduled Data Sync Pipeline
description: "Several scheduled jobs (frequent fetch, daily reset, daily archive) delegate to one service that pulls external data, stores snapshots, upserts daily records and recalculates parent aggregates."
aliases: [periodic external sync, fetch reset archive jobs]
keywords: [scheduled job, sync, external api, snapshot, upsert, aggregate, daily reset, archive]
tags: ["domain:backend", "layer:backend", "project:indamedia-adtrack", "status:single-project"]
category: integration
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: []
related: [quartz-scheduled-job, external-api-adapter-pattern, data-snapshot-versioning, upsert-create-or-update, safe-failure-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Data that lives in an external system (here: advertising cost) must stay fresh in the application database. A small set of scheduled jobs does this: a frequent job fetches the current state, a daily job resets per-day counters, a daily job closes entities past their end date. The jobs hold no logic; one service does the work, so the same code can also be called from operations.

## Practice

### Platform base

- The agent-docs describe no scheduler. Scheduling is project infrastructure (OSGi components configured through Configuration Admin, see [[quartz-scheduled-job]]). The practice below is therefore project practice built on platform data access.
- Data access inside the service uses the generated DAOs injected with `@Reference`, the fluent query API ending in `selectOne` / `selectList`, and `create` with the generated `ForCreate` builder or `update` ([data access guide](../../agent-docs/backend/data-access-guide.md#query-result-methods)).
- Updating an entity returned by the DAO works only when the loaded version is written back; a hand-built payload without `__version` skips optimistic locking ([platform behaviour](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)).
- A scheduled run is not a request, so no interceptor fires and no actor or request context exists. Interceptors fire only for built-in behaviour operations triggered through the dispatcher ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Anything a job writes through the DAO bypasses them.

### Project practice: three thin jobs, one service

This layer is project practice (indamedia-adtrack), not a platform feature:

- **Fetch job** (every few minutes, business hours): iterates active parent entities, syncs each child through the external API adapter ([[external-api-adapter-pattern]]), stores the raw response as a snapshot ([[data-snapshot-versioning]]), upserts the day's cost record ([[upsert-create-or-update]]) and recalculates the parent aggregates (total spend, remaining budget).
- **Daily reset job** (just after midnight): zeroes the per-day counters, fetches the previous day's final figures, recalculates aggregates.
- **Archive job** (daily): finds entities past their end date, fetches the final data, sets the status to finished.
- Mark the jobs non-concurrent so a slow run is not overlapped by the next one.
- Catch failures per parent entity and continue ([[safe-failure-pattern]]); a single API error must not stop the whole run.
- The three jobs depend on timing, not on each other: make each idempotent and recompute aggregates from stored rows rather than adding increments.

```java
// Example project code: AggregatedService, CostDao and the job configuration are project classes
@Component(configurationPid = "fetchJob", configurationPolicy = ConfigurationPolicy.REQUIRE)
public class FetchDataJob implements Runnable {
    @Reference AggregatedService service;

    @Override
    public void run() {
        service.fetchCurrentState(LocalDateTime.now());   // all logic lives in the service
    }
}

void updateOrCreateCosts(List<CostInfo> costs) {
    for (CostInfo info : costs) {
        Optional<Cost> existing = costDao.query()
            .filterByDate(DateFilter.equalTo(info.getDate()))
            .selectOne();
        if (existing.isPresent()) {
            existing.get().setAmount(info.getAmount());
            costDao.update(existing.get());
        } else {
            costDao.create(CostForCreate.builder()
                .withDate(info.getDate()).withAmount(info.getAmount()).build());
        }
    }
}
```

## Rationale

- Thin jobs keep scheduling concerns apart from business logic and let operations reuse the service.
- Snapshots of the raw response make a wrong aggregate explainable and replayable.
- Splitting fetch, reset and archive keeps each job short and independently schedulable.

## Example

Indamedia-AdTrack tracks advertising campaign cost. The fetch job runs every three minutes from 01:00 to 23:59: it iterates all ongoing campaigns, syncs each tracked campaign through the ads API, stores a fetched-data snapshot, upserts the cost record, and recalculates today's spend, total cost, remaining budget, remaining days and remaining average daily spend. The reset job runs at 00:01, resets counters and fetches the previous day's costs. A third job at 00:01 archives finished campaigns. A fourth, a reminder job for budget alerts, is only a placeholder. All jobs are configured as non-concurrent.

## When to avoid

- The source can push changes (webhooks, events): react to them instead of polling.
- The API has tight rate limits: frequent full re-fetches (this pattern has no incremental sync) will hit them.
- The sync needs strict ordering between steps: timing-based coordination between jobs is fragile; use one job or an explicit workflow.

## Related

- [[quartz-scheduled-job]] — the scheduler infrastructure the jobs run on
- [[external-api-adapter-pattern]] — the adapter that talks to the external API
- [[data-snapshot-versioning]] — storing raw responses as snapshots
- [[upsert-create-or-update]] — the daily record upsert
- [[safe-failure-pattern]] — continue after a per-item failure
