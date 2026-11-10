---
id: custom-operation-osgi-component
title: Custom Operation OSGi Component Registration
description: "A custom operation is an OSGi Declarative Services component that implements the generated operation interface, registered with @Component(immediate = true, service = ...) and wired with @Reference."
aliases: [CustomImplementation, custom operation registration, operation component]
keywords: [custom operation, osgi, component, declarative services, reference, CustomImplementation, generator-ignore]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:mlszksz-platform", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:InterfaceRegister", "project:judo-partner", "project:workflow-poc", "project:doors-model", "status:established"]
category: di
status: established
projects: [trivia, rackinspect, itracker, alba, mlszksz-platform, viterra_demo, judo-demo-miniworkflow, ubives, park-here, indamedia-adtrack, InterfaceRegister, judo-partner, workflow-poc, doors-model]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "itracker:unrecorded", "alba:unrecorded", "mlszksz-platform:unrecorded", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "InterfaceRegister:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "doors-model:unrecorded"]
alternatives: [script-driven-operations]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Every operation the model marks as custom needs a handwritten implementation. The platform wires it through OSGi Declarative Services: the class implements the generated interface and is registered as an OSGi service, and its dependencies (DAOs, other operations, project services) come in through `@Reference`.

## Practice

### Platform contract

The platform docs define this pattern ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)):

```java
@Component(immediate = true, service = GeneratedOperationInterface.class)
public class OperationNameCustomImplementation implements GeneratedOperationInterface {

    @Reference
    EntityDao entityDao;

    @Reference
    ExternalService externalService;   // example project service

    @Override
    public ReturnType apply(EntityType _this, InputType input) {
        // business logic using injected DAOs
    }
}
```

- `immediate = true` starts the component when the bundle activates; `service = X.class` registers it as the OSGi service for the generated interface.
- `@Reference` injects DAOs, other custom operations, `VariableResolver` and your own services ([injecting DAOs and services](../../agent-docs/backend/data-access-guide.md#injecting-daos-and-services)). Field injection is the default; method injection suits delegation ([field vs. method injection](../../agent-docs/backend/patterns-and-best-practices.md#field-vs-method-injection)). A mandatory reference that is missing stops the component from activating.
- The generator emits a `.java.default` stub for each custom operation in the generator's own package under `.generated-files`; write your class in the same package without the `.default` suffix and add the stub's path to `.generator-ignore` ([generator-emitted package convention](../../agent-docs/backend/custom-operations.md#generator-emitted-package-convention)). Never edit the `.default` file.
- A fully implemented class can still carry the stub `G E N E R A T E D` header; compare with the `.default` sibling, whose body only throws `UnsupportedOperationException`.
- Declare any fault the implementation throws in the model, otherwise the build fails with `not compatible with throws clause`. An implementation of an inherited abstract operation must be `stateful`, matching all overloads ([rules for custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).
- Interceptors and write guards never fire for custom operations, so permission checks go inside the implementation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- The class name `<Op>CustomImplementation` is a convention; the interface path names the model operation.

### Project practice: keep the component thin

Most projects keep the component to a few lines and delegate to a shared service injected with `@Reference` ([[service-delegation-pattern]]); mlszksz-platform has more than 60 operations that inject only services such as a post, audit-log or actor service (example project classes). For heavy logic with many dependencies, the component can build a plain Java object and pass the injected services to it through setters, so the logic is testable without OSGi (delegated implementation with dependency injection bridge, [custom operations example 4](../../agent-docs/backend/custom-operations.md#example-4-delegated-implementation-with-dependency-injection-bridge); see also [[integration-test-reflection-injection]]).

- One operation per class; group classes by the model's transfer-object path, mirroring the generated packages.
- Start from the DAO-level patterns in [[dual-dao-pattern]] and [[entity-re-fetch-pattern]] when the operation receives a bound instance.
- Model scripts can implement logic without Java ([[script-driven-operations]]).
- Operations that are only declared in the model (for example in a repository that provides the implementations separately) leave the `.default` stubs unimplemented until the backend project supplies the components.

## Rationale

- Standard OSGi wiring, hot deployment in Karaf, and a clear split between generated and handwritten code.
- Cost: needs an OSGi container (or a test bridge) to run, and a build/regeneration cycle when the model operation changes.

## Example

Trivia implements eight operations (register, enter, and others) that inject DAOs and the e-mail service. Ubives has 42 operations over ten service domains that delegate with one-line service calls. judo-partner has 15 operations delegating to seven service classes. workflow-poc registers four operations plus two utility components that are injected into them. Several demo projects leave the generated `.default` stubs unimplemented and rely on model scripts.

## When to avoid

- When the logic can be a model expression, derived member or script: no component is needed.
- When a built-in create/update/delete only needs a pre or post step: use an interceptor instead ([[interceptor-crud-lifecycle]]).

## Related

- [[service-delegation-pattern]] — thin operation, logic in a service
- [[dual-dao-pattern]] — DAO usage inside operations
- [[entity-re-fetch-pattern]] — re-load the bound instance
- [[script-driven-operations]] — alternative without Java
- [[generator-ignore-config-protection]] — keeping custom classes safe from regeneration
- [[interceptor-crud-lifecycle]] — pre/post steps for built-in operations
