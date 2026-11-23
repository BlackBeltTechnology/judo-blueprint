# custom-operations.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/custom-operations.md.

## Understanding Generated Default Implementations

- Never edit `*.java.default`: read-only blueprints, regenerated on every build (`./judo.sh build`). Edits are overwritten and can break the build.
- Instead create a NEW `X.java` (no `.default`) beside the twin and copy structure from the `.default`.
- `.default` is emitted under `application/app/src/main/java/.generated-files/<generator-package>/custom/`. Interfaces are generated under `.generated-files/`.
- Generator emits only `.java.default`, never `.java`: no `.generator-ignore` entry for either file.
- Custom impl goes in the SAME package as its `.default` twin: `<generated-root-package>.<app>.custom` (e.g. `com.example.orders.orders.custom`). Do not invent `operations/` packages; OSGi wiring and `@Component` discovery key off the generator package.
- Find twins: `find application/app/src/main/java -name '*.java.default'`.
- Gotcha: the `resetChecksum` goal can wipe `.generated-files/`. Recover with `git checkout -- application/app/src/main/java/.generated-files`; run a full generator only if the ESM model changed.
- `.generator-ignore` is gitignore-style, only for generated files hand-edited in place (e.g. `application/pom.xml`). Renamed `X.java` and brand-new hand-written files need no entry; `.default` paths must not be listed.
- Best practices: check `.default` first; never modify it; keep it for reference; compare after regeneration; document deviations.

## When to Implement Custom Operations

- Use for: logic not expressible in ESM, external API integration, validation beyond basic constraints, computed values with business rules, multi-step transactions.

## Implementation Steps

- 1. Define the operation in the ESM model (`/model/<app>.model`) with the Judo Designer tool; do not edit the XML. Mark it custom/script-based; define inputs/outputs. See `../model/README.md`.
- 2. Regenerate: `./judo.sh build` or `mvn clean install -DskipFrontendReact`.
- 3. Implement in `application/app/`: extend generated service interfaces, use injected DAOs.
- 4. Build: `cd application/app && mvn install`. With Karaf running, hot deployment applies it.

## OSGi Component Registration Pattern

- Register every custom impl with `@Component(immediate = true, service = <OperationInterface>.class)` and implement the generated interface.
- `immediate = true`: starts when the bundle activates. `service=`: publishes as OSGi service.

## Rules for Custom Operations

