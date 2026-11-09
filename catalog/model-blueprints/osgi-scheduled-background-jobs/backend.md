## Overview

Implements scheduled background jobs as OSGi Declarative Services components in a dedicated `scheduler` Maven module. Each job is a thin `Runnable` that delegates to a shared business service, with configuration via OSGi Configuration Admin for cron expressions and operational parameters.

## Implementation Pattern

**Job structure:**
- Each job is a `@Component(immediate=true, configurationPid="...", configurationPolicy=REQUIRE, service=Runnable.class)` with `scheduler.concurrent:Boolean=false` to prevent overlapping executions
- The `configurationPolicy=REQUIRE` ensures the job only activates when its configuration (cron expression) is provided via OSGi Config Admin
- Business logic lives in shared services (`@Reference` injection); the job class is 10-20 lines of boilerplate
- Jobs with configurable parameters use `@Designate(ocd=Config.class)` with `@ObjectClassDefinition` for typed configuration

**Typical job categories:**
1. **Data cleanup jobs** -- query entities by status/timestamp filters, delete or transition expired records (e.g., registration cleanup, stale token cleanup, news feed cleanup)
2. **Processing pipeline jobs** -- pick up PENDING records and process them (e.g., notification delivery, feed population)
3. **Expiration jobs** -- find published entities past their expiry date and transition them to EXPIRED status (e.g., post expiration)
4. **Sync jobs** -- reconcile data across entities (e.g., feed-organization sync for new members)
5. **External data refresh jobs** -- fetch data from external APIs and update local entities (e.g., exchange rate updates, ad campaign cost sync)

**Module structure:**
- All jobs live in a `scheduler` module with its own `pom.xml`
- A `SingleInstanceSchedulerActivator` component logs module lifecycle
- Jobs reference services from the `common` module or DAOs from the generated SDK

**Error handling:**
- Each job wraps its `run()` body in try-catch, logging errors but never propagating exceptions (scheduler must not crash)
- Business services handle individual item failures independently (one bad record does not block the batch)

**Transaction management (variant):**
- Some jobs manage their own transactions via `@Reference UserTransaction` with explicit `begin()/commit()/rollback()` when calling generated operation interfaces that require a transactional context
- Other jobs delegate to services that handle transactions internally

## Examples

### mlszksz-platform
- Key files: `scheduler/NotificationDeliveryJob.java`, `scheduler/FeedPopulationJob.java`, `scheduler/PostExpirationJob.java`, `scheduler/RegistrationCleanupJob.java`, `scheduler/StaleTokenCleanupJob.java`, `scheduler/NewsFeedCleanupJob.java`, `scheduler/FeedOrganizationSyncJob.java`
- Pattern: 7 scheduled jobs in a dedicated `scheduler` module, each implementing `Runnable` with `configurationPolicy=REQUIRE` and `scheduler.concurrent=false`. Jobs delegate to services in the `common` module.
- Notable: `StaleTokenCleanupJob` uses `@Designate(ocd=Config.class)` for configurable threshold days. `PostExpirationJob` queries Offers and Requests with `filterByStatus(PUBLISHED).filterByValidUntil(lessThan(now))` then delegates to `PostLifecycleService.expireOffer()/expireRequest()`. All jobs catch exceptions at the top level to prevent scheduler crashes.
- DI wiring: Jobs `@Reference` shared services (PushNotificationService, FeedService, PostLifecycleService) or DAOs (OfferDao, RequestDao, RegistrationRequestDao)

### rackinspect
- Key files: `scheduler/UpdateExchangeRatesJobFirst.java`, `scheduler/UpdateExchangeRatesJobSecond.java`, `scheduler/SingleInstanceSchedulerActivator.java`, `scheduler/RdbmsBasedSchedulerActivator.java`
- Pattern: 2 scheduled jobs for fetching exchange rates from the MNB (Hungarian National Bank) SOAP API at different times (13:00 and 14:00). Jobs implement `Runnable` (not `service=Runnable.class`) with `configurationPid` and `configurationPolicy=REQUIRE`. Jobs manage their own transactions via `@Reference UserTransaction` with explicit `begin()/commit()/rollback()`.
- Notable: Jobs check a `Configuration.updateExchangeRates` boolean flag via `ConfigurationDao` before executing -- providing an admin toggle to enable/disable exchange rate updates. Two scheduler activator variants: `SingleInstanceSchedulerActivator` (RAM-based Quartz for single-node) and `RdbmsBasedSchedulerActivator` (JDBC-backed Quartz for clustered deployments using Liquibase for schema creation with PostgreSQL/HSQLDB dialect detection).
- DI wiring: Jobs `@Reference UpdateExchangeRates` (generated operation interface), `UserTransaction` (JTA), `ConfigurationDao` (feature flag). Activators `@Reference ConfigurationAdmin` (OSGi) and optionally `DataSource` + `LiquibaseExecutor` (for JDBC store).

### indamedia-adtrack
- Key files: `scheduler/FetchCampaignCost.java`, `scheduler/ResetDailyAttributes.java`, `scheduler/UpdateExpiredAggregatedCampaignStatus.java`, `scheduler/SendReminderJob.java`, `scheduler/SingleInstanceSchedulerActivator.java`, `scheduler/RdbmsBasedSchedulerActivator.java`
- Pattern: 4 scheduled jobs in a dedicated `scheduler` module, each implementing `Runnable` with `configurationPid` and `configurationPolicy=REQUIRE`. Jobs delegate to shared services (`AggregatedCampaignService`, `TrackedCampaignService`) from the `common` module. Both `SingleInstanceSchedulerActivator` (RAM-based) and `RdbmsBasedSchedulerActivator` (JDBC-backed) are present.
- Notable: `FetchCampaignCost` fetches current ad spend from external Google Ads API via the service layer. `ResetDailyAttributes` resets daily spend counters and updates cost data for ongoing campaigns. `UpdateExpiredAggregatedCampaignStatus` transitions campaigns past their end date to FINISHED status. `SendReminderJob` is a placeholder (stub implementation). The `RdbmsBasedSchedulerActivator` uses Liquibase to create Quartz JDBC tables, with PostgreSQL/HSQLDB dialect auto-detection -- identical to the rackinspect variant.
- DI wiring: Jobs `@Reference AggregatedCampaignService`, `TrackedCampaignService`, `AggregatedCampaignTransferDao`. Activators `@Reference ConfigurationAdmin`, `DataSource`, `LiquibaseExecutor`.
