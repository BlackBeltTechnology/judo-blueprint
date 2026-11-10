---
id: builder-pattern-entity-creation
title: Builder Pattern for Entity Creation (ForCreate Types)
description: "Entities are created through generated EntityForCreate builders passed to the DAO create method; relations to existing entities are set in the builder, and composition children can be created through the parent DAO."
aliases: [ForCreate builder, entity creation builder]
keywords: [builder, forcreate, create, dao, relations, entity creation]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:mlszksz-platform", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:judo-partner", "project:workflow-poc", "status:established"]
category: data-access
status: established
projects: [trivia, rackinspect, itracker, alba, mlszksz-platform, judo-demo-miniworkflow, ubives, park-here, indamedia-adtrack, judo-partner, workflow-poc]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "itracker:unrecorded", "alba:unrecorded", "mlszksz-platform:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded"]
alternatives: [relation-based-entity-creation]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Create entities in backend code through the generated `<Entity>ForCreate` types instead of the read/update entity type. The creation contract is separate from the read/update contract, so only creatable fields can be set, and the compiler checks field names and types.

## Practice

### Platform base

- The generated DAO has `create`/`createAll` (with and without a mask) only for mapped, non-abstract transfer object types ([which types get a full DAO](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)).
- Creation uses the generated builder: `entityDao.create(EntityForCreate.builder().withField(...).build())` returns the persisted entity ([CRUD operations](../../agent-docs/backend/data-access-guide.md#crud-operations)).
- Relations to existing entities are set in the builder, including collections (`.withAudience(list)`). Setting a single relation needs a real object: a `null` fails with a NullPointerException, so leave it unset instead; clearing an existing relation is `unset<Relation>` ([clearing a relation](../../agent-docs/backend/data-access-guide.md#clearing-a-relation-unset-not-setnull)).
- Whether a getter returns a plain value or an `Optional` follows the model's `required` flag, and a field never set is absent, not null ([absent, null and empty](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)).
- Created entities are signed by the runtime when returned to clients. Code cannot mint a signed identifier ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md#signed-identifiers)).

```java
// Example project code: Entity and its generated builder
Entity entity = entityDao.create(EntityForCreate.builder()
    .withField1(value1)
    .withStatus(Status.CREATED)
    .withTimestampOfCreation(LocalDateTime.now())
    .withRelation(existingEntity)
    .build());
```

### Project practice

- Nested creation: build the related entity first and pass it in, for example `.withIdentity(identityDao.create(IdentityForCreate.builder()...build()))`. For composition children use the parent DAO's create method, see [[relation-based-entity-creation]].
- Model-script operations use `new Entity(field = value, ...)`, which produces the same kind of creation; Java code uses the builder.
- One project (mlszksz-platform) used a `ForCreate.create()` factory followed by setters instead of `.builder()`; the agent docs only show the builder, so prefer it.
- Wrap repeated builders for tests in a data builder factory ([[test-data-builder-factory]]).

## Rationale

- Compile-time checking of field names and types, a fluent and declarative style, and relations set in one expression.
- Cost: the creation type is different from the read/update type and cannot be reused; there is no partial creation type.

## Example

Trivia creates a test with status, player, contest, a generated id and a creation timestamp in the enter operation. ALBA sets collection relations inline when creating a product with 15 or more fields. Ubives nests builders when it creates an identity for an invitation or an account principal during seed data. judo-partner creates partners with eight or more fields and log rows through the same builder.

## When to avoid

- To change an existing entity: use `update` with a mask ([[mutable-entity-update-pattern]]).
- To create composition children of a parent: use the parent DAO's create method ([[relation-based-entity-creation]]).
- For bulk loads of many rows: see [[excel-data-seed-import]] and the import practices for batching.

## Related

- [[dao-fluent-query-filter]] — querying the entities after creation
- [[relation-based-entity-creation]] — creating children through the parent
- [[test-data-builder-factory]] — reusing builders in tests
- [[mutable-entity-update-pattern]] — updating instead of creating
