---
id: init-data-seeding
title: Application Init Data Seeding Operation
description: "Seed reference data and initial accounts with an Init custom operation (model script or Java with DAOs) that is safe to run repeatedly, so a fresh deployment is usable without manual data entry."
aliases: [init operation, startup seeding, bootstrap data]
keywords: [init, seeding, reference data, initializer, idempotent, startup, bootstrap]
tags: ["domain:backend", "layer:backend", "project:itracker", "project:mlszksz-platform", "project:viterra_demo", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:InterfaceRegister", "project:doors-model", "status:established"]
category: operation
status: established
projects: [itracker, mlszksz-platform, viterra_demo, judo-demo-miniworkflow, ubives, park-here, InterfaceRegister, doors-model]
evidence: ["itracker:unrecorded", "mlszksz-platform:application/app/src/main/java/hu/blackbelt/mlszksz/platform/mlszkszplatform/custom/mlszkszplatform/_default_transferobjecttypes/entities/initializer/InitCustomImplementation.java", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "InterfaceRegister:unrecorded", "doors-model:unrecorded"]
alternatives: [excel-data-seed-import]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A fresh deployment needs lookup rows, default configuration and a first account before anyone can use it. An init operation creates them. It runs with no input and no user, and it can be run again without duplicating data.

## Practice

### Platform base

The model defines an initializer operation kind: it must be static and take no input ([operation metamodel](../../agent-docs/model/esm_metamodel/operation.md)). The generated custom-operation class is implemented as an OSGi component with the generated DAOs injected by `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md)); the docs show an `Init` implementation that delegates to a plain importer class. Custom operations are not wrapped by interceptors ([interceptors](../../agent-docs/backend/interceptors.md)). The agent-docs do not describe a startup hook that calls the operation: how and when it runs is a convention (see [[initializer-entity-with-init-operation]] and [[initializer-operation]]).

The platform runs every initializer at each start of the application, when the model's OSGi component activates. Each initializer runs in its own transaction, with no principal and no ACTOR, and a failing initializer is logged while the others still run. Plan for a run on every start, so every seed must be repeatable. See [initializer operations](../../agent-docs/backend/platform-behavior-reference.md#initializer-operations).

### Practice notes: seed through DAOs, guard against repeats

- Put the init operation on a dedicated entity or a singleton entity. It takes no input and returns nothing.
- Simple data sets: a model script body creates the rows. Larger or conditional sets: Java with the generated DAOs ([[excel-data-seed-import]] for spreadsheet-driven seeding).
- Make it repeatable: check before creating (for example an existence check, an emptiness check on the entity, or a counter of completed migration steps). Without a guard a second run creates duplicates. In the OSGi runtime the platform runs every initializer on each start of the model bundle ([platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md#initializer-operations)), so the guard applies on every start.
- Split big seeds into several small named operations, one per reference data group.
- Do not use the principal or actor: there is no signed-in user when it runs.
- For a running-app (browser automation) test the DAO-based initializer is not a test hook. Seed state in the database instead: the `dump` and `import` commands of the generated `judo.sh` script manage PostgreSQL dumps, so build a base dump once and derive test data from it. Values the application sets itself (for example creation timestamps) probably cannot be set through the generated REST API (*verify*); backdate them with SQL against the PostgreSQL container, or leave that rule untested.

```java
// Example code
@Component(immediate = true, service = Init.class)
public class InitCustomImplementation implements Init {
    @Reference CategoryDao categoryDao;

    @Override
    public void accept(Initializer _this) {
        if (categoryDao.query().count() > 0) return;   // guard: already seeded
        categoryDao.create(CategoryForCreate.builder().withName("Category A").build());
    }
}
```

Some applications use a parameterless `void run()` style instead. The method signature is whatever the generated interface declares: follow the generated `.default` template.

## Rationale

- The application is usable right after deployment and seed data lives in version control with the code.
- A numbered-step counter allows data changes in later releases without re-running old steps.
- Cost: data hard-coded in code or script, no guard means duplicates, and large sets are better imported from a file or SQL migration.

## Example

- A model-script init seeds a few categories, regions and users with different roles.
- A Java init generates default logos and initial configuration.
- A demo init creates two default users, each with an existence check.
- An admin-user init guarded by a count, and an identity-provider configuration init.
- A multi-step init (email templates and layout images into the FileStore, configuration, sites, staff, bookable slots) guarded by an emptiness check; see [[handlebars-email-template]].
- Separate init operations, one per reference data domain.
- A static operation seeds a large set of reference types, plus a versioned migration operation with a counter and several numbered steps.
- A template stub whose comments document the sample data (for example categories, locations, periods and reports).

## When to avoid

- Large reference data sets: import them from a file ([[excel-data-seed-import]]) or migrate with scripts.
- Data that users maintain at runtime: seed only the first state.

## Related

- [[excel-data-seed-import]] — spreadsheet-based seeding for large sets
- [[script-driven-operations]] — model-script operation bodies
- [[custom-operation-osgi-component]] — how the init class is registered
- [[initializer-entity-with-init-operation]] — the model shape that hosts the operation
- [[initializer-operation]] — the static initializer operation kind
- [[handlebars-email-template]] — templates seeded into the FileStore
