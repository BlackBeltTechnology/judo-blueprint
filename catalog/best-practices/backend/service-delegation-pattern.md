---
id: service-delegation-pattern
title: Service Delegation from Thin Custom Operations
description: "Custom operation implementations stay thin adapters that delegate to shared, plain-Java OSGi service classes holding the business logic, so logic is reused across operations and unit-testable."
aliases: [thin operation, service layer, operation adapter]
keywords: [service layer, delegation, thin operation, custom implementation, OSGi service, reuse, testability]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "status:established"]
category: service
status: established
projects: [rackinspect, mlszksz-platform, ubives, park-here, indamedia-adtrack, judo-partner]
evidence: ["rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/_default_transferobjecttypes/entities/position/DeletePositionCustomImplementation.java", "mlszksz-platform:application/app/src/main/java/hu/blackbelt/mlszksz/platform/mlszkszplatform/custom/mlszkszplatform/services/admin/city/ActivateToggleCustomImplementation.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/AuditLogServiceImpl.java", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded"]
alternatives: [facade-service-pattern]
related: [custom-operation-osgi-component, test-data-builder-factory, facade-service-pattern, action-delegation-workflow, role-based-invitation-guard]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

The generated operation interface fixes the method signature and the declared faults. The logic behind it is often shared by several operations, several actor views of the same operation, or scheduled jobs. The custom implementation therefore only adapts the call and hands it to a service class; the service holds the logic and the DAOs.

## Practice

### Platform base

- This is the platform's documented "custom service layer": the generated `Operation` implementation stays thin and delegates to a handwritten `Service` that contains the logic and injects DAOs ([architectural patterns](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer)).
- Both the operation implementation and the service are OSGi Declarative Services components. `@Component(service = ...)` registers them and `@Reference` injects DAOs and other services ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern), [component annotations](../../agent-docs/backend/patterns-and-best-practices.md)).
- The operation must declare every fault it can throw. A fault that is thrown from a service must be declared on the operation or the SDK interface has no matching `throws` clause ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). Fault classes are generated per application.
- A JCL script operation cannot raise a modeled fault and cannot call an OSGi service. The JCL grammar has no `throw` or fault statement and no service-reference form; its statements are declarations, calls, `return`, `unset`, `delete`, create statements, blocks, `if`, `for` and `while`. Put fault-raising logic and OSGi service calls in a Java custom implementation.
- Interceptors do not fire for custom operations, and a service called from an operation is not intercepted either. Permission and state checks go into the service or the adapter ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- The agent-docs state that synchronous interceptors run inside the operation's transaction; they do not describe the transaction of a service called from an operation, so verify rollback behaviour of a delegated call in a test.

### Practice notes: how applications shape it

This layer is a convention built on the platform, not a platform feature:

- Group services by domain object (`ItemService`, `UserService`, `BookingService`), not by operation. Several operations, including the same operation on several actor views, call one method.
- The adapter body is one to three lines: call the service, then optionally write an audit entry or recalculate something. Typical sizes: a single call, or two calls such as validate then create.
- Put code that must not depend on OSGi in plain service classes taking DAOs as collaborators, so it can be unit-tested; wire it with `@Reference` in the component.
- A helper such as `ActorService`, `EmailSenderService` or `AuditLogService` is itself such a service. Services may call other services.
- Convert identifiers at the adapter: pass `_this.identifier().getIdentifier()` or the entity, whichever the service wants, and keep platform types out of the service API when it is shared with jobs.

```java
// Example code: OperationInterface, SharedService, Entity, Input are generated types
@Component(immediate = true, service = OperationInterface.class)
public class OperationCustomImplementation implements OperationInterface {
    @Reference SharedService sharedService;

    @Override
    public ReturnType method(Entity _this, Input input) throws BusinessErrorException {
        // BusinessErrorException is a fault modeled by the application, not a platform class
        return sharedService.doBusinessLogic(_this, input);
    }
}

@Component(immediate = true, service = SharedService.class)
public class SharedServiceImpl implements SharedService {
    @Reference EntityDao entityDao;
    @Reference OtherService otherService;

    public ReturnType doBusinessLogic(Entity entity, Input input) { /* logic */ }
}
```

## Rationale

- One implementation of a rule, however many operations, actors or jobs reach it.
- The adapter is trivial, so the logic can be tested without the operation plumbing.
- The cost is one more layer and one more interface per service, and a call chain that is longer to trace.

## Example

- One application: most custom operations delegate to a set of services (orders, audit registry, items, price modifiers, job tasks, reports, e-mail, containers). The close-order operation is one line that calls the order service.
- One application: many operations delegate to many services; each operation delegates, then writes an audit entry.
- Another application: many mostly one-line operations, repeated across several actor views.
- One application: a set of operations over a few services; the booking operation validates input, then creates the booking.
- Another application: a set of operations over a few services; untracking calls the tracked-item service, then recalculates spendings.
- A third application: a set of operations over a few services; account creation calls the account service, then logs the action.

## When to avoid

- A tiny operation with one DAO call and no reuse: a service adds indirection without benefit.
- The logic is a status change that the model can express itself ([[script-driven-operations]]).
- Do not let the service become a god class: split by domain object, or use a facade deliberately ([[facade-service-pattern]]).

## Related

- [[custom-operation-osgi-component]] — how the adapter component is registered
- [[facade-service-pattern]] — one service in front of several others
- [[action-delegation-workflow]] — delegation through entity-bound operations instead of services
- [[test-data-builder-factory]] — testing services and operations
- [[role-based-invitation-guard]] — a guard placed in the operation before delegating
- [[script-driven-operations]] — the no-Java alternative
