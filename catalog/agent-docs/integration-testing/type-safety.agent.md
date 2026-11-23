# type-safety.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/type-safety.md.

## Overview
- JUDO has two type layers that must not be mixed: entity layer (DAO persistence) and service layer (custom operation inputs and outputs).
- DAOs return entity-layer objects; service inputs expect service-layer types. This is the usual compile error.
- Entity package: `api.*._default_transferobjecttypes.entity.*`. Service package: `api.*.service.*`.

## The Two Type Layers
- Entity layer: used by DAOs; direct database representation.
- Service layer: used by custom operations; external API contract.

## Pre-Generation Checklist
- Decide whether the call is a DAO (`EntityDao.create(EntityForCreate.builder()…)`, entity result) or a custom operation (`CustomOperation.accept(ServiceInput.builder()…)`, service inputs).
- Find service input classes with `find application/sdk/target/generated-sources -name "*Input.java"`. Read builder methods for parameter types.
- Mismatch: passing a DAO result into `withParent(...)` of a service builder fails to compile.

## The Solution: adaptTo() Pattern
- `entityObject.adaptTo(ServiceType.class)` converts an entity to its service-layer type.

## Common Type Conversions
- Every DAO-to-service pair in the table needs `adaptTo()`: User, Address, Activity, Settlement.

## Step-by-Step Type Safety Verification
- Read the custom operation signature (input type is service layer).
- Check each builder parameter: primitives are fine; service-layer types need adaptation.
- For each service-layer parameter, identify the prerequisite entity, the DAO that creates it, and the entity type it returns.
- Generated test: get DAOs from `fixture.getInjector()`, create prerequisites, build the input with `.adaptTo(...)`, run the operation, verify through a DAO query.
- Operation is instantiated with `ReferenceInjector.createAndInject(Class, fixture.getInjector())`.

## Optional Type Handling
- Check whether the service input expects `Optional` or raw values. Wrapping a raw value in `Optional.of(...)` fails to compile when the builder expects a raw `LocalDate`.
- Entity-layer getters may return `Optional` for nullable fields: unwrap with `isPresent()` and `get()` in assertions.

## Enum Type Handling
- Use the generated enum (e.g. `UserRole.ADMIN`), never a string literal.

## Quick Reference: Type Safety Checklist
- Identify prerequisite entities; check each service parameter type; plan `adaptTo()` calls; check Optional handling; use generated enums; use `1L` long literals for ID fields; compile before writing logic.

## Debugging Type Mismatches
- Compiler message names the expected service type and the provided entity type. Fix: add `.adaptTo(<service type>.class)`.

## Examples by Complexity
- Simple: no prerequisites (e.g. CreatePostalCode with a String code).
- Medium: one prerequisite (CreateAddress requires Settlement).
- Complex: several prerequisites (CreatePollingStation requires Address and SettlementElectoralDistrict), each adapted.

## Advanced Mapping Scenarios
- `adaptTo()` is not enough when service and entity differ in derived values, aggregation, field sets or projections.
- Read-by-ID pattern: create via DAO, take `entity.identifier()`, fetch with `dao.getById(id).orElseThrow(...)`, then adapt the fetched object.

## When to Use Read-by-ID Pattern
- Use `dao.getById(entity.identifier())` for lazy relationships, database-generated fields, computed fields from triggers or procedures, complex mappings, aggregations, view projections, and after mutations.

## Common Workflow: Create + Fetch + Adapt
- Create prerequisites (entity layer), create the main entity with its relationship, re-fetch with `getById`, adapt to the service type, build the input, execute the operation.

## Debugging Mapping Issues
- Verify both layers exist in `application/sdk/target/generated-sources` (`*_default_transferobjecttypes/entity/*` and `*/service/*`).
- Compare fields: internal audit fields (createdAt, modifiedAt, version) are missing in service; computed fields (fullName, displayName) are missing in entity; names may differ (`userName` vs `username`).
- If `adaptTo()` yields null or missing data, re-fetch first with `getById(...).orElseThrow()`.

## Key Takeaways
- `adaptTo()` works for simple mappings with identical structure.
- Re-fetch by ID after create when mappings are complex.
- Relationships may be lazy; database-generated fields appear only after fetch.
- When in doubt, re-fetch.

## Quick Decision Tree
- No relationships or computed fields: `entity.adaptTo(ServiceType.class)`.
- Relationships or computed fields: `dao.getById(entity.identifier()).orElseThrow().adaptTo(ServiceType.class)`.
- NullPointerException or missing data: always re-fetch.

## Next Steps
- Getting started with tests (`./getting-started.md`), advanced patterns (`./advanced-patterns.md`), best practices (`./best-practices.md`).
