---
title: Interceptor Testing with the JUDO Testkit
description: "Integration test for an interceptor: testing OperationCallInterceptor implementations with @JudoTest(interceptors = …), JudoRuntimeFixture.addInterceptor(…), spy interceptors and execution order."
aliases: [test an interceptor, interceptor integration test, testing interceptors, interceptor execution order in tests, spy interceptor, interceptor dependency injection in tests]
keywords: [OperationCallInterceptor, JudoTest, JudoRuntimeFixture, addInterceptor, TestOperationCallInterceptorProvider, ReferenceInjector, injectReferences, preCall, postCall, shareInjector, clearInterceptors]
tags: [domain:testing, layer:test, status:platform]
---
# Interceptor Testing with the JUDO Testkit

This page covers testing `OperationCallInterceptor` implementations with `@JudoTest(interceptors = …)` and `JudoRuntimeFixture.addInterceptor(…)`. For the production side (what interceptors are, when to write them) see [Interceptors](../backend/interceptors.md).

## OperationCallInterceptor Contract Seen from Tests

```java
public interface OperationCallInterceptor {
    String getName();

    // Empty collection = intercept ALL operations
    default Collection<EOperation> getOperations(AsmModel asmModel) {
        return Collections.emptyList();
    }

    // Called BEFORE the operation executes; may modify the input
    default Object preCall(EOperation operation, Object parameterPayload) {
        return parameterPayload;
    }

    // Called AFTER the operation executes; may modify the output
    default Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        return returnPayload;
    }
}
```

## Interceptor Execution Order

All interceptors registered for an operation run in **registration order** for `preCall` **and** for `postCall`. `postCall` is not reversed. The order of the `interceptors = {A.class, B.class}` array (or of the `addInterceptor` calls) is therefore the order of both hooks.

```
Dispatcher.callOperation()
    ▼
FOR EACH interceptor (registration order): preCall(operation, input)
    ▼
Execute the actual operation
    ▼
FOR EACH interceptor (registration order): postCall(operation, input, output)
    ▼
Return result
```

## Deferred Injection of Interceptor Dependencies

Interceptors need DAOs and services, but the Guice injector is created after the interceptor provider is configured. `JudoRuntimeFixture.init(module, testInstance)` solves this in order:

1. Instantiate every interceptor class with its **public no-arg constructor** (a missing constructor fails with a clear message).
2. Register the instances in a `TestOperationCallInterceptorProvider`.
3. Build the JUDO default module with that provider, `Modules.combine(module, judoDefaultModule, databaseModule)`, and create the injector.
4. Inject dependencies into the already registered instances with `ReferenceInjector.injectReferences(interceptor, injector)`.

`ReferenceInjector` injects **by type**: every non-static, non-final field and every single-argument `set*` method whose type the injector can provide. It ignores `@Reference` and `@Inject` (OSGi's `@Reference` has CLASS retention and is invisible to reflection), so an interceptor field of an unbound type stays `null` silently.

## Pattern: Annotation-Based Interceptor Test

```java
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest;
import hu.blackbelt.judo.dispatcher.api.Dispatcher;

class MyInterceptorIntegrationTest {

    @JudoTest(interceptors = {AuditInterceptor.class, ValidationInterceptor.class})
    void testMultipleInterceptors(JudoRuntimeFixture fixture) {
        Dispatcher dispatcher = fixture.getInjector().getInstance(Dispatcher.class);

        // preCall and postCall both run AuditInterceptor first, then ValidationInterceptor
        dispatcher.callOperation("model.User.createUser",
            Payload.map("__exposed", true, "email", "test@example.com"));
    }
}
```

## Pattern: Programmatic Interceptor Registration

Use this when an interceptor needs constructor arguments. Register interceptors **before** `init()`; `getInterceptorProvider()` is only available after `init()`.

```java
fixture = new JudoRuntimeFixture();
fixture.prepare("modelName", dataSource, "hsqldb");

fixture.addInterceptor(AuditInterceptor.class);                    // created via no-arg constructor
fixture.addInterceptor(new ConfiguredInterceptor("custom-value")); // pre-configured instance

fixture.init(new AbstractModule() {}, null);                       // deferred injection happens here
```

Pre-configured instances receive the same by-type injection as class-registered ones. Call `fixture.tearDown()` and close the datasource in `@AfterEach`.

## Pattern: Unit-Testing Interceptor Logic Directly

```java
@JudoTest
void testPreCallLogic(JudoRuntimeFixture fixture) {
    MyInterceptor interceptor = ReferenceInjector.createAndInject(
        MyInterceptor.class, fixture.getInjector());

    Object result = interceptor.preCall(null, Payload.map("email", "test@example.com"));
    assertNotNull(result);
}
```

## Pattern: Spy Interceptor

```java
public class SpyInterceptor implements OperationCallInterceptor {
    private final AtomicInteger preCallCount = new AtomicInteger();
    private final AtomicInteger postCallCount = new AtomicInteger();

    @Override public String getName() { return "SpyInterceptor"; }
    @Override public Object preCall(EOperation op, Object payload) { preCallCount.incrementAndGet(); return payload; }
    @Override public Object postCall(EOperation op, Object in, Object out) { postCallCount.incrementAndGet(); return out; }
    public int getPreCallCount() { return preCallCount.get(); }
    public int getPostCallCount() { return postCallCount.get(); }
    public void reset() { preCallCount.set(0); postCallCount.set(0); }
}

@JudoTest(interceptors = {SpyInterceptor.class})
void testWithSpy(JudoRuntimeFixture fixture) {
    SpyInterceptor spy = (SpyInterceptor) fixture.getInterceptorProvider().getInterceptors().get(0);
    // call an operation through the Dispatcher, then:
    assertEquals(1, spy.getPreCallCount());
    assertEquals(1, spy.getPostCallCount());
}
```

### Stateful Interceptors with a Shared Injector

With `shareInjector = true` on a `BY_CLASS` or `SINGLETON` class, the same injector and therefore the same interceptor **instance** is reused across test methods, so counters accumulate. The default (`shareInjector = false`) gives every method a fresh interceptor while still sharing the datasource and model loader. If you opted in to sharing, call `spy.reset()` in `@BeforeEach`, or drop back to `dataSourceMode = BY_METHOD`.

## Pattern: Changing Interceptors Mid-Test

```java
@JudoTest(interceptors = {InterceptorA.class})
void testDynamicInterceptors(JudoRuntimeFixture fixture) {
    TestOperationCallInterceptorProvider provider = fixture.getInterceptorProvider();
    provider.addInterceptor(new InterceptorB());   // appended: runs after A
    // ... call operation: A then B
    provider.clearInterceptors();                  // no interceptor runs any more
}
```

## Checklist: Writing Interceptor Tests

- [ ] The interceptor has a public no-arg constructor (or is registered as an instance).
- [ ] `addInterceptor(...)` is called before `init()` in programmatic setups.
- [ ] `getInterceptorProvider()` is used only after `init()`.
- [ ] Dependencies are fields or `set*` setters of types bound in the Guice injector (injection is by type, annotations are ignored).
- [ ] The test relies on registration order for both `preCall` and `postCall`.
- [ ] Stateful interceptors are reset or isolated when the injector is shared.
