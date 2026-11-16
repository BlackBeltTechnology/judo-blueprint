# agent-docs/deployment: sweep inventory (95 items)

Each item: id, kind, target, source, status, claim, fact, evidence.

## DE-001 [mention-only] initdatatests are very long — run them only when init data changes
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The `initdatatests` suite takes a long time and should only be run when the init data actually changes; it is not part of the normal baseline build/test cycle. Record this so the baseline workflow does not always execute them.
- evidence: ['judo-cli-sessions__2026-09-26T14-47 : "When you run the baseline, you not run the initdatatests right? If yes, then write down to somewhere that only need to run the initdatatests if the init data needs to changed because these tests run very long"']

## DE-002 [missing] YugabyteDB/PostgreSQL TestContainers in test fixtures; initdatatests
- target: agent-docs/(general) | src: session:jb-020.json | status: reported-unvalidated
- fact: JUDO test fixtures use YugabytedbSQLContainer / withDatabaseName TestContainers; 'initdatatests' are very long, run only when init data changes.
- evidence: gaps P17-03, S06-06

## DE-003 [missing] Tatami Maven workflow plugin configuration and generation switches
- target: agent-docs/(general) | src: session:jb-020.json | status: rejected
- fact: judo-tatami-jsl-workflow-maven-plugin default-model-workflow goal parameters: generateBehaviours, runInParallel, generate-sources phase; judo-tatami-client-workflow-maven-plugin default-workflow goal; SDK generator template params apiPrefix/generateOptionalTypes/generatePayload; feature switches generateActors/generateOperations. Later judged irrelevant to app developers (P20-02, P24-05, P26-02, P32-01 marked IRRELEVANT).
- evidence: gaps P22-04, P20-02, P24-05, P26-02, P32-01

## DE-004 [missing-how-to] CLI GraphQL query language and schema inspection
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: `query <model> <Type>` builds GraphQL queries with --select/--where/--limit/--offset where where operators eq, contains, startsWith, endsWith, regex, icontains, istartsWith, iendsWith, iregex, gt, gte, lt, lte; `graphql` runs arbitrary documents with --variables/-o/--schema, and `--schema` exports the GraphQL SDL to .judo-schema.graphql. Collection fields pluralize (EClass->eclasses) and nested reference filtering is AND-combined.
- evidence: ['judo-model-cli@9f6a4bd:src/main/java/hu/blackbelt/judo/cli/commands/QueryCommand.java:390', 'judo-model-cli@9f6a4bd:openspec/specs/graphql-queries/spec.md:7', 'judo-model-cli@9f6a4bd:src/main/java/hu/blackbelt/judo/cli/JudoModelServer.java:752']

## DE-005 [missing-how-to] Adding a new database dialect (Dialect / parameter mapper / function mapper)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO ships only hsqldb and postgresql dialect bundles. To support another RDBMS a developer implements the Dialect interface (getName(), getDualTable()), a RdbmsParameterMapper (or extends DefaultRdbmsParameterMapper, which maps String->VARCHAR(2000), Integer->NUMERIC(10,0), Long->NUMERIC(20,0), Boolean->BOOLEAN, BigDecimal via RdbmsDecimalType, BigInteger->NUMERIC(n,0)), an RdbmsInit (execute(DataSource) to create schema via Liquibase), and a FunctionMapper subclass whose getFunctionBuilderMap() maps FunctionSignatures to MessageFormat SQL patterns (an unregistered signature throws UnsupportedOperationException 'Unsupported function'). A database is chosen by its dialect name, e.g. resolveDialect("oracle") currently throws IllegalArgumentException.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/Dialect.java:25', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/DefaultRdbmsParameterMapper.java:123', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/query/map