- Declare modeled faults in the model (`<faults>` in ESM, `throws` in JSL). Without it the SDK interface lacks `throws` and the build fails with `not compatible with throws clause`. See [Error Handling Guide](error-handling-guide.md#modeled-faults).
- Interceptors and write guards do NOT fire for custom (SDK-implemented) or script operations. CRUD on a mapped transfer object IS intercepted. Put permission checks inside each `*CustomImplementation`. See [Interceptors](interceptors.md#which-operations-are-intercepted).
- Transactions: one transaction per custom op. A thrown exception rolls back all writes. A returned fault also rolls back. A non-`stateful` operation is always rolled back, so an op that writes data must be `stateful`. A caught DAO exception does not roll back by itself (no rollback-only flag; the dispatcher commits a normal return); PostgreSQL then aborts the whole transaction, HSQLDB drops only the failed statement. Rethrow or return a fault to roll back.
- Optional input getters return `null` (not `Optional.empty()`) when the key is absent; `Optional` only when present. Null-check before `.orElse(...)`.
- Mapping: `<Op>CustomImplementation` implements `...operation.<model>.<path>.<Op>`; the interface path names the model operation.
- Stateful flag: a bound op keeps parameters compatible with every inherited op of the same name. Implementing an inherited abstract op must be `stateful`; the flag must match every overload that has an implementation.
- A fully implemented file can still carry the stub `G E N E R A T E D` header. Compare with `.java.default` (stub only throws `UnsupportedOperationException`) instead of trusting the header.
- Reserved payload keys on exposed ops: see [Platform Behavior Reference](platform-behavior-reference.md#reserved-payload-keys).

## Example 1: Simple Toggle Operation

- Pattern: boolean toggle with validation. `@Reference EntityDao`, `EntityValidationDao`, `VariableResolver`.
- `VariableResolver.resolve(String.class, "ACTOR", "identifier")` gets the current actor; reject self-modification.
- After toggle, check business rule (minimum active entities per permission level). Throw a declared fault (generated checked exception, HTTP 422), not `IllegalStateException` (reaches client as 500).

## Example 2: Complex Multi-Entity Operation

- Pattern: validation and recalculation across related entities.
- Load with mask: `ParentEntityMask.parentEntityMask().withValidationErrors(...).withIsValid()`.
- Navigate relations via DAO query methods: `queryChildEntities(parent).maskedBy(...).selectList()`, `queryDefaultChild(...)`.
- Compare identity with `identifier().getIdentifier().equals(...)`, not object equality.
- Update with mask: the mask shapes only the read-back; the write carries the entity's payload. To write fewer fields, set only those fields: `dao.update(entity, Mask)`.

## Example 3: External Service Integration

- Pattern: scheduled sync against an external service from another bundle.
- Query with filters: `StringFilter.equalTo/notEqualTo`, `DateFilter.equalTo`; `orderByDescending(...ATTRIBUTE)`; `selectOne()`/`selectList()`; `.orElse(null)`.
- Create via generated `ExternalDataEntityForCreate.builder()...build()`.
- Wrap external call in try/catch `RuntimeException` and rethrow with a meaningful message.
- Use `TemporalUtils.dateNow()` / `timestampNow()`.

## Example 4: Delegated Implementation with Dependency Injection Bridge

- Pattern: OSGi component delegates to a POJO (`DataImporter`) holding the logic.
- Inject DAOs with setter methods annotated `@Reference` (method injection), passing them to the delegate.
- Inject other custom ops (e.g. `RecalculateRelatedData`) the same way.
- Use when logic is easier to unit-test as POJO, shared across implementations, or the dependency list is large.

## Testing Custom Operations

- Test with integration tests on the JUDO Runtime Core Testkit in `application/integration-test` (a separate project, not a submodule).
- `@JudoTest(modelName, dialect = "hsqldb", transaction, truncateTables = true, modelSource = JudoTest.ModelSource.CLASSPATH, modules = {...DaoModules.class})`.
- Inject the impl with `ReferenceInjector.createAndInject(Impl.class, fixture.getInjector())`. It injects every non-static, non-final field the Guice injector can resolve; `@Reference` (class retention) is not read.
- Get DAOs via `fixture.getInjector().getInstance(EntityDao.class)`.
- Transaction modes: AUTO_ROLLBACK (default), AUTO_COMMIT, MANUAL, NONE.
- Savepoints under MANUAL: `fixture.beginTransaction()`, `fixture.createSavePoint()`, `fixture.rollbackToSavePoint(sp)`, `fixture.commitTransaction()`, `fixture.rollbackTransaction()`.
- Patterns: success (AUTO_COMMIT); validation failure with `assertThrows` (AUTO_ROLLBACK); idempotency (run twice, compare `countAll()`, NONE).
- Run: build the app first (`mvn clean install -DskipTests` from project root), then `cd application/integration-test && mvn test [-Dtest=Class#method]`.
- Full reference: [Integration Testing Guide](../integration-testing/README.md).

## See Also

- [Data Access Guide](data-access-guide.md) — querying, filtering, masks.
- [Type System Guide](type-system-guide.md) — Service vs. Entity layer types.
- [Patterns and Best Practices](patterns-and-best-practices.md) — other backend patterns and utilities.
- [Interceptors](interceptors.md) — cross-cutting concerns.
- [Integration Testing](../integration-testing/README.md) — testing custom operations.
