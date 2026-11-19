# judo-ng framework: issues for the framework developers

Generators, templates, transformations, runtime and `judo.sh`. CLI issues are in [CLI.md](CLI.md).
`session L<n>` = `reports/research/webshop-run/2026-11-11T14-06-20-342Z_01a1caee-58b6-724e-ae62-d32987dbcd2d.jsonl.gz`.
judo-ng base: latest `develop` (worktrees in `target/judo-ng-read/wt/`); paths below are relative to it. The catalog documents the user-side workarounds.

| # | Issue | Repo | Source |
|---|---|---|---|
| 1 | Generated frontend imports a type twice; depends on actor order | runtime__judo-tatami-client (esm2ui Zeta), template__judo-ui-react-template | R16-1, R16-4, R19-12, R19-17, session L6619, L10287, L10473 |
| 2 | `XMI ID COLLISION DETECTED` for action ids in the ESM to UI transform | runtime__judo-tatami-client | R10-15, R19-17, R17 and R18 (session L8990, L9547–L9551) |
| 3 | `anonymous` defaults to `true`: an actor created without the flag skips token checks | models__judo-meta-esm | R19-12 |
| 4 | `judo.sh build -M -B` stops and deletes Karaf, then builds only the frontend | template__judo-esm-fullstack-project-template | R19-12 (d) |
| 5 | Generated Playwright config retries every failing test four times | template__judo-ui-e2e-template | R16 |
| 6 | Integration-test pom uses an unset `i18n-api` version | template__judo-esm-fullstack-project-template | R16 |
| 7 | Liquibase prehook logs ERROR on every start; health stays 503 | runtime__judo-platform | R16, R17, R19, session L6813, L8946, L9047, L10124 |
| 8 | Generated REST client drops a numeric `__version` | template__judo-ui-typescript-rest-template | R16-9 |
| 9 | Cards container in a view is fed a refresh action the page does not provide | template__judo-ui-react-template | R16U, session L7474–L7477, L7514–L7556, L8563, L8620 |
| 10 | Company price rows compute derived product fields for every product | runtime__judo-runtime-core | R16U, session L8150–L8182, L8620, L9004 |
| 11 | Schema apply fails on an empty PostgreSQL database | runtime__judo-rdbms-schema | R19, session L10063–L10079 |
| 12 | Foreign-key columns get no index | runtime__judo-tatami-base | R18, R19, session L9838–L9849, L10126–L10145 |
| 13 | Integration-test module has no dependency hook; provided libraries are missing | template__judo-esm-fullstack-project-template | R19, session L10023–L10028 |
| 14 | Zeta and EVL validators disagree; the mismatch names no element | models__judo-meta-expression | R19, session L10598–L10605 |
| 15 | `judo-cli.jar` disappears after generate or build | template__judo-esm-fullstack-project-template | R16U, R17, R19, session L7321, L7339, L8817–L8820, L10344–L10405 |
| 16 | `judo.sh build -d` removes the Karaf directory before Karaf has stopped | template__judo-esm-fullstack-project-template | R19, session L10036–L10047 |

## 1. Duplicate type imports, depending on actor order