## DE-006 [missing-how-to] Selecting the integration-test database via system properties (dialect/container/tz)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JudoDatasourceFixture selects the test database from system properties: `dialect` (hsqldb default | postgresql), `container` (none | yugabytedb, valid only with postgresql), and `tz` (default GMT). Only hsqldb and postgresql are accepted; anything else throws IllegalStateException. A developer must know these properties to run integration tests against HSQLDB vs PostgreSQL vs YugabyteDB and how the choice affects the LocalSource/JDBC URL.
- evidence: ['judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/JudoDatasourceFixture.java:72', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/JudoDatasourceFixture.java:151']

## DE-007 [missing-how-to] YugabyteDB / PostgreSQL TestContainers in JUDO test fixtures
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Integration tests can run against a YugabyteDB container via `YugabytedbSQLContainer` (image `yugabytedb/yugabyte:2.1.8.2-b1`, PostgreSQL wire protocol, port 5433, default db/user/password `yugabyte`, fluent overrides withDatabaseName/withUsername/withPassword). Postgres tests use TestContainers. A developer must know how to wire these containers into a JUnit test and when to select them via the `container=yugabytedb` system property.
- evidence: ['judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/YugabytedbSQLContainer.java:35', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/blackbelt/judo/runtime/core/jsl/fixture/YugabytedbSQLContainer.java:62', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/common/src/main/java/hu/b

## DE-008 [missing-topic] Eclipse m2e launcher configurations and IDE run workflow
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The template ships Eclipse m2e launch configurations: BuildApplication.launch (clean install of <project>/application with JudoBuildApplicationLauncher), BuildApplicationWithoutFrontend.launch (adds -DskipDocker=true -DskipFrontend=true), CompileCustomApp.launch (clean install of application/app), RunApplication.launch (starts the backend from application/karaf-offline with -DrunKaraf=true using JudoApplicationBackendLauncher), and RunFrontend.launch (react-build profile, -pl model,<actorType>, -DskipDist=true -DrunServer=true from application/frontend).
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/launcher/RunApplication.launch.hbs:22', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/launcher/BuildApplicationWithoutFrontend.launch.hbs:22', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-templa

## DE-009 [wrong-fact] README JudoDefaultModule.builder API
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: JudoDefaultModule.builder().asmModel(...).rdbmsModel(...)
- fact: These builder methods do not exist; also JettyContainer.getServer() does not exist (webServer is private).
- evidence: session C147/C148

## DE-010 [wrong-fact] TEST-CONFIGURATION BY_CLASS caching
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: BY_CLASS caches Injector and gives >=5x speed-up by default
- fact: Caching only occurs with shareInjector = true, default false.
- evidence: session C149

## DE-011 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:106
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter.builder() creates the builder.
- fact: The Lombok builder method is named generatorParameter (@Builder(builderMethodName = 'generatorParameter')), so the call is GeneratorParamete
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:106

## DE-012 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:108
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter builder has .targetDirectory(dir) (File).
- fact: The field is targetDirectoryResolver, a Supplier<File>; there is no targetDirectory builder property.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:108

## DE-013 [wrong-fact] src/main/resources/agent-docs/components/model-generator.md:91
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter.builder() is the builder entry point.
- fact: The builder method is generatorParameter().
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/model-generator.md:91

## DE-014 [wrong-fact] src/main/resources/agent-docs/guides/user-guide.md:73
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter.builder() with .targetDirectory(outputDir).
- fact: The builder method is generatorParameter() and there is no targetDirectory property; the field is targetDirectoryResolver.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/user-guide.md:73

## DE-015 [mention-only] Health-check endpoint wire format and Accept-header serializer selection
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The HealthCheckExecutorServlet picks a serializer by Accept header: application/json -> ResultJsonSerializer, text/html -> ResultHtmlSerializer, text/plain -> ResultTxtSerializer. The JSON body is {"overallResult": <STATUS>, "results": [{name, status, timeInMs, finishedAt, tags, messages:[{status, message, exception?}]}]} with finishedAt formatted yyyy-MM-dd'T'HH:mm:ss.SSS (no timezone designator); debug messages are omitted unless includeDebug is set, and exceptions are serialized as a stack-trace string under the exception key. The plain-text serializer returns only the overall status name (e.g. OK or CRITICAL), intended for load balancers. Statuses used by the HTML serializer include statusOK, statusWARN, statusTEMPORARILY_UNAVAILABLE, statusCRITICAL, statusHEALTH_CHECK_ERROR; JSONP is supported via a jsonpCallback parameter (body becomes <callback>(<json>)).
- evidence: ['judo-platform@2d22cf41:judo-platform-services/judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/servlet/ResultJsonSerializer.java', 'judo-platform@2d22cf41:judo-platform-services/judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/servlet/ResultTxtSerializer.java', 'judo-platform@2d22cf41:openspec/specs/healthcheck-monit

## DE-016 [mention-only] Health-check HTTP endpoint usage and configuration (/system/health)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The Felix Health Check servlet exposes a per-deployment endpoint at `/system/health` (default servletPath) with format extensions .html, .json, .jsonp, .txt and .verbose.txt. Query parameters include tags, names, format, httpStatus (e.g. CRITICAL:503), combineTagsWithOr, forceInstantExecution, timeout, hcDebug and a JSONP callback (default processHealthCheckResults). Overall status maps to HTTP codes: OK/WARN -> 200, TEMPORARILY_UNAVAILABLE/CRITICAL -> 503, HEALTH_CHECK_ERROR -> 500. Config keys control allowed_formats, cors_accessControlAllowOrigin (default '*'), disable_request_configuration and disabled.
- evidence: ['judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/servlet/HealthCheckExecutorServletConfiguration.java:34', 'judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/servlet/HealthCheckExecutorServlet.java:83', 'judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/h

## DE-017 [mention-only] OpenAPI/Swagger documentation generation of the REST API
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: When `generateOpenApiAnnotations=true`, the rest module runs swagger-maven-plugin (resolve) writing OpenAPI JSON/YAML under `target/api-documentation-swagger`, embedded into the bundle via Include-Resource/Openapi-Content, and every service/DTO carries `@Schema`/OpenAPI annotations. The generated `ApplicationConfig` emits an `@OpenAPIDefinition` with one Server per actor (`url = <baseUrl>/api/<restPath>/<actor>`) and an OPENIDCONNECT security scheme (`openIdConnectUrl = <authenticationUrl>/auth/realms/<realm>/.well-known/openid-configuration`) for actors with a realm. Runtime Docagger UI is switched on via `JUDO_PLATFORM_SWAGGER_UI` / `JUDO_PLATFORM_SWAGGER_UI_PATH` (default `/swagger-ui`).
- evidence: ['judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/rest/pom.xml.hbs:146', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/application.config.java.hbs:15', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/application.config.java.hbs:21']

## DE-018 [mention-only] Consolidating incremental schema migration folders into one continuous generated step
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: When many model changes accumulate, instead of stacking per-snapshot migration folders (e.g. 130051→175110) plus hand-written steps, regenerate one continuous migration folder from the two model files (base model -> current generated model) and move any hand-written steps into it, deleting the intermediate folder. The `judo-rdbms-schema` maven plugin generates the folder; the model files (base and updated) are the inputs, and an unexpected 'DATABASE HAVE TO BE UPDATED' exit is part of the normal generate step.
- evidence: ['judo-cli-sessions 2026-09-24 : [U] A (my recommendation): one migration folder from 100755 to now, generated from the two model files. My hand-written 04/06 steps move into it and the 130051 → 175110 folder is deleted. Production then goes through one continuous step.']

## DE-019 [mention-only] Environment provisioning: admin-user env wiring and schema-update rollback flow
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: For init-time admin user creation a new environment must wire the `RACKINSPECT_ADMIN_USERS` / `RACKINSPECT_ADMIN_PASSWORD` variables through the application startup template (e.g. `app-startup.sh.tpl`) and terraform config; keycloak admin users are otherwise silently not created on first init. Schema updates run as `./update.sh --version <v> --schema generate|execute --ignoreReview`; the runner snapshots a Neon backup branch (e.g. `backup-<ts>`) and rollback is `--schema restore --branch backup-<ts>`. Environments (prod/test/demo) must be kept distinct, including keycloak reachable IPs (karaf.env) and per-env seed data.
- evidence: ['rackinspect 2026-05-28T08:04 : [U] check mate.madura@blackbelt.hu is why not created with the keycloak as an admin user trought the prod init', 'rackinspect 2026-05-28T08:04 : [U] explore the two enviroment more cerafully ... for example app-startup.sh.tpl not contains the RACKINSPECT_ADMIN_USERS=${rackinspect_admin_users} ⏎ RACKINSPECT_ADMIN_PASSWORD=${rackinspect_admin_password}.', 'rackinspec

## DE-020 [missing] Rackinspect schema migration layout
- target: agent-docs/deployment | src: session:jb-006.json | status: reported-unvalidated
- fact: Schema migrations are 18 steps (diff model + Liquibase changesets 00..08); only non-empty data-migration changesets (04, 06) carry developer knowledge. judo.sh commands: env|clean|prune|update|generate|generate-root|dump|import|build|reckless|start|stop|status|schema-upgrade; generate uses `-DgenerateApplication -DskipApplicationBuild`, generate-root `-DgenerateRoot`.
- evidence: rackinspect judo.sh lines ~143-163, 1252-1270

## DE-021 [missing] deployment: judo.sh commands undocumented
- target: agent-docs/deployment | src: session:jb-007.json | status: reported-unvalidated
- fact: Undocumented: judo.sh start -o runtime=compose,..., dump/import, schema-upgrade, generate, and the build option table.
- evidence: DE-007/008/009

## DE-022 [missing] Jasypt-encrypted config values and PAX-JDBC passwords
- target: agent-docs/deployment | src: session:jb-020.json | status: validated
- fact: Config can embed secrets as password=ENC(encrypted_password); the org.jasypt.encryption.StringEncryptor OSGi service (karaf-jasypt-support, osgi-encryption) decrypts; passwords can be encrypted with a Karaf command and replaced in DBCP2 config files.
- evidence: karaf-jasypt-support:README.md:22 (gap P27-01)

## DE-023 [missing] OSGi model bundle packaging and DS unit testing
- target: agent-docs/deployment | src: session:jb-020.json | status: reported-unvalidated
- fact: Models are packaged as OSGi bundles with a Judo-Models manifest header (ModelBundleTracker). OSGi DS components can be unit-tested without a container using MockOsgi (ComponentContext, BeanUtil setReferences).
- evidence: gaps P29-04 and K253 in review sheet

## DE-024 [missing-how-to] Custom health checks
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO registers Apache Felix health-check rules (ModelsCheck, OperationsCheck, PlatformComponentsCheck) and exposes a status page at http://localhost:8181/system/health?tags=<ModelName>. Custom health checks are added by creating an OSGi component implementing org.apache.felix.hc.api.HealthCheck, which lets an application publish its own readiness/liveness signals into the same status endpoint.
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/05_healthcheck.adoc:37', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/05_healthcheck.adoc:10', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/05_healthcheck.adoc:14']

## DE-025 [missing-how-to] Bootstrapping an application project from Maven archetypes
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Beyond the JUDO Designer 'New project' flow, applications can be bootstrapped from Maven archetypes: judo-jsl-springboot-archetype (Spring Boot app with generated application.yml, HSQLDB + Liquibase changelog classpath:model/@judo-model-name@-liquibase_hsqldb.changelog.xml, judo.modelName placeholder), judo-sdk-archetype for custom-operation implementation projects (run with run-offline.sh / Run-Offline.ps1 starting Karaf), and judo-tatami-jsl-workflow-maven-plugin goal default-model-workflow running in generate-sources (reads ${basedir}/src/main/resources/model, writes ${basedir}/target/generated-sources/model). Generated SDK package conventions follow e.g. my.test.test.sdk.test.test for model Test + entity Person.
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/00_developing_custom_operations.adoc:30', 'documentation@3eec62f:docs/modules/ROOT/pages/getting-started/04_bootstrap-spring-boot-project.adoc:21', 'documentation@3eec62f:docs/modules/ROOT/pages/getting-started/03_bootstrap-plain-java-project.adoc:86', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/00_d

## DE-026 [missing-how-to] Schema migration review-required .sql.missing workflow
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO RDBMS schema evolution distinguishes identical, applyable and review-required change types across base/update/incremental models. At startup the application stops with an error when the base model stored in the database differs from the application's base model, requiring an incremental model to be executed. Schema generation (schema CLI tool or schema Maven plugin) writes into a folder named by base and update model versions; .sql.missing files for review-required changes must be renamed to .sql and placed in the review directory before the incremental change can be applied. Schema generation overwrites all files in the output folder except review files.
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/04_schema_migration.adoc:95', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/04_schema_migration.adoc:102', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/04_schema_migration.adoc:98', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/04_schema_migration.adoc:109']

## DE-027 [missing-how-to] Raw Maven code-generation and backend-build flags and goals
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The judo-esm-generator-maven-plugin exposes goals generate (phase generate-resources), create (requiresProject=false), checksum, clean, resetChecksum, synchronizeGitignore with parameters esm, uris, helpers, type, destination, templateParameters, contextAccessor, scanDependencies, actors; generate destination defaults to ${project.basedir}/target/fullstack-project. Generation runs Maven 'compile' with VM flags -DgenerateRoot=true -DgenerateApplication=true -DskipApplicationBuild=true; version updates add -DupdateJudoVersions=true; new-project scaffolding runs the judo-version-updater-maven-plugin create-judo-project goal with -DmodelName, -DprojectGroupId, -DprojectArtifactId, -DprojectVersion, -Dversion; the backend is started with 'clean install' in application/karaf-offline plus -DrunKaraf=true.
- evidence: ['judo-meta-esm@65b02f94:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/esm/generator/maven/plugin/EsmProjectGenerateMojo.java:38', 'judo-meta-esm@65b02f94:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/esm/generator/maven/plugin/EsmProjectGenerateMojo.java:48', 'judo-meta-esm@65b02f94:designer-eclipse-runtime/src/main/java/hu/blackbelt/judo/meta/esm/designer/eclipse/runt

## DE-028 [missing-how-to] EsmGenerator Maven plugin goals, parameters and template URIs
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The ESM generator is driven by a Maven plugin with six goals: generate (GENERATE_RESOURCES), create (standalone, requiresProject=false), checksum (GENERATE_RESOURCES), clean (CLEAN), resetChecksum (CLEAN), and synchronizeGitignore (PROCESS_RESOURCES). The generate goal takes esm (required; file path or mvn: URL), destination (required), uris (required), type (default fullstack-project), actors, helpers, scanDependencies (default false) and validateChecksum (default true). Template URIs accept mvn:groupId:artifactId:version or mvn:groupId:artifactId:version!path/in/jar over tgz/tar.gz/zip/jar/bz2. An empty actors list generates code for all actor types; a non-empty list restricts to the listed actor FQNames. Parameters come from templateParameters (inline map), parameterFiles (properties files) and variablePrecedence (conflict order).
- evidence: ['judo-meta-esm@65b02f94:openspec/specs/esm-generator-plugin/spec.md:17 — Maven goals: generate (GENERATE_RESOURCES), create (standalone, requiresProject = false), checksum (GENERATE_RESOURCES), clean (CLEAN), resetChecksum (CLEAN), synchronizeGitignore (PROCESS_RESOURCES).', 'judo-meta-esm@65b02f94:openspec/specs/esm-generator-plugin/spec.md:28 — generate parameters: esm (required; file path or m

## DE-029 [missing-how-to] UI generator Maven goals and checksum index internals
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The judo-ui-generator-maven-plugin exposes five goals with default lifecycle phases: generate (generate-resources, requires the YAML descriptor type), checksum (generate-resources), clean (clean), resetChecksum (clean) and synchronizeGitignore (process-resources). Checksums are stored in a .generated-files CSV (path,md5), with per-application names .generated-files-<appName>. clean deletes only tracked files whose disk MD5 still matches the saved checksum; resetChecksum rewrites the stored records for the output directory; synchronizeGitignore maintains a managed gitignore block delimited by '# JUDO GENERATOR BLOCK START/END' and takes an ignoredFiles glob list.
- evidence: ['judo-meta-ui@7bdc5ac:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/ui/generator/maven/plugin/UiProjectCleanMojo.java:29', 'judo-meta-ui@7bdc5ac:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/ui/generator/maven/plugin/UiProjectResetChecksumMojo.java:29', 'judo-meta-ui@7bdc5ac:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/ui/generator/maven/plugin/UiProject

## DE-030 [missing-how-to] Supplying the UI model artifact to the generator (mvn: URI and archive extraction)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The generator's ui parameter accepts either a file path or a Maven coordinate of the form mvn:<groupId>:<artifactId>[:<extension>[:<classifier>]]:<version>[!path/in/archive]. The '!' suffix selects one entry inside the artifact, extracted to a temp file. Supported archive inputs are .tgz, .tar.gz, .zip, .jar, .bz2 and .tar.bzip2 (a plain .tar is rejected). Extraction uses a string-prefix match on entry names, so path 'templates' also matches 'templates-old/...' entries.
- evidence: ['judo-meta-ui@7bdc5ac:openspec/specs/generator/maven-plugin/spec.md:130', 'judo-meta-ui@7bdc5ac:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/ui/generator/maven/plugin/AbstractUiProjectMojo.java:205', 'judo-meta-ui@7bdc5ac:generator-maven-plugin/src/main/java/hu/blackbelt/judo/meta/ui/generator/maven/plugin/AbstractUiProjectMojo.java:263', 'judo-meta-ui@7bdc5ac:generator-maven-plugi

## DE-031 [missing-how-to] Checksum-ignore file and whitespace-tolerant generated-file comparison
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The generator has two ways to tolerate differences in generated files. '.generator-checksum-ignore' (GLOB patterns, walked from the file's directory up to rootPath, cached per-directory) makes matching files be overwritten even when manually modified. Separately, a whitespace-tolerant normalizer compares a checksum-mismatched file against the saved checksum: fileNormalizers YAML presets (auto, none, java, ts, js, rust, go, python, xml, html, css, json) expand to per-extension normalizers; 'auto' expands to all, 'none' disables, and a missing/empty fileNormalizers list falls back to 'auto'. When normalized content matches, the file is kept unchanged and its checksum is updated (INFO log), and the top-level normalizeContent=false disables normalized comparison.
- evidence: ['judo-generator-commons@caeda00:src/main/java/hu/blackbelt/judo/generator/commons/ChecksumIgnore.java:41', 'judo-generator-commons@caeda00:src/main/java/hu/blackbelt/judo/generator/commons/ChecksumIgnore.java:67', 'judo-generator-commons@caeda00:src/main/java/hu/blackbelt/judo/generator/commons/GeneratorModel.java:124', 'judo-generator-commons@caeda00:src/main/java/hu/blackbelt/judo/generator/com

## DE-032 [missing-how-to] Derived-model generation and reload via CLI transform/discard
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: `transform` runs the ESM->PSM->ASM->RDBMS pipeline (plus esm2ui) writing derived models to cli-generated/ (or -o <dir>) and, with --load, reloads them into the running daemon. Derived models are found by suffix -psm.model, -asm.model, -rdbms_<db>.model, -ui.model from the first directory holding a match (custom path, then generated-resources/model, then cli-generated; UI searched first in application/frontend-react/model). `discard --derived --from <dir>` resets them. The catalog covers the transformation concept but not the CLI-based regenerate/reload workflow.
- evidence: ['judo-model-cli@9f6a4bd:openspec/specs/transform-command/spec.md:15', 'judo-model-cli@9f6a4bd:src/main/java/hu/blackbelt/judo/cli/JudoModelServer.java:891', 'judo-model-cli@9f6a4bd:openspec/specs/discard-command/spec.md:28']

## DE-033 [missing-how-to] Incremental schema-migration review workflow: review scripts, .missing placeholders, applyable check, and the useXmiId/ignoreReview flags
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The rdbms-schema generator produces an eight-phase set of changesets (check, backup, beforeIncremental, updateDataBeforeIncremental, incremental, updateDataAfterIncremental, aferIncremental [sic] -> script 07_aferIncremental, dropBackup) plus an aggregated 00_<model>_incremental_<dialect>.changeset.xml and a <model>-rdbms_<version>_<dialect>.model. Generation records review scripts whose absence makes changes not applyable: isApplyable() is false when review scripts are missing, createMissingReviewScripts writes <name>.missing placeholders, and execute/apply throw IllegalStateException 'Missing scripts' when the generator reports missing review scripts. Builder/CLI flags are useXmiId (default true; controls rename as Modify vs Delete+Create) and ignoreReview (default false for generate, true for the Maven execute/apply goals). Version markers latest.version / previous.version are written to the output directory and drive base/update version resolution.
- evidence: ['judo-rdbms-schema@008bd34:judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/RdbmsIncrementalGenerator.java', 'judo-rdbms-schema@008bd34:judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/IncrementalLiquibaseExecutor.java', 'judo-rdbms-schema@008bd34:judo-rdbms-schema-maven-plugin/src/main/java/hu/blackbelt/judo/rdbms/schema

## DE-034 [missing-how-to] Signed identifier stability requires a configured @IdentifierSignerSecret
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Entity identifiers exposed to clients are JWT/HMAC-signed (DefaultIdentifierSigner) and carried by clients as __signedIdentifier. The HMAC secret comes from an optional @IdentifierSignerSecret binding (Base64-decoded). If it is not bound, JudoDefaultModule generates a fresh random 1024-bit key via generateNewSecret() on every module construction, so signed identifiers become invalid across JVM restarts and across nodes.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/dispatcher/DefaultIdentifierSignerProvider.java:23', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/JudoDefaultModule.java:245', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/JudoDefa

## DE-035 [missing-how-to] Spring Boot application wiring keys (spring.datasource.*, spring.liquibase.change-log, judo.modelName)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: A JUDO Spring Boot app is configured via `application.properties`: `spring.datasource.url`/`username`/`password`, `spring.liquibase.change-log=classpath:model/<Model>-liquibase_hsqldb.changelog.xml`, and `judo.modelName=<Model>` to select the JUDO model. `JudoRuntimeCoreSpringApplication` is a `SpringApplication.run` main with `@EventListener(ApplicationReadyEvent)`. Developers need these exact keys to stand up a Spring-based JUDO application.
- evidence: ['judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-spring-itest/src/main/resources/application.properties:21', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-spring-itest/src/main/resources/application.properties:24', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-spring-itest/src/main/resources/application.properties:25']

## DE-036 [missing-how-to] OSGi/DS transformation services hard-code the HSQLDB dialect
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The Declarative-Services trackers and transform services that generate RDBMS and Liquibase models inside a running OSGi container hard-code the dialect to 'hsqldb' (Asm2RdbmsTransformationAsmModelTracker and Rdbms2LiquibaseTranformationSerivce call install with dialect 'hsqldb'). The direct Java API and the Work units, by contrast, honor the configured dialect/TransformationMode. So in an OSGi/Karaf deployment the generated schema model is always HSQLDB-shaped regardless of the database the application is configured to use.
- evidence: ['judo-tatami-base@14847b0:judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/osgi/Asm2RdbmsTransformationAsmModelTracker.java:72', 'judo-tatami-base@14847b0:judo-tatami-rdbms2liquibase/src/main/java/hu/blackbelt/judo/tatami/rdbms2liquibase/osgi/Rdbms2LiquibaseTranformationSerivce.java:80', 'judo-tatami-base@14847b0:judo-tatami-rdbms2liquibase/src/main/epsilon/generations/sql/B

## DE-037 [missing-how-to] judo-tatami-client-workflow-maven-plugin `default-workflow` goal parameter reference
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The Maven plugin goal `default-workflow` (bound to the compile phase) runs the ESM→UI pipeline during a build. Parameters: `destination` (default ${project.basedir}/target/classes/model), `runInParallel` (true), `enableMetrics` (true), `ignoreEsm2Ui` (false), `validateModels` (false), `saveModels` (false), and optional `esm`/`ui` model inputs. Model inputs use `mvn:<groupId>:<artifactId>[:<extension>[:<classifier>]]:<version>[!path/in/archive]` URI syntax (resolved via Aether; `!path` extracts a sub-path from .tgz/.tar.gz/.zip/.jar/.bz2/.tar.bzip2), or plain filesystem paths — a `file:` scheme is NOT stripped. On workflow failure models are saved before the Mojo throws. A developer needs this to wire UI-model generation into a build reliably.
- evidence: ['judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow-maven-plugin/src/main/java/hu/blackbelt/judo/tatami/client/workflow/maven/plugin/DefaultWorkflowMojo.java:71', 'judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow-maven-plugin/src/main/java/hu/blackbelt/judo/tatami/client/workflow/maven/plugin/DefaultWorkflowMojo.java:99', 'judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow-mav

## DE-038 [missing-how-to] Generated ESM/UI artifact names and unvalidated-save default
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The client workflow saves three artifacts per model to the destination: `<modelName>-esm.model` (ESM), `<modelName>-ui.model` (XMI/EMF) and `<modelName>-ui.json` (EMFCloud Jackson via `JsonUuidResource`, with `OPTION_SERIALIZE_DEFAULT_VALUE` and `OPTION_USE_ID`). Models are saved with validation DISABLED (`VALIDATE_MODELS_ON_SAVE=false`); validation is a separate pipeline step that only runs when `validateModels=true`. The Mojo only writes models when `saveModels=true` or the workflow threw. A developer must know these names and that generated models are not auto-validated.
- evidence: ['judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow/src/main/java/hu/blackbelt/judo/tatami/client/workflow/DefaultClientWorkflowSave.java:76', 'judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow/src/main/java/hu/blackbelt/judo/tatami/client/workflow/DefaultClientWorkflowSave.java:80', 'judo-tatami-client@c0d1a6a6e:judo-tatami-client-workflow/src/main/java/hu/blackbelt/judo/tatami/clie

## DE-039 [missing-how-to] Deploying a model as an OSGi bundle (Judo-Models manifest header)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO models can be deployed not just as raw .psm/.esm files in the Karaf deploy folder, but as OSGi bundles that declare a `Judo-Models` manifest header naming the models (with optional version attributes). BundleModelHolder loads each model from bundle resources with a strict naming convention: model/<name>-esm.model, -psm.model, -asm.model, -measure.model, -expression.model, -openapi.model, -keycloak.model; per-dialect resources are model/<name>-rdbms_<dialect>.model, -asm2rdbms_<dialect>.model and -liquibase_<dialect>.changelog.xml. Deployment must model a `dialects` (comma-separated) config; a missing version uses the bundle version, blank becomes 1.0.0.<timestamp>_SNAPSHOT, and .SNAPSHOT suffixes get a timestamp substitution.
- evidence: ['judo-services@ced983fe:judo-services-model-bundle-deployer/src/main/java/hu/blackbelt/judo/services/model/bundle/deployer/ModelBundleTracker.java:57', 'judo-services@ced983fe:judo-services-model-bundle-deployer/src/main/java/hu/blackbelt/judo/services/model/bundle/deployer/BundleModelHolder.java:112', 'judo-services@ced983fe:judo-services-model-bundle-deployer/src/main/java/hu/blackbelt/judo/ser

## DE-040 [missing-how-to] Startup banner and JMX readiness configuration
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO prints a startup banner once seven platform services (Dispatcher, JaxRsApplicationsReady, PersistenceReady, ScriptsReady, SdkOperationsReady, IdentityManagerReady, InitScriptsCompleted) are all registered for a model, on which a JudoApplicationReady service is published. Config keys: bannerEnabled (default true), bannerFonts (default = built-in list; unknown font names are silently dropped), bannerHslStart/bannerHslEnd (format '<hue>,<saturation>,<lightness>', random when unset), enableJMX (default false) which names MBeans `hu.blackbelt.judo:type=<model>,name=Application` and health-check MBeans '<SimpleName>_<model>', and the system property `disableJudoAnsiColors` (any value suppresses ANSI colour).
- evidence: ['judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/ApplicationListener.java:149', 'judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/ApplicationListener.java:224', 'judo-services@ced983fe:judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osg

## DE-041 [missing-how-to] Runtime Liquibase model-store version enforcement and ignoreVersionCheck
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Before a datasource is used, LiquibaseModelDataSourcePrehook either runs the Liquibase migration or checks/records the model version in the `JUDO_MODEL_VERSIONS` table and verifies the RDBMS model matches the database. When a stored version differs, prepare() throws IllegalStateException 'There are RDBMS model changes which have not been applied to database'. Setting ignoreVersionCheck=true skips the model-store check and only runs the Liquibase update. Note: a LiquibaseException during prepare is logged and NOT rethrown, so the datasource is handed out even if migration failed; executeLiquibaseScript swallows non-Liquibase exceptions silently.
- evidence: ['judo-services@ced983fe:judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:178', 'judo-services@ced983fe:judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:129', 'judo-services@ced983fe:judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/Liqu

## DE-042 [missing-how-to] Embedded HSQLDB server provisioning and configuration
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: For local development and tests JUDO provisions an embedded HSQLDB TCP server per LiquibaseModel: HsqldbServer requires dataSourceName, databaseName and databasePath (all String, no default) with optional port (default 9001); the Liquibase tracker auto-assigns ports starting at 30000 and increments per model, sets pax-jdbc.url=jdbc:hsqldb:hsql://localhost:<port>/<databaseName> and creates an org.ops4j.datasource factory configuration marked .__created_by_hsqldb_server=true. Config keys prefixed pax-jdbc. are forwarded to the datasource config with the prefix stripped.
- evidence: ['judo-services@ced983fe:judo-services-persistence-hsqldb/src/main/java/hu/blackbelt/judo/services/persistence/hsqldb/LiquibaseModelToEmbeddedHsqlDatabaseServiceTracker.java:54', 'judo-services@ced983fe:judo-services-hsqldb-server/src/main/java/hu/blackbelt/judo/services/hsqldb/server/HsqldbServer.java:52', 'judo-services@ced983fe:judo-services-hsqldb-server/src/main/java/hu/blackbelt/judo/service

## DE-043 [missing-how-to] RDBMS naming-prefix configuration for generated schema objects
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Generated tables, columns, foreign keys, inverse foreign keys, and junction tables use configurable prefixes: T_, C_, FK_, FK_INV_, J_ respectively, each overridable with '-' to suppress the prefix. These prefixes are set in the workflow Maven plugin configuration.
- evidence: ['judo-tatami-jsl@c1693a5b:docs/pages/judo-tatami-jsl-workflow-maven-plugin.md:174']

## DE-044 [missing-how-to] default-model-workflow Maven plugin configuration and generated artifact naming
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The workflow Maven plugin exposes the default-model-workflow Mojo (bound to COMPILE). Key parameters: dialects (default postgresql,hsqldb), destination (default ${project.basedir}/target/model), transformationMode=ETL (vs Zeta), runInParallel, useCache, saveModels, ignore* flags (ignorePsm2AsmTrace, ignoreAsm2Keycloak, ignoreJsl2PsmTrace), and rdbms table/column names prefixes T_/C_/FK_/FK_INV_/J_. Generated artifacts are named <modelName:':'->'_'>-<suffix>.model, with per-dialect -rdbms_<dialect>.model and -liquibase_<dialect>.changelog.xml.
- evidence: ['judo-tatami-jsl@c1693a5b:judo-tatami-jsl-workflow-maven-plugin/src/main/java/hu/blackbelt/judo/tatami/jsl/workflow/maven/plugin/DefaultWorkflowMojo.java:40 (Mojo default-model-workflow bound to COMPILE; defaults dialects=postgresql,hsqldb, destination=target/model, transformationMode=ETL, runInParallel, useCache, saveModels, ignoreAsm2Keycloak, rdbms prefixes T_/C_/FK_/FK_INV_/J_)', "judo-tatami

## DE-045 [missing-how-to] Karaf container administration for deployed apps (JAAS users, startup feature)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: A deployed JUDO app runs in a Karaf container whose console access is configured through JAAS users.properties in the format USER=PASSWORD,_g_:GROUP, with roles (group, admin, manager, viewer, systembundles, ssh) granted per group; an admin user can be enabled at boot via the karaf_enable_admin_user switch, and the offline assembly's startup feature is overridable at runtime via the JUDO_STARTUP_FEATURE environment variable. Operators must know these knobs to secure and customize the deployed container.
- evidence: ['judo-tatami-tests@80e27d28:karaf-offline/src/main/resources/etc/users.properties:32', 'judo-tatami-tests@80e27d28:karaf-offline/src/main/resources/etc/users.properties:33', 'judo-tatami-tests@80e27d28:karaf-offline/pom.xml:36', 'judo-tatami-tests@80e27d28:models/ActionGroupTest/judo.properties:31']

## DE-046 [missing-how-to] Shipped Docker Compose environments and ./judo.sh env
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The template ships two docker-compose profiles. compose-develop runs Traefik + Keycloak start-dev + the app on *.traefik.me over plain HTTP (proxy.traefik.me, auth.traefik.me:8080, app.traefik.me:8181) with JUDO_PLATFORM_FILESTORE=rdbms. compose-postgresql-https is production-like with TLS on 80/443, Keycloak on PostgreSQL, the app on PostgreSQL with a filesystem filestore, a helper container that downloads the traefik.me cert, and declares the network and volumes external (they must exist before compose up). These profiles are selected via compose-dev.properties (runtime=compose, compose_env=compose-develop) using './judo.sh env compose-dev build start'.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/docker/compose-develop/docker-compose.yml.hbs:30', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/docker/compose-postgresql-https/docker-compose.yml.hbs:93', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-

## DE-047 [missing-how-to] Maven extension fragments for generated backend modules
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Every generated Maven module (application root, app, interceptors, karaf-features, schema, e2e, web-root) includes empty extension fragments that are injected at fixed points of the generated POM: pom.xml.extra-dependencies.fragment.hbs into <dependencies>, pom.xml.extra-plugins.fragment.hbs into <build><plugins>, pom.xml.extra-plugin-management.fragment.hbs into pluginManagement, plus extra-profiles, extra-modules, extra-properties-definition, distributionManagement and repositories fragments. A project adds custom Maven dependencies, plugins, profiles or repositories by creating a file with exactly that name in the module, and it survives regeneration (no .generator-ignore entry needed).
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/app/pom.xml.hbs:178', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/app/pom.xml.hbs:96', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/pom.xml.hbs:296', 'j

## DE-048 [missing-how-to] Docker image build customization (tags, base image, agents)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The generated docker module builds one image tar per architecture with jib-maven-plugin 3.3.2: x86_64/amd64/arm64 profiles write target/<artifactId>-<version>_docker_image_<arch>.tar, all using a hard-coded azul/zulu-openjdk-debian:21-latest base. Image tags come from the property DOCKER_IMAGE_TAGS (default 'dev'). JMX exporter, Elastic APM and New Relic agents are only added when the template variables dockerPrometheusJmxExporterAgentVersion, dockerElasticApmAgentVersion and dockerNewrelicAgentVersion are set. The image entrypoint runs /<name>/bin/karaf,run,clean and exposes ports 8181, 8081, 1099, 44444, 5000, 9090, 5005 with /<name>/deploy and /<name>/data volumes; files placed in ${project.basedir}/overrided are copied into the image.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/docker/pom.xml.hbs:16', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/docker/pom.xml.hbs:53', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/docker/pom.xml.

## DE-049 [missing-how-to] Node/pnpm version pinning and automatic toolchain bootstrap
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Node and pnpm versions are pinned by template parameters (defaults node-version 24.13.1, pnpm-version 10.15.0; frontend-maven-plugin version fixed at 1.12.1). The build installs Node and pnpm into ${maven.multiModuleProjectDirectory}/.nodejs via the prepare-nodejs / prepare-nodejs profiles (install-node-and-pnpm goal), so the frontend and e2e modules do not require a pre-installed Node toolchain. The Maven properties nodeVersion/pnpmVersion override the defaults.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/pom.xml.hbs:17', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/e2e/pom.xml.hbs:14', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/e2e/pom.xm

## DE-050 [missing-how-to] Bootstrapping a new JUDO JSL Spring Boot project (archetype + parent-POM constraints)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: A new JUDO app is generated from the maven-archetype-plugin (3.1.1:generate) with `modelName` as the only required parameter (regex ^[a-zA-Z0-9]+$); groupId defaults to com.example, artifactId to lowercased modelName, package to groupId.artifactId, and the main class to <ModelName>Application. A generated project inherits from hu.blackbelt.judo.jsl:judo-jsl-springboot and must set two properties: `sdkPackagePrefix` (Java package of the generated SDK) and `modelName`. modelName must exactly match the `.jsl` filename under src/main/resources/model/ AND the `model` declaration inside it, because modelName is interpolated into the generated-source path (target/generated-sources/model/sdk/<modelName>) added by build-helper; a mismatch yields an empty source root and a silent compile of nothing.
- evidence: ['judo-jsl-springboot-archetype@a2c8094:src/main/resources/META-INF/maven/archetype-metadata.xml:33', 'judo-jsl-springboot-parent@02441c9:AGENTS.md:26', 'judo-jsl-springboot-parent@02441c9:README.md:38']

## DE-051 [missing-how-to] judo-spring-maven-plugin transformerWorkflow configuration (dialect auto-detection, SDK template cartridges, skip flags)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The build runs the judo-spring-maven-plugin goal `transformerWorkflow` bound to generate-sources. Key parameters a developer configures: `dialects` (auto-detected from project dependencies - hsqldb when org.hsqldb:hsqldb present, postgresql when org.postgresql:postgresql present; a user-set value overrides; HSQLDB takes precedence when both are present and one Liquibase master `liquibaseFile` is written); `sdkTemplateCartridges` (defaults to the mvn:hu.blackbelt.judo.generator:judo-psm-generator-sdk-core-{common,api,impl,spring} set, referenced via the `mvn:<groupId>:<artifactId>[:<extension>:<classifier>][:<version>][!path/in/archive]` URL scheme); `sdkTemplateParameters` (generateOptionalTypes=true, generatePayloadValidator=true, apiPrefix/implPrefix/springPrefix derived from sdkPackagePrefix); and the ignore* trace flags (ignoreJsl2Psm, ignorePsm2Asm, ignoreAsm2Rdbms, ignoreRdbms2Liquibase, ignoreAsm2Expression, etc.). Output defaults: sources=src/main/resources/model, destination=target/generated-sources/model, sdkOutputDirectory=<destination>/sdk/<modelName>, and modelName is auto-set from the single root model when the project has no judo-model-name property.
- evidence: ['judo-spring-maven-plugin@a750f28:judo-spring-maven-plugin/src/main/java/hu/blackbelt/judo/spring/maven/plugin/TransformerWorkflowMojo.java:358', 'judo-spring-maven-plugin@a750f28:judo-spring-maven-plugin/src/main/java/hu/blackbelt/judo/spring/maven/plugin/TransformerWorkflowMojo.java:369', 'judo-spring-maven-plugin@a750f28:judo-spring-maven-plugin/src/main/java/hu/blackbelt/judo/spring/maven/plu

## DE-052 [missing-how-to] Project generation toggles and single-actor vs multi-actor mode
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Project generation is controlled by per-module flags (`shouldGenerate*`, sourced from `generator-parameter.properties`): model, sdk, application, rest, internal, frontend, docker, interceptor, schema, karaf, keycloak-theme, web-root, e2e and launcher. Defaults: everything true except e2e and launcher (false). `shouldGenerateSingleActorApplication()` collapses to a single-actor app: it forces `shouldGenerateWebrootModule()` false (single-actor apps get no separate web-root) and throws `IllegalArgumentException('Do not use "generateSingleActorApplication" with "generateWebrootModule"')` when combined with `generateWebrootModule`+`generateWebrootContent`. Frontend base path also differs: `/` for single-actor, else `/`model`_react/<actor>`. A developer choosing deployment shape must know these flags and the single-actor constraint.
- evidence: ['judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-common/src/main/java/hu/blackbelt/judo/jsl/fullstack/karaf/project/archetype/StoredVariableHelper.java:146', 'judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-common/src/main/java/hu/blackbelt/judo/jsl/fullstack/karaf/project/archetype/StoredVariableHelper.java:1

## DE-053 [missing-how-to] Frontend build recovery: delete source dirs and rerun ./judo.sh build -i
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: When ./judo.sh build -i fails on the frontend reactor (frequently after OpenSpec changes — e.g. TS2307 'Cannot find module ~/services/data-axios/Servicesrack_serviceRackServiceForAvailableRackElementsImpl'), the reliable recovery is to delete the frontend-react module's generated src/pages/, src/dialog/, src/containers/ and src/servicies/ folders and re-run ./judo.sh build -i; the generator recreates them. A full clean/src deletion is the documented workaround, not just re-running build.
- evidence: ["judo-cli-sessions__2026-09-16T17-03 : [U] 'Here is how we should run the build: ... if the ./judo.sh build -i comand does not works, then delete the frontend-react's src's folders src/pages/, src/dialog , src/containers and src/servicies folder and then rerun the ./judo.sh build -i command. A lot of time there are build tasks for the openspec, but always fails, and this can help it'", 'judo-cli-

## DE-054 [missing-how-to] Schema evolution: additive stored model members need NO manual liquibase/schema-upgrade step — the generated changelog carries them
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: When a model change merely adds a stored member (attribute) to an entity, the schema migration is produced automatically: the model's generated liquibase changelog (application/model/target/generated-resources/model/rackinspect-liquibase_postgresql.changelog.xml) already contains the new column (e.g. C_AI_PROCESSING). No manual schema upgrade / migration step is required and the user treats it as wrong to run one. A manual schema-upgrade step only becomes relevant for genuinely non-additive/backward-incompatible changes.
- evidence: ['<judo-cli-sessions__sessions__2026-09-18T09-07-56-772Z_01a0b3c5-c0e3-771d-838f-c8cafda1cb5c.jsonl> : "NO LIQUIBASE increemnt need. Please continue the implementtion of the spec"', '<judo-cli-sessions__sessions__2026-09-19T17-24-47-307Z_01a0bab2-fc4a-733d-868a-f23612a2e150.jsonl> : "`schema-upgrade` is NOT a prerequisite for this — corrected after challenge. `aiProcessing` is a STORED member, and

## DE-055 [missing-how-to] Stale Maven SNAPSHOT jars in ~/.m2 vs generated sources; rebuild with ./judo.sh build -i
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Tests can pass while the installed SNAPSHOT jars in ~/.m2 are stale — so unit tests compiled against fresh generated sources behave differently from the artifacts actually run. Always rebuild with `./judo.sh build -i` (which forces regeneration, ignoring checksums and deleting hand-edits not covered by .generator-ignore), and verify installed jar content with `javap`/`unzip` rather than relying on jar mtimes. The `-i` flag is the required form; plain `./judo.sh` is insufficient.
- evidence: ['judo-cli-sessions 2026-09-22 : [U] So the tests are good, but the artifacts are stale?', 'judo-cli-sessions 2026-09-22 : [U] Maybe the problem was that I develop in two copied repo parallel. Now I rebuild the project I will tell you when it is done and you can run the currently failing tests', 'judo-cli-sessions 2026-09-23 : [U] If the build fails then try with ./judo.sh build -i command. Also w

## DE-056 [missing-how-to] Local email testing with Mailpit vs production SMTP env-provided values
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Email is tested locally with a catcher like Mailpit: SMTP host/port come from `judo-karaf.env` (`localhost:1025`, no auth/TLS) for local runs, while test/demo/prod read `JUDO_PLATFORM_MAIL_SMTP_*` (+ `_FROM`) from deployment env vars in `environments/<env>/app-compose/docker-compose.yml`. Nothing in the app depends on Mailpit itself; it only catches outgoing SMTP. New-user/activation emails also route through this same SMTP so mailpit can capture them too.
- evidence: ['judo-cli-sessions__2026-10-01T08-16 : "Mailpit is only something to run locally. It catches outgoing mail so you can look at it. Nothing in the app depends on it, because the app only knows an SMTP host and port, and those come from environment variables"', 'judo-cli-sessions__2026-10-01T08-16 : "test / demo / prod: environments/<env>/app-compose/docker-compose.yml reads JUDO_PLATFORM_MAIL_SMTP_

## DE-057 [missing-how-to] GCS bucket as JUDO S3 filestore (HMAC + env config)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: Google Cloud Storage exposes an S3-compatible XML API, so JUDO's S3FileStoreService works against GCS with no GCS-specific code or config: point the client at https://storage.googleapis.com using HMAC credentials (S3 config keys). The platform reads the choice from JUDO_PLATFORM_ environment variables (FILESTORE type, s3Bucket, s3Region, plus filestoreTokenExpiry) resolved from the DispatcherServiceActivator config template; bucket lifecycle (e.g. delete-after-1-day rule) is provisioned in GCS.
- evidence: ['rackinspect 2026-10-05 : "GCS exposes an S3-compatible XML API. `S3FileStoreService` works against it for files of any size... GCS is ordinary S3 configuration pointed at `https://storage.googleapis.com` with HMAC credentials."', 'rackinspect 2026-10-05 : "s3Bucket = ${s3Bucket!""} / s3Region = ${s3Region!"us-east-1"}" (DispatcherServiceActivator.template)', 'rackinspect 2026-10-07 : "The dashbo

## DE-058 [missing-how-to] JUDO multi-repo version propagation and snapshot builds
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: A JUDO runtime change spans several Git repositories (judo-runtime-core, judo-platform, osgi-filestore) plus the application. To develop end-to-end you create parallel feature branches, build bottom-up (runtime-core → install snapshot into local ~/.m2 → platform pins new runtime-core → application pins platform), and propagate versions in BOTH application/pom.xml and judo-version.properties. The judo-versions repo holds the real versions in its pom.xml <properties>; src/main/resources/versions.properties is only ${} placeholders. Before merging you verify commit ancestry (the feature commit must be an ancestor of the develop build) and confirm the new artifact is actually in the assembled karaf-offline zip/docker image. ./judo.sh upgrade refreshes the pinned versions.
- evidence: ['rackinspect-sessions-...2026-10-15T19-33-24Z : "u should create local test branch on judo-runtime-core and judo-platform where u apply this cache and a test branch on rackinspect, use snapshot build for the change"', 'rackinspect-sessions-...2026-10-19T12-05-26Z : "we will update the judo versions check first the versions on judo-versions against our properties ones"', 'rackinspect-sessions-...2

## DE-059 [missing-how-to] AI pi-analyzer plugin credential seeding-once & volume persistence
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The pi-analyzer plugin seeds credentials once: seed-credentials.mjs skips if the target file exists, so RI_AUTH_JSON (or the auth file) is ignored once auth.json exists. Rotating a credential therefore requires deleting the seeded file (e.g. docker compose rm -sf pi-analyzer before up), and it must be mounted on a named volume or it lives in the container layer and is lost on replace — while persisting it means data lives on the app VM's boot disk.
- evidence: ['deploy-md-converter-demo : [A!] Seeding is strictly once. If auth.json exists, RI_AUTH_JSON is ignored. So rotation hinges entirely on whether that file survives a container recreate.', "deploy-md-converter-demo : [A!] Upstream's dev compose.yml mounts three named volumes — but our template mounts nothing", 'deploy-md-converter-demo : [A!] The volume is called app-compose_rackinspect-data ... Th

## DE-060 [missing-topic] Running JUDO on Spring Boot (autoconfiguration, model discovery)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO provides a full set of Spring Boot autoconfiguration modules (judo-runtime-core-spring, spring-hsqldb, spring-postgresql) that assemble the RDBMS runtime (DAO, dispatcher, query factory, variable resolver, identifier signer) without OSGi/Karaf. The runtime model is discovered from the judo.modelName property (default empty); if blank, the context scans classpath*:/model/*.model for a *-asm.model file, and startup fails with 'modelName is not set and could not be determined' when none is found. Database dialect autoconfiguration is gated on the datasource URL containing 'hsqldb' or 'postgresql' (@ConditionalOnExpression on spring.datasource.url). The ANTLR runtime check (< 3.5) runs unconditionally on startup.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-spring/src/main/java/hu/blackbelt/judo/runtime/core/spring/JudoModelLoaderConfiguration.java:42', 'judo-runtime-core@b34d8ea1:judo-runtime-core-spring/src/main/java/hu/blackbelt/judo/runtime/core/spring/JudoModelLoaderConfiguration.java:65', 'judo-runtime-core@b34d8ea1:judo-runtime-core-spring-hsqldb/src/main/java/hu/blackbelt/judo/runtime/core/spring

## DE-061 [missing-topic] The target-datasource-model concept (targetDatasourceModelName)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: In a multi-model JUDO deployment, one model owns the shared datasource and every other model is configured against it. Every per-model activator reads a `targetDatasourceModelName` config key and, for the model whose name equals it, suppresses its own per-model components (dialect/mapper/sequence, Keycloak connector/login interceptor, dispatcher PIDs, health checks, realm extractor, access manager). The managed datasource carries `dao.datasource.name`, `managed.datasource.name` and `judo.model.name`, and components bind per model via filters like `(dao.datasource.name=<name>)`.
- evidence: ['judo-services@ced983fe:judo-services-persistence-hsqldb/src/main/java/hu/blackbelt/judo/services/persistence/hsqldb/HsqldbComponentActivator.java:73', 'judo-services@ced983fe:judo-services-security-cxf-osgi/src/main/java/hu/blackbelt/judo/services/security/cxf/osgi/CxfSecurityActivator.java:126', 'judo-services@ced983fe:judo-services-dispatcher-osgi/src/main/java/hu/blackbelt/judo/services/dispa

## DE-062 [missing-topic] PostgreSQL bootstrap retry and pax-jdbc datasource configuration keys
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The PostgreSQL datasource tracker waits for the database with a resilience4j retry loop before creating an org.ops4j.datasource factory configuration: retryMaxAttempts (default 1000), retryExponentialBackoff (default true), retryWaitDuration (default 1000ms) and ignoreVersionCheck (default false). `pax-jdbc.*` config keys are copied into the datasource configuration with the `pax-jdbc.` prefix stripped (the HSQLDB tracker keeps the prefix). An HsqldbServer component likewise forwards `pax-jdbc.` properties to its generated datasource config. If the connection still fails after retries, the error is only logged and no datasource configuration is created for that model.
- evidence: ['judo-services@ced983fe:judo-services-persistence-postgresql/src/main/java/hu/blackbelt/judo/services/persistence/postgresql/LiquibaseModelToPostgresqlDatabaseServiceTracker.java:64', 'judo-services@ced983fe:judo-services-persistence-postgresql/src/main/java/hu/blackbelt/judo/services/persistence/postgresql/LiquibaseModelToPostgresqlDatabaseServiceTracker.java:176', 'judo-services@ced983fe:judo-s

## DE-063 [missing-topic] Generated artifact naming and where workflow output lands (<modelName>-rdbms_<dialect>.model, <modelName>-<realm>-keycloak.json, <modelName>-liquibase_<dialect>.changelog.xml, operation bundle)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The workflow save step emits deterministic artifact filenames from the model name and dialect: RDBMS models as <modelName>-rdbms_<dialect>.model, Keycloak realm configuration as <modelName>-<realm>-keycloak.json, Liquibase changelogs as <modelName>-liquibase_<dialect>.changelog.xml, and the generated Java operation bundle as an OSGi bundle whose Bundle-SymbolicName is <modelName>-script2operation. Models are written to destination only when saveModels is true (default) or when the workflow failed, and destination must already exist (it is not created).
- evidence: ['judo-tatami@13186706:judo-tatami-workflow/src/main/java/hu/blackbelt/judo/tatami/workflow/DefaultWorkflowSave.java:100', 'judo-tatami@13186706:judo-tatami-workflow/src/main/java/hu/blackbelt/judo/tatami/workflow/DefaultWorkflowSave.java:122', 'judo-tatami@13186706:judo-tatami-workflow/src/main/java/hu/blackbelt/judo/tatami/workflow/DefaultWorkflowSave.java:126', 'judo-tatami@13186706:judo-tatami

## DE-064 [missing-topic] Spring Boot auto-configuration of generated SDK DAOs
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The spring module of the SDK generator emits one Spring @Configuration class per model (<Model>DaoModules in the springPrefix package) with three @Autowired fields (DAO, AsmModel, PayloadValidator) and one @Bean method per DAO, static navigation and static data (allDaoTransferObjectType / allStaticNavigation / allStaticData) that news up the impl and calls setDao/setAsmModel/setPayloadValidator. It also writes META-INF/spring.factories with EnableAutoConfiguration=<class> and META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports, so the config auto-registers when the bundle is on the classpath.
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-spring/src/main/resources/spring/spring-dao-provider.java.hbs:5', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-spring/src/main/resources/spring/spring-dao-provider.java.hbs:17', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-spring/src/main/resources/psm-sdk-core.yaml:9', 'judo-psm-generator-sdk

## DE-065 [missing-topic] Full frontend environment-variable reference
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: The generated frontend consumes a specific env-var set: VITE_API_DEFAULT_BASE_URL (fallback window.location.origin), VITE_API_RELATIVE_PATH (fallback '/api'), VITE_FILE_DEFAULT_BASE_URL (fallback the API base URL), and optionally VITE_MUI_LICENSE_KEY. The API base path is API_DEFAULT_BASE_URL + API_RELATIVE_PATH, and the file base path is FILE_DEFAULT_BASE_URL + '/<application.modelName>'.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/main.tsx.hbs:45', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/main.tsx.hbs:66', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/vite-env.d.ts.hbs:7']

## DE-066 [missing-topic] Building Flutter frontends via the JUDO Maven plugin (flutter / install-flutter goals)
- target: agent-docs/deployment | src: gap-mining | status: mined
- fact: JUDO generates Flutter frontends alongside React, and drives their build with Maven plugin goals: `install-flutter` (installs the Flutter SDK from a pinned version archive or a Git channel, default channel `stable`, verified via `flutter doctor`/`flutter --version`) and `flutter` (runs arbitrary flutter CLI commands, default `pub get`). Key parameters/properties: flutter.arguments, flutter-version, flutter-channel, flutter-skip, flutter-install-skip, workingDirectory/installDirectory/tempDirectory (defaults ${basedir}, ${basedir}/.flutter, ${basedir}/target/temp), and Maven-proxy inheritance (flutterInheritsProxyConfigFromMaven=true).
- evidence: ['judo-maven-plugin@12540e1:src/main/java/hu/blackbelt/judo/maven/plugin/FlutterMojo.java:45', 'judo-maven-plugin@12540e1:src/main/java/hu/blackbelt/judo/maven/plugin/InstallFlutterMojo.java:52', 'judo-maven-plugin@12540e1:src/main/java/hu/blackbelt/judo/maven/plugin/AbstractFlutterMojo.java:60', 'flutter-maven-plugin@bd51a8c:src/main/java/hu/blackbelt/flutter/maven/plugin/mojos/flutter/FlutterMoj

## DE-067 [wrong-fact] deployment: judo.sh build docker option
- target: agent-docs/deployment | src: session:jb-007.json | status: validated
- claim: ./judo.sh build -DskipDocker=false builds docker.
- fact: judo.sh has no -D pass-through; use -d. The docker profile activates on !skipDocker so =false still skips Docker.
- evidence: judo-esm-fullstack-project-template@c312243 (DE-001)

## DE-068 [wrong-fact] deployment env var names
- target: agent-docs/deployment | src: session:jb-007.json | status: validated
- claim: JUDO_PLATFORM_DATASOURCE_*, JUDO_PLATFORM_FILESTORE_PATH, judo-karaf.env.development/production files generated.
- fact: Sources use JUDO_PLATFORM_RDBMS_DB_* and JUDO_PLATFORM_HIKARI_*; filestore is JUDO_PLATFORM_FILESTORE_DIRECTORY; env files are not generated, environment selection is via judo.sh env <name>. Karaf SSH 8101/karaf is the Apache Karaf default (not set in project; doc fine if labelled).
- evidence: template compose files (DE-002..006)

## DE-069 [wrong-fact] Runtime BOM does not pin jaxrs-cxf-server
- target: agent-docs/deployment | src: session:jb-011.json | status: reported-unvalidated
- claim: Root AGENTS.md says the BOM pins every runtime artifact
- fact: judo-runtime-core-jaxrs-cxf-server has no entry in dependencyManagement of judo-runtime-core-dependencies/pom.xml.
- evidence: session C141

## DE-070 [wrong-fact] root AGENTS export-jxls packaging
- target: agent-docs/deployment | src: session:jb-011.json | status: reported-unvalidated
- claim: export-jxls is a plain jar
- fact: export-jxls/pom.xml:11 declares packaging bundle.
- evidence: session C145

## DE-071 [wrong-fact] Community docs: Maven version, antora-lunr
- target: agent-docs/deployment | src: session:jb-013.json | status: reported-unvalidated
- claim: 01_system-requirements.adoc: Maven must start with 3.8 yet uses 3.9.x
- fact: root pom sets <maven>3.9.4</maven> property; generate-site.js requires 'antora-lunr' not in package.json (only @antora/lunr-extension); pom clean-plugin has two <directory> in one <fileset> (second may be ignored).
- evidence: community-documentation@ec8768c, reader C245

## DE-072 [wrong-fact] Admin guide wrong parameter names/defaults
- target: agent-docs/deployment | src: session:jb-013.json | status: reported-unvalidated
- claim: SAME_USERNAME policy; keycloakPublicUrl; mail port default 10025
- fact: SAME_USERNAME not valid; parameter is keycloakAuthPublicUrl; mail port code default 1025. 06_application_metrics.adoc:137 nested try-with-resources both declare `outer` (won't compile; rename inner).
- evidence: session, reader C249

## DE-073 [wrong-fact] Quick reference, line 71
- target: agent-docs/deployment/README.md | src: agent-docs-review:deployment.json | status: reported
- claim: Production build: ./judo.sh build -DskipDocker=false
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:33 (judo.sh build has no -D pass-through; Docker is enabled with -d --docker); judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-application/src/main/resources/docker/pom.xml.hbs:24 (docker profile activates on !skipDocker, so skipDocker=false still disa

## DE-074 [wrong-fact] Command reference (judo.sh start options)
- target: agent-docs/deployment/README.md | src: agent-docs-review:deployment.json | status: reported
- claim: Start/run options are only documented as start/stop/status/reckless
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:50-52 (start -o runtime=karaf|compose, compose_env=compose-develop|compose-postgresql-https, dbtype=hsqldb|postgresql, karaf_port, postgres_port, keycloak_port)

## DE-075 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:105
- target: agent-docs/deployment/application-config.md | src: judo-ng-read | status: validated
- claim: Database is configured with JUDO_PLATFORM_DATASOURCE_URL, JUDO_PLATFORM_DATASOURCE_USERNAME and JUDO_PLATFORM_DATASOURCE_PASSWORD (also in t
- fact: judo.sh and the Docker compose stacks export JUDO_PLATFORM_RDBMS_DB_DATABASE, JUDO_PLATFORM_RDBMS_DB_USER, JUDO_PLATFORM_RDBMS_DB_PASSWORD a
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:105

## DE-076 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:27
- target: agent-docs/deployment/application-config.md | src: judo-ng-read | status: validated
- claim: Quick-reference variable name JUDO_PLAT-FORM_DATASOURCE_USERNAME (contains a hyphen; same typo on line 28 for PASSWORD).
- fact: The variable prefix is JUDO_PLATFORM_ with no hyphen, and the variable actually used is JUDO_PLATFORM_RDBMS_DB_USER.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:27

## DE-077 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:244
- target: agent-docs/deployment/application-config.md | src: judo-ng-read | status: validated
- claim: File storage directory is configured with JUDO_PLATFORM_FILESTORE_PATH.
- fact: The Docker compose stack uses JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:244

## DE-078 [wrong-fact] Environment-specific files, lines 487-490
- target: agent-docs/deployment/application-config.md | src: agent-docs-review:deployment.json | status: reported
- claim: judo-karaf.env.development and judo-karaf.env.production files are used per environment
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:103 (env <env> option selects an alternate custom properties file; the template only ships judo-karaf.env.hbs)

## DE-079 [wrong-fact] Database variables, lines 26, 56, 105, 388, 409
- target: agent-docs/deployment/application-config.md | src: agent-docs-review:deployment.json | status: reported
- claim: JUDO_PLATFORM_DATASOURCE_URL (and DATASOURCE_USERNAME/PASSWORD/DRIVER_CLASS_NAME, MAX/MIN_POOL_SIZE)
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:598-599 (JUDO_PLATFORM_RDBMS_DB_HOST, JUDO_PLATFORM_RDBMS_DB_PORT); judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-application/src/main/resources/docker/compose-postgresql-https/docker-compose.yml.hbs:67 (JUDO_PLATFORM_RDBMS_DB_HOST=postgres); judo.sh

## DE-080 [wrong-fact] JUDO_PLATFORM_FILESTORE_PATH, line 244
- target: agent-docs/deployment/application-config.md | src: agent-docs-review:deployment.json | status: reported
- claim: JUDO_PLATFORM_FILESTORE_PATH sets the filestore location
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-application/src/main/resources/docker/compose-postgresql-https/docker-compose.yml.hbs:62 (JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore)

## DE-081 [wrong-fact] Mail and cache variables, lines 270 and 344
- target: agent-docs/deployment/application-config.md | src: agent-docs-review:deployment.json | status: reported
- claim: JUDO_PLATFORM_MAIL_SMTP_HOST and JUDO_PLATFORM_CACHE_SIZE are supported settings
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo-karaf.env.hbs:1-4 (only JUDO_PLATFORM_LOG_SMTP_SERVER and JUDO_PLATFORM_FILESTORE found; mail/cache keys not found in sources checked)

## DE-082 [missing] Multi-module build: install model+schema before sdk; stale ~/.m2 model jar
- target: agent-docs/deployment/build-process.md | src: session:jb-029.json | status: reported-unvalidated
- fact: A JUDO app is a Maven reactor (model, schema, sdk, internal, app, common). Installing sdk standalone fails with 'Could not collect dependencies'; use -pl with -o and validateModels=false after installing model+schema. The SDK pom regenerates at generate-sources FROM the installed model jar in ~/.m2, not edited model source, so a stale jar poisons the chain; mvnd may print BUILD SUCCESS while installing stale jars (S17-05, S04-01).
- evidence: knowledge-gaps-report.md §2 Multi-module build order

## DE-083 [missing] Handlebars constructs in template agent-docs
- target: agent-docs/deployment/build-process.md | src: session:jb-033.json | status: validated
- fact: Template agent-docs (.hbs) use only: {{{docLink "path" "text" "skill"}}} (89x), {{{localHubLink "text" "skill"}}} (44x), {{ lowerCase model.name }} (219x), {{ model.name }}, escaped literals (\\{{ }}), and a few #if/#each/#unless blocks that appear only as examples. Helpers are in EsmProjectHelper.java (docLink at line 182, docLinkSimple at 222), in judo-esm-fullstack-project-template-common. docLink becomes [text](path) and localHubLink becomes [text](./README.md).
- evidence: judo-ng template@6273a87:EsmProjectHelper.java:182

## DE-084 [missing] How to create a new project from the ESM fullstack template
- target: agent-docs/deployment/build-process.md | src: session:jb-033.json | status: reported-unvalidated
- claim: build-process.md only says the project was 'initially generated using the JUDO ESM Fullstack Project Template' with generator-parameter.properties.
- fact: There is no how-to for creating a new project. Template modules: judo-esm-fullstack-project-template-{root,application,common,test}. The artifacts are in ~/.m2/repository/hu/blackbelt/judo/template/judo-esm-fullstack-project-template-root/ (versions 1.0.0-SNAPSHOT and 1.0.0.20260903_235856_3b675ffd_develop). The root module's resources (judo-ng/template/.../judo-esm-fullstack-project-template-root/src/main/resources) contain pom.xml.hbs, judo.sh.hbs, generator-parameter.properties.hbs, AGENTS.md.hbs, README.adoc.hbs and pom.xml.*.fragment.hbs. The pom has a generate-root execution with synchronizeGitignore (esm=${basedir}/model/{{createdModelName}}.model, ignoredFiles pom.xml,**/pom.xml,judo.sh,.mvn/jvm.config). Generated projects use ./judo.sh build and need Docker. ~/.m2/settings.xml needs a <server> with id '<app>-distribution'. A model lives in model/<app>.model. A how-to for creating from scratch should be written.
- evidence: session 2026-11-09T14:44, bash; Rackinspect README.adoc

## DE-085 [wrong-fact] judo.sh command reference
- target: agent-docs/deployment/build-process.md | src: agent-docs-review:deployment.json | status: reported
- claim: Commands listed: build, start, stop, status, reckless, clean, prune; no dump/import/env/schema-upgrade
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:118-121 (generate, generate-root, dump, import); judo.sh.hbs:25 (schema-upgrade); judo.sh.hbs:90 (env <profile>)

## DE-086 [wrong-fact] judo.sh build options
- target: agent-docs/deployment/build-process.md | src: agent-docs-review:deployment.json | status: reported
- claim: Build options list (-DskipDocker style passed via judo.sh)
- evidence: judo-esm-fullstack-project-template@c312243:judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:27-42 (build -v, -p, -a, -f, -sc, -d, -M, -B, -F, -KA, -S, -ma, -q, -i)

## DE-087 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/local-development.md.hbs:35
- target: agent-docs/deployment/local-development.md | src: judo-ng-read | status: validated
- claim: Application is reachable at http://localhost:8080 (and Karaf runs on port 8080 for the app, line 32).
- fact: judo.sh defaults the Karaf HTTP port to 8181 (karaf_port unset -> 8181); 8080 is the Keycloak default.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/local-development.md.hbs:35

## DE-088 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/local-development.md.hbs:99
- target: agent-docs/deployment/local-development.md | src: judo-ng-read | status: validated
- claim: curl http://localhost:8080/api/entity/Address tests the running app.
- fact: The app's HTTP port defaults to 8181, not 8080.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/local-development.md.hbs:99

## DE-089 [wrong-fact] Karaf SSH access, lines 37 and 147 (also README.md.hbs:142, production.md.hbs:200,237,240)
- target: agent-docs/deployment/local-development.md | src: agent-docs-review:deployment.json | status: reported
- claim: Karaf SSH on port 8101 with password karaf
- evidence: judo-ng@HEAD:packages/karaf-features: no sshd port or user config found; port is Apache Karaf upstream default, not set in the project sources

## DE-090 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:234
- target: agent-docs/deployment/production.md | src: judo-ng-read | status: validated
- claim: Health check: curl http://localhost:8080/health.
- fact: The generated UI calls /system/health?tags=<model>&format=json; no /health route appears in the template, and the documented health path els
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:234

## DE-091 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:93
- target: agent-docs/deployment/production.md | src: judo-ng-read | status: validated
- claim: Docker container is configured with -e DB_HOST, DB_PORT, DB_NAME, DB_USER and DB_PASSWORD.
- fact: The compose stack configures JUDO_PLATFORM_RDBMS_DB_HOST, JUDO_PLATFORM_RDBMS_DB_DATABASE, JUDO_PLATFORM_RDBMS_DB_USER and JUDO_PLATFORM_RDB
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:93

## DE-092 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:145
- target: agent-docs/deployment/production.md | src: judo-ng-read | status: validated
- claim: KEYCLOAK_URL=http://localhost:8080/auth configures Keycloak.
- fact: The template uses JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL; no template file reads KEYCLOAK_URL.
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/production.md.hbs:145

## DE-093 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:411
- target: agent-docs/deployment/schema-evolution.md | src: judo-ng-read | status: validated
- claim: Model version is set in application/model/pom.xml as 1.2.0.${maven.build.timestamp}_${git.commit.id.abbrev}_${git.branch}
- fact: The generated model pom sets model-version to ${project.version}; the composite timestamp/commit/branch form is not generated, and -Dmodel-v
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:411

## DE-094 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:165
- target: agent-docs/deployment/schema-evolution.md | src: judo-ng-read | status: validated
- claim: Entity tables are named t_entity_<name> (examples: t_entity_user in UPDATE and ALTER statements at lines 165, 476-485)
- fact: generate-domain-docs.py assumes database tables are named T_ENTITIES_<NAME> and filters on that prefix; the two conventions contradict each 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:165

## DE-095 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:111
- target: agent-docs/deployment/schema-evolution.md | src: judo-ng-read | status: validated
- claim: Schema artifacts and images are named <name>-application-schema (JAR, Docker image lines 291, 298, 319; schema JAR at line 547)
- fact: The schema module artifactId is <name>${projectPostfix}-schema and the jib image is ${project.artifactId}, so the -application infix only ap
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/schema-evolution.md.hbs:111

