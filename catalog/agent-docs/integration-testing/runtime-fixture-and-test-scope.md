---
title: Runtime Fixture Internals and Test Scoping
description: "This page explains how the testkit builds the runtime for a test, and how to keep integration tests small and fast."
---
# Runtime Fixture Internals and Test Scoping

This page explains how the testkit builds the runtime for a test, and how to keep integration tests small and fast.

## Guice Injector Composition in Tests

`JudoRuntimeFixture` builds the injector in `init(Module module, Object injectModulesTo)`:

```java
Module modules = Modules.combine(module, judoDefaultModule, databaseModule);
injector = Guice.createInjector(modules);
```

- `module` is your test module (bindings for DAOs, mocks, `@JudoTest(modules = …)` classes).
- `judoDefaultModule` is the JUDO runtime (dispatcher, query factory, interceptor provider, coercer).
- `databaseModule` provides the datasource and transaction manager.
- `injectModulesTo` is the test instance; the fixture injects `@Inject` fields into it from the combined modules.

With `@JudoTest` all of this happens in the extension. A custom fixture only needs to call `prepare(modelName, dataSource, dialect)` and then `init(module, testInstance)`. The `getInjector()` result is the source for DAOs, `Dispatcher` and any bound service: `fixture.getInjector().getInstance(UserDao.class)`.

## Fixture Lifecycle per Test

For every test method the extension prepares a fixture, begins a transaction (`AUTO_ROLLBACK` and `AUTO_COMMIT` only), and in the after-each step rolls back (`AUTO_ROLLBACK`), commits and optionally truncates (`AUTO_COMMIT`), or only truncates (`MANUAL`). `tearDown()` always rolls back a transaction that is still open. The `JudoRuntimeFixture` is the only fixture type the test method may declare as a parameter, next to `JudoDatasourceFixture`.

## Keep Integration Tests Self-Contained

- Create exactly the entities a test needs through DAOs (`EntityForCreate.builder()`), not the application-wide init or master-data seeding. Seeding everything in every test is slow and hides missing setup.
- Prefer class-scoped tests (`dataSourceMode = BY_CLASS`, optionally `shareInjector = true`) over singleton shared state. `BY_CLASS` reuses the datasource and the cached model loader per class, and `SINGLETON` shares them JVM-wide at the price of isolation.
- Do not depend on data left by another test class. Use `AUTO_ROLLBACK` and build the entities in the test or in a helper.
