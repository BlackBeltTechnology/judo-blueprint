---
id: test-data-builder-factory
title: Test Data Builder Factory with Service Injection Bridge
description: Integration tests build their prerequisite entities through one application-owned builder class with cached defaults, and wire services into the test context with the platform ReferenceInjector plus small project helpers.
aliases: [test fixture factory, test data factory, service injection bridge]
keywords: [test, data, builder, factory, fixture, JudoTest, ReferenceInjector, JudoRuntimeFixture, DAO, rollback]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "status:emerging"]
category: testing
status: emerging
projects: [rackinspect, mlszksz-platform]
evidence: ["rackinspect:application/test/src/test/java/hu/blackbelt/rackinspect/testsupport/wiring/RackInspectServicesTestModule.java", "mlszksz-platform:application/integration-test/src/test/java/hu/blackbelt/mlszksz/platform/integration/ReferenceInjector.java", "mlszksz-platform:application/integration-test/src/test/java/hu/blackbelt/mlszksz/platform/integration/AuditLogServiceTest.java"]
alternatives: []
related: [service-delegation-pattern, custom-operation-osgi-component, integration-test-reflection-injection]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Integration tests of business logic need the same prerequisite entities again and again (a currency, an item, an order). An application-owned builder class creates them through the generated DAOs and caches the shared defaults, so each test states only what is special about it. A second helper wires services into the test context.

## Practice

### Platform base

The platform testkit provides the test frame: a `@JudoTest` class receives a `JudoRuntimeFixture`, whose Guice injector returns the generated DAOs. The default transaction mode is `AUTO_ROLLBACK`, so entities created in a test disappear afterwards; `truncateTables` applies only to the other modes ([`@JudoTest` parameters](../../agent-docs/integration-testing/getting-started.md), [transaction mode selection](../../agent-docs/integration-testing/best-practices.md)). For custom operations and services, `ReferenceInjector.createAndInject(Class, injector)` creates the instance and fills every non-static, non-final field and single-argument setter whose type the injector can provide. It injects by type and ignores `@Reference` ([Testing Custom Operations with ReferenceInjector](../../agent-docs/integration-testing/getting-started.md#pattern-2-testing-custom-operations-with-referenceinjector)). The platform docs also show a fixture class for reusable test data ([Test Data Management](../../agent-docs/integration-testing/best-practices.md)).

### Builder layer

Everything below is application code, not platform API:

- A `TestDataBuilder` class takes the `JudoRuntimeFixture` in its constructor and resolves the DAOs from `fixture.getInjector()`.
- One `create<Entity>` method per commonly needed entity, with sensible defaults and the few parameters a test usually varies (`createCurrency("USD", "Dollar")`, `createItemWithTimeBased(45, 8000.0, usd)`).
- Defaults that every test reuses (a base currency) are created once per builder and cached in a field. The cache lives as long as the builder, which is built per test in `@BeforeEach`, so it never outlives the rolled-back transaction.
- Builder methods create entities through `ForCreate` payloads and the DAO `create`, and return the created DTO, so a test can pass it on as a relation target.

### Injection bridge layer

Where `ReferenceInjector` is not enough, a helper completes the wiring. Types the injector cannot provide are set reflectively after injection (a field-setting helper), and collaborators that a test does not care about are replaced by stubs, for example Java dynamic proxies that return neutral values. Keep these helpers in one place; they break when a service gets a new dependency.

```java
@JudoTest(modelName = "app", dialect = "hsqldb",
    transaction = TransactionHandling.AUTO_ROLLBACK)
class PricingTest {
    TestDataBuilder builder;

    @BeforeEach void setup(JudoRuntimeFixture fixture) {
        builder = new TestDataBuilder(fixture);
    }

    @Test void pricesOrder(JudoRuntimeFixture fixture) {
        Currency usd = builder.createCurrency("USD", "Dollar");
        Order order = builder.createOrder(usd);
        PriceService service = ReferenceInjector.createAndInject(
            PriceServiceImpl.class, fixture.getInjector());
        // call the service and assert
    }
}
```

`PriceService` and `TestDataBuilder` are example classes.

## Rationale

- Tests stay short and show intent, because setup noise lives in one class.
- Cached defaults avoid duplicate master data inside one test.
- Pros and cons: the builder is cheap to maintain, but reflective helper code is fragile and needs updating when service dependencies change.
- Alternatives: test-specific Guice modules through the `modules` parameter, or mock-based unit tests without the runtime.

## Example

- One application: many test files. `TestDataBuilder` creates currencies, items with pricing, orders, containers and audit registries and caches commonly used defaults such as a base currency. A service injector uses `ReferenceInjector.createAndInject()` plus manual reflective field injection for complex services. Several pricing test files cover time-based calculation, currency conversion and minimum price enforcement.
- One application: many test classes use helper methods instead of one builder. An actor-service factory sets the `VariableResolver` mock, the user DAO and the i18n mock reflectively. Entity helpers such as `createTestAccount()` and `createTestUser()` create data, and no-op mocks stand in for the e-mail service and an in-memory file store. Tests are grouped into entity, operation, service and job tests.

## When to avoid

- The test needs a single entity: call the DAO directly.
- The logic under test is pure and has no runtime dependencies: a plain unit test is faster.
- The builder grows into a second implementation of the domain rules: keep it to creating data.

## Related

- [[integration-test-reflection-injection]] — the reflective injection part in detail
- [[service-delegation-pattern]] — thin operations whose services these tests target
- [[custom-operation-osgi-component]] — the components wired by `ReferenceInjector`
