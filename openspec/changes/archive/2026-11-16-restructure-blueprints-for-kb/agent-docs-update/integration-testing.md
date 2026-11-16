# agent-docs/integration-testing: sweep inventory (15 items)

Each item: id, kind, target, source, status, claim, fact, evidence.

## IN-001 [missing-how-to] Guice injector composition in tests (Modules.combine, init(module, testInstance))
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JudoRuntimeFixture builds the Guice injector via `Modules.combine(module, judoDefaultModule, databaseModule)` and `init(Module, Object injectModulesTo)` injects fields into the test instance. JudoRuntimeExtension does this per-test in beforeEach (beginning a transaction) and commits + truncates in afterEach. A developer writing a custom fixture must know how to combine their test module with the JUDO default and database modules and how injection is wired.
- evidence: ['judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/JudoRuntimeFixture.java:140', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/JudoRuntimeExtension.java:52']

## IN-002 [missing-how-to] Integration tests should create only the entities they need, not load full init/master data
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO integration tests should be class-scoped and self-contained: create exactly the entities a test needs via DAO builders/fixtures instead of invoking the application-wide `initializeMasterData`/Init seeding. Reusing a runtime version that caches the model loader makes this style faster; avoid a heavy shared init-load in every test and do not depend on a singleton test state.
- evidence: ['rackinspect 2026-05-05T15-48 session : [U] initializeMasterData is used for most he test which is unesserary in most of the times, please apply the optimize-test-suite-runtime (i updated the runtime with cheched model etc)', 'rackinspect 2026-05-05T15-48 session : [U] we should use class definned tests not singetlon', 'rackinspect 2026-05-06T11-54 session : [U] UploadOfferDocumentTest,GenerateEr

## IN-003 [wrong-fact] integration-testing: fixture imports and API
- target: agent-docs/integration-testing | src: session:jb-007.json | status: validated
- claim: Imports hu.blackbelt.judo.runtime.core.jsl.fixture; inject JudoTestFixture; fixture.begin/commit/rollback/newInstance.
- fact: JudoTest lives in ...guice.testkit.fixture; TransactionHandling is nested inside JudoTest; the extension resolves JudoRuntimeFixture (JudoTestFixture does not exist); manual mode uses beginTransaction/commitTransaction/rollbackTransaction and DAOs come from getInjector().
- evidence: judo-runtime-core-esm-itest@7b86b96 (IT-001..003)

## IN-004 [wrong-fact] truncateTables behaviour in AUTO_ROLLBACK
- target: agent-docs/integration-testing | src: session:jb-007.json | status: reported-unvalidated
- claim: truncateTables truncates before every test.
- fact: AUTO_ROLLBACK javadoc says tables are not truncated. Medium confidence; verify against JudoTestExtension before editing.
- evidence: IT-004, subagent unsure

## IN-005 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/README.md.hbs:28
- target: agent-docs/integration-testing/README.md | src: judo-ng-read | status: validated
- claim: integration-testing/README.md.hbs:28-30 says .sdkmanrc pins java=21.0.7-zulu and maven=3.9.10 (its verify lines 47-48 also say 21.0.7-zulu /
- fact: The sdkmanrc template pins java=21.0.4-zulu and maven=3.9.9 (mvnd=1.0.2 matches).
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/README.md.hbs:28

## IN-006 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/access-and-derived-testing.md.hbs:91
- target: agent-docs/integration-testing/access-and-derived-testing.md | src: judo-ng-read | status: validated
- claim: Literal escape sequences \u2014 appear in rendered prose (lines 91, 95, 99, 105, 195-203, 207, 209), so the Markdown shows the text '\u2014'
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/access-and-derived-testing.md.hbs:91

## IN-007 [wrong-fact] ## Writing Your First Tests
- target: agent-docs/integration-testing/getting-started.md | src: agent-docs-review:integration-testing.json | status: reported
- claim: Imports JudoTest, JudoTestFixture, JudoRuntimeExtension, TransactionHandling from hu.blackbelt.judo.runtime.core.jsl.fixture.*
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:1

## IN-008 [wrong-fact] ### Basic Test Structure
- target: agent-docs/integration-testing/getting-started.md | src: agent-docs-review:integration-testing.json | status: reported
- claim: Test methods take a JudoTestFixture parameter (e.g. testSomething(JudoTestFixture fixture))
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTestExtension.java:437

## IN-009 [wrong-fact] #### 3. `MANUAL`
- target: agent-docs/integration-testing/getting-started.md | src: agent-docs-review:integration-testing.json | status: reported
- claim: Manual mode uses fixture.begin(), fixture.commit(), fixture.rollback()
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoRuntimeFixture.java:343

## IN-010 [wrong-fact] ### Table Truncation Behavior
- target: agent-docs/integration-testing/getting-started.md | src: agent-docs-review:integration-testing.json | status: reported
- claim: @JudoTest(truncateTables = true) truncates all tables before EACH test method (default), regardless of transaction mode
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:262

## IN-011 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/osgi-ds-descriptor-tests.md.hbs:75
- target: agent-docs/integration-testing/osgi-ds-descriptor-tests.md | src: judo-ng-read | status: validated
- claim: The complete example asserts four @Reference fields across four custom-operation classes
- fact: The example class has two assertions (operationA_myService_hasProfileFilter and operationB_myService_hasProfileFilter) covering two classes 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/osgi-ds-descriptor-tests.md.hbs:75

## IN-012 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:232
- target: agent-docs/integration-testing/supplementary-patterns.md | src: judo-ng-read | status: validated
- claim: validateDateRange checks endDate.isBefore(startDate) and throws 'End date must be after start date'. Equal start and end dates therefore pas
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:232

## IN-013 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:176
- target: agent-docs/integration-testing/supplementary-patterns.md | src: judo-ng-read | status: validated
- claim: Production ValidationUtils is documented in ./common-patterns.md#validationutils
- fact: No common-patterns.md exists under agent-docs/backend or integration-testing. The ValidationUtils section is in backend/patterns-and-best-pr
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:176

## IN-014 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:177
- target: agent-docs/integration-testing/supplementary-patterns.md | src: judo-ng-read | status: validated
- claim: Production ValidationUtils pattern is documented in ./custom-operations.md#validationutils-pattern
- fact: custom-operations.md.hbs has no ValidationUtils heading. Its '## When to Implement Custom Operations' section is at line 190 and contains no
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:177

## IN-015 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:341
- target: agent-docs/integration-testing/supplementary-patterns.md | src: judo-ng-read | status: validated
- claim: Idempotent operation pattern is documented in ./custom-operations.md#idempotent-operation-pattern
- fact: custom-operations.md.hbs has no Idempotent heading, so the anchor is dangling.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/integration-testing/supplementary-patterns.md.hbs:341