- **Behaviour:** the generated admin frontend contains `import type { CsvFile, CsvFile, CsvFileStored, CsvFileStored }`; `./judo.sh build` stops at `pnpm run format` (biome: `Declarations inside of a import declaration may not have duplicates`).
- **Reproduction (the app's own Maven pipeline, `mvn -o` on `frontend-react/model` then `<app>__admin generate-sources`):** the same commit with a third actor last in the model file: 48 admin files (12 pages) with duplicates; with that actor first: none.
- **Cause:** `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/zeta/Esm2UiZetaTransformation.java`
  - `:1720-1723` runs the transformation once per actor, in model file order, into one shared UI model.
  - `fixCallOperationActionDefinitions` (`:835-907`) collects the call-operation actions of **all** actors from the shared resource set (`:847-858`), looks up the `ClassType` by the name prefix before `::` in the **current** actor's application (`findContainerClassType`, `:1182-1197`) and calls `setOperation` with the current actor's copy (`:888`, `:907`).
  - So a later actor rebinds earlier actors' actions to its own operation copy: 126 cross-actor operation references in the failing model (36 from Admin), 54 with the actor first.
  - `template__judo-ui-react-template/judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/UiPageHelper.java:154` collects page imports in a `HashSet<ClassType>` (identity); `:181` adds the rebound output class next to the page's own copy, and the templates (`actor/src/dialogs/customization.ts.hbs:4`, `index.tsx.hbs:51`, `hooks.tsx.hbs:6`) emit one import per entry.
- **Expected:** an action keeps the operation of its owning actor (look up and rebind within the action's own application); the output does not depend on actor order. Defensive: deduplicate page imports by class name.
- **Workaround:** create the new actor at the first position; check the generated sources for duplicate imports after `generate`.
- **Also seen:** a third anonymous actor of any kind fails the same way (R16, session L6619); R19 builds show the same duplicates with a third actor (session L10287, L10473). The catalog's known-issue entry in `build-process.md` covers the workaround.

## 2. XMI ID collisions in the ESM to UI transform

- **Behaviour:** the frontend-react model step logs `[ERROR] XMI ID COLLISION DETECTED: ID 'Admin/(esm/<id>)/TabularReferenceFieldLinkCreateAction' is being reassigned from Action (obj@...) to Action (obj@...)` for five `TabularReferenceFieldLink*Action` ids of one tabular reference field, in every actor order; the build continues. A transform UI model also had 111 `xmi:id` values used twice, all on `icon` elements.
- **Expected:** unique ids, or no error-level log when the duplicate is harmless.
- **Also seen:** R17 and R18 builds print many `XMI ID COLLISION DETECTED` errors for `TabularReferenceField` link actions, about ten per build (session L8990, L9547–L9551).

## 3. `anonymous` defaults to `true`

- **Behaviour:** `models__judo-meta-esm/model/model/esm.ecore:434-436` (`anonymous`, `defaultValueLiteral="true"`). An `ActorType` created without the flag and without a mapped principal is effectively anonymous (`esm.genmodel:506-507`): no realm, no Keycloak client, and `runtime__judo-runtime-core/judo-runtime-core-security-keycloak-cxf/.../KeycloakLoginInterceptor.java:138-139` verifies a bearer token only when the actor has a realm. Its accesses are public.
- **Expected:** a secure default (`false`), or a validation warning for an anonymous actor with accesses.
- **Related CLI symptom:** `managed` is then refused on that actor (`models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmFieldRules.java:425-428`) but stored as `true` (CLI.md #2).

## 4. `judo.sh build -M -B` leaves the application down

- **Behaviour:** `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:837-841` stops Karaf and runs `rm -rf $KARAF_DIR` whenever the Karaf package is built (default), before Maven; with `-M -B` the branch at `:850-851` then runs only `mvnd install -f frontend-react`. No model, backend or Karaf package is rebuilt, so the application stays down; a full build that fails in a later module leaves it down the same way.
- **Expected:** `-M -B` keeps Karaf (no package rebuild), or stops it only when a new package will be built.
- **Workaround:** `./judo.sh build -f` for a frontend-only build.

## 5. Generated Playwright config retries every failing test four times

- **Behaviour:** `playwright.config.ts.hbs` sets `fullyParallel: true` (line 11) and `retries: 4` (line 15) unconditionally. Its comment says "Retry on CI only"; `workers` on line 17 is already conditional on the CI flag. A local run retries every failing test four times, in parallel, against shared seed data.
- **Expected:** `retries: process.env.CI ? 4 : 0`, the form the catalog recommends (`catalog/agent-docs/e2e-testing/troubleshooting.md`, "Tests work locally but fail in CI").
- **Workaround:** run with `--retries=0`; keep serial runs for shared seed data (`troubleshooting.md`, "Shared Data and Parallel Workers").
- **Evidence:** `template__judo-ui-e2e-template/judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/playwright.config.ts.hbs:11,15,17`.
- **Source:** R16 (review item R16-R21; the same template in the build-test app).

## 6. Integration-test pom uses an unset `i18n-api` version

- **Behaviour:** `integration-test/pom.xml.hbs:226` declares `hu.blackbelt.osgi.i18n:i18n-api` with `<version>{{ osgiI18nApiVersion }}</version>`. No generator code in the judo-ng base defines `osgiI18nApiVersion`, so the generated module has an empty version and cannot build.
- **Expected:** the variable is set from the dependency management, or the dependency is not emitted without a version.
- **Workaround:** set the version in the generated integration-test pom under `.generator-ignore`. The catalog documents it (`catalog/agent-docs/integration-testing/getting-started.md`, "Known Issue: empty `i18n-api` version").
- **Evidence:** grep of the judo-ng base finds the variable only in that template.
- **Source:** R16 (session not cited; the catalog entry is a known issue, the defect remains).

## 7. Liquibase prehook logs ERROR on every start; health stays 503

- **Behaviour:** every start logs `ERROR … Could not find compatible schema model` with `NoClassDefFoundError` for `hu.blackbelt.epsilon.runtime.execution.contexts.EolExecutionContext` (from the rdbms OSGi bundle). The compatibility check cannot run. `/system/health` stays 503 (`PersistenceReady`, `InitScriptsCompleted` missing) while the application serves requests.
- **Expected:** the class is resolvable in the bundle; health is 200 after a normal start.
- **Workaround:** none. The catalog documents the message as known (`catalog/agent-docs/deployment/schema-evolution.md`, "When No Manual Step Is Needed").
- **Evidence:** `runtime__judo-platform/judo-platform-services/judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:228` logs the error.
- **Source:** R16, R17, R19; session L6813, L8946, L9047, L10124.

## 8. Generated REST client drops a numeric `__version`

- **Behaviour:** `common/utils.ts.hbs:15` copies `__version` only when `typeof instance.__version === 'string'`; the server sends a number. The version is dropped on load, so a save omits it and optimistic locking is off. In a browser test, a second editor overwrote a stock value 11 with 7.
- **Expected:** numeric versions are copied too.
- **Workaround:** send `__version` explicitly (`catalog/agent-docs/backend/platform-behavior-reference.md`, "Optimistic Locking and `__version`").
- **Evidence:** `template__judo-ui-typescript-rest-template/judo-ui-typescript-rest-api/src/main/resources/common/utils.ts.hbs:15`.
- **Source:** R16 (gaps R16-9).

## 9. Cards container in a view is fed a refresh action the page does not provide

- **Behaviour:** the generated relation component passes `actions.<relation>RefreshAction` to the cards container, but the view page does not provide it. `CardsContainer.tsx.hbs` has no `RefreshAction` reference (grep: 0). The list stays empty and the browser logs `TypeError: fetch is not a function` (six per page). The table variant loads its own rows (`LazyTable`).
- **Expected:** the view page provides the refresh action, or the cards container loads its own rows.
- **Workaround:** a custom list that loads its own rows (`catalog/agent-docs/frontend/extension-points.md`, "Cards Configuration Hook" documents the caveat).
- **Evidence:** `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/components/widgets/CardsContainer.tsx.hbs` (no `RefreshAction`). Session L7514–L7556. A related page showed zero rows in the DOM because of this symptom (session L7474–L7477); the wrong column name in the first DB check was a builder mistake.
- **Source:** R16U; session L8563, L8620.

## 10. Company price rows compute derived product fields for every product

- **Behaviour:** reading a company price row computes the derived product fields (`onSale`, `lowStock`, `priceLabel`) for every product in the join. With about 150 products and 120 companies, company pages take 4 to 9 s; order, product and category lists answer in under 0.5 s.
- **Expected:** derived fields are computed only for the rows and fields the response needs.
- **Workaround:** `catalog/agent-docs/backend/data-access-guide.md`, "Known Issues of the Generated DAO".
- **Evidence:** `pg_stat_activity` shows the derived SELECT (session L8150–L8182). Code path `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/executors/SelectStatementExecutor.java` (not re-read in this pass).
- **Source:** R16U; session L8620, L9004.

## 11. Schema apply fails on an empty PostgreSQL database

- **Behaviour:** `judo-rdbms-schema:apply` on an empty PostgreSQL database fails with `relation judo_model_versions does not exist`: the apply step reads the version table before the schema creates it. The catalog describes apply as the fresh schema route.
- **Expected:** apply creates the version table when it is missing, or the fresh route is documented as dev-build only.
- **Workaround:** the restore route in `catalog/agent-docs/deployment/schema-evolution.md`, "When No Manual Step Is Needed".
- **Evidence:** `runtime__judo-rdbms-schema/judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/IncrementalLiquibaseExecutor.java:67` (version table constant); session L10063–L10079.
- **Source:** R19; session L10063–L10079.

## 12. Foreign-key columns get no index

- **Behaviour:** the generator creates an `IDX_` index only for identifier attributes (`AttributeRules.java:285`, guard `isIdentifierAttributeInEntityType`). Foreign-key columns get none. Derived members that join over them scan unindexed columns: with about 1 800 accounts a checkout took about 20 s and two smoke tests failed.
- **Expected:** index foreign-key columns by default, or allow index declarations in the model.
- **Workaround:** a schema changeset with a hand-made index (`catalog/agent-docs/deployment/generator-plugins.md`, "Indexes").
- **Evidence:** `runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/rules/AttributeRules.java:283-287` (identifier guard); session L10126–L10145.
- **Note:** a slow first call of a list check in R18 (1204 ms) was a warm-up effect of the test, not a platform defect (session L9838–L9849).
- **Source:** R19; R18 (session L9838–L9849).

## 13. Integration-test module has no dependency hook; provided libraries are missing

- **Behaviour:** `integration-test/pom.xml.hbs` has fragment hooks for properties, plugin management and plugins, but none for dependencies; its `<dependencies>` block (line 73) takes no project additions. The app module has one (`app/pom.xml.hbs:178`). A library the app declares with `provided` scope (for example PDFBox) is not on the integration-test class path, so a test that uses it fails with `NoClassDefFoundError`.
- **Expected:** an extra-dependencies fragment in the integration-test pom.
- **Workaround:** declare the same artifact in the integration-test module with `provided` scope, under generator-ignore control (`catalog/best-practices/backend/generator-ignore-config-protection.md`).
- **Evidence:** `integration-test/pom.xml.hbs:73`; `app/pom.xml.hbs:178`; session L10023–L10028.
- **Source:** R19; session L10023–L10028.

## 14. Zeta and EVL validators disagree; the mismatch names no element

- **Behaviour:** the ASM expression validation (Zeta run) reports `ObjectExpressionMatchesBinding`, which the EVL run does not report. The transform stops with `Zeta validation result mismatch` and no element name. Reported case: an object-valued access added to an anonymous actor fails; the same expression on an authenticated actor validates (session L10598–L10605).
- **Expected:** both runs agree, and the mismatch names the element.
- **Workaround:** none verified. Check the reference type first: the EVL rule says a reference to a collection must not be assigned an expression that yields one object. If the model is valid, record a validator mismatch; do not drop the feature silently.
- **Evidence:** `models__judo-meta-expression/model/src/main/java/hu/blackbelt/judo/meta/expression/validation/ExpressionZetaValidator.java:263`; `models__judo-meta-expression/model/src/main/epsilon/validations/expression/referenceBinding.evl:16-20`.
- **Note:** not re-run in this pass; the session transcript is the only reproduction.
- **Source:** R19; session L10598–L10605.

## 15. `judo-cli.jar` disappears after generate or build

- **Behaviour:** `target/judo-cli.jar` is missing after a frontend build (`build -f -i`) and after generate runs. Every `judo` call then fails with `Unable to access jarfile` until `./judo.sh generate-root` recreates it.
- **Expected:** build and generate keep the jar, or recreate it.
- **Cause:** not located. The jar is copied only by `generate-root` (`template__judo-esm-fullstack-project-template/.../pom.xml.hbs:541`). `judo.sh.hbs` removes only the Karaf directory in `build()` (`:839-840`); no code that deletes the jar was found in the templates or Java sources searched.
- **Workaround:** `./judo.sh generate-root` (`catalog/agent-docs/deployment/local-development.md`, "Unable to access jarfile").
- **Source:** R16U, R17, R19; session L7321, L7339, L8817–L8820, L10344–L10405.

## 16. `judo.sh build -d` removes the Karaf directory before Karaf has stopped

- **Behaviour:** `stop_karaf` sends `bin/stop` and does not wait (`judo.sh.hbs:555-566`). `build()` then runs `rm -rf $KARAF_DIR` at once (`:839-840`). With Karaf still alive, `rm` fails with `Directory not empty`. The next run says Karaf is not running and exits 1; a run with `-KA` exits 1 without a message; no Docker image is built.
- **Expected:** wait until Karaf has stopped; check the `rm` exit status; print a message.
- **Workaround:** stop Karaf and wait for it to exit, then rerun.
- **Related:** section 4 (`-M -B`) hits the same block (`:837-841`); this is the Docker branch and the race.
- **Evidence:** `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:555-566, 839-840`; session L10036, L10043, L10047.
- **Source:** R19; session L10036–L10047.
