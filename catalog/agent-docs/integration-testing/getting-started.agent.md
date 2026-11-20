# getting-started.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/getting-started.md.

## Table of Contents
- Section list only; pull the section you need with `kb_get`.

## Project Structure
- Module: `application/integration-test/` (`pom.xml`, `src/test/java/<pkg>/<model>/integration/`, `src/test/resources/logback-test.xml`, `.classpath`).
- Subpackages: `dao/` (DAO tests), `service/` (service layer, type conversions), `custom/` (custom operations: computed attrs, event handlers, validations), `utils/` (fixtures, helpers e.g. `VariableResolverMockHelper`).

## Dependencies
- `hu.blackbelt.judo.runtime:judo-runtime-core-guice-testkit` (test scope): `@JudoTest`, `JudoRuntimeFixture`, transaction utilities.
- Project `<yourmodel>-model` and `<yourmodel>-service` (test scope, `${project.version}`).
- App-declared `provided` libs (e.g. PDFBox) are not on the IT class path (NoClassDefFoundError): declare them `provided` in the integration-test module too; the IT pom has no fragment, so use generator-ignore.
- `junit-jupiter`, `mockito-core` (test); `logback-classic` (test).
- Surefire `3.2.5`; includes `**/*Test.java`, `**/*IntegrationTest.java`.

## Testing Fundamentals
- `@JudoTest` (package `...guice.testkit.fixture.JudoTest`): sets up runtime, DAOs, DI; manages transactions; optional truncation.
- Parameters (defaults):
  - `transaction` = `AUTO_ROLLBACK`.
  - `truncateTables` = `true`; applies only to `AUTO_COMMIT` and `MANUAL`. `AUTO_ROLLBACK` never truncates (rollback is cleanup). `NONE` cleans nothing.
  - `modelName` = `"example"`.
  - `dialect` = `"hsqldb"` (`hsqldb` | `postgresql`); env `JUDO_TEST_DIALECT` overrides.
  - `container` = `"none"` (`none` | `postgresql` | `yugabytedb`); env `JUDO_TEST_CONTAINER` overrides. With `postgresql` dialect: `none`/`postgresql` → PostgreSQL container, `yugabytedb` → YugabyteDB; other values → no container, setup fails. Yugabytedb liveness check is empty: don't rely on it.
  - `modelSource` = `AUTO` (filesystem, then classpath) | `FILESYSTEM` | `CLASSPATH`.
  - `modules` = `{}` extra Guice modules (public no-arg ctor).
  - `dataSourceMode` = `BY_METHOD` | `BY_CLASS` | `SINGLETON`.
  - `shareInjector` = `false`; reuse injector across methods (with `BY_CLASS`/`SINGLETON`).
  - `interceptors` = `{}` `OperationCallInterceptor` classes.
- Transaction modes:
  - `AUTO_ROLLBACK` (default): begin before, rollback after (success or failure). Clean DB; use for isolation.
  - `AUTO_COMMIT`: commit after success, rollback on failure. Data persists until truncated; keep `truncateTables=true`.
  - `MANUAL`: `fixture.beginTransaction()`, `commitTransaction()`, `rollbackTransaction()`; wrap in try/catch with rollback. Tables truncated after test even if nothing committed.
  - `NONE`: no framework transactions; each DAO/service op may own one. Many ops fail without tx. Read-only/perf tests.
- Disable truncation (`truncateTables = false`) only for expensive setup, migration scenarios or debugging; causes test interdependencies.

## Writing Your First Tests
- Pattern 1 — DAO test: `UserDao userDao = fixture.getInjector().getInstance(UserDao.class)`; `userDao.create(UserForCreate.builder()...build())`; `identifier()`; `getById(...)`, `update`, `delete`. Default AUTO_ROLLBACK cleans up.
- Pattern 2 — custom operation: `ReferenceInjector.createAndInject(CustomImpl.class, fixture.getInjector())` (package `...guice.testkit.util`).
  - Injects by TYPE: every non-static, non-final field and single-arg `set*` method the Guice injector can provide. Does NOT read `@Reference`/`@Inject` (OSGi `@Reference` is CLASS retention, invisible to reflection).
  - `injectReferences(instance, injector)` for an existing instance.
  - Create prerequisite entities first; call the custom op; verify result.
- Pattern 3 — manual tx: `@JudoTest(transaction = MANUAL)`; each boundary explicit with begin/commit/rollback in try/catch. Begin while a tx is open → `IllegalStateException` ('Previous transaction was not completed'). Covers multi-tx, rollback behaviour, isolation checks (`query().selectList().size()`).
- Key points: entity `EntityForCreate.builder()`; `identifier()` for queries.

## Running Tests
- Module is NOT in `application/pom.xml`: `mvn -pl application/integration-test` fails ("Could not find the selected project in the reactor"). Run Maven from `cd application/integration-test`.
- `mvn clean test`; single class `-Dtest=UserDaoTest`; single method `-Dtest=UserDaoTest#testCreateUser`.
- Debug logging: set `<root level="DEBUG">` in `src/test/resources/logback-test.xml` (ConsoleAppender STDOUT).
- Skip tests in build: `mvn clean install -DskipTests`.
- Model load failure (`modelSource` `AUTO`): `Could not load model '<name>'. Filesystem error: ... Classpath error: ...`; check the name and the classpath artifact.
- Known issue: generated `pom.xml` has `<version></version>` for `hu.blackbelt.osgi.i18n:i18n-api` (`osgiI18nApiVersion` never set by generator). Set the version explicitly before running tests.

## Next Steps
- `type-safety.md` (Entity vs Service types, `adaptTo()`); `advanced-patterns.md` (VariableResolver mocking, Optional fields, entity reference validation); `best-practices.md`.
- Hub: `README.md`.
