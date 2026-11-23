---
id: quartz-scheduled-job
title: Quartz Scheduled Job with OSGi Configuration
description: Practice for background jobs on an application-bundled Quartz scheduler configured by an OSGi activator, with cron triggers from configuration and an explicit transaction inside each job because jobs run outside any request.
aliases: [Quartz job, cron job, scheduler activator, background job]
keywords: [quartz, scheduled, job, osgi, configuration, cron, scheduler, UserTransaction, RAMJobStore, clustering]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:park-here", "project:indamedia-adtrack", "status:established"]
category: scheduling
status: established
projects: [rackinspect, mlszksz-platform, park-here, indamedia-adtrack]
evidence: ["rackinspect:application/scheduler/src/main/java/hu/blackbelt/rackinspect/scheduler/RdbmsBasedSchedulerActivator.java", "rackinspect:application/scheduler/src/main/java/hu/blackbelt/rackinspect/scheduler/UpdateExchangeRatesJobFirst.java", "mlszksz-platform:application/scheduler/src/main/java/hu/blackbelt/mlszksz/platform/scheduler/SingleInstanceSchedulerActivator.java", "mlszksz-platform:application/scheduler/src/main/java/hu/blackbelt/mlszksz/platform/scheduler/PostExpirationJob.java", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Run periodic work (rate refresh, expiry, cleanup, reminders, external sync) from inside the Karaf runtime. This is entirely a convention: the platform provides no scheduler, and the agent-docs say nothing about Quartz or scheduled jobs. What the platform does document is the OSGi component model, the DAO API and the interceptor and transaction behaviour the jobs have to work around.

## Practice

### Platform: what a job can rely on

- A job is an ordinary OSGi component, so the Declarative Services rules apply ([OSGi component registration](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)); the scheduler runs in its own bundle ([[osgi-karaf-bundle-architecture]]).
- Request-scoped context is absent. Code on other threads runs outside the operation's transaction and without context variables ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)), so a job cannot use the `ACTOR` variable of a logged-in user. The docs do not describe the transaction and variable context of a plain scheduler thread; the practice below manages the transaction itself.
- Interceptors fire only for the built-in behaviour operations, and custom operations never hit them ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). The docs do not mention scheduler threads; a job writes through DAOs, so treat denormalization or validation interceptors as not applying and repeat that logic in the job's service if needed.

- The Karaf runtime has no Quartz feature, so the application has to supply Quartz itself. The platform has no scheduler (see [scheduled work](../../agent-docs/backend/platform-behavior-reference.md#scheduled-work)).

### Practice notes: scheduler activator, jobs, own transactions

- A scheduler activator component (example code `SingleInstanceSchedulerActivator`) requires its configuration PID (`configurationPolicy = REQUIRE`), starts Quartz with an in-memory job store and a small thread pool, and registers each job with a cron trigger. The RDBMS variant is optional: it sets the `org.apache.karaf.scheduler.quartz` PID and adds a JDBC job store; a shipped setup can use the in-memory single-instance mode instead:

```java
// Example code: not a platform type
@Component(configurationPid = { "schedulerConfig" },
           configurationPolicy = ConfigurationPolicy.REQUIRE, immediate = true)
public class SingleInstanceSchedulerActivator {
    // RAMJobStore, 4 threads
    void register(Scheduler scheduler, JobDetail job) throws SchedulerException {
        scheduler.scheduleJob(job, TriggerBuilder.newTrigger()
            .withSchedule(CronScheduleBuilder.cronSchedule("0 0 13 * * ?")).build());
    }
}
```

- Each job manages its own `UserTransaction`: begin, do the work, commit, roll back on failure.

```java
// Example code
public class UpdateRatesJob implements Job {
    @Override
    public void execute(JobExecutionContext ctx) {
        UserTransaction tx = lookupTransaction();   // from the OSGi service registry
        try {
            tx.begin();
            if (config.getUpdateRates()) {          // a configuration entity can switch the job off
                rateService.updateRates();
            }
            tx.commit();
        } catch (Exception e) {
            rollbackQuietly(tx);
            log.error("Job failed", e);             // never let the exception escape
        }
    }
}
```

- Keep the job body thin and delegate to a shared business service ([[service-delegation-pattern]]); catch failures per item so one bad record does not stop the batch ([[safe-failure-pattern]]).
- Disable overlapping runs of the same job (`scheduler.concurrent=false` in the observed applications).
- Two stores were used: the in-memory store (state is lost on restart, one instance only) and an RDBMS-backed store whose tables are created by Liquibase and which supports clustering; the dialect is detected from the configured database.
- Observed jobs: daily rate refresh, hourly expiry of past-due records, 30-minute sync and reminder jobs within a daily time window, nightly cleanup of old entries and expired registrations, daily reset of counters, cost sync from an external API every few minutes.

## Rationale

- Quartz gives reliable cron scheduling, and OSGi configuration lets operators change the schedule or disable a job without a code change.
- An explicit transaction is needed because no request transaction exists around a job.
- Costs: hand-written transaction code is error-prone, the in-memory store forgets missed runs after a restart, there is no built-in retry, and writes bypass interceptors.

## Example

A nightly job in one application deletes entries older than a limit at 02:00 and another cleans expired registrations at 03:00; both delegate to a service and log failures per item. A reminder job runs every 30 minutes between 06:00 and 22:00 and sends the day's booking reminders; on the RDBMS store, two nodes do not run the same trigger twice.

## When to avoid

- When the work is a reaction to a user action, use an operation or an interceptor, not a timer.
- When the schedule belongs to the infrastructure (Kubernetes CronJob, system cron calling a REST operation), which keeps the scheduler out of the runtime.
- When exactly-once execution across several nodes is needed and only the in-memory store is configured.

## Related

- [[osgi-karaf-bundle-architecture]] — the scheduler bundle next to app and interceptors
- [[soap-client-integration]] — a typical job target
- [[safe-failure-pattern]] — per-item catch inside jobs
- [[service-delegation-pattern]] — keep the job a thin trigger
- [[scheduled-data-sync-pipeline]] — jobs that run a sync
