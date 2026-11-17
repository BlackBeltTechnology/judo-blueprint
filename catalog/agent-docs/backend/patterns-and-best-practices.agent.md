# patterns-and-best-practices.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/patterns-and-best-practices.md.

## Table of Contents

- Lists the source's sections: OSGi, patterns 1, 4, 5, 6, utilities, query patterns, best practices.

## Core Technologies: OSGi and Declarative Services

- Backend code runs in OSGi; use Declarative Services annotations.
- `@Component(immediate = true, service = X.class, property = {...})`: marks an OSGi component; `service` is what it implements.
- `@Reference`: injects another OSGi service (DAO, platform utility). `cardinality = OPTIONAL` for optional, `MULTIPLE` for `List<...>`. Default is mandatory: activation fails if missing.
- `@Activate`: runs after injection and activation.
- Field injection is the default; method injection (`@Reference public void setX(...)`) is for delegation to a POJO.

## 1. Manual Polymorphic Factory

- Use when an operation creates one of several concrete subtypes based on an input type field (e.g. enum `VoteType`).
- Branch with `if/else if` or `switch` on the type field; in each branch create the concrete entity with its own DAO and `ForCreate` builder.

## 4. Pattern: Accessing User & Request Context

- Inject `hu.blackbelt.judo.dispatcher.api.VariableResolver`; call `variableResolver.resolve(String.class, "ACTOR", "email")` (Java equivalent of JQL `!getVariable("ACTOR", "email")`). Also `"identifier"`.
- Advanced, break-glass only: generic `hu.blackbelt.judo.dao.api.DAO` plus `AsmModel`/`AsmUtils` to look up `EClass` by name, then `dao.addReferences()`. Bypasses typed DAOs; use with extreme care.

## 5. Pattern: Implementing a Custom Data Type

- Use for rich non-primitive types (e.g. GPS, Money). Persisted and sent over API as `String`. JQL supports only direct attribute selection; no custom methods in JQL.
- Steps: (1) model a `CustomType` in the `types` package; (2) Java class with `toString()` and static `parseString(String)`; (3) class implementing `Converter<String, YourType>`; (4) OSGi component that calls `DataTypeManager.registerCustomType(...)` on activation.
- `DataTypeManager` is per model, with property `judo.model.name=<model>`; use `@Reference(target = "(judo.model.name=<App>)")`. Same for `AsmModel`.
- Resolve model type: `new AsmUtils(asmModel.getResourceSet()).resolve("<App>.types.Gps")`, cast to `EDataType`.
- Registering the same `EDataType` twice throws `IllegalStateException("Custom type already registered")`. Call `unregisterCustomType(modelType)` in `@Deactivate`.
- Overload `registerCustomType(modelType, javaClassName, converters, formatter)` takes a `Formatter<T>` (`getType()`, `convertValueToString`, `parseString`) and creates both converter directions; no hand-written `Converter` needed.
- Coercer: one `ExtendableCoercer` per model; `coerce(value, Class)`. `Converter` has `getSourceType()`, `getTargetType()`, `apply(Object)`. OSGi `ExtendableCoercerService` also picks up registered `Converter` services.

## 6. Pattern: Implementing Custom Validation

- Throw standard unmodeled exceptions (package `hu.blackbelt.judo.runtime.core.exception`, module `judo-runtime-core`; unchecked `ClientException` subclasses):
  - `ValidationException` (takes a collection of `ValidationResult`) -> HTTP 400
  - `AuthenticationRequiredException` -> 401
  - `AccessDeniedException` -> 403
  - `NotFoundException` -> 404
  - Other three take a single `ValidationResult`.
