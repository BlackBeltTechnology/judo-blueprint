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
evidence: ["itracker:unrecorded", "mlszksz-platform:unrecorded", "viterra_demo:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "InterfaceRegister:unrecorded", "doors-model:unrecorded"]
alternatives: [excel-data-seed-import]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A fresh deployment needs lookup rows, default configuration and a first account before anyone can use it. An init operation creates them. It runs with no input and no user, and it can be run again without duplicating data.

## Practice

### Platform base

The model defines an initializer operation kind: it must be static and take no input ([operation metamodel](../../agent-docs/model/esm_metamodel/operation.md)). The generated custom-operation class is implemented as an OSGi component with the generated DAOs injected by `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md)); the docs show an `Init` implementation that delegates to a plain importer class. Custom operations are not wrapped by interceptors ([interceptors](../../agent-docs/backend/interceptors.md)). The agent-docs do not describe a startup hook that calls the operation: how and when it runs is a project convention (see [[initializer-entity-with-init-operation]] and [[initializer-operation]]).

### Project practice: seed through DAOs, guard against repeats

- Put the init operation on a dedicated entity or a singleton entity. It takes no input and returns nothing.
- Simple data sets: a model script body creates the rows. Larger or conditional sets: Java with the generated DAOs ([[excel-data-seed-import]] for spreadsheet-driven seeding).
- Make it repeatable: check before creating (for example an existence check, an emptiness check on the entity, or a counter of completed migration steps). Without a guard a second run creates duplicates.
- Split big seeds into several small named operations, one per reference data group.
- Do not use the principal or actor: there is no signed-in user when it runs.

```java
// Example project code
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

Some projects use a parameterless `void run()` style instead. The method signature is whatever the generated interface declares: follow the generated `.default` template.

## Rationale

- The application is usable right after deployment and seed data lives in version control with the code.
- A numbered-step counter allows data changes in later releases without re-running old steps.
- Cost: data hard-coded in code or script, no guard means duplicates, and large sets are better imported from a file or SQL migration.

## Example

- itracker: a model-script init seeds three categories, two regions and three users with different roles.
- mlszksz-platform: a Java init generates default platform logos and initial configuration.
- judo-demo-miniworkflow: two default users created with an existence check before each.
- Ubives: an admin-user init guarded by a count and an identity-provider configuration init.
- ParkHere: a multi-step init (email templates and floor plans into the FileStore, configuration, garages, doormen, parking slots) guarded by an emptiness check; see [[handlebars-email-template]].
- InterfaceRegister: four separate init operations, one per reference data domain.
- doors-model: about 170 contract types seeded by a static operation, plus a versioned migration operation with a counter and seven numbered steps.
- viterra_demo: a template stub whose comments document the sample data (commodities, silos, periods, reports, stock).

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
