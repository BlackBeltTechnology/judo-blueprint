---
id: osgi-scheduled-background-jobs
title: OSGi Scheduled Background Job Framework
description: A pattern for running scheduled background jobs in a JUDO application as thin OSGi Declarative Services components that delegate to shared services.
aliases: [scheduled jobs, background jobs, OSGi scheduler]
keywords: [osgi, scheduled, background, job, framework, jobs, cron, scheduler]
tags: [domain:model, layer:backend, project:mlszksz-platform, project:rackinspect, project:indamedia-adtrack, project:park-here, status:established]
category: pattern
status: established
projects: [mlszksz-platform, rackinspect, indamedia-adtrack, park-here]
evidence: ["mlszksz-platform:application/scheduler/src/main/java/hu/blackbelt/mlszksz/platform/scheduler/SingleInstanceSchedulerActivator.java", "rackinspect:application/scheduler/src/main/java/hu/blackbelt/rackinspect/scheduler/SingleInstanceSchedulerActivator.java", "indamedia-adtrack:unrecorded", "park-here:unrecorded"]
alternatives: []
related: [osgi-service-layer-delegation, ongoing-finished-deleted-status-enum]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Run periodic work (cleanup, expiry, sync, external refresh) outside the request cycle, without putting the business logic in the job class. The job only triggers; a shared service does the work and can be reused by operations.

### Jobs are thin and configured from outside

Each job is an OSGi component that implements `Runnable`. Its schedule and tuning values come from OSGi Configuration Admin, so the cron expression can change without a code change. A job without its configuration does not start.

### One scheduler module, one run at a time

The jobs live together in a dedicated scheduler module, and a job is not allowed to overlap with its own previous run. The module is a backend-only concern; no model element is generated for it.

## Structure

A job is a component that exposes the `Runnable` service and requires its configuration before it activates. It references one shared business service (and through it the generated DAOs). The job body is a short wrapper around a single service call. Configurable values are declared with a typed configuration definition.

Jobs fall into five kinds: data cleanup (delete or transition stale records), processing pipeline (pick up pending records), expiration (move past-due records to an expired state), sync (reconcile related data), and external refresh (pull data from an outside API).

## Constraints

- The job must not let an exception escape `run()`. It logs the error and returns, so the scheduler keeps running.
- Business services handle each item independently, so one bad record does not block the batch.
- Overlapping runs of the same job are switched off in the component properties.
- The job activates only when its configuration is present (configuration policy `require`).
- A job has no acting user of its own. If a rule depends on who acts, the service must receive that information explicitly.
- The scheduler is not a JUDO interceptor and not a custom operation, so interceptors never run for it (interceptors fire only on built-in operations, and not even on custom ones). Rules that apply to the data must be enforced in the service it calls.
- A scheduled run is outside any request-scoped transaction. In the source projects each job or service manages its own transaction around its database work (project practice, see [[quartz-scheduled-job]]).

## Variations

- **Cleanup or expiry job.** Query by status and timestamp, then transition or delete in the service. Use this for records that age out.
- **Pipeline job.** Pick up records in a pending state and process them in batches. Use this for queued work such as notifications.
- **External refresh job.** Call an external API through an adapter and update local entities. Keep the adapter behind an interface so it can be replaced in tests.
- **Shared service with operations.** The same service may also be called from a custom operation, so the job and the operation share one code path.

## When to use

- Work must happen on a schedule and not in response to a user action.
- The same business logic is needed both from a schedule and from an operation.
- Schedules must be changeable without redeploying code.

## When to avoid

- The work must run immediately when a user changes data. Use an operation or an interceptor for built-in create, update and delete.
- The work is a long-running data pipeline with its own state and retries. Use a dedicated pipeline pattern instead.
- A job would need to run on several instances at once without coordination.

## Related

- [[osgi-service-layer-delegation]] — the shared service layer that every job calls
- [[quartz-scheduled-job]] — the Quartz-based variant of the same job idea, with transaction handling
- [[ongoing-finished-deleted-status-enum]] — scheduled jobs reuse the same service that the lifecycle operations use
