# supplementary-patterns.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/supplementary-patterns.md.

## Overview
- Extra patterns from real JUDO integration test implementations; complement the core testing docs.

## Pattern: Test Fixtures for Complex Hierarchies
- Fixture class creates prerequisites in dependency order via DAOs from `injector.getInstance(...)`.
- Method `createAllPrerequisites()` returns `this` for chaining; getters per entity.
- Use `entity.adaptTo(ServiceEntity.class)` when passing to custom operation inputs.
- Benefits: less duplication, enforced order, reuse across test classes.

## Pattern: Common Validation Utilities
- Production docs: Backend patterns (ValidationUtils) and Backend error handling (validation strategy).
- `ValidationUtils` is example project code, not a platform class; write own helper in the application module.
- Methods: `validateRequired(String, name)`, `validateNotNull(Object, name)`, `validateDateRange(start, end)` (equal dates rejected), `validateRange(BigDecimal, min, max, name)` (inclusive), `validateLength(String, max, name)`, `validateEmail(String)`.
- All throw `IllegalArgumentException`.
- Custom operation: validate required, lengths, optional date range only when both present.
- Tests: `assertDoesNotThrow` for valid; `assertThrows` and message `contains`.

## Pattern: Idempotent Operations
- Production docs: Backend patterns, Idempotent Operation Pattern.
- Check existing data (`configDao.query().filterByKey(StringFilter.equalTo(...)).count()`); return early if present.
- Alternative upsert: `selectOne()`, then `update` or `create`.
- Test: call `run()` three times; count stays the same; no throw.
- Use cases: system init, one-time migration, feature flags, cache warming.

## Pattern: Date Range Validation
- Basic: validate required fields, then date range when both optional dates present.
- Advanced constraints: minimum and maximum duration via `ChronoUnit.DAYS.between`; future-only start date.
- Test with `@JudoTest(transaction = TransactionHandling.AUTO_ROLLBACK)`; `assertThrows` and message contains `date`.

## Pattern: Paired Field Validation
- Coordinate pair: both or neither; validate latitude and longitude bounds with `validateRange`.
- Generic `validatePairedFields(Optional<?>, name, Optional<?>, name)`: throws when only one is present.
- Test: supply only latitude; message contains `both`.

## Pattern: Test Logging with SLF4J
- `LoggerFactory.getLogger(TestClass.class)`; log intent at info, details at debug.
- `logback-test.xml`: project package at DEBUG, `hu.blackbelt.judo` at INFO, root INFO.

## Pattern: Get Current User from VariableResolver
- Production code: `@Reference VariableResolver` and `UserDao` (OSGi `@Reference` annotations).
- `variableResolver.resolve(String.class, "ACTOR", "userName")`; null → `IllegalStateException`.
- Lookup via `userDao.query().filterByUserName(StringFilter.equalTo(name)).selectOne().orElseThrow(...)`.
- Testing: VariableResolverMockHelper in Advanced Patterns.

## Pattern: Multiple Field Uniqueness Validation
- Separate checks per field (`filterByUserName`, `filterByEmail`), `count()` > 0 → `IllegalStateException` with field-specific message.
- Test: same username, different email; message contains field name and value.

## Pattern: At Least One Flag Required
- `Boolean.TRUE.equals(flag)` ORed together; throw when none set.
- Generic `ValidationUtils.validateAtLeastOneTrue(Boolean[], message)`.

## Pattern: Default Boolean Values
- Set explicit defaults on `XForCreate` (`false` for permission flags, `true` for active); never null.

## Pattern: Past/Future DateTime Validation
- Past only: reject `isAfter(LocalDateTime.now())`.
- Future only: reject `isBefore(LocalDateTime.now())`.
- Window: `minusDays(30)` to `plusDays(30)`.

## Pattern: Email and Pattern Validation
- `Pattern.compile(...)` constants in `ValidationUtils`; `matcher(value.trim()).matches()`.
- Generic `validatePattern(value, pattern, fieldName, formatDescription)`.
- Example regexes: postal code, E.164 phone, UUID; adapt to domain.

## Summary
- Twelve patterns summarised as numbered list.

## Quick Reference
- Table: pattern, use-when, key benefit (fixtures for 3+ prerequisites; ValidationUtils for repeated checks; idempotent init; date range; paired fields; logging; current user; uniqueness; at-least-one flag; default booleans; past/future datetime; pattern validation).

## Next Steps
- Getting started with tests; Type Safety and adaptTo(); Advanced authentication patterns; Best practices and anti-patterns.
