---
id: "quartz-scheduled-job"
title: "Quartz Scheduled Job with OSGi Configuration"
domain: "backend"
category: "scheduling"
score: 75.9
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
---
## Description

Background scheduled jobs using Quartz Scheduler integrated with OSGi. A `SingleInstanceSchedulerActivator` component configures and starts the Quartz scheduler via OSGi ConfigurationAdmin. Jobs are registered with cron triggers. Each job manages its own `UserTransaction` for database operations since scheduled execution happens outside the request-scoped transaction context.

## Structure

```java
// Scheduler activator
@Component(configurationPid = { "schedulerConfig" },
           configurationPolicy = ConfigurationPolicy.REQUIRE, immediate = true)
public class SingleInstanceSchedulerActivator {
    // RAMJobStore, 4 threads
    // Register jobs with CronTrigger
    scheduler.scheduleJob(jobDetail, CronTriggerBuilder.newTrigger()
        .withSchedule(cronSchedule("0 0 13 * * ?")).build());
}

// Scheduled job
public class UpdateExchangeRatesJob implements Job {
    @Override
    public void execute(JobExecutionContext ctx) {
        UserTransaction tx = // lookup from OSGi
        try {
            tx.begin();
            // Check configuration flag before executing
            if (config.getUpdateExchangeRates()) {
                exchangeRateService.updateRates();
            }
            tx.commit();
        } catch (Exception e) {
            tx.rollback();
        }
    }
}
```

## Examples

### RackInspect
`UpdateExchangeRatesJobFirst` runs at 13:00 daily via Quartz cron. Checks `Configuration.updateExchangeRates` boolean flag before executing. Uses explicit `UserTransaction` management (begin/commit/rollback). `SingleInstanceSchedulerActivator` configures RAMJobStore with 4 threads, ensures single-instance execution.

### mlszksz-platform
4 scheduled jobs: `PostExpirationJob` (hourly, expires past-due offers/requests), `FeedOrganizationSyncJob` (every 30 min, syncs new orgs to feeds), `NewsFeedCleanupJob` (daily 2 AM, deletes old news), `RegistrationCleanupJob` (daily 3 AM, cleans expired registrations). All use `scheduler.concurrent=false`. Safe failure: individual item failures are caught and logged, processing continues.

### ParkHere
3 scheduled jobs with RDBMS-backed persistence via `RdbmsBasedSchedulerActivator` (Liquibase creates Quartz tables, supports clustering). `SendReminderJob` (every 30 min, 6-22h, sends reservation start/end reminders). `SendEmailToDoormanJob` (every 30 min, 7-23h, sends daily reservation summary to doormen, only on working days). `SetPastActiveReservationToExpiredJob` (daily 4 AM, expires past active reservations). All use `scheduler.concurrent=false` with auto-detected database dialect (PostgreSQL/HSQLDB).

### Indamedia-AdTrack
4 scheduled jobs with both RAM and RDBMS activators. `FetchCampaignCost` (every 3 min, 01:00-23:59, syncs Google Ads spending). `ResetDailyAttributes` (daily 00:01, resets todaySpend to zero). `UpdateExpiredAggregatedCampaignStatus` (daily 00:01, archives finished campaigns by setting status to FINISHED). `SendReminderJob` (every 30 min, 06:00-22:00, placeholder for budget alerts). All use `scheduler.concurrent=false`. RDBMS activator includes Liquibase for Quartz tables with PostgreSQL/HSQLDB support.

## Trade-offs

- Pros: Reliable cron scheduling, OSGi-integrated, configurable via ConfigurationAdmin, explicit transaction control
- Cons: RAMJobStore loses state on restart, manual UserTransaction management is error-prone, no built-in retry
- Alternative: OSGi Scheduler service, external scheduler (cron, Kubernetes CronJob), or event-driven approach

## Related Patterns

- osgi-karaf-bundle-architecture
- soap-client-integration
