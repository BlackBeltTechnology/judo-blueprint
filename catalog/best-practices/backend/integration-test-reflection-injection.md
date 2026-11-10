---
id: integration-test-reflection-injection
title: Integration Test Service Wiring via Reflection Injection
description: "In integration tests, wire handwritten services by hand: create the instance, set its @Reference fields by reflection with DAOs from the test injector and mocks for external services, or let the testkit ReferenceInjector fill them by type."
aliases: [reflection injection, test service wiring, ReferenceInjector, manual service wiring]
keywords: [integration test, reflection, injection, service wiring, ReferenceInjector, mock, JudoTest]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: testing
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Container-free tests of services: the OSGi `@Reference` fields of a service are not filled outside the OSGi runtime, so the test fills them itself. Real DAOs come from the test runtime's Guice injector, and external collaborators (variable resolver, mail, file store, i18n) are replaced by mocks.

## Practice

### Platform base: the testkit and ReferenceInjector

The platform docs describe the integration testing setup: a `@JudoTest` class receives a `JudoRuntimeFixture`, whose Guice injector provides the generated DAOs; the transaction mode is chosen per test (rollback is the default) ([getting started](../../agent-docs/integration-testing/getting-started.md), [best practices](../../agent-docs/integration-testing/best-practices.md)). For custom operations the testkit's `ReferenceInjector.createAndInject(Class, injector)` instantiates the class and fills every non-static, non-final field (and single-argument setter) whose type the injector can provide. It injects by type and does not read `@Reference`, because that annotation is invisible to reflection. `injectReferences(instance, injector)` wires an existing instance.

Types the injector cannot provide, such as the `VariableResolver`, are replaced after injection with a reflective field set ([mocking VariableResolver](../../agent-docs/integration-testing/advanced-patterns.md)).

### Project practice: hand-written wiring helpers for service chains

The mlszksz-platform project goes further and wires whole service chains in helper methods: instantiate the implementation, set each field by name through reflection, take DAOs from the fixture's injector, and set mocks for the rest.

```java
// Example project code: ActorServiceImpl, VariableResolver mock helpers are project classes
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
```

- Prefer `ReferenceInjector` for fields the injector can provide, and use hand-written `setField` only for the mocks and for service chains that the injector does not know.
- Typical mocks: the variable resolver returns a test actor e-mail for the actor category, a mail service that does nothing, an in-memory file store, an i18n implementation returning fixed English strings.
- Use rollback per test (and truncating tables where tests depend on empty tables) so tests stay independent.
- Keep field names in one place: the helpers are the single spot that breaks when a field is renamed.

## Rationale

- The real service logic runs against real DAOs and an in-memory database, with no OSGi container.
- Full control over the mocks.
- Cost: reflection by field name fails when a field is renamed (and fails at run time), manual wiring of deep chains is tedious, and mocks must follow interface changes. Mockito or test-specific Guice modules reduce the manual work, and full container tests are slower but more realistic.

## Example

mlszksz-platform: more than twenty test classes use helper methods that build service chains (actor service, user service, post service). Mocks: a variable resolver returning a test e-mail, a no-op mail service, an in-memory file store, an i18n returning fixed English strings. The tests cover entities, operations, services and scheduled jobs, with rollback per test.

## When to avoid

- A test of one custom operation whose dependencies are all DAOs: `ReferenceInjector` alone is enough.
- Pure logic that needs no database: unit-test it with plain mocks.

## Related

- [[test-data-builder-factory]] — creating test entities
- [[service-delegation-pattern]] — the services being wired
- [[actor-resolution-variable-resolver]] — the resolver that tests mock
- [[i18n-osgi-service]] — the i18n service that tests mock
