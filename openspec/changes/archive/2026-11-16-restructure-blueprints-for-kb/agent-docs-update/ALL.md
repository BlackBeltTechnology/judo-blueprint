# Out-of-area sweep items (107) — route each to its proper home

## MO-005 [decision] Pin agent-docs import to template commit 6273a87
- target: agent-docs/(general) | src: session:jb-033.json | status: operator-stated
- fact: Import agent-docs from judo-esm-fullstack-project-template@6273a87 (the review's preferred base). The commit before 5bddd8b ('JNG-6380 Remove agent-docs from the template') differs by only 8 files. Render the Handlebars to static markdown and drop domain/. The domain/ dir is generated per model by generate-domain-docs.sh. Agent used neutral model name 'myapp'. Renderer: openspec/changes/restructure-blueprints-for-kb/oneoff/agent-docs-import/render.py.
- evidence: judo-blueprint@07612bf, judo-ng template@6273a87
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-009 [missing] Consuming blueprint catalog from other projects via kb git source
- target: agent-docs/(general) | src: session:jb-000.json | status: validated
- fact: pi-dashboard-kb supports SourceConfig {kind: filesystem|npm|git|https, ref, priority, subdir, pin, refresh: on-index|manual|{ttlMs}}. A consumer project adds in .pi/dashboard/knowledge_base.json e.g. {kind:'git', ref:'git@github.com:BlackBeltTechnology/judo-blueprint.git', pin:'develop' or tag, subdir:'model-blueprints', priority:-5, refresh:{ttlMs:86400000}}, repeated per subdir (best-practices, agent-docs); clone cache shared (kind+ref+pin, inferred). Constraints: trust-on-first-use (first kb index must be interactive, else KbUntrustedSourceError, background reindex fails); SSH key needed for private repo; include/exclude are global to the config not per source so subdir is the only way to exclude .claude/ and PROGRESS.md; kb_search tool has no per-source filter (CLI has --root id).
- evidence: pi-agent-dashboard packages/kb/src/config.ts:16-24, src/sources.ts:27-34,117,136,270
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-010 [missing] Handlebars helpers in template agent-docs and how to render
- target: agent-docs/(general) | src: session:jb-002.json | status: validated
- fact: Template .hbs docs use: docLink (89 uses), localHubLink (44), lowerCase model.name (218 uses, in 'model/{{ lowerCase model.name \}}.model'), #if (1, deployment/build-process) with rdbmsCreateSimpleName, projectPostfix (1, integration-testing/osgi-ds-descriptor-tests), model.name. docLink/localHubLink in EsmProjectHelper.java:176/187 already output plain markdown links ([text](path), [text](./README.md)); context arg ignored. Render lowerCase model.name to neutral <app> placeholder; #if/projectPostfix handle individually. Escaped \{{ }} (63 lines) are literal output.
- evidence: judo-esm-fullstack-project-template-common/.../EsmProjectHelper.java:176,187
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-011 [missing] cciu branch adds agent-docs content not in template
- target: agent-docs/(general) | src: session:jb-002.json | status: validated
- fact: origin/feature/cciu-model-patterns touches 44 agent-docs with ~616 lines not in template: junk (rendered 'webshop' text, ./SKILL.md back links, 'judo-frontend-docs skill' refs) and real content (~112 lines debugging-and-monitoring, ~76 advanced-modeling-patterns, ~56 deployment/README, Keycloak realm sync, menu-item rule 'Add the Menu Item Entry' in model-development). Keep real parts merged into synced docs and suggest upstreaming to template.
- evidence: session 2026-11-03T13:02:57, ctx_execute diff HEAD...origin/feature/cciu-model-patterns
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-012 [missing] Top missing-knowledge themes (High priority)
- target: agent-docs/(general) | src: session:jb-020.json | status: reported-unvalidated
- fact: High themes by session count: judo-model-cli usage (22); inspection fault registry/ticketing; model changes that break generated/custom frontend code; generated DAO/SDK surprises; UI model values that break the generator; offline-first mobile ingest (localId idempotency, two-stage upload, change stamps); binary upload/download two-phase token flow; SYSTEM/non-principal actors (exposure, transfer-object closure, realm); multi-module build order and stale artifacts; DAO read/write performance (seek, batching, eager owned relations); enforce rules server-side not only in UI; E2E methodology (baseline dump, real-UI first, time budget); model workflow gates as derived predicates over status.
- evidence: session 2026-11-06T09:38:51, render.py output
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-066 [wrong-fact] blueprint agent-docs/ is a stale copy of template docs
- target: agent-docs/(general) | src: session:jb-002.json | status: validated
- claim: agent-docs/ (68 files) in judo-blueprint is considered current
- fact: All 68 files come from one 'Initial commit' (molnar-botond, 2026-03-05) and never changed. Template (judo-esm-fullstack-project-template-root/src/main/resources/agent-docs, 74 .hbs) had 15 more commits, latest 1db5acb 2026-09-04. Measured: 9 identical, 59 differ, 6 missing (model/judo-cli.md, model/transformation-pipeline.md, model/ui-authoring-guide.md, etc.). Blueprint copy contains 4 domain/ files which must come only from the template (model-dependent); move to legacy/.
- evidence: session 2026-11-03T13:00-13:04, operator + agent measurement
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-067 [wrong-fact] Template agent-docs removed from judo-esm-fullstack-project-template
- target: agent-docs/(general) | src: session:jb-006.json | status: validated
- claim: Template ships agent-docs (74 files: backend 12, deployment 7, domain 4, e2e-testing 7, frontend 16, integration-testing 8, model 19, README.md.hbs).
- fact: Commit 5bddd8b 'JNG-6380 Remove agent-docs from the template' (branch feature/JNG-6380_cli_guidance, already contained in origin/develop; develop has 0 agent-docs files). Template's JUDOSPEC agent system (18 subagents, 10 commands, 32 hooks) is extracted via openspec change extract-agent-tooling-from-template; judo-blueprint now holds the agent-docs; a new pi plugin takes agent behaviour. Generated AGENTS.md/openspec/project.md/agent-docs are checksum-tracked and overwritten by ./judo.sh generate-root (release notes say so); generateAgentCli name kept.
- evidence: judo-esm-fullstack-project-template@5bddd8b / 9ff75d0b
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-068 [wrong-fact] Backend docs: JQL link and transfer object supertypes
- target: agent-docs/(general) | src: session:jb-013.json | status: reported-unvalidated
- claim: 07_access_token.adoc:12 links ROOT:howto/02_jql_variables.adoc; 02_service_model.adoc:98 says transfer objects have Supertypes
- fact: Real page: developer-guide/backend/02_jql_variables.adoc; line 102 says TO inheritance not allowed, mixins used.
- evidence: session, reader C257
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-069 [wrong-fact] agent-docs README points to a local .claude skill
- target: agent-docs/(general) | src: session:jb-033.json | status: validated
- claim: "## CLI Documentation: For JUDO Model CLI commands, see the judo-model-cli skill in .claude/skills/judo-model-cli/."
- fact: Replace with '## Platform CLI', linking model/judo-cli.md (why the CLI is mandatory, platform invariants) and model/transformation-pipeline.md (ESM → PSM → ASM → RDBMS → Liquibase, server vs client regeneration, in-memory state). The .claude directory is removed in the restructure.
- evidence: rendered template README.md:38
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-070 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:138
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: public static GeneratorModel loadYamlURL(URL yamlUrl).
- fact: loadYamlURL is public static GeneratorModel loadYamlURL(String originalUri, URL yaml, ModelGenerator.CreateGeneratorContextArgument args) th
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:138
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-071 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:154
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: public GeneratorModel overrideTemplates(GeneratorModel override) returns a new merged model.
- fact: overrideTemplates returns void and takes a Collection<GeneratorTemplate>; it changes the templates in place.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:154
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-072 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:112
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter has actorTypePredicate(Predicate<ActorType>) and actorTypeTargetDirectoryResolver(Function<ActorType, File>).
- fact: The generic fields are discriminatorPredicate (Predicate<T>) and discriminatorTargetDirectoryResolver (Function<T, File>); the names actorTy
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:112
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-073 [wrong-fact] src/main/resources/agent-docs/components/model-generator.md:27
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ModelGenerator.createGeneratorContext is called with six arguments (templateLoader, urlResolver, generatorModel, helperClasses, valueResolve
- fact: createGeneratorContext takes a single CreateGeneratorContextArgument.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/model-generator.md:27
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-074 [wrong-fact] src/main/resources/agent-docs/components/model-generator.md:53
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ModelGenerator.recalculateChecksumToDirectory(param) with one GeneratorParameter argument.
- fact: The public overloads are recalculateChecksumToDirectory(File targetDirectory, String generatorFilesName) and recalculateChecksumToDirectory(
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/model-generator.md:53
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-075 [wrong-fact] src/main/resources/agent-docs/components/checksum-validation.md:132
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ModelGenerator.recalculateChecksumToDirectory(param) with one GeneratorParameter argument.
- fact: No single-argument overload exists; the overloads take (File, String) or (GeneratorParameter<T>, Collection<T>).
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/checksum-validation.md:132
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-076 [wrong-fact] src/main/resources/agent-docs/guides/user-guide.md:63
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ModelGenerator.createGeneratorContext is called with six arguments.
- fact: createGeneratorContext takes a single CreateGeneratorContextArgument.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/user-guide.md:63
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-077 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:23
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: domain-overview.md holds the high-level overview and the ER diagrams, generated or maintained by the domain tooling
- fact: generate-domain-docs.py writes entity-reference.md and er-diagram.md only; no shipped script writes domain-overview.md
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:23
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-078 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:282
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Fully automated update: run 'python scripts/generate_domain_docs.py'
- fact: The shipped script is agent-docs/domain/generate-domain-docs.py; there is no scripts/ directory in the generated project
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:282
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-079 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:182
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Tests live at /tests/test_model_interrogator.py (also /tests/README.md, /tests/QUICK_START.md, /tests/example_usage.py, /tests/TEST_SUMMARY.
- fact: No such test files are generated; the fullstack-project.yaml entries for agent-docs/domain only produce README.md, diagram_generator.py, gen
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:182
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-080 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:304
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Copy agent-docs/domain/domain_documentation_template.md into a new project
- fact: domain_documentation_template.md is not generated or shipped; the agent-docs/domain entries in fullstack-project.yaml list only the four dom
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:304
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-081 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:394
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Quick test: ./tests/run_tests.sh
- fact: No tests/run_tests.sh is generated; agent-docs/domain ships no test scripts
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/domain/README.md.hbs:394
- from: model | previous agent note: Concerns import process, template, backend/generator docs or the domain/ area, not catalog/agent-docs/model

## MO-007 [mention-only] OpenAPI/Swagger UI serving location per model (/api-spec/<model>)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: A SwaggerUIServlet is registered per OpenapiModel on the HttpService at `/api-spec/<model name>` (API_SPEC_URL + '/' + name). The `apiRoot` config key defaults to `/api` and becomes the swagger.json basePath prefix: basePath = apiRoot + '/' + model name; swagger.json is generated per request, sets host from the request server name (port appended unless 80/443) and schemes from the request scheme. Responses are gzip'd on Accept-Encoding: gzip and use ETag caching (index.html/swagger.json no-cache; png/css/json max-age=31536000).
- evidence: ['judo-services@ced983fe:judo-services-swagger-ui/src/main/java/hu/blackbelt/judo/services/swagger/ui/SwaggerServletActivatorOpenAPIModelServiceTracker.java:98', 'judo-services@ced983fe:judo-services-swagger-ui/src/main/java/hu/blackbelt/judo/services/swagger/ui/SwaggerServletActivatorOpenAPIModelServiceTracker.java:56', 'judo-services@ced983fe:judo-services-swagger-ui/src/main/java/hu/blackbelt/j
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-008 [mention-only] X-Judo-* REST request protocol headers
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated REST operation signatures expect protocol headers `X-Judo-CountRecords` (→ `__countRecords`), `X-Judo-Mask` (→ `__mask`), `X-Judo-RequestParameters` (→ `__requestParameters`, parsed by `RestUtils.parseHeaderRequestParams` into a `Map`), `X-Judo-SignedIdentifier` (bound operations), and `X-Judo-MarkSelectedRangeItems` (range operations); the impl also derives `__principal` from SecurityContext and `__locale` from the first Accept-Language. A malformed `X-Judo-RequestParameters` header yields HTTP 400. These headers are how clients control masking, filtering/params, paging counts, and signed-identifier calls.
- evidence: ['judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:26', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/rest.service.operation.fragment.hbs:68', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.utils.java.hbs:12']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-018 [missing-how-to] ~meta security discovery and ~principal actor endpoints
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Each Actor exposes GET /api/<Model>/Actor/<Actor>/~meta whose security[0] entry provides tokenEndpoint, clientId and openIdConfigurationUrl used to obtain an OAuth access_token for that Actor, and GET /api/<Model>/Actor/<Actor>/~principal returning the authenticated principal (email plus __identifier/__signedIdentifier). These are the self-service endpoints a custom frontend needs to implement login/authentication against Keycloak.
- evidence: ['judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Special_FilteredAccess.postman_collection.json:47', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Special_FilteredAccess.postman_collection.json:173', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Special_FilteredAccess.postman_collection.json:497']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-023 [missing-how-to] Packaging and deploying a model as an OSGi bundle (Judo-Models manifest header and bundle model/ resource layout)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: A JUDO model is deployed to the running platform as an OSGi bundle that declares a Judo-Models manifest header (entry name=<model-name>, optional version). The bundle must carry model resources under model/ with a strict naming scheme: <name>-asm.model, -measure.model, -expression.model, -keycloak.model, -asm2keycloak.model, and per dialect <name>-rdbms_<dialect>.model, -asm2rdbms_<dialect>.model, -liquibase_<dialect>.changelog.xml. The ModelBundleTracker (config key dialects, default empty string) loads these; generated attached jars reuse classifiers sdk, sdk-internal, jaxrsapi, script2operation. Version fallback rules apply when the version attribute is missing/blank/.SNAPSHOT.
- evidence: ['judo-platform@2d22cf41:judo-platform-services/judo-services-model-bundle-deployer/src/main/java/hu/blackbelt/judo/services/model/bundle/deployer/ModelBundleTracker.java', 'judo-platform@2d22cf41:judo-platform-services/judo-services-model-bundle-deployer/src/main/java/hu/blackbelt/judo/services/model/bundle/deployer/BundleModelHolder.java', 'judo-rdbms-schema@008bd34:judo-rdbms-schema-testdata/te
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-024 [missing-how-to] Per-model Keycloak connector configuration: acceptableClients actor-to-client map, access types, and user-manager toggle
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The KeycloakSecurityActivator creates per-Keycloak-model components whose config keys include serverUrl, publicUrl, adminUser, adminPassword, clientSecret (on KeycloakConnectorComponent) and updateExistingUsers, requiredActions, enabled (on KeycloakUserManagerComponent). managementEnabled=false registers only the connector component; managementEnabled=true registers all seven (admin client, realm synchronizer, user manager, password policies). The KeycloakLoginInterceptorComponent reads acceptableClients (default "") in the format ActorFQN=client1,client2;OtherActor=client3 (client IDs may contain dashes/dots) to map Keycloak client IDs to actors; password-policy ids are NO_PASSWORD, SAME_EMAIL, SAME_USERNAME.
- evidence: ['judo-platform@2d22cf41:judo-platform-services/judo-services-security-keycloak-osgi/src/main/java/hu/blackbelt/judo/services/security/keycloak/osgi/KeycloakSecurityActivator.java', 'judo-platform@2d22cf41:judo-platform-services/judo-services-security-keycloak-cxf-osgi/src/main/java/hu/blackbelt/judo/services/security/keycloak/cxf/osgi/component/KeycloakLoginInterceptorComponent.java', 'judo-platf
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-025 [missing-how-to] Per-model backend CORS filter configuration keys
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: CxfSecurityActivator registers a per-model CrossOriginResourceSharingFilter with service filter application.filter=(judo.model.name=<model name>) and derives it from OSGi config keys: cors_allowOrigin (default "*", comma-split when set), cors_allowCredentials (true), cors_allowHeaders (default "Content-Type,Origin,Accept,Authorization,X-Judo-SignedIdentifier,X-Judo-CountRecords"), cors_exposeHeaders ("X-Exchange-Id,X-Fault,X-Judo-Count"), cors_maxAge (-1), cors_prefligthErrorStatus (400), cors_blockIfUnauthorized (false), cors_defaultOptionsMethodsHandlePreflight (false).
- evidence: ['judo-platform@2d22cf41:judo-platform-services/judo-services-security-cxf-osgi/src/main/java/hu/blackbelt/judo/services/security/cxf/osgi/CxfSecurityActivator.java']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-026 [missing-how-to] Bound operations and signed identifier mechanics
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Bound operations (on a specific instance) rely on a JWT-signed identifier. DefaultIdentifierSigner builds a compact JWS whose subject is the identifier, with claims ver (version), immutable, and issuer = FQName of the producing EReference/EOperation; it writes __updateable, __deleteable and __immutable flags into payloads from the 'permissions' extension annotation (update/delete, default false). The Dispatcher rejects an exposed bound operation without the SIGNED_IDENTIFIER_KEY header with ValidationException ERROR_MISSING_IDENTIFIER_OF_BOUND_OPERATION, rejects a mapped transfer payload carrying an identifier without a signed identifier with IllegalArgumentException 'Identifier is not allowed without signed identifier', and throws AccessDeniedException ACCESS_DENIED_INVALID_TYPE when the producing type is not the accessed type or a supertype.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultIdentifierSigner.java:300', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultIdentifierSigner.java:204', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/d
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-027 [missing-how-to] @JudoTest runtime caching (shareInjector, BY_CLASS/SINGLETON)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The @JudoTest testkit supports caching the derived runtime (QueryFactory, Liquibase execution, Guice Injector) across test methods via the boolean shareInjector() element (default false), active only for class-level BY_CLASS and SINGLETON test modes; BY_METHOD and method-level annotations are never cached. The cache key for BY_CLASS combines modelName, dialect, modelSource, testClass, modules and interceptors. A shared injector means the interceptor provider is class-shared mutable state, so sibling methods see each other's runtime mutations and tests need BY_METHOD or @BeforeEach resets.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:215', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/ByClassCacheKey.java:23', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-028 [missing-how-to] Actor resolution claim-mapping lookup order and checkMappedActors
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: DefaultActorResolver maps a JudoPrincipal to an actor entity. getActorByClaims picks the lookup attribute in this order: the USERNAME-claim attribute if its claim is present, then the EMAIL-claim attribute, then the first identifier attribute (sorted by name) present in claims; otherwise it throws IllegalStateException. No matching actor throws AccessDeniedException AUTHENTICATED_ENTITY_NOT_FOUND; multiple matches throw SecurityException 'Multiple actors found in database by token'. authenticateActor calls authenticateByPrincipal only when the exchange has no ACTOR_KEY and checkMappedActors is true (default false). Claims whose matching attribute is annotated transient are copied onto the returned actor payload.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultActorResolver.java:202', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultActorResolver.java:101', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatc
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-029 [missing-how-to] ActorResolver SPI: custom principal-to-actor resolution
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: ActorResolver is the security SPI that maps an authenticated JudoPrincipal or token claims to a persisted actor Payload. It exposes authenticateActor(Map exchange), authenticateByPrincipal(JudoPrincipal) returning Optional<Payload>, and getActorByClaims(EClass actorType, Map claims) returning a payload. A DefaultActorResolver is wired by JudoDefaultModule, but the interface can be overridden to implement custom matching, just-in-time provisioning or rejection of principals.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/security/ActorResolver.java:40', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/security/ActorResolver.java:47', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispa
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-030 [missing-how-to] Platform EXPORT operation and Excel Export SPI (JxlsExport)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Modeled EXPORT operations run through an Export SPI whose reference implementation is JxlsExport, producing XLSX via JXLS/POI. Sheet layout is fixed (row 0 headers, row 1 placeholders, data from row 2) and cell formats are derived from ASM types: Timestamp 'dd/mm/yyyy hh:mm:ss', Date 'dd/mm/yyyy', Time 'hh:mm:ss', Decimal '#,##0.00', Integer '0'. Only the AsmModel+fqName overloads work; the Class-based overloads throw UnsupportedOperationException. If no Export is configured, JudoDefaultModule binds UnsupportedExportImpl, so export calls fail with 'Not implemented'.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-export-jxls/src/main/java/hu/blackbelt/judo/runtime/core/export/JxlsExport.java:22', 'judo-runtime-core@b34d8ea1:judo-runtime-core-export-jxls/src/main/java/hu/blackbelt/judo/runtime/core/export/JxlExportUtil.java:214', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/UnsupportedExportImp
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-031 [missing-how-to] Testkit runtime caching and env-var overrides for @JudoTest
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The testkit caches heavy runtime components for speed: @JudoTest.shareInjector (default false) is only honoured for class-level dataSourceMode BY_CLASS or SINGLETON, and only when true are the Injector, QueryFactory, Liquibase executor and TxManager reused across methods. Cache keys are built from modelName, dialect, modelSource, modules and interceptors; SINGLETON shares one cached runtime JVM-wide across matching classes, while BY_CLASS shares per class. Dialect and container resolution also honour env vars JUDO_TEST_DIALECT and JUDO_TEST_CONTAINER ahead of annotation attributes.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:215', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTestExtensionRouting.java:46', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/jud
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-032 [missing-how-to] Maven wiring for JUDO test models (judo-psm-generator-maven-plugin generate)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Each JUDO test model module runs `judo-tatami-jsl-workflow-maven-plugin` and `judo-psm-generator-maven-plugin` goal `generate` in the generate-test-sources phase, reading `target/generated-test-sources/model/<Base>-psm.model` (named after the JSL file base name) and writing SDK code to `target/generated-test-sources/sdk-core/<Name>`, registered with build-helper `add-test-source`. Naming is inconsistent (e.g. `sdk-core/Paging` vs `sdk-core/PagingModel`). A developer adding a test model must know this plug-in wiring.
- evidence: ['judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/models/PagingModel/pom.xml:36', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/models/AbstractModel/pom.xml:31', 'judo-runtime-core-jsl@db6dcf3f:judo-runtime-core-jsl-itest/models/AbstractModel/pom.xml:57']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-033 [missing-how-to] Multi-client Keycloak whitelist (JUDO_PLATFORM_ACCEPTABLE_CLIENTS)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: When several Keycloak clients (frontends) authenticate against the same realm, JUDO maps the token's azp claim to an actor type. By default the client name is derived from azp by replacing '-' with '.'; if a frontend client's name does not match an actor FQN, the actor cannot be resolved. The platform provides a whitelist, parsed by AcceptableClientsParser, in the format ActorTypeFQN=client1,client2;OtherActor=client3 (env var JUDO_PLATFORM_ACCEPTABLE_CLIENTS). Client IDs are normalised (dash to dot); ambiguous client-to-actor mappings are rejected. KeycloakLoginInterceptor also accepts an optional clientToActorMap builder map that remaps azp names to actor names.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-security/src/main/java/hu/blackbelt/judo/runtime/core/security/AcceptableClientsParser.java:53', 'judo-runtime-core@b34d8ea1:judo-runtime-core-security/src/main/java/hu/blackbelt/judo/runtime/core/security/AcceptableClientsParser.java:55', 'judo-runtime-core@b34d8ea1:judo-runtime-core-security-keycloak-cxf/src/main/java/hu/blackbelt/judo/runtime/core/
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-034 [missing-how-to] Keycloak client access-type and user-provisioning defaults
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The KeycloakRealmSynchronizer provisions realms/clients from the keycloak metamodel with defaults: systemDefaultAccessType=CONFIDENTIAL for system actors and humanDefaultSystemAccessType=BEARER_ONLY for actors with @actorType kind HUMAN (a client's own publicClient/bearerOnly overrides). Existing realms/clients are only updated when a compared field differs; redirect URIs/web origins are merged as sorted unions. User provisioning (KeycloakUserManager) is gated on identityManagerReady (checkState throws until setIdentityManagerReady(true), done by the synchronizer), runs async by default, and parses requiredActions from a comma-separated config string.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-security-keycloak/src/main/java/hu/blackbelt/judo/runtime/core/security/keycloak/KeycloakRealmSynchronizer.java:60', 'judo-runtime-core@b34d8ea1:judo-runtime-core-security-keycloak/src/main/java/hu/blackbelt/judo/runtime/core/security/keycloak/KeycloakRealmSynchronizer.java:237', 'judo-runtime-core@b34d8ea1:judo-runtime-core-security-keycloak/src/main
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-035 [missing-how-to] Model-annotation-driven Keycloak realm/client generation and claim mapping
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The ASM→Keycloak transformation generates Keycloak realms and clients from the model itself: each distinct non-blank `realm` EAnnotation value across actor types becomes a realm (id=realm, enabled, loginWithEmailAllowed), and each actor type with a realm annotation becomes a client (name/clientId=FQName with '.'→'-', enabled/directAccessGrantsEnabled/publicClient=true, bearerOnly=false, redirectUris=["*"]). Claim identity is EMAIL→email, USERNAME→username, and plain attribute names email/username become _email/_username. A developer should know that adding a realm annotation to actor types provisions Keycloak without manual client setup.
- evidence: ['judo-tatami-base@14847b0:judo-tatami-asm2keycloak/src/main/epsilon/transformations/keycloak/modules/realm.etl:17', 'judo-tatami-base@14847b0:judo-tatami-asm2keycloak/src/main/epsilon/transformations/keycloak/modules/client.etl:11', 'judo-tatami-base@14847b0:judo-tatami-asm2keycloak/src/main/epsilon/transformations/keycloak/modules/client.etl:31', 'judo-tatami-base@14847b0:judo-tatami-asm2keycloa
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-037 [missing-how-to] Keycloak runtime connector, realm and client-type configuration
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The runtime Keycloak integration is configured per model: KeycloakConnectorComponent takes serverUrl, publicUrl, adminUser, adminPassword (PASSWORD), clientSecret (optional). Management components are only provisioned when managementEnabled=true (default false, connector-only). KeycloakRealmSynchronizerComponent reads realm_loginByEmail (default true), client_accessType_human (default 'CONFIDENTIAL') and client_accessType_system (default 'BEARER_ONLY') — values are parsed via AccessType.valueOf so they must be exact enum names, else activation fails with IllegalArgumentException. Retry defaults asyncServiceCall=true, retryMaxAttempts=1000, retryExponentialBackoff=true, retryWaitDuration=1000ms. Password policies are registered as NO_PASSWORD, SAME_EMAIL, SAME_USERNAME; KeycloakUserManagerComponent requires a `requiredActions` comma-separated config (no default).
- evidence: ['judo-services@ced983fe:judo-services-security-keycloak-osgi/src/main/java/hu/blackbelt/judo/services/security/keycloak/osgi/component/KeycloakConnectorComponent.java:43', 'judo-services@ced983fe:judo-services-security-keycloak-osgi/src/main/java/hu/blackbelt/judo/services/security/keycloak/osgi/component/KeycloakRealmSynchronizerComponent.java:97', 'judo-services@ced983fe:judo-services-security-
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-039 [missing-how-to] Generated REST API contract: tilde subresource verbs and signed identifiers
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: A generated JUDO application exposes a REST API under /api/<Model>/<Actor>/ whose operations are tilde-prefixed subresource verbs: ~create, ~update, ~delete on entities, ~list/~range for collections, and ~set/~add to mutate a many-relation. Entity payloads carry __identifier and __signedIdentifier fields, and collection/relation requests address the owning entity via an X-Judo-SignedIdentifier request header instead of a body path. Errors come back as an HTTP status plus a JSON error array with machine-readable codes (e.g. PATTERN_VALIDATION_FAILED). A developer calling the generated backend directly must know these endpoint shapes, the signed-identifier header, and the error envelope.
- evidence: ['judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:60', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:116', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:535', 'judo-tatami-tests@80e27d28:models/ActionGroupTest/postman/ActionGroupTest.postman_co
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-040 [missing-how-to] REST operation URL path suffixes (~create, ~list, ~range, ~upload-token, ...)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Every generated REST operation is routed on a `~`-suffixed path built by `OperationHelper.toJAXRSPath`: LIST maps to `~list` (cardinality -1) or `~get`, CREATE_INSTANCE to `~create`, and the full suffix set is `~create`, `~validate`, `~update`, `~delete`, `~set`, `~unset`, `~add`, `~remove`, `~range`, `~template`, `~principal`, `~meta`, `~export`, `~upload-token` and `~refresh` (→ `classifier/~get`). The model-name prefix and `_default_transferobjecttypes` segment are stripped, and `.`/`#` become `/`. A dev writing a direct REST client, webhook, or external integration must know these exact routes and that stateless no-input operations are GET while everything else is POST with `application/json`.
- evidence: ['judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/java/hu/blackbelt/judo/psm/generator/jaxrs/api/OperationHelper.java:119', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/java/hu/blackbelt/judo/psm/generator/jaxrs/api/OperationHelper.java:161', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/rest.service.ope
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-041 [missing-how-to] REST response DTO metadata fields (__identifier, __signedIdentifier, __version, __deleteable, ...)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Generated REST DTOs carry reserved double-underscore metadata fields on mapped transfer objects: response DTOs get `__deleteable` (Boolean), `__updateable` (Boolean), `__entityType` (String), `__identifier`, `__signedIdentifier`, `__version` (Integer) and `__referenceId` (String); request DTOs get only `__identifier`, `__signedIdentifier` and `__referenceId`; create-request DTOs get `__referenceId`. Setters for `__deleteable`/`__updateable` take a primitive boolean while getters return Boolean. Clients must know these names to read row capabilities (deleteable/updateable/entity type/version) and to reference existing entity instances when creating/updating via `__referenceId`.
- evidence: ['judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/dtoForResponse.java.hbs:120', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/dtoForRequest.java.hbs:51', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-api/src/main/resources/rest/api/dtoForCreateRequest.java.hbs:16']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-044 [missing-how-to] Signed identifiers: minted only while serving a REST response; there is no reachable plain mint API
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Client/server code that must pass a ticket's `__signedIdentifier` cannot mint one itself with a normal API call: the runtime only mints a signed identifier while it is serving a REST response (i.e. when the AI queries the defect ticket and gets one back in the payload). There is no reachable mint API for custom code to produce a fresh signed identifier on demand. So a client that needs a signed id should receive it from a query result rather than attempt to produce it.
- evidence: ['<judo-cli-sessions__sessions__2026-09-19T17-24-47-307Z_01a0bab2-fc4a-733d-868a-f23612a2e150.jsonl> : "no mint API is reachable, the runtime only mints while serving a REST response."', '<judo-cli-sessions__sessions__2026-09-19T17-24-47-307Z_01a0bab2-fc4a-733d-868a-f23612a2e150.jsonl> : "The AI will get a signed ID when it queries the defectTicket. So it wont be a problem."']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-053 [missing-topic] Access-control runtime semantics: signed identifiers
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO enforces access at runtime via signed identifiers: the signed identifier encodes the access/navigation edge used to obtain an instance, so an update is rejected when the instance was reached through an access that does not allow updates (e.g. ordersInMyRegion marked updatable vs not). Transfer-object identifiers are type-specific: a ProductInfo identifier cannot be used as an AdminProduct identifier (different TO types are not interchangeable). Generated CRUD operations per relation: 'create' for Creatable relations, 'update' for updatable targets, 'set' for all relations of the updatable type, plus unset/add/remove for single relations and range operations for human-exposed or range-defined relations.
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/04_access_control.adoc:100', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/04_access_control.adoc:104', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/04_access_control.adoc:49', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/04_access_control.adoc:52']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-055 [missing-topic] REST wire conversion contract: enums as ordinals, binaries as filestore tokens
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: On the wire, RequestConverter/ResponseConverter translate payloads for transfer types: enum attributes travel as integer ordinals (RequestConverter looks up the input literal via getEEnumLiteral and stores getValue(); ResponseConverter converts an Integer ordinal back to the literal string), binary byte[] attributes travel as filestore download tokens (whose CONTEXT claim must name an attribute of the same binary type), and unknown keys are dropped unless in keepProperties. Enum filter rendering in query customizers uses the form 'this.<attr> == <EnumFQN with ::>#<LITERAL>'.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/RequestConverter.java:358', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/ResponseConverter.java:81', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/Resp
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-056 [missing-topic] Query-customizer filter operator codes and query-mask wire syntax
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The query-customizer parameter processor maps a numeric filter operator code per attribute type: for strings 0 '<', 1 '>', 2 '<=', 3 '>=', 4 '==', 5 '!=', 6 '~' (matches), 7 'like'; numeric/date/time/timestamp use 0-5; boolean only 0 (EQ); enumeration only 0 (EQ) and 1 (NEQ). A 'query mask' string (e.g. under _mask, overridden by the __mask exchange key) is parsed by QueryMaskStringParser and unknown attribute/relation names throw IllegalArgumentException; a mask that fails to parse raises ValidationException 'Invalid query mask' with code INVALID_QUERY_MASK.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/QueryCustomizerParameterProcessor.java:137', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/QueryCustomizerParameterProcessor.java:281', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dispatcher/src/
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-057 [missing-topic] Keycloak realm synchronization and auto-provisioning from the model
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JudoKeycloakModule wires a KeycloakRealmSynchronizer as an eager singleton, so synchronizeAllRealms() runs when the injector is created: realms, clients and users are provisioned from the model's asm2keycloak trace. Its behaviour is controlled by options such as loginByEmail (default true), client access types for human vs system (CONFIDENTIAL vs BEARER_ONLY), CORS allow-origin '*', async service calls and retry/backoff (maxAttempts 1000, waitDuration 1000, exponential backoff true). An identity-manager-ready callback sets userManager.setIdentityManagerReady(true).
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-guice-keycloak/src/main/java/hu/blackbelt/judo/runtime/core/security/keycloak/guice/providers/KeycloakRealmSynchronizerProvider.java:113', 'judo-runtime-core@b34d8ea1:judo-runtime-core-guice-keycloak/src/main/java/hu/blackbelt/judo/runtime/core/security/keycloak/guice/providers/KeycloakRealmSynchronizerProvider.java:68', 'judo-runtime-core@b34d8ea1:ju
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-060 [missing-topic] Actor SSO/security metadata (_metadata operation and _MetadataSecurityFor type)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Every actor gets a `_metadata` unbound operation (GET_METADATA) returning a `_MetadataFor<Actor>` type, and actors with a principal additionally get a `_principal` operation returning the principal type. A `_MetadataSecurityFor<Actor>` unmapped type exposes 9 attributes: required `name` plus optional `openIdConfigurationUrl`, `issuer`, `authEndpoint`, `tokenEndpoint`, `logoutEndpoint`, `clientId`, `clientBaseUrl`, `defaultScopes` (all StringType maxLength 8192). A claim attribute is generated when identity+claim modifiers are present, and a guard modifier compiles to a filtering JQL LogicalExpressionType on the managed mapped actor type.
- evidence: ['judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/actor/actorType.etl:232', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/java/hu/blackbelt/judo/tatami/jsl/jsl2psm/zeta/rules/actor/ActorTypeRules.java:273', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/java/hu/blackbelt/judo/tatami/jsl/jsl2psm/zeta/rules/actor/ActorTypeRules.j
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-061 [missing-topic] Model-driven actor OpenID Connect client configuration (generated _MetadataSecurityFor<actor> client fields)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: For each ESM actor with a mapped principal, the transformation generates an actor metadata transfer-object type _MetadataFor<actor> with an embedded security relation to _MetadataSecurityFor<actor>, which carries nine fixed transfer attributes: name, openIdConfigurationUrl, issuer, authEndpoint, tokenEndpoint, logoutEndpoint, clientId, clientBaseUrl and defaultScopes (name, clientId and defaultScopes are required). These are what an application consumes to configure the OpenID Connect client per actor/realm.
- evidence: ['judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/zeta/rules/ActorRules.java:304', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/epsilon/transformations/psm/modules/actor/actorType.etl:93', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/zeta/rules/ActorRules.java:374']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-062 [missing-topic] JasperReports report generation from the model
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The report generator (judo-psm-generator-report) produces a full JasperReports layer for every qualifying TransferObjectType: a `{Type}Report` facade with `generate{Type}Report(OutputType, dto, File|OutputStream[, Map<String,Object> additionalParameters])` overloads, `{Type}DataSource`/`{Type}DataSourceProvider`/`{Type}DataFactory` support classes, a per-model `ReportUtil` (OutputType enum: PDF, XLSX, CSV, HTML; compiles `.jrxml` at runtime when no `.jasper` is found), and master/sub `.jrxml` reports with sub-report wiring for embedded collection relations. Developers must know how to enable the generator (type psm-report, `reportPrefix`, `reportFqNameFilter`, `locales`), compile `.jrxml`→`.jasper`, and call the facade/`ReportUtil.generateReport` from custom operations to export reports.
- evidence: ['judo-psm-generator-report@eb9bbaa:judo-psm-generator-report-jasper-java/src/main/resources/java/report/report.java.hbs:18', 'judo-psm-generator-report@eb9bbaa:judo-psm-generator-report-jasper-java/src/main/resources/java/utils/ReportUtil.java.hbs:43', 'judo-psm-generator-report@eb9bbaa:judo-psm-generator-report-jasper-report/src/main/resources/jasper/master-report.jrxml.hbs:3']
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-063 [missing-topic] REST Assured generated test client (ApiClient) for API-level tests
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The REST Assured generator (judo-psm-generator-restassured) emits a static `ApiClient.api(Config)` entry point per model with `BASE_URL_<ACTOR>` constants, `authTo<Actor>(grantType, userName, password)` OIDC password-grant helpers (posting `client_id=<model>-<actor>`, password, `grant_type`), and one REST-Assured wrapper class per exposed transfer object whose operations are nested static classes pinning `REQ_METHOD` (GET only when stateless with no input, else POST) and `REQ_URI` (a compile-time `toJAXRSPath` constant), plus `body(...)`, `xJudoCountRecordsHeader`/`xJudoMaskHeader`/`xJudoSignedIdentifierHeader`, and `execute()` variants. `Config.apiConfig()` installs JacksonObjectMapper by default.
- evidence: ['judo-psm-generator-restassured@ecff962:judo-psm-generator-restassured-api/src/main/resources/restassured/api/apiClient.java.hbs:34', 'judo-psm-generator-restassured@ecff962:judo-psm-generator-restassured-api/src/main/resources/restassured/api/apiClient.java.hbs:84', 'judo-psm-generator-restassured@ecff962:judo-psm-generator-restassured-api/src/main/resources/restassured/api/operationApi.java.hbs
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-064 [missing-topic] X-Judo-* wire-protocol headers
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: All generated REST services communicate via custom headers: X-Judo-SignedIdentifier (target signed id on commands), X-Judo-Mask (response projection on commands), X-Judo-CountRecords / X-Judo-Count (request/response total-count), and X-Judo-MarkSelectedRangeItems (marks already-attached items in range requests). A developer doing manual REST calls, debugging, or writing custom clients must know these exact header names and their semantics.
- evidence: ['judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-api/src/main/resources/rest/headers.ts.hbs:1', 'judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-api/src/main/resources/rest/headers.ts.hbs:6', 'judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-api/src/main/resources/rest/headers.ts.hbs:21', 'judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescrip
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-065 [missing-topic] Engine principal-to-actor resolution (getActorByClaims) and its latency
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Under the hood the dispatcher resolves an authenticated principal into the actor payload via DefaultActorResolver.getActorByClaims: it picks the actor type EClass, finds the attribute annotated with claim=USERNAME, then calls dao.search(...) on that actor type with the claim value — the actor (and its DB read) is resolved on every principal-bearing request. This engine path explains why a partner-related user principal took ~3 seconds to resolve, and it is the part to profile/tune (not the application's #_principal interceptor).
- evidence: ['rackinspect 2026-10-05 (introduce-lean-user-principal) : "add to the proposal why it taked 3 second to get the principal for a parnter related user"', 'rackinspect 2026-10-05 : "public Payload getActorByClaims(final EClass actorType, final Map<String, Object> claims) { ... filter(claim -> Objects.equals(getExtensionAnnotationValue(claim, "claim", false).orElse("-"), "USERNAME")) ... dao.search(.
- from: model | previous agent note: Runtime/REST/security/deployment/testing topic belongs to backend, deployment or integration-testing docs

## MO-017 [missing-how-to] Payload transfer-object library (factories, typed accessors, transient keys)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Payload is a Map<String,Object> data-transfer type with static factories (asPayload(map), map(String k1, Object v1, ...) overloads for 1-20 pairs, map(Entry...), entry) and typed accessors (getAs(Class<T>, String), getAsCollectionPayload(String), getAsPayload(String)). PayloadImpl stores values in a TreeMap; the constructor wraps nested Map/Collection values as Payload but put()/putAll() do not. Transient keys use the '__$' prefix (PayloadImpl.TRANSIENT_PREFIX): equals() ignores them but hashCode() includes them, so payloads equal() may differ in hashCode().
- evidence: ['judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/Payload.java:28', 'judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/Payload.java:170', 'judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/PayloadImpl.java:89', 'judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/PayloadImpl.java:150']
- from: model | previous agent note: Payload library belongs to backend data-access docs

## MO-175 [missing] agent-docs render must use <app> placeholder and hand-edit rule
- target: agent-docs/model/model-development.md | src: session:jb-034.json | status: validated
- claim: Rendered agent-docs contained sample names 'myapp' and 'webshop' (i18n.md, interceptors.md, README, development-workflow).
- fact: Model name rendered as <app> (225 occurrences); remaining 'myapp' samples in frontend/i18n.md (faults.myapp.entities.BusinessError.*, application.model.name) and backend/interceptors.md (myapp.access_management.AccessRole#_addReference...) still need fixing. Added section 'Do not edit the model file by hand': the ESM model file model/<app>.model is XMI; never edit as text, change only through the JUDO CLI.
- evidence: commit 2c2ee92; catalog/agent-docs/frontend/i18n.md:61-127; backend/interceptors.md:648-651
- from: model | previous agent note: myapp/webshop samples are in frontend/backend docs; model dir already uses <app>
## BA-003 [mention-only] Customizing the generated Keycloak login theme (FreeMarker FTL)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated project ships a Keycloak theme module (`<model>-theme`, packaged as a zip of `src/main/resources/themes`) whose login pages are FreeMarker templates: `login.ftl` (username/password, remember-me gated on `realm.rememberMe`, forgot-password on `realm.resetPasswordAllowed`, registration/social sections), `register.ftl` (password/`recaptchaRequired` with `${recaptchaSiteKey}`), `error.ftl`, `template.ftl` (registrationLayout macro with nested header/form/info/socialProviders sections), and an empty `footer.ftl` content-macro override point. Styling is in `theme.properties` (parent=base, `kc*` CSS-class keys) and `login.css`. The theme is tested via `test-theme-with-compose.sh` against a dev Keycloak (admin/judo, TEST_USERS realm).
- evidence: ['judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/theme.properties.hbs:1', 'judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/lo
- from: backend | previous agent note: Keycloak theme: belongs to deployment/auth docs, not backend

## BA-009 [missing-how-to] Filestore S3/GCS backend configuration and access-URL semantics
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The FileStoreService has filesystem, RDBMS and S3-compatible backends. Beyond the env-var surface (JUDO_PLATFORM_FILESTORE=s3, JUDO_PLATFORM_FILESTORE_S3_BUCKET), the S3/GCS backend component (S3FileStoreService) requires config keys protocol, bucketName, accessKey and secretKey, with endpoint defaulting to empty (AWS; a trailing slash is appended) and region defaulting to us-east-1. Uploads of >=5 MiB use multipart (MULTIPART_THRESHOLD = 5*1024*1024). Crucially, getAccessUrl() returns an internal `<protocol>:<fileId>-<filename>` URL resolved by the OSGi URL stream handler - not a public or signed link - so downloads flow through the Karaf servlet. The S3 backend has no metadata cache: every getMimeType/getFileName/getSize/getCreateTime issues a HEAD request.
- evidence: ['osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:42', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:94', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:153', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/o
- from: backend | previous agent note: filestore: deployment area

## BA-010 [missing-how-to] OpenAPI / Swagger API documentation generation
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated REST module can emit an OpenAPI spec: when the isGenerateOpenApiAnnotations generator parameter (or input variable ignoreOpenAPI=false) is set, generateOpenApiAnnotations becomes true and the swagger-maven-plugin resolves the spec to target/api-documentation-swagger as both openapi.json and openapi.yaml; swagger-annotations 2.2.8 is also added to the Karaf feature. This is the only documented way to produce machine-readable API docs for the generated JAX-RS endpoints.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/rest/pom.xml.hbs:152', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/karaf-features/src/main/feature/feature.xml.hbs:20']
- from: backend | previous agent note: OpenAPI generation: deployment area

## BA-012 [missing-how-to] Customizing the JUDO Keycloak auth theme (login/account/email)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO ships a custom Keycloak theme (judo-keycloak) that overrides the stock `keycloak` theme via `parent=base` + `import=common/keycloak` and defines the branded login/account/admin/welcome/email templates as FreeMarker files (login.ftl, template.ftl, welcome/index.ftl). A developer who wants to brand the authentication screens must edit these templates and the theme.properties CSS-class mapping keys (kcButtonClass, kcButtonPrimaryClass, kcInputClass, kcFormCardClass, kcHeaderWrapperClass, kcInputErrorMessageClass), understand the `registrationLayout` macro's nested sections (header/form/info/show-username), and the realm-driven label logic in login.ftl (username/email/usernameOrEmail, rememberMe, resetPasswordAllowed).
- evidence: ['judo-keycloak@e159f55d4b:keycloak/login/theme.properties:1', 'judo-keycloak@e159f55d4b:keycloak/login/theme.properties:34', 'judo-keycloak@e159f55d4b:keycloak/login/template.ftl:42', 'judo-keycloak@e159f55d4b:keycloak/login/login.ftl:100', 'judo-keycloak@e159f55d4b:openspec/specs/login-theme/spec.md:14']
- from: backend | previous agent note: Keycloak theme: belongs to deployment/auth docs, not backend

## BA-017 [missing-topic] Custom Keycloak login theme development
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The fullstack template ships a generated keycloak-theme Maven module (src/main/resources/themes/keycloak-theme/) containing FreeMarker login pages (login.ftl, register.ftl, error.ftl, template.ftl with the registrationLayout macro), a theme.properties (parent=base, import=common/keycloak, styles=css/login.css), a PatternFly-based login.css, a TEST_USERS test realm (test-users-realm.json, import via --import-realm) and a test-theme-with-compose.sh script that unzips the built <artifactId>-<version>-assets.zip into ./keycloak-themes and starts Keycloak on port 8080. The login theme name must exactly match the realm's loginTheme value ('<lowercase model.name><projectPostfix>-theme').
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/template.ftl.hbs', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/theme.properties.hbs:1', 'judo-e
- from: backend | previous agent note: Keycloak theme: belongs to deployment/auth docs, not backend

## BA-019 [missing-topic] Generating OSGi Declarative Services REST clients from OpenAPI specs
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The openapi-generator-cxf-jaxrs-client-osgi-ds generator (generator name `jaxrs-cxf-client-osgi-ds`) produces a CXF JAX-RS client that is packaged as an OSGi bundle with a Declarative Services activator. From an OpenAPI spec it emits API/model packages plus a `ClientApiServiceActivator` with @ObjectClassDefinition config properties: endPoint (default basePath), log_payload, log_payload_limit (1000), connection_timeout (10000 ms), receive_timeout (15000 ms). Config options: activatorPackage (default org.openapitools.activator), activatorDsConfigurationRequired (false), useGzipFeature, useLoggingFeature; activatorDsConfigurationRequired=true emits configurationPolicy=REQUIRE.
- evidence: ['openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:README.md:158', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:README.md:70', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:src/main/java/hu/blackbelt/openapi/codegen/JavaCXFClientOsgiDsCodegen.java:54', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:openspec/specs/codegen/spec.md:76']
- from: backend | previous agent note: OpenAPI client generator: deployment area

## BA-040 [mention-only] Running Liquibase changelogs from OSGi bundles (LiquibaseExecutor)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: osgi-liquibase exposes a LiquibaseExecutor service with executeLiquibaseScript(Connection, scriptPathInBundle, Bundle) and an overload taking a Map<String,Object> of changelog parameters. DefaultLiquibaseExecutor is an immediate DS component that swaps the thread-context classloader, enters a Liquibase Scope with the Slf4jLogService, resolves changelog resources via BundleResourceAccessor, and applies parameters via setChangeLogParameter before update. Only LiquibaseException is rethrown; any other exception is swallowed so the caller sees success. The SPI logging service Slf4jLogService has default priority 5, overridable via system property hu.blackbelt.osgi.liquibase.logging.Slf4jLogService.priority.
- evidence: ['osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/LiquibaseExecutor.java:38', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/LiquibaseExecutor.java:48', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/impl/DefaultLiquibaseExecutor.java:99', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/logging/Slf4jLogService.java:35']
- from: backend | previous agent note: osgi-liquibase executor: deployment/schema area

## BA-044 [missing] Backend generator fragment override layouts
- target: agent-docs/backend | src: session:jb-001.json | status: reported-unvalidated
- claim: n/a
- fact: Generator scans two equivalent fragment-file layouts (project may mix): Layout A sibling: application/karaf-features/src/main/feature/feature.xml.<slot>.fragment.hbs and application/<module>/pom.xml.<slot>.fragment.hbs; second layout also supported. Slots: feature.xml: extra-repositories, extra-bundles, model-bundles; each pom.xml: project-definition, properties-definition, extra-plugin-management, extra-plugins, extra-dependencies; app-root pom: extra-modules. Slot names come from '<!-- To define create ...fragment.hbs file -->' markers. Analyzer should glob *.fragment.hbs.
- evidence: cciu-model-patterns .claude/agents/judo-backend-analyzer.md
- from: backend | previous agent note: generator fragment layouts: deployment/build-process area; also unvalidated

## BA-048 [missing] Keycloak defaults and qualifier count
- target: agent-docs/backend | src: session:jb-011.json | status: validated
- claim: DOX row says 21 qualifiers
- fact: 22 qualifiers (JudoKeycloakModuleConfiguration lines 17-143); keycloakServerUrl default http://localhost:8080/auth (line 17), keycloakAdminPassword default 'judo' (line 26).
- evidence: session C147 validation
- from: backend | previous agent note: Keycloak defaults: deployment area

## BA-111 [missing-topic] JUDO SDK generator template parameters (apiPrefix / generateOptionalTypes / generatePayloadValidator / debugPrint / identifierType)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The judo-psm-generator-sdk-core generator reads five Handlebars template variables (set as Maven plugin <parameters> / generator-parameter.properties values and read through StoredVariableHelper from a ThreadLocal while templates execute): apiPrefix (string package prefix prepended to generated API package names), generateOptionalTypes (boolean; when true, non-required attributes and relations are wrapped in java.util.Optional), generatePayloadValidator (boolean; gates payload validation via validatePayload in the generated DAO impls), debugPrint (boolean; adds debug comment banner lines), and identifierType (the Java type used for identifiers in generated DAO/DTO code, e.g. java.io.Serializable). These flags change the shape of the generated SDK API a developer writes against.
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/api/StoredVariableHelper.java:48', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/api/StoredVariableHelper.java:60', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/jav
- from: backend | previous agent note: SDK generator parameters: deployment area
## BA-015 [missing-pattern] E2E baseline orchestration: prepared DB dump (incl. Keycloak users) built once, parallel stacks on distinct ports
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: For E2E suites the team wanted a reusable prepared dump produced by judo.sh containing all test data and base roles together with Keycloak users (Keycloak shares the backend DB), rebuilt once, and a flow that recreates it when it goes stale. Because cold app start is ~10 minutes, the dump/image must be built once and reused across runs; parallel E2E groups run full stacks on different ports to avoid collisions, and host-machine images are reused.
- evidence: ['rackinspect-sessions-20261103__--Users-gaborflorian-projects-rackinspect--__2026-09-16T20-36-39-237Z_01a0abef-90c4-74f5-9fa9-3fea0b4ecf3a.jsonl : i want to run the test on a mode where we use a prepared dump which created bz the judo.sh and all the test data and base roles are there with kezcloak users (keycloak use the smae db as the backend) so we use the dump as a base start four our test, at
- from: backend | previous agent note: E2E orchestration: e2e-testing area
## BA-011 [missing-how-to] OIDC logout, profile popup, and signed-in gating
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Authenticated frontend behavior: logout calls signoutRedirect with post_logout_redirect_uri set to the current URL without its hash fragment; the avatar/profile popup (HeaderProfile + ProfilePopup) is generated only when application.authentication is on, and the profile page opens as a dialog when application.profilePage and openInDialog are set. The layout also blocks rendering until principal.__signedIdentifier exists and maps error code AUTHENTICATED_ENTITY_NOT_FOUND to a 'User not found' message.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/Header/HeaderContent/HeaderProfile/index.tsx.hbs:64', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/ProfilePopup/index.tsx.hbs:34', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/index.tsx.hbs:42', 'judo-ui-react-template@af315252:judo-ui-reac
- from: backend | previous agent note: frontend auth behaviour
## MO-052 [missing-how-to] Modern JUDO integration-testkit configuration and performance (BY_CLASS, shareInjector, model-runtime cache)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The current `@JudoTest` testkit (judo-runtime-core-guice-testkit) has datasource modes BY_METHOD / BY_CLASS / SINGLETON and a `shareInjector` opt-in; BY_CLASS and SINGLETON cache heavy resources (DataSource, JudoModelLoader) across methods, and a model/X QueryFactory build is the dominant per-class cost (~20s for a real model), which is why ~300 test classes took over an hour. An opt-in system property `judo.testkit.shareModel` (JNG-6421) shares one model loader and QueryFactory per JVM per (modelName, dialect, modelSource) key. A guide on writing tests that reuse these modes (instead of default fresh-per-class bootstrap) is what makes suites run in minutes instead of hours.
- evidence: ['rackinspect-20261031 15:37 : [U] u should analize the integrations test and its running time, our goal do cerease the runnig time of the integrations test becouse its took an hour or more, check where we loose time', 'rackinspect-20261031 15:37 : [U] u should add a guide the test how should the test created, whats the best practicies and etc u should add to hte foders AGENTS.md too, the goal to
- from: model | previous agent note: Testkit performance belongs to integration-testing docs
## BA-070 [missing-how-to] GenModel generator configuration and output control
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The MWE2/Xtext generator is configured by a RuntimeModelGeneratorConfig: resolveModelName and resolveModelVersion (when blank, the generated code exposes name/version as settable fields; when set, getName()/getVersion() return the literal value and no setter is generated), genModelNames (empty list = generate every GenModel), and printXmlOnError (when true the generated ValidationException message appends asString()). The MWE2 workflow defaults javaPath=src and javaGenPath=src-gen, runs a DirectoryCleaner that deletes javaGenPath before each run, splits a 'gen-once' outlet into javaPath, and requires modelDir to be supplied by the caller.
- evidence: ['judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/generator/runtimemodel/templates/RuntimeModel.xtend:14', 'judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/generator/runtimemodel/engine/RuntimeModelGeneratorConfig.xtend:10', 'judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/genera
- from: backend | previous agent note: GenModel generator config: not backend dev

## BA-118 [wrong-fact] EmptyMapIntstanceCollector name
- target: agent-docs/backend | src: session:jb-008.json | status: reported-unvalidated
- claim: agent-docs/README.md row says `EmptyMapInstanceCollector`.
- fact: The class in dao-core is spelled `EmptyMapIntstanceCollector` (typo is real, referenced in dao-core collectors/AGENTS.md).
- evidence: session 2026-11-04T09:47, subagent reader B098 (judo-runtime-core-dao-core)
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-120 [wrong-fact] Oracle dialect does not exist
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Row lists an oracle dialect bundle among Dialect implementations
- fact: Only hsqldb and postgresql implement Dialect in this checkout; no Oracle bundle.
- evidence: session 2026-11-04T13:22, subagent C134
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-121 [wrong-fact] SelectStatementExecutor constructor responsibilities
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Constructor sets up METRICS scopes and getConstantFields() set/remove
- fact: Constructor only registers expression translators; METRICS scope/constant fields handling happens in selectMetadata, executeSelect and countSelect.
- evidence: session 2026-11-04T13:22, subagent C137
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-122 [wrong-fact] dispatcher extension-points.md signatures
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Signatures for ActorResolver, VariableResolverManager, DispatcherFunctionProvider, IdentifierSigner and Export
- fact: These signatures do not match the code.
- evidence: session C141
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-124 [wrong-fact] custom-queries SKILL uses nonexistent translator.register
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: uses translator.register(...) and lists FilterMapper class
- fact: No register method exists (map reachable only via getTranslators()); FilterMapper class is not in the repo.
- evidence: session C141, C145 (Translator has no register; custom-functions skill line 82)
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-125 [wrong-fact] query-debugging SKILL rdbmsReference
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: calls resolver.rdbmsReference(...)
- fact: Does not exist; M:N lookup is rdbmsJunctionTable(EReference).
- evidence: session C141
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-126 [wrong-fact] getTransferObjectGraph return type in expression docs
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: returns bare type
- fact: Code returns Optional.
- evidence: session C145
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-128 [wrong-fact] FeatureFactory '~90 converters'
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: ~90 converters
- fact: FeatureFactory registers 78 converters.put calls; feature/AGENTS.md lists 72 converter files.
- evidence: session C156
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-129 [wrong-fact] Converter AGENTS rows wrong
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: StringAggregated handles concatenate; Matches adds one operand parameter
- fact: StringAggregatedExpressionToFeatureConverter switch handles only MIN and MAX; MatchesToFeatureConverter adds two parameters (STRING and PATTERN).
- evidence: session C157/C158
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-130 [wrong-fact] transferObjectType.etl generateBehaviours guard
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: The doc says the whole family of rules is generateBehaviours-guarded.
- fact: `CreateQueryOrderingType`, `CreateQueryFilterType`, `CreateQuerySeekingType`, the get-range input rules and `CreateUploadTokenType` have no such guard.
- evidence: batch C371
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-131 [wrong-fact] Asm2Keycloak AGENTS.md claims
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: ClientRules.java.AGENTS.md says `createKeycloakClientClaim` reads `keycloakResource`. Asm2Keycloak.java.AGENTS.md claims MD5 keying for script URIs. Asm2KeycloakRuleNames AGENTS.md says `CreateRealm` is an ETL rule name.
- fact: All three claims are wrong. The code does not read `keycloakResource` there, does no MD5 keying, and `realm.etl` has no `CreateRealm` rule.
- evidence: batch C389
- from: backend | previous agent note: judo-ng internal AGENTS docs

## BA-132 [wrong-fact] asm2rdbms zeta rules AGENTS.md counts and perf test sizes
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: zeta/rules/AGENTS.md:8: 'ten eClassToTable*Field rules'. The perf test sizes are 10/50/100.
- fact: ClassRules.java has nine eClassToTable*Field rules plus eClassToRdbmsTable, ten @TransformRule methods in total. The perf test sizes in code are 100/500/1000. In `ReferenceRules.java:558`, `fk2.setSqlName` runs only if the source table and PK exist, but fk2 is still added to the junction table and traced, so its sqlName may be null with no warning.
- evidence: batch C392
- from: backend | previous agent note: judo-ng internal AGENTS docs
## FR-006 [missing-topic] UI element fully-qualified-name (FQN) conventions
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: FQN resolution rules for the UI model are non-uniform: an Application's FQN is its simple name; a Theme is <AppName>::Theme; a Frame is <containerFQN>::Frame; MimeType uses type/subType with a '/' separator; other NamedElements use a :: hierarchy; elements without a usable name fall back to the XMI URI fragment. These rules are implemented in UiFqnResolverImpl and drive the CLI's model type 'ui' and FqnCache-backed resolution.
- evidence: ['judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:125', 'judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:136', 'judo-meta-ui@7bdc5ac:model/src/main/java/hu/blackbelt/judo/meta/ui/cli/UiFqnResolverImpl.java:164', 'judo-meta-ui@7bdc5ac:openspec/specs/runtime/osgi-and-cli/spec.md:135']
- from: frontend | previous agent note: UI FQN conventions belong to the model/CLI docs

## BA-083 [missing-how-to] Embedding the ESM→UI transformation programmatically (Esm2Ui API)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The transformation can be invoked from Java via `Esm2Ui.executeEsm2UiTransformation(Esm2UiParameter)` built with `esm2UiParameter()` (defaults: transformationMode ETL, parallel=false, applicationType "default", applicationColumns 12, useCache=true), or as a workflow work unit `Esm2UiWork` / `Esm2UiWorkParameter` run inside a `TransformationContext`. `calculateEsm2UiTransformationScriptURI()` resolves the script root from jar/bundle/directory sources; ETL runs `esmToUi.etl` once per ActorType with context vars `actorType/esmUtils/uiUtils/applicationType/applicationColumns`. A developer embedding generation in custom tooling needs this API surface.
- evidence: ['judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2Ui.java:109', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2Ui.java:63', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2UiWork.java:46', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/
- from: backend | previous agent note: tatami transformation internals: model area

## BA-084 [missing-how-to] Transformation mode switching (ETL vs ZETA vs DUAL)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The tatami-core transformation engine can run in ETL (Epsilon), ZETA (Java), or DUAL (run both and compare) modes, selected via the `judo.transformation.mode` system property (e.g. `-Djudo.transformation.mode=ETL`). The default is ZETA since the mode flip; an explicit `transformationMode(TransformationMode.ETL)` work parameter overrides on a per-step basis, and DUAL runs both engines to compare output. A developer must know how to choose and pass the mode when running a model build.
- evidence: ['judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationMode.java:86', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationMode.java:122', 'judo-tatami-core@a81a4bf0:openspec/changes/change-default-transformation-mode/proposal.md:107']
- from: backend | previous agent note: tatami transformation internals: model area

## BA-085 [missing-how-to] Composable workflow engine API (Sequential/Parallel/Conditional/Repeat flows)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The tatami-core workflow engine composes transformation steps into flows through builders: `WorkFlowEngineBuilder.aNewWorkFlowEngine().build()`, `SequentialFlow.Builder.aNewSequentialFlow()`, `ParallelFlow`, `ConditionalFlow.Builder.aNewConditionalFlow().execute(w1).when(WorkReportPredicate.COMPLETED).then(w2).otherwise(w3)`, and `RepeatFlow` with `.repeat(work).times(n)`/`.until(...)`. Work flows nest (WorkFlow extends Work), the name must be unique per workflow, and each Work must catch exceptions and report WorkStatus.FAILED.
- evidence: ['judo-tatami-core@a81a4bf0:README.md:318', 'judo-tatami-core@a81a4bf0:documentation/workflow.md:156', 'judo-tatami-core@a81a4bf0:documentation/workflow.md:238', 'judo-tatami-core@a81a4bf0:AGENTS.md:161']
- from: backend | previous agent note: tatami transformation internals: model area

## BA-086 [missing-how-to] Transformation trace service (navigating the model trace chain)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: TransformationTraceService is an OSGi service that registers TransformationTrace objects per model name and lets callers navigate the transformation chain in both directions from a single EObject: ascendants/descendants via `getAscendantsOfInstanceByModelType`, `getRootAscendantsOfInstance`, and `getTraceEntriesForInstance(modelName, instance)` (multi-source, carrying ruleName/discriminator). Element identity is by resource URI + URI fragment, and queries throw IllegalArgumentException when the model name was never registered.
- evidence: ['judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceService.java:195', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceService.java:135', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceServiceImpl.java:286']
- from: backend | previous agent note: tatami transformation internals: model area

## BA-109 [missing-topic] Generation feature switches and their defaults (generateActors/generateOperations/generateBehaviours/generateTransferObjectTypes/generateDefaultTransferObjectTypes, stringMaxLength)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The ESM-to-PSM transformation is gated by five boolean switches carried on every parameter builder: generateActors, generateOperations, generateBehaviours, generateTransferObjectTypes and generateDefaultTransferObjectTypes, all defaulting to true, plus stringMaxLength (default 65536) which controls the generated _StringType. The switches are not uniform: e.g. the _...ForDefaultTransferObjectType attribute rules are gated by generateDefaultTransferObjectTypes (not generateTransferObjectTypes), and the query-customizer/ordering/filter families are gated by generateBehaviours.
- evidence: ['judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/Esm2PsmZeta.java:122', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/Esm2PsmWork.java:58', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/epsilon/transformations/psm/modules/service/transferAttribute.etl:82']
- from: backend | previous agent note: generation switches: model/deployment area
## FR-007 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:139
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: String helper capitalize: 'hello' becomes 'Hello'.
- fact: No capitalize helper exists. The equivalent is firstToUpperCase(String).
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:139
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-008 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:140
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: String helper camelToSnake: 'myVar' becomes 'my_var'.
- fact: No camelToSnake helper exists. The helper is camelCaseToSnakeCase, which returns UPPER_UNDERSCORE, so 'myVar' becomes 'MY_VAR'.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:140
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-009 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:36
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: The camel-to-snake example uses CaseFormat.LOWER_UNDERSCORE and returns lowercase snake_case.
- fact: StringHelper.camelCaseToSnakeCase uses CaseFormat.UPPER_UNDERSCORE.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:36
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-010 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:146
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: URI helpers pathOf and schemeOf exist.
- fact: Neither pathOf nor schemeOf exists. UriHelper provides calculateRelativeURI, concatUri and lastPart.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:146
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-011 [wrong-fact] src/main/resources/agent-docs/components/helpers.md:120
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Collection<Class<?>> helpers = TemplateHelperFinder.collectHelpers(packageName, classLoader).
- fact: collectHelpers returns Collection<String> (class names). The Class-returning method is collectHelpersAsClass.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/helpers.md:120
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-012 [wrong-fact] src/main/resources/agent-docs/components/template-system.md:94
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ChainedURLTemplateLoader.createFromURIs(Arrays.asList(overrideUri, baseUri), 'templates').
- fact: createFromURIs takes only Collection<URI>; the second 'templates' argument does not exist.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/template-system.md:94
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-013 [wrong-fact] src/main/resources/agent-docs/components/generator-ignore.md:73
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: A '!' prefix in .generator-ignore negates a pattern, so '!generated/important.txt' keeps the file.
- fact: GeneratorIgnore has no negation handling. Each line is passed unchanged to FileSystems.getPathMatcher('glob:' + line) and the results are OR
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/generator-ignore.md:73
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## FR-014 [wrong-fact] src/main/resources/agent-docs/components/generator-ignore.md:96
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: Patterns from deeper directories take precedence over patterns from higher levels.
- fact: shouldExcludeFile returns true if any pattern from any level matches. It walks upward and stops at the first match, but there is no preceden
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/components/generator-ignore.md:96
- from: frontend | previous agent note: generator-commons agent-docs (helpers/template-system/generator-ignore) are not in catalog/agent-docs/frontend

## BA-004 [missing] kb frontmatter keys: only title/description/aliases/keywords searchable; facets tags,status,author,category,date
- target: agent-docs/(general) | src: session:jb-000.json | status: validated
- claim: Blueprint frontmatter (id, domain, category, score, usage_count, alternative_count, projects, first_seen, last_updated) is assumed queryable
- fact: kb DEFAULT_SEARCHABLE_KEYS = title, description, aliases, keywords; DEFAULT_FACET_KEYS = tags, status, author, category, date(date type). Score/projects/id/domain are invisible to kb; the engine supports Filter{key,op eq|in|gte|lte} but the kb_search tool doesn't expose facet filters, so query-catalog.py remains the only structured query tool.
- evidence: pi-agent-dashboard packages/kb/src/frontmatter.ts:142-149, src/types.ts:96-102,144
- from: backend | previous agent note: kb frontmatter facts: authoring/skill concern

## BA-005 [missing] agent-docs drift from template
- target: agent-docs/(general) | src: session:jb-003.json | status: reported-unvalidated
- claim: agent-docs/ mirrors the template
- fact: 68 files copied from the JUDO project template on 2026-03-05; today 59 differ and 6 missing. agent-docs must be static harness-neutral markdown with path parity to template <path>.hbs (excluding domain/); plan adds parity check unblocking template tasks 9.1/9.2. 72 catalog entries rest solely on rackinspect+mlszksz-platform.
- evidence: design.md Context, session 2026-11-03T14:09
- from: backend | previous agent note: process note about template drift

## BA-006 [missing] judo-ng repos carrying their own agent-docs
- target: agent-docs/(general) | src: session:jb-006.json | status: validated
- fact: judo-ng/runtime/judo-runtime-core/* modules (accessmanager, security, dao-rdbms, dao-rdbms-liquibase, dao-rdbms-hsqldb, expression, guice-*, spring-*) have their own agent-docs/ dirs (73 md files total) — source for domain knowledge. Blueprint repo catalog: best-practices frontend 62, backend 74, model 71; agent-docs frontend 16, backend 12, integration-testing 6, e2e-testing 7, deployment 7, model 15, domain 1. judo-ng top-level: models (judo-meta-*), packages, spring, template, runtime.
- evidence: ~/Projects/judo-ng find, judo-blueprint ls, session 2026-11-04T08:42
- from: backend | previous agent note: inventory of judo-ng agent-docs; no doc change

## BA-013 [missing-how-to] JSL editor / IDE tooling (VS Code extension and TextMate bundle)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO models are authored in JSL (.jsl files). Two artifacts provide IDE support: the JUDO JSL VS Code extension (lazy `onLanguage:jsl` activation, registers language id `jsl`, grammar scope `source.jsl`, embeds a Java language server `jsl-standalone`/`jsl-standalone.bat` that runs over LSP stdio, packaged as jsl-language.vsix) and the JSL TextMate bundle (judo-jsl-tmbundle) for VS Code/JetBrains/Sublime, installable in IntelliJ via the TextMate Bundles plugin pointing at the cloned bundle directory with `*.jsl` association. JSL grammar scopes follow TextMate conventions like `storage.types.class.jsl` and `keyword.operator.comparison.jsl`.
- evidence: ['judo-jsl-vscode@85e2e53:package.json:22', 'judo-jsl-vscode@85e2e53:README.md:28', 'judo-jsl-tmbundle@f129e20:pom.xml:50', 'judo-jsl-tmbundle@f129e20:doc/install-idea.md:10']
- from: backend | previous agent note: IDE tooling

## BA-021 [wrong-fact] dao-rdbms skill name prefix inconsistent
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: INSTALL.md uses /judo-dao-rdbms: prefix
- fact: plugin.json manifest uses the judo-runtime: prefix for skill names; the two disagree.
- evidence: session C141
- from: backend | previous agent note: judo-ng internal skill/design docs

## BA-022 [wrong-fact] testkit api-reference.md errors
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: modelName defaults 'exa'; resolveDialect public static; tearDown cleans resources; @Reference/@Inject select targets
- fact: JudoTest.java:44 default is 'example'; resolveDialect is package-private (JudoRuntimeFixture.java:229); tearDown only rolls back an open transaction; ReferenceInjector injects every eligible field and set* method and ignores those annotations.
- evidence: session C149
- from: backend | previous agent note: judo-ng internal skill/design docs

## BA-023 [wrong-fact] submodule-agent-docs design stale
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: agent-docs under src/main/resources; webhook-interceptor.java marked done
- fact: Dispatcher pom copies from ${basedir}/agent-docs (submodule root); file on disk is webhook-interceptor.java.example.
- evidence: session C164
- from: backend | previous agent note: judo-ng internal skill/design docs
## DE-004 [missing-how-to] CLI GraphQL query language and schema inspection
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: `query <model> <Type>` builds GraphQL queries with --select/--where/--limit/--offset where where operators eq, contains, startsWith, endsWith, regex, icontains, istartsWith, iendsWith, iregex, gt, gte, lt, lte; `graphql` runs arbitrary documents with --variables/-o/--schema, and `--schema` exports the GraphQL SDL to .judo-schema.graphql. Collection fields pluralize (EClass->eclasses) and nested reference filtering is AND-combined.
- evidence: ['judo-model-cli@9f6a4bd:src/main/java/hu/blackbelt/judo/cli/commands/QueryCommand.java:390', 'judo-model-cli@9f6a4bd:openspec/specs/graphql-queries/spec.md:7', 'judo-model-cli@9f6a4bd:src/main/java/hu/blackbelt/judo/cli/JudoModelServer.java:752']
- from: deployment | previous agent note: CLI GraphQL query usage belongs to a CLI doc area

## DE-071 [wrong-fact] Community docs: Maven version, antora-lunr
- target: agent-docs/deployment | src: session:jb-013.json | status: reported-unvalidated
- claim: 01_system-requirements.adoc: Maven must start with 3.8 yet uses 3.9.x
- fact: root pom sets <maven>3.9.4</maven> property; generate-site.js requires 'antora-lunr' not in package.json (only @antora/lunr-extension); pom clean-plugin has two <directory> in one <fileset> (second may be ignored).
- evidence: community-documentation@ec8768c, reader C245
- from: deployment | previous agent note: targets community/admin documentation; this doc already uses keycloakAuthPublicUrl and no SAME_USERNAME-as-option claims

## DE-072 [wrong-fact] Admin guide wrong parameter names/defaults
- target: agent-docs/deployment | src: session:jb-013.json | status: reported-unvalidated
- claim: SAME_USERNAME policy; keycloakPublicUrl; mail port default 10025
- fact: SAME_USERNAME not valid; parameter is keycloakAuthPublicUrl; mail port code default 1025. 06_application_metrics.adoc:137 nested try-with-resources both declare `outer` (won't compile; rename inner).
- evidence: session, reader C249
- from: deployment | previous agent note: targets community/admin documentation; this doc already uses keycloakAuthPublicUrl and no SAME_USERNAME-as-option claims

## FR-001 [missing] Other agent-docs topics from knowledge-gaps-report
- target: agent-docs/(general) | src: session:jb-029.json | status: reported-unvalidated
- fact: Topics listed (agent-docs section): binary upload/download two-phase token flow; SYSTEM/non-principal actors exposure and realm; UI model values that break the generator; long-running operations frontend/proxy 503 timeout; creating/upgrading a JUDO project (archetypes, version updater); static navigations and static data; request tracing (exchange id); low-level persistence hooks; API-level tests with ApiClient/Postman; backend CORS filter config; Flutter frontend build (scope-gated).
- evidence: knowledge-gaps-report.md headings lines 117-639 (session 2026-11-09T09:25:04Z)
- from: frontend | previous agent note: index of topics from knowledge-gaps-report; frontend topics handled by their own items, others belong to other areas

## FR-003 [missing-how-to] Binary file upload/download two-phase token flow
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: File upload/download over REST is a two-phase, token-gated protocol: uploadFile first POSTs '<attributePath>/~upload-token' to obtain a token, then POSTs multipart data to the upload path with an X-Token header; downloadFile GETs the download path with ?disposition=inline|attachment plus X-Token and a blob response. The generated fileHandling hook (downloadFile/uploadFile/exportFile/extractFileNameFromToken) wraps this. A developer building custom attachments must understand the token dance and the disposition inline-vs-attachment branch (inline renders in a dialog iframe).
- evidence: ['judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:36', 'judo-ui-typescript-rest-template@3c06fe9:judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:64', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/utilities/file-handling.tsx.hbs:54', 'judo-ui-react-templat
- from: frontend | previous agent note: binary upload/download token flow is REST client / data access behaviour, cross-area

## BA-016 [missing-topic] Automated API-level testing of generated services (Postman / OpenAPI)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated application ships Postman collections (v2.1.0) that exercise the REST API against a running instance (local Karaf on http://localhost:8181), asserting status codes, error codes and response shapes. The service is annotated with swagger-annotations and generation exposes an OpenAPI toggle (ignoreOpenAPI). Developers need a documented workflow for obtaining and iterating on the OpenAPI spec of their generated service and for running/adapting Postman collections, including environment variables that hold signed identifiers ({{...SignedId}}) used in ~set/~add bodies.
- evidence: ['judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:48', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:535', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:596', 'judo-tatami-tests@80e27d28:models/DebateTest/pom.xml:196', 'judo-tatami-tests@80e27d
- from: backend | previous agent note: Postman/OpenAPI testing: integration/e2e area
