---
id: "integration-test-deterministic-time-and-gates"
title: "Deterministic Time, Working-Day and Owner-Gate Testing for JUDO Services"
domain: "backend"
category: "testing"
score: 68.0
usage_count: 1
alternative_count: 0
first_seen: "2026-07-07"
last_updated: "2026-07-07"
projects:
  - park-here
---
## Description

Techniques for writing **deterministic** integration tests over JUDO backend services whose logic
depends on the wall clock, the working-day calendar, per-user notification, or owner-or-admin
authorization. Builds on `integration-test-reflection-injection` (real DAOs + reflection-injected
`@Reference` mocks) and adds four reusable moves that keep such tests stable regardless of when they
run:

1. **Prefer overridable clock seams; fall back to real-clock seeding.** Where a service exposes
   protected `today()` / `currentTime()` seams, subclass and override them for a fixed instant. Where
   a method reads `LocalDate.now()` / `LocalTime.now()` **directly** (no seam), seed the row on the
   real current day with a whole-day window (`00:00`–`23:59`) so a "currently running" predicate holds
   for essentially any run time, and use real future/past dates for the negative cases.
2. **Force the working-day branch with an `AdditionalDay` override.** For clock-reading services that
   gate on `DateService.isWorkingDay(now)` (e.g. a doorman notification job), seed an `AdditionalDay`
   WORK override for `LocalDate.now()` to guarantee a working day (or HOLIDAY to guarantee a
   non-working day), then inject a real `DateServiceImpl` so the override is honoured.
3. **Wire the real ActorService to exercise owner-or-admin gates.** A blanket `ActorService` mock
   leaves `validateCurrentUserHasPermissionTo(...)` a no-op. To actually test the gate, inject the
   real `ActorServiceImpl` with a mocked `VariableResolver` that resolves the acting user by email.
4. **Assert business errors by i18n key and notifications by mock verification.** Mock the I18n
   service with a default answer that echoes each method name, so a thrown business error's message
   equals its i18n key; expose the notification-service mock from the fixture to `verify(...)` the
   per-type notify matrix.

## Structure

```java
// (1a) Overridable seam
ReservationServiceImpl svc = new ReservationServiceImpl() {
    @Override protected LocalDate today() { return fixedDay; }
    @Override protected LocalTime currentTime() { return fixedNow; }
};

// (1b) No seam (method calls LocalDate.now() directly) -> seed on the real day, whole-day window
Reservation running = seedActive(user, slot, NORMAL, LocalDate.now(),
        LocalTime.of(0, 0), LocalTime.of(23, 59));      // cancelable for any run time
Reservation future  = seedActive(user, slot, NORMAL, LocalDate.now().plusDays(5), t9, t10); // rejected

// (2) Force today's working-day classification, then inject a real DateServiceImpl
additionalDayDao.create(AdditionalDayForCreate.builder()
        .withDay(LocalDate.now()).withTypeOfDay(DayType.WORK).build());   // or HOLIDAY
setField(emailSenderService, "dateService", realDateServiceImpl);

// (3) Real ActorServiceImpl + mocked VariableResolver for the owner-or-admin gate
ActorServiceImpl actor = ReferenceInjector.createAndInject(ActorServiceImpl.class, injector);
VariableResolver vr = Mockito.mock(VariableResolver.class);
Mockito.when(vr.resolve(String.class, "ACTOR", "email")).thenReturn(currentUser.getEmail());
setField(actor, "variableResolver", vr);

// (4) i18n key echo + notification verification
ParkHereI18n i18n = Mockito.mock(ParkHereI18n.class, inv -> inv.getMethod().getName());
assertEquals("no_permission_to_delete_other_user_holiday", ex.getDetails().getMessage());
verify(emailSenderMock, times(1)).notifyCreatedReservation(any(Reservation.class));
verify(emailSenderMock, never()).notifyDoorman();
```

## Examples

### park-here
Closing the reservation TEST-GAPS.md P0/P1 items (2026-07): `HolidayServiceTest` uses the real
`ActorServiceImpl` + mocked `VariableResolver` for the `deleteHoliday` owner-or-admin gate, and
seeds real-future dates because `UserReservationPanel.activeReservations` is filtered
`status==ACTIVE && date >= now()`. `CancelReservationTest` seeds a whole-day reservation on
`LocalDate.now()` because `reservationIsCancelable` reads the real clock. `DoormanNotificationJobTest`
seeds an `AdditionalDay` WORK/HOLIDAY override for today to make `notifyDoorman()`'s working-day
branch deterministic. `CreateReservationNotificationTest` verifies the per-type notify matrix through
an exposed `EmailSenderService` mock. All assert business errors against the echoed i18n key.

## Trade-offs

- Pros: tests stay green regardless of the run date/time; genuinely exercises authorization gates and
  the working-day calendar instead of stubbing them out; error-message assertions are stable (keys,
  not localized text).
- Cons: whole-day-window seeding is theoretically fragile in the first/last minute of the day; the
  `VariableResolver`/i18n mock wiring duplicates production DI; reflection field-name coupling (shared
  with `integration-test-reflection-injection`).
- Gotcha: getter optionality is per-attribute — a mandatory flag returns `Boolean` while an optional
  one returns `Optional<Boolean>` (on the same entity). Grep the generated getter's return type before
  asserting; do not assume all flags are Optional.
- Gotcha: do not invent a "per-recipient resilience" test for a loop that has no try/catch — assert
  only the behaviour the code implements.

## Related Patterns

- integration-test-reflection-injection
- actor-resolution-variable-resolver
- handlebars-email-template
