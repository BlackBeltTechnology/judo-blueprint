---
id: "test-data-builder-factory"
title: "Test Data Builder Factory with Service Injection Bridge"
domain: "backend"
category: "testing"
score: 23.8
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - mlszksz-platform
---
## Description

Integration test infrastructure consisting of: (1) `TestDataBuilder` -- a factory class that creates commonly-needed test entities (currencies, items, offers, racks) with caching for reused defaults, (2) `ServiceInjector` -- a utility that bridges OSGi `@Reference` annotated services into the Guice-based test context using reflection-based field injection and Java dynamic proxies for stubs. Tests use `@JudoTest` annotation with HSQLDB and auto-rollback transactions.

## Structure

```java
// Test annotation
@JudoTest(modelName = "app", dialect = "hsqldb",
    transaction = TransactionHandling.AUTO_ROLLBACK,
    modules = { AppDaoModules.class })
class MyServiceTest {
    @Inject JudoRuntimeFixture fixture;
    TestDataBuilder builder;

    @BeforeEach void setup() {
        builder = new TestDataBuilder(fixture);
    }

    @Test void testPricing() {
        Currency huf = builder.createCurrency("HUF", "Forint");
        Item item = builder.createItemWithStandardMinutes(45, 8000.0, huf);
        Offer offer = builder.createOffer(huf);
        // ... test logic
    }
}

// Service injection bridge
PriceService priceService = ReferenceInjector.createAndInject(PriceServiceImpl.class, injector);
```

## Examples

### RackInspect
37 test files. `TestDataBuilder` creates currencies, items with pricing, offers, racks, and fault registries with caching for commonly-used defaults (e.g., HUF currency). `ServiceInjector` uses `ReferenceInjector.createAndInject()` plus manual reflection-based `injectField()` for complex services. 19 pricing test files validate standard minutes calculation, currency conversion, minimum price enforcement.

### mlszksz-platform
20+ test classes with helper-method-based service creation instead of TestDataBuilder. `createActorService(fixture, email)` uses reflection `setField()` to inject VariableResolver mock, UserDao, and i18n mock. Entity helpers: `createTestOrganization()`, `createTestUser()`, `createTestOffer()`. No-op mocks for email service and in-memory FileStore. Tests categorized into entity, operation, service, and job tests.

## Trade-offs

- Pros: Reusable test data creation, caching avoids duplicate entities, bridges OSGi services to test context
- Cons: Reflection-based injection is fragile, ServiceInjector requires manual maintenance when services change
- Alternative: Test-specific Guice modules, or mock-based unit tests instead of integration tests

## Related Patterns

- service-delegation-pattern
- custom-operation-osgi-component
