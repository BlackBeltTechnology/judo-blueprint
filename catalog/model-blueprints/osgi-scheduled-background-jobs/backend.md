## Overview

Scheduled jobs are OSGi Declarative Services components in a dedicated scheduler module. Each job implements `Runnable`, is configured through OSGi Configuration Admin, and calls one shared business service. The job itself holds no business logic.

## Implementation Pattern

### Job component
- Expose the job as a `Runnable` service. Set the component to require its configuration, so the job starts only when its cron expression is provided.
- Turn off overlapping runs of the same job with the scheduler's concurrency property.
- Use a typed configuration definition for each tunable value (cron, thresholds, batch size).

```java
@Component(immediate = true, configurationPid = "example.job.cleanup",
           configurationPolicy = ConfigurationPolicy.REQUIRE,
           property = { "scheduler.concurrent:Boolean=false" },
           service = Runnable.class)
@Designate(ocd = CleanupJobConfig.class)
public class StaleRecordCleanupJob implements Runnable {

    @Reference
    private StaleRecordService staleRecordService; // example project code

    @Override
    public void run() {
        try {
            staleRecordService.purgeStaleRecords();
        } catch (Exception e) {
            LOG.error("Cleanup job failed", e); // never let the scheduler see the exception
        }
    }
}
```

`StaleRecordService` and the class names are example project code, not platform API.

### Business logic
- The service holds the work and reads the DAOs of the generated SDK through `@Reference`.
- The service handles each item on its own. A bad record is logged and skipped, so it does not stop the batch.
- Because a job is not an operation, interceptors do not run for the work it does (platform: interceptors fire only on built-in operations). If the same rules must hold for the data, call them from the service explicitly.
- A scheduled run has no request transaction. Open and close a transaction in the job or service around the database work (project practice, see [[quartz-scheduled-job]]); the job also has no principal or actor, so pass the acting identity explicitly if a rule needs it.

### Job categories
1. Cleanup: find records by status and age, then delete or transition them.
2. Pipeline: pick up records in a pending state and process them in batches.
3. Expiration: find published records past their end date and move them to an expired state.
4. Sync: reconcile related data after a change (for example, new members joining an organization).
5. External refresh: fetch data from an outside API through an adapter and update local entities.

### Module layout
- All jobs live in one `scheduler` module with its own build descriptor.
- A small activator component logs the module lifecycle. It does not run any work.
- Jobs depend on services in the common module, not on the other job modules.

### Error handling
- Wrap the body of `run()` in a try-catch. Log the error and return.
- Let the service decide per item what to do with a failure.
