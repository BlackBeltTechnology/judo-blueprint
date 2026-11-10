---
id: excel-data-seed-import
title: Excel-Based Initial Data Seeding
description: Seed master data at startup from Excel files by keeping the OSGi component thin and moving the reading and creating into a plain Java importer.
aliases: [Excel import, seed from spreadsheet, initial data from xlsx, init importer]
keywords: [excel, seed, import, init, initializer, POI, DAO, setter injection, idempotent, master data, startup]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: operation
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [init-data-seeding]
related: [custom-operation-osgi-component, service-delegation-pattern, bulk-json-import-export, init-data-seeding]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An application needs a lot of master data from the start (countries, currencies, roles, users, catalogs). Business people can maintain that in spreadsheets. Read the spreadsheets from the classpath in a custom init operation and create the entities through generated DAOs, in dependency order.

## Practice

### Trigger it from an init operation

The trigger is project convention, not a platform startup hook: an operation on an initializer entity that a deployment step or a person calls (see [[init-data-seeding]] and [Custom Operations](../../agent-docs/backend/custom-operations.md#when-to-implement-custom-operations)). The platform does not call it on start by itself.

### Keep the component thin, the importer plain

The operation implementation is an OSGi component that receives the DAOs and hands them to a plain Java importer class, which reads rows and creates entities. The importer can then be unit tested without OSGi. With many DAOs, setter injection with `@Reference` on the setters forwards each one (see [Field vs. Method Injection](../../agent-docs/backend/patterns-and-best-practices.md#field-vs-method-injection)). A thin component delegating to a service is the shape described in [The Custom Service Layer](../../agent-docs/backend/architectural-patterns.md#2-the-custom-service-layer).

### Create in dependency order

Import referenced data before the data that points to it (permissions before roles, roles before users). Create entities with the generated `ForCreate` builder, then link relations with the DAO relation methods. To clear an optional single relation use `unset`, since `set` with null throws (see [Clearing a Relation](../../agent-docs/backend/data-access-guide.md#clearing-a-relation-unset-not-setnull)).

### Make the run repeatable

The source project had no incremental import. Add a guard so a second call does nothing or only fills gaps: check by a natural key with a typed filter and a count, or skip when the initializer has already run (see [Query Result Methods](../../agent-docs/backend/data-access-guide.md#query-result-methods)). Use masks for these existence checks, and an empty mask for the cheapest one.

### Read spreadsheets safely

Apache POI is a project dependency. Read cell values by type, since a numeric cell is not a string, and convert dates and enumerations explicitly (enumerations are written by their model literal, not by ordinal). Do not log passwords from user sheets. A user created here must also exist in the identity provider: the entity row and the Keycloak user can drift, so the init must create or verify the database row itself (see [Keycloak Users and the Entity Store](../../agent-docs/backend/platform-behavior-reference.md#keycloak-users-and-the-entity-store)).

### Mind the transaction and size

The whole import runs in the operation's transaction. A failure in any row rolls back the lot. For very large files split the import into several operations. A custom operation is not intercepted, so interceptors that denormalize on create do not fire for rows created here; run the same recalculation yourself (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

## Rationale

- Spreadsheets are a format business people can edit without developers.
- A plain importer is testable, and the OSGi component only wires.
- Limit: many DAOs mean many setters, and there is no incremental update unless you build it.

## Example

RackInspect: the init component forwards over 30 DAOs by setter injection to an importer. A reader utility reads rows and cells from Excel files on the classpath. The importer creates countries, currencies, languages, permissions, roles, users, brands, dimension templates, error categories and codes, rack types, repair types and items.

## When to avoid

- A handful of rows: create them in code or in a model script (see [[init-data-seeding]]).
- The data changes often after go-live: use migrations or a bulk import operation (see [[bulk-json-import-export]]).
- Test data: use a builder or factory in the test instead.

## Related

- [[init-data-seeding]] — the same trigger without Excel
- [[custom-operation-osgi-component]] — registering the operation implementation
- [[service-delegation-pattern]] — thin component delegating to plain code
- [[bulk-json-import-export]] — bulk import over JSON
