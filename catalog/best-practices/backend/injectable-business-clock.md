---
id: injectable-business-clock
title: Injectable Business Clock with Shared Working-Day Helpers
description: One injectable clock that every custom operation and interceptor uses for the current time, with a configuration or environment override for tests and demos, and one date service for working-day logic.
aliases: [fake now, business clock, date service, working day service]
keywords: [clock, now, time, fake now, override, working day, closed day, date service, deterministic, test]
tags: ["domain:backend", "layer:backend", "project:park-here", "status:single-project"]
category: operation
status: single-project
projects: [park-here]
evidence: ["park-here:application/common/src/main/java/hu/blackbelt/park/here/common/utils/ParkHereClock.java", "park-here:application/common/src/main/java/hu/blackbelt/park/here/common/impl/DateServiceImpl.java"]
alternatives: []
related: [interceptor-derived-statistics-calculation, data-snapshot-versioning]
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Business rules depend on "now": the next working day, a time window, an expiry. If each class reads `LocalDate.now()` itself, tests and demos cannot move time and different classes can disagree on the time zone. Keep one clock in one place, read it everywhere, and allow a start-up override so a test or demo can run at a chosen date.

## Practice

### Platform base

- `Timestamp!now()` in model expressions follows the platform parameter `defaultZoneId`, while `LocalDateTime.now()` in custom Java follows the JVM time zone ([Time and Time Zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones)). A single clock for custom Java removes that second source of divergence in Java code, but not in model expressions.
- Custom operations are OSGi components that reach services with `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). Interceptors are also components ([the interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).

### Practice notes: one clock, one override

The classes below are example code, not platform API.

1. A clock holder: a final class with static accessors (`today()`, `now()`, `nowUtc()`, `instant()`, `get()` and a UTC variant). It has no OSGi dependency, so common services, custom operations and interceptors all use it the same way. An injected `java.time.Clock` field is the alternative when the caller is a component that tests can construct.
2. Production: no override, so it is `Clock.systemDefaultZone()`.
3. Test or demo: a system property or an environment variable holds an ISO local date-time (a bare date means start of day). It is read once at class load.
4. The overridden clock is an offset clock: it starts at the chosen instant and keeps advancing, so timers and audit ordering still work. It does not freeze time.
5. A value that cannot be parsed logs a warning and falls back to real time. It never throws at class load.
6. Log a warning whenever the override is active and keep it out of production configuration.

```java
Clock system = Clock.systemDefaultZone();
Duration offset = Duration.between(Instant.now(), fake.atZone(system.getZone()).toInstant());
Clock business = Clock.offset(system, offset);   // advancing, not frozen
LocalDate today = LocalDate.now(business);
```

Every custom operation and interceptor takes "now" from this holder and never calls `LocalDate.now()` or `Clock.systemUTC()` directly.

### Shared working-day helpers

A date service (an OSGi component) holds the calendar logic that several operations need: `isWorkingDay(date)`, `nextWorkingDay(date)`, `getWorkingDaysBetween(start, end)`. It combines weekends, fixed and moveable public closed days computed per year, and an entity of extra days (extra closed days and extra working days) that administrators maintain. Extra working days win over weekends and closed days. The operation reads the date from the clock and asks the date service for the rule, so a fake "now" also moves every working-day answer.

## Rationale

- One seam makes time-dependent behavior testable without sleeping or patching system time.
- One place for the zone avoids operations that disagree about which day it is.
- Working-day rules in one component stay consistent across operations.
- Cost: a static holder is resolved once, so changing the override needs a restart; the extra-days entity is a query per year on each call unless cached.

## Example

An application has an operation that returns the selectable date window of a quick booking. It takes today from the clock holder, asks the date service for the next working day and the working-day flag of today, and returns the minimum and maximum dates. An end-to-end run sets the environment variable to a Monday morning and gets the same window every time.

## When to avoid

- The application has no time-dependent rules: use plain `java.time`.
- Time must be frozen exactly: use a fixed clock in unit tests instead of an advancing offset.
- The override must change at run time: inject a clock service you can reset, because the static holder is read once.

## Related

- [[interceptor-derived-statistics-calculation]] — an interceptor that builds its thresholds from an injected clock
- [[data-snapshot-versioning]] — snapshot timestamps should come from the same clock as the later queries
- [[test-data-builder-factory]] — test data that depends on the chosen time
