# advanced-patterns.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/advanced-patterns.md.

## Overview
- Four topics: query filters, authentication context (VariableResolver), null Optional fields, entity reference validation.
- Read the matching pattern section; use `kb_get` for code.

## Pattern: Query Filters

- Import from `hu.blackbelt.judo.sdk.query`: `StringFilter`, `NumberFilter`, `BooleanFilter`, `LocalDateFilter`.
- `StringFilter.equalTo`, `like` (`%` wildcards); case-insensitive needs DB-level `LOWER`.
- `NumberFilter.equalTo`, `greaterThan`, `lessThan`, `greaterThanOrEqualTo`, `lessThanOrEqualTo`.
- `BooleanFilter` has no `equalTo(boolean)`: use `isTrue()` / `isFalse()`.
- `LocalDateFilter` supports `equalTo`, `greaterThanOrEqualTo`, `lessThanOrEqualTo`.
- Several `filterBy*` calls combine with AND.
- Result calls: `selectList()` (list), `selectOne()` (throws if multiple), `dao.countAll()`.
- Single-valued relation: `childDao.queryParent(child)` returns the entity directly; no `selectOne()`.
- Multi-valued relation: `parentDao.queryChildren(parent)` returns a query customizer; relation customizers do not support `orderByCode()`, so sort in Java.
- OR logic: `filterBy("expr")` with JQL. Use `==` (not `=`), `!=`, `< > <= >=`, `and`, `or`, `(this.field)!like('%x%')`, single-quoted strings.
- Not supported in `filterBy`: navigation (`this.relation.field`), SQL-style `like`, single `=`.

## Pattern: Mocking VariableResolver for Authentication

- Problem: custom operations call `VariableResolver.resolve("ACTOR", "userName")`; OSGi `@Reference` injection is null in tests.
- Helper: `VariableResolverMockHelper` in `src/test/java/.../integration/utils/`.
- `createTestUser(userDao, userName)` uses `UserForCreate.builder()`.
- `injectMockVariableResolver(customImplementation, userName)`: Mockito mock returns `userName` for `resolve(String.class, "ACTOR", "userName")`; sets the field by reflection.
- `findVariableResolverField` walks the class hierarchy for a `VariableResolver` field.
- Order: create the instance with `ReferenceInjector.createAndInject(Class, fixture.getInjector())` first, then inject the mock.
- One mock per operation instance; any ACTOR property can be mocked.
- Real authentication: test through the REST API with a Bearer token (requires deployment).

## Pattern: Handling Optional Fields That Return Null

- Generated input getters return `null` (not `Optional.empty()`) when the key was never set; `orElse` on `null` throws NPE.
- Always null-check the getter first: `input.getField() != null && input.getField().orElse(false)`.
- Set entity fields with `if (input.getField() != null) input.getField().ifPresent(entity::setField)`.
- Cause: the generated class keeps a `Map<String, Object> internal`; missing key gives `null`.
- `withField(null)` differs from not calling `withField()`; test both.
- Test patterns: missing optional fields do not throw NPE (`assertDoesNotThrow`); a set floor without building number throws `IllegalArgumentException` with `Building number is required`.
- `@JudoTest(transaction = TransactionHandling.AUTO_ROLLBACK)` is used for isolated tests.

## Pattern: Validating Related Entity References

- Deleted reference: create then `settlementDao.delete(settlement)`; the operation must throw `IllegalArgumentException` containing `not found`.
- Required reference: a null `getSettlement()` throws `Settlement is required`.
- Validate with `settlementDao.getById(input.getSettlement().identifier()).isPresent()`.
- Convert with `input.getSettlement().adaptTo(...Settlement.class)` before passing to `AddressForCreate.builder()`.
- Why explicit checks: DB foreign keys do not surface cleanly under test transaction isolation; clear messages beat constraint errors.

## Quick Reference: Complete Custom Operation Template

- Order in `customCall`: required-field checks, reference existence checks, business rules on optional fields, uniqueness check (`filterByPostalCode(StringFilter.equalTo(...)).selectList()`), build entity, set optional fields with null checks, `addressDao.create`, `log.info`.

## Summary
- Selection table maps each challenge to its pattern.
- Takeaways: `isTrue()`/`isFalse()` for booleans; single-valued relations return entities; relation customizers do not order; mock VariableResolver by reflection; null-check optional fields; validate references; test missing fields, deleted references and invalid combinations.

## Next Steps

- Links: getting started (`./getting-started.md`), type safety and `adaptTo()` (`./type-safety.md`), best practices (`./best-practices.md`).
