---
id: dual-dao-pattern
title: Dual DAO Injection (Entity-Level + Actor-Level)
description: A custom operation may see two generated DAOs for one entity, one for the entity and one for an actor's transfer view, whose simple names may or may not clash. Know which one you inject and why.
aliases: [two DAOs same name, actor DAO, entity DAO and transfer DAO]
keywords: [dao, injection, actor, entity, transfer object, package, reference, service layer, entity layer]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:indamedia-adtrack", "status:emerging"]
category: di
status: emerging
projects: [trivia, indamedia-adtrack]
evidence: ["trivia:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: []
related: [custom-operation-osgi-component, identifier-adaptation-pattern]
first_seen: 2026-03-04
last_updated: 2026-11-11
---
## Intent

For one entity the generator can produce more than one DAO type: one for the entity itself and one for a transfer object that an actor sees. Whether their simple names clash depends on how the transfer object is named. If it carries the entity's name, both DAOs share a simple name in different packages. If it has a distinct name, for example one ending in `Transfer`, the DAO name is distinct too (`…TransferDao`). A custom operation that injects both must keep them apart. In most operations one DAO is enough, and the entity DAO is the right default.

## Practice

### Default to the entity DAO

The entity DAO has full create, read, update and delete methods and relation accessors. The generated DAO interface gives full CRUD only for mapped, non-abstract transfer object types, and unmapped transfer objects get only `query...()` accessors (see [Which Types Get a Full DAO](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)). The platform describes two type layers, a service layer used in operation inputs and outputs and an entity layer used by DAOs for persistence (see [Backend Type System Guide](../../agent-docs/backend/type-system-guide.md)). Persist and query through the entity layer.

### Inject the actor-side DAO only when you need its view

Inject the actor-side DAO only if the operation must read or return the actor-scoped shape of the data, for example to reuse what the actor can see. If the simple names collide, use a fully qualified name for one of the two; with distinct transfer object names a plain import is enough. Do not inject it as a precaution: an injected but unused DAO adds an OSGi dependency and noise.

### Do not rely on the choice of DAO for permissions

The agent-docs do not describe the DAO type as an access control mechanism. Permission scope comes from the actor's transfer objects and access paths in the model. Interceptors never fire for custom operations, so a permission check for a custom operation belongs inside the implementation (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

### Convert instead of double-fetching

When an input carries a service-layer object and the DAO wants an entity-layer one, convert with `getById(input.getX().identifier())` or `adaptTo`, rather than injecting a second DAO to fetch it. `getById` also checks that the instance exists (see [Converting Between Layers](../../agent-docs/backend/type-system-guide.md#converting-between-layers)).

## Rationale

- Using only the DAOs you need keeps the operation readable and its dependency list short.
- Two same-named types in different packages compile fine and import wrongly. Fully qualified names make the choice visible. With distinct names the service-layer DAO is told apart by its name alone.
- The exact package layout depends on the generator version. This entry records what one application saw, not a platform contract. Check the generated sources of your application.

## Example

A custom implementation of an operation on `Order` injects the entity DAO for `Order` for all reads and writes. It also injects the DAO generated for the customer actor's `Order` view, using its fully qualified name. The customer-side DAO is never called in the current code, so the injection is redundant.

An operation on a tracked-item transfer object injects the service-layer `…TransferDao` and calls a `query...()` accessor, and scheduled jobs inject the grouped-item transfer DAO. Their names do not clash with the entity DAOs.

## When to avoid

- The operation needs only entity data: inject the entity DAO alone.
- You want field-level restriction for the caller: model it in the actor's transfer object and access, or filter in the operation, instead of relying on a second DAO.

## Related

- [[custom-operation-osgi-component]] — how DAOs reach a custom operation through `@Reference`
- [[identifier-adaptation-pattern]] — converting identifiers between the two types
