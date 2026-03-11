---
id: "scheduled-data-sync-pipeline"
title: "Scheduled Data Synchronization Pipeline from External API"
domain: "backend"
category: "scheduling"
score: 57.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - indamedia-adtrack
---
## Description

A scheduled background job pipeline that periodically fetches data from an external API, creates snapshot records of raw API responses, updates or creates daily cost/metric records, and recalculates aggregated summary values across parent entities. The pipeline runs on a frequent schedule (e.g., every 3 minutes) during business hours. It consists of multiple coordinated jobs: (1) a frequent data fetcher for current state, (2) a daily reset job for per-day counters, and (3) a daily archiver for expired entities. The pattern ensures data freshness while handling missing dates, deduplication, and cumulative calculations.

## Structure

```java
// 1. Frequent sync job (every N minutes)
@Component(configurationPid = "fetchJob", configurationPolicy = REQUIRE)
public class FetchDataJob implements Runnable {
    @Reference AggregatedService service;

    @Override
    public void run() {
        service.fetchCurrentState(LocalDateTime.now());
        // Iterates all active parent entities
        // For each: syncs child entities via external API
        // Creates snapshot records (FetchedData)
        // Updates daily cost records (upsert pattern)
        // Recalculates parent aggregations (totalSpend, remainingBudget)
    }
}

// 2. Daily reset job (midnight)
@Component(configurationPid = "resetJob", configurationPolicy = REQUIRE)
public class ResetDailyAttributesJob implements Runnable {
    @Override
    public void run() {
        service.dailyReset(LocalDate.now());
        // Resets todaySpend to zero on all active entities
        // Fetches previous day's final cost data
        // Recalculates aggregations
    }
}

// 3. Daily archiver (midnight)
@Component(configurationPid = "archiveJob", configurationPolicy = REQUIRE)
public class ArchiveExpiredJob implements Runnable {
    @Override
    public void run() {
        service.archiveExpired(LocalDate.now());
        // Finds entities past their end date
        // Fetches final cost data
        // Sets status to FINISHED
    }
}

// Cost record upsert pattern
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
                .withDate(info.getDate())
                .withAmount(info.getAmount())
                .build());
        }
    }
}
```

## Examples

### Indamedia-AdTrack
4-job pipeline for Google Ads campaign cost tracking: `FetchCampaignCost` (every 3 min, 01:00-23:59) calls `aggregatedCampaignService.fetchTheCurrentStateOfTheCampaigns()` which iterates all ONGOING campaigns, syncs each tracked campaign via Google Ads API, creates `FetchedData` snapshots, upserts `Cost` records, and recalculates `todaySpend`, `totalCost`, `remainingBudget`, `remainingDays`, `remainingAverageDailySpend`. `ResetDailyAttributes` (daily 00:01) resets counters and fetches previous day's costs. `UpdateExpiredAggregatedCampaignStatus` (daily 00:01) archives finished campaigns. `SendReminderJob` (placeholder for budget alerts). All use `scheduler.concurrent=false`.

## Trade-offs

- Pros: Near-real-time data freshness, automatic cost tracking, resilient to individual sync failures, clear separation of sync/reset/archive concerns
- Cons: Frequent API polling can hit rate limits, no incremental sync (re-fetches full data), job coordination relies on timing rather than explicit dependencies
- Alternative: Webhook/push-based updates (reduces polling), event-driven sync, message queue for decoupled processing

## Related Patterns

- quartz-scheduled-job
- external-api-adapter-pattern
- data-snapshot-versioning
- upsert-create-or-update
