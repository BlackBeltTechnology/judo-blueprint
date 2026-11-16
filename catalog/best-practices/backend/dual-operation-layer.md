---
id: dual-operation-layer
title: Dual Operation Layer (Actor-Level and Entity-Level)
description: The same business operation can exist on the entity and again on actor-facing transfer objects. Keep the logic in one place and let the duplicates delegate.
aliases: [operation duplicates, actor operation and entity operation, duplicated custom operations]
keywords: [operation, actor, entity, transfer object, mapped, custom implementation, delegation, scaffold, default file]
tags: ["domain:backend", "layer:backend", "project:itracker", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:InterfaceRegister", "project:doors-model", "status:established"]
category: operation
status: established
projects: [itracker, viterra_demo, judo-demo-miniworkflow, ubives, park-here, InterfaceRegister, doors-model]
evidence: ["itracker:unrecorded", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "InterfaceRegister:unrecorded", "doors-model:unrecorded"]
alternatives: []
related: [custom-operation-osgi-component, dual-dao-pattern, script-driven-operations]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Operations are declared on entities and, for the API an actor sees, again on transfer objects. In an application with several actors or pages the same business action therefore appears several times, each with its own generated interface and its own custom implementation to write. Decide which copy holds the logic and make every other copy delegate.

## Practice

### Know why there are several copies

Each operation declaration, wherever it sits (entity, actor transfer object, service-style transfer object), produces its own generated interface and its own `.default` stub. Each custom-implemented copy needs its own `<Op>CustomImplementation` component, placed in the package the generator emitted for its `.default` twin (see [Generator-Emitted Package Convention](../../agent-docs/backend/custom-operations.md#generator-emitted-package-convention)). An operation on a transfer object can also be mapped to the entity operation in the model, which then needs no second implementation; the model side of that is described in [[mapped-operation-delegation]].

### Keep the logic in one service

Put the business rule in a service (or in the entity-level implementation) and let each copy do only the type conversion and call it. This is the thin-adapter shape of the custom service layer (see [The Custom Service Layer](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer)). Several applications did this, turning a modest set of unique actions into a larger set of implementations, all delegating.

### Respect the signature differences

Copies may differ in input and output types. The actor-level copy can return the created object or a UI-facing transfer object while the entity-level copy returns nothing. The bound `_this` is the type of the declaring object, so convert it before calling DAOs (see [Backend Type System Guide](../../agent-docs/backend/type-system-guide.md)). A bound operation must keep parameters compatible with every inherited operation of the same name, and an implementation of an inherited abstract operation must be `stateful` (see [Rules for Custom Operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations)).

### Guard every copy

Interceptors never fire for custom operations, so a permission or state check in one copy does not protect the others. Repeat the check in each copy, or put it in the shared service that all copies call (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Hiding a button does not protect the operation either.

### Keep UI hint fields on the transfer object

Fields such as `editable` or `hideApprove` that exist only for the screen belong on the actor's transfer object, as derived members. They are not operation logic and do not need a second operation.

## Rationale

- One implementation of the rule means one place to fix and test.
- The generator multiplies stubs by declaration, not by behaviour. Delegation keeps the extra code small.
- Limit: every copy is still a class to create and a `.default` to track in `.generator-ignore`. Reduce copies in the model first (see [[mapped-operation-delegation]]).

## Example

- Plan workflow: five operations (create, send for approval, approve, reject, archive plan) exist on the entity and on the actor's initiative view. The actor-level create returns the created object, the entity-level create returns nothing, and the actor view adds several UI fields.
- One invitation operation appears in several views, each implementation calling the same service.
- Calendar operations appear in several panels, all calling a calendar service.
- Create operations exist on the user entity and on the dashboard, bound to different `_this` types and sharing input types.

## When to avoid

- A single actor or screen uses the operation: declare it once.
- The copy would only forward the call and the model can map it to the entity operation instead.
- You cannot keep the copies in step: remove the duplicates rather than letting them drift.

## Related

- [[custom-operation-osgi-component]] — registering each implementation
- [[dual-dao-pattern]] — the two DAO types the copies may see
- [[script-driven-operations]] — the alternative for small bodies
- [[mapped-operation-delegation]] — model-side delegation without a second implementation
