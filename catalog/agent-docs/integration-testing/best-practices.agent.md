# best-practices.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/best-practices.md.

## Quick Navigation
- Links to hub, best practices, anti-patterns, custom-operation pitfalls, test organisation.

## Overview
- Maintainable, efficient integration tests and anti-patterns to avoid.

## Best Practices
### 1. Test Organization
- Organise tests by functionality.

### 2. Transaction Mode Selection
- `@JudoTest(transaction = TransactionHandling.X)`: `AUTO_ROLLBACK` for read-only verification; `AUTO_COMMIT` for persistence tests; `MANUAL` for multi-transaction flows (test controls boundaries).

### 3. Test Data Management
- Reusable fixtures for test data; use in tests via helpers.

### 4. Assertion Strategies
- Test the right things; assert on values, not framework-set fields (e.g. `identifier()` is always set by framework).
- Compare relationships via `identifier()`.

### 5. Logging and Debugging
- Configure `logback-test.xml`: pattern `%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n`; app package DEBUG; `hu.blackbelt.judo` INFO; `org.hibernate.SQL` DEBUG; `BasicBinder` TRACE; root INFO.

### 6. Test Isolation
- `@JudoTest(truncateTables = true)` (default). Effective for AUTO_COMMIT and MANUAL; AUTO_ROLLBACK relies on rollback.
- `truncateTables = false` only for expensive shared setup; test must handle existing data.

### 7. Performance Considerations
- Use masks for partial loads: `dao.getById(id, Mask.x().withField()...)`.
- Existence check: `dao.getById(id, Mask.x()).isPresent()` with empty mask; never full load.

### 8. Helper Method Reuse
- Base test classes for common patterns.

### 9. BaseIntegrationTest Pattern for Complex Entity Dependencies
- Use when entities need prerequisites (e.g. Address needs Country; FaultRegistry needs Address and User).
- Base class has helper methods creating prerequisites; tests get consistent data; logic centralised.
- `AppDaoModules` is written in the test module (not provided by generated project or testkit): one `@Provides` method per DAO, creating the generated `*DaoImpl` via `ReferenceInjector`.
- Benefits: cleaner tests, consistency, maintainability, reusability, self-documenting helper names.
- Production reference: `application/integration-test/src/test/java/*/integration/BaseIntegrationTest.java`.

## Common Anti-Patterns
### Anti-Pattern 1: Type Layer Confusion
- Mixing entity and service layer types fails to compile. Fix: `adaptTo()` to convert between layers. See Type Safety Guide.

### Anti-Pattern 2: Assuming Entity Relationships Are Navigable
- Relations not loaded. Fix: create prerequisites first and set relations explicitly.

### Anti-Pattern 3: Wrong Transaction Mode
- `AUTO_ROLLBACK` for a persistence test passes falsely (data never persists). Fix: `AUTO_COMMIT` for persistence.

### Anti-Pattern 4: Not Importing TransactionHandling Correctly
- Wildcard import misses nested enum classes. Fix: import the nested enum explicitly.

## Common Pitfalls in Custom Operations
### Anti-Pattern 6: Not Checking Optional Field Nulls
- Optional field getters can return `null`, not `Optional.empty()`. Fix: null-check before calling Optional methods (`ifPresent` NPEs on null).

### Anti-Pattern 6.5: Not Handling Optional<T> Return Types in Assertions
- Some generated getters return `Optional<T>` (depends on model: optional strings, numerics, nullable fields). Use Optional-aware assertions. Example: `assertEquals("Test Street", created.getStreetName().orElse(null))`.

### Anti-Pattern 7: Using adaptTo() to Get Identifiers
- Fix: `input.getSettlement().identifier()` directly, not `adaptTo(SettlementIdentifier.class)`.

### Anti-Pattern 7.5: Validating Foreign Key References in Custom Operations
- Explicit validation fails in tests due to transaction isolation. Fix: let database constraints handle it.

### Anti-Pattern 8: Using getById().isPresent() for Existence Checks
- Loads whole entity. Fix: empty mask for existence check.

### Anti-Pattern 9: Not Using Masks for Partial Loads
- Loading full entities wastes resources. Fix: masks with only required fields.

## Quick Reference: Custom Operation Patterns
- Reference validation pattern; optional field pattern; entity conversion pattern; complete custom operation template.

## Test Organization Best Practices
### Naming Conventions
- Test class and method naming examples.

### Test Structure
- Arrange-Act-Assert.

### Test Coverage Guidelines
- Test: happy path, validation rejection, business rules, edge cases, graceful error handling.
- Do not test: framework behaviour, generated code (DAOs, entities), database constraints, third-party libraries.

## Summary
### Best Practices Checklist
- Organise by functionality; correct transaction mode; reusable fixtures; test business logic not framework; logging; `truncateTables = true` isolation; masks; base test classes.

### Anti-Patterns to Avoid
- Mixing entity and service types; assuming relations loaded; wrong transaction mode; wrong TransactionHandling import; not null-checking optionals; overcomplicated identifier access; explicit FK validation; full loads for existence; no masks.

### Key Takeaways
- Type safety (`adaptTo()` correctly); transaction mode by intent; null-check optionals; masks for performance; Arrange-Act-Assert; test business logic.

## Next Steps
- Hub, getting started, type safety and adaptTo(), advanced patterns.
