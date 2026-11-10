---
id: initializer-entity-with-init-operation
title: Initializer Entity with Static Init Operation
description: A non-CRUD Initializer entity whose single static init operation seeds reference data once at application startup.
aliases: [initializer, init operation, data seeding entity]
keywords: [initializer, static, init, seeding, startup, singleton]
tags: [domain:model, layer:model, layer:backend, project:mlszksz-platform, project:rackinspect, project:park-here, project:ubives, project:workflow-poc, project:judo-demo-miniworkflow, project:trivia, project:itracker, project:viterra_demo, project:InterfaceRegister, project:mjsz, project:doors-model, project:ams-model, status:established]
category: pattern
status: established
projects: [mlszksz-platform, rackinspect, park-here, ubives, workflow-poc, judo-demo-miniworkflow, trivia, itracker, viterra_demo, InterfaceRegister, mjsz, doors-model, ams-model]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "park-here:unrecorded", "ubives:unrecorded", "workflow-poc:unrecorded", "judo-demo-miniworkflow:unrecorded", "trivia:unrecorded", "itracker:unrecorded", "viterra_demo:unrecorded", "InterfaceRegister:unrecorded", "mjsz:unrecorded", "doors-model:unrecorded", "ams-model:unrecorded"]
alternatives: [platform-configuration-singleton]
fragment: initializer-entity-with-init-operation
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give the application one well-known place where reference data is seeded. A static operation named `init` on a dedicated entity is called once per deployment (by the project's startup or deployment routine) and fills the tables that the rest of the model depends on. The entity itself holds no business data and is not edited through the generated actions.

### Initializer is non-CRUD

The entity turns off generated create, update and delete. Only the init operation changes data, so no user can create a second initializer or edit the marker.

### Init is idempotent or guarded

The operation must be safe to run on every start. Either it checks whether the seed data already exists, or it uses a marker that records a completed run.

## Structure

The Initializer entity has a marker attribute and a single static operation. The marker is either a required timestamp (`createdAt`), a required boolean, or absent. The `init` operation is a static, stateful operation flagged as an initializer, with a custom implementation or a model-defined body. Variants split the work into several named static operations (for example `initUsers` and `initVendors`), or put the operation directly on a domain entity when no separate entity is wanted.

## Constraints

- The entity is non-CRUD: createable, updateable and deleteable are all false in the common form.
- The init operation is static and marked as an initializer, and it is stateful because it writes data. The platform rule is that an initializer operation is static and takes no input. The platform defines the operation kind; calling it at startup is a project convention.
- The init operation must not depend on a request user. The project calls it from a startup or deployment routine, not from a signed-in actor, so do not rely on actor or principal variables.
- A seeding operation that runs on every start must check for existing data first, or it creates duplicates.
- Built-in operations and interceptors do not wrap `init`, because `init` is a custom operation. Any audit or logging around the seed has to be written inside `init`.

## Variations

- **Timestamp marker.** The entity has a required `createdAt` timestamp, written when the seed completes.
- **Boolean marker.** The entity has a required `initialized` boolean that defaults to true.
- **No marker.** The entity has no attributes and the operation guards itself with a check on the seeded data.
- **Multiple named initializers.** The entity has several static operations, one per reference data group, each marked as an initializer.
- **Counter-based migrations.** An integer counter records which numbered migration step has run, so each step runs once across deployments.
- **Initializer on a domain entity.** The init operation sits on the entity it seeds, with no separate Initializer entity.
- **Reference data import plus user creation.** The init operation imports reference data from a spreadsheet and also creates identity-server users for the imported people through a user service.

## When to use

- The application needs reference data (codes, default configuration, an admin account) before users can use it.
- The seed must run once per deployment, not once per request.
- Reference data changes over time and needs ordered, repeatable migration steps.

## When to avoid

- The data is user-generated or changes at runtime. Use a normal entity and an operation instead.
- The seed is large and slow. Run it as an out-of-band migration, not on startup.
- A singleton configuration row is all that is needed. See [[platform-configuration-singleton]].

## Related

- [[platform-configuration-singleton]] — a singleton entity for configuration; an initializer can create it
- [[audit-log-entity]] — an audit row for the seed must be written inside `init`, because interceptors do not run for custom operations
- [[interceptor-derived-statistics-calculation]] — interceptors do not wrap custom operations such as `init`