- Build results with `ValidationResult.builder().code("...").level(ValidationResult.Level.ERROR).build()`.
- Business rules the client should handle as typed errors are modeled faults (HTTP 422), see [Error Handling Guide](error-handling-guide.md).
- Platform codes (constants on `Validator`): `MISSING_REQUIRED_ATTRIBUTE`, `MISSING_REQUIRED_RELATION`, `MAX_LENGTH_VALIDATION_FAILED`, `PATTERN_VALIDATION_FAILED`, `NOT_ACCEPTED_BY_RANGE`. The runtime enforces required attributes and relations; do not repeat them.
- Generic model-driven validator: create a component implementing `hu.blackbelt.judo.runtime.core.validator.Validator` (module `judo-runtime-core-validator`). Model trigger element (e.g. custom type `FutureTime`); `isApplicable(EStructuralFeature)` selects targets; `validateValue(Payload, EStructuralFeature, Object, Map<String,Object>)` returns `ValidationResult`s. Runs on every applicable attribute in every request.

## Utility Patterns

### ValidationUtils

- Centralize reusable checks: `validateEmail`, `validateDateRange` (end not before start), `validateRequired(value, fieldName)`, `validateNotNull`. They throw `IllegalArgumentException`.
- Private constructor throwing `UnsupportedOperationException`. Email regex is in the source.

### TypeConverter

- Null-safe `convert(MapHolder source, Class<T>)` using `source.adaptTo(targetClass)`; returns null on null input.
- Use it because generated `.from()` methods are not null-safe. Service layer `MapHolder` to entity layer types.

### Current User Resolution Pattern

- Inject `VariableResolver`, `UserDao`; resolve `"ACTOR", "userName"`; throw `IllegalStateException` if null or not found; look up with `userDao.query().filterByUserName(StringFilter.equalTo(...)).selectOne()`.
- Use for auditing (`withCreatedBy(...)`) and authorization.

### Idempotent Operation Pattern

- Check existence first (`query()...selectOne()`); early return if present; create only when missing. For init scripts and retries.

### Conditional Validation Pattern

- Requirement depends on another field: e.g. consent given makes signer name required.
- Paired fields: latitude and longitude both or neither (compare `isPresent()` flags).
- Optional getters: check `null`, `isPresent()`, then `.get()`.

### Multiple Field Uniqueness Pattern

- One `count() > 0` query per field (`filterByUserName`, `filterByEmail`); throw `IllegalStateException` on duplicate.

### Temporal Validation Pattern

- Reject future timestamps for historical events (`isAfter(LocalDateTime.now())`).
- Validate date ranges with `ValidationUtils.validateDateRange` when both optional dates are present.

### "At Least One" Flag Required Pattern

- Several optional boolean flags: `Boolean.TRUE.equals(...)` OR-ed; throw `IllegalArgumentException` if none set.

## Query Patterns

### Uniqueness Validation

- `dao.query().filterByX(StringFilter.equalTo(v)).count() > 0`.

### Entity Existence Check

- `dao.getById(id).isPresent()`; throw `IllegalArgumentException` if absent.

### Complex Query with Multiple Filters

- Chain `filterByDate(DateFilter.equalTo(d))`, `filterByType(EnumerationFilter.equalTo(...))`, `orderByDescending(Attribute.TIMESTAMP)`, `selectOne()`.

### Using Masks for Performance

- Masks (projections) control loaded fields; critical for large entities.
- Empty mask `EntityMask.entityMask()` for existence checks: loads only identifier.
- Load specific fields: `UserMask.userMask().withUserName().withEmail()`.
- In queries: `.maskedBy(...)` before `.selectList()`.
- Nested: `withSettlement(SettlementMask.settlementMask().withName().withCounty(...))`.
- Partial update: `dao.update(entity, EntityMask.entityMask().withStatus())`.
- See [Data Access Guide - Using Masks](data-access-guide.md#using-masks-projections).

## General Best Practices

- Single responsibility per method; use DAOs, do not bypass the runtime.
- Validate inputs early with clear messages; do not expose internal details.
- Log meaningful events; unit-test business rules.
- Use OSGi injection; respect model constraints (required fields, relations).
- Use masks to fetch only needed fields; leave cross-cutting concerns to interceptors.

## See Also

- [Custom Operations](custom-operations.md) — implementation examples.
- [Interceptors](interceptors.md) — cross-cutting concerns.
- [Testing Guide](testing-guide.md) — quality assurance.
- [Debugging and Monitoring](debugging-and-monitoring-guide.md) — troubleshooting.
