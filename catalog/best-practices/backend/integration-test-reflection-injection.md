---
id: "integration-test-reflection-injection"
title: "Integration Test Service Wiring via Reflection Injection"
domain: "backend"
category: "testing"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

An integration test pattern where service implementations are instantiated manually and their OSGi `@Reference` dependencies are injected via Java reflection. Helper methods create service instances, use `Field.setAccessible(true)` to bypass access control, and inject DAOs from the JudoRuntimeFixture's Guice injector plus mock implementations for external services (VariableResolver, EmailService, FileStoreService, I18n). This bridges the gap between OSGi runtime DI and test-time DI.

## Structure

```java
@JudoTest(modelName = "App", dialect = "hsqldb",
    transaction = TransactionHandling.AUTO_ROLLBACK,
    truncateTables = true,
    modules = { AppDaoModules.class })
class ServiceTest {

    private ActorService createActorService(JudoRuntimeFixture fixture, String email) throws Exception {
        ActorServiceImpl service = new ActorServiceImpl();
        setField(service, "variableResolver", createMockVariableResolver(email));
        setField(service, "userDao", fixture.getInjector().getInstance(UserDao.class));
        setField(service, "i18n", createMockI18n());
        return service;
    }

    private void setField(Object target, String fieldName, Object value) throws Exception {
        Field field = target.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(target, value);
    }

    // Mock VariableResolver returns email for ACTOR category
    private VariableResolver createMockVariableResolver(String email) {
        return (type, category, name) -> {
            if ("ACTOR".equals(category) && "email".equals(name))
                return type.cast(email);
            return null;
        };
    }

    // No-op email service mock
    private static final PlatformEmailService NO_OP_EMAIL = new PlatformEmailService() {
        @Override public void sendInvitationEmail(...) { }
        @Override public void sendVerificationEmail(...) { }
    };
}
```

## Examples

### mlszksz-platform
20+ test classes use this pattern. Each test class has helper methods to create service chains (ActorService -> UserService -> PostService). Mocks: `VariableResolver` returns test email, `PlatformEmailService` is no-op, `FileStoreService` is in-memory HashMap implementation, `MLSZKSZPlatformI18n` returns hardcoded English strings. Tests cover entities, operations, services, and scheduled jobs with `AUTO_ROLLBACK` and `truncateTables=true`.

## Trade-offs

- Pros: Tests real service logic with real DAOs and in-memory DB, no OSGi container needed, full control over mock behavior, covers integration paths
- Cons: Reflection is fragile (field name changes break tests silently), manual service wiring is tedious for complex dependency chains, mocks must be maintained when service interfaces change
- Alternative: Test-specific Guice modules for cleaner DI, Mockito for mock creation, or full OSGi container tests (slower but more realistic)

## Related Patterns

- test-data-builder-factory
- service-delegation-pattern
- actor-resolution-variable-resolver
