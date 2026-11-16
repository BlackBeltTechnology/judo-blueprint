# agent-docs/backend: sweep inventory (181 items)

Each item: id, kind, target, source, status, claim, fact, evidence.

## BA-001 [decision] Open question: known-issue notes in agent-docs vs issue tracker
- target: agent-docs/(general) | src: session:jb-029.json | status: operator-stated
- claim: Should validated platform bugs appear in agent-docs as known issues or only in judo-ng issue trackers?
- fact: Boti's answer: both - short known-issue note in agent-docs that links the judo-ng issue.
- evidence: review-decisions.boti.md, session 2026-11-09T09:20:49Z

## BA-002 [decision] agent-docs owned by judo-blueprint, one-time import, not in skills
- target: agent-docs/(general) | src: session:jb-034.json | status: operator-stated
- claim: JUDO template shipped agent-docs.
- fact: Template deleted agent-docs on develop (5bddd8b, 2026-11-03); judo-blueprint owns them. Import is one-time from 5bddd8b^ (70 non-domain docs, rendered .hbs to static markdown), no sync afterwards. Import/verification steps live only in the change folder, never in skills. A sweep that finds an agent-docs error lists it in its PR body and does not edit agent-docs; any agent-doc change needs an accepted operator-reviewed finding.
- evidence: openspec/changes/restructure-blueprints-for-kb/specs/agent-docs-catalog/spec.md

## BA-003 [mention-only] Customizing the generated Keycloak login theme (FreeMarker FTL)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated project ships a Keycloak theme module (`<model>-theme`, packaged as a zip of `src/main/resources/themes`) whose login pages are FreeMarker templates: `login.ftl` (username/password, remember-me gated on `realm.rememberMe`, forgot-password on `realm.resetPasswordAllowed`, registration/social sections), `register.ftl` (password/`recaptchaRequired` with `${recaptchaSiteKey}`), `error.ftl`, `template.ftl` (registrationLayout macro with nested header/form/info/socialProviders sections), and an empty `footer.ftl` content-macro override point. Styling is in `theme.properties` (parent=base, `kc*` CSS-class keys) and `login.css`. The theme is tested via `test-theme-with-compose.sh` against a dev Keycloak (admin/judo, TEST_USERS realm).
- evidence: ['judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/theme.properties.hbs:1', 'judo-jsl-fullstack-karaf-project-template@d1ddf8d:judo-jsl-fullstack-karaf-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/lo

## BA-004 [missing] kb frontmatter keys: only title/description/aliases/keywords searchable; facets tags,status,author,category,date
- target: agent-docs/(general) | src: session:jb-000.json | status: validated
- claim: Blueprint frontmatter (id, domain, category, score, usage_count, alternative_count, projects, first_seen, last_updated) is assumed queryable
- fact: kb DEFAULT_SEARCHABLE_KEYS = title, description, aliases, keywords; DEFAULT_FACET_KEYS = tags, status, author, category, date(date type). Score/projects/id/domain are invisible to kb; the engine supports Filter{key,op eq|in|gte|lte} but the kb_search tool doesn't expose facet filters, so query-catalog.py remains the only structured query tool.
- evidence: pi-agent-dashboard packages/kb/src/frontmatter.ts:142-149, src/types.ts:96-102,144

## BA-005 [missing] agent-docs drift from template
- target: agent-docs/(general) | src: session:jb-003.json | status: reported-unvalidated
- claim: agent-docs/ mirrors the template
- fact: 68 files copied from the JUDO project template on 2026-03-05; today 59 differ and 6 missing. agent-docs must be static harness-neutral markdown with path parity to template <path>.hbs (excluding domain/); plan adds parity check unblocking template tasks 9.1/9.2. 72 catalog entries rest solely on rackinspect+mlszksz-platform.
- evidence: design.md Context, session 2026-11-03T14:09

## BA-006 [missing] judo-ng repos carrying their own agent-docs
- target: agent-docs/(general) | src: session:jb-006.json | status: validated
- fact: judo-ng/runtime/judo-runtime-core/* modules (accessmanager, security, dao-rdbms, dao-rdbms-liquibase, dao-rdbms-hsqldb, expression, guice-*, spring-*) have their own agent-docs/ dirs (73 md files total) — source for domain knowledge. Blueprint repo catalog: best-practices frontend 62, backend 74, model 71; agent-docs frontend 16, backend 12, integration-testing 6, e2e-testing 7, deployment 7, model 15, domain 1. judo-ng top-level: models (judo-meta-*), packages, spring, template, runtime.
- evidence: ~/Projects/judo-ng find, judo-blueprint ls, session 2026-11-04T08:42

## BA-007 [missing-how-to] CXF / JAX-RS REST customization
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO REST services are exposed through Apache CXF. Developers can (1) add CXF interceptors as OSGi components implementing org.apache.cxf.interceptor.Interceptor with properties judo.model.name and interceptor.direction (in, out or fault) — built-in JAXRSInInterceptor runs at Phase.UNMARSHAL and JAXRSOutInterceptor at Phase.MARSHAL, and ExchangeIdResponseWriter writes the CXF ExchangeID to the HTTP X-Exchange-Id header; (2) add JAX-RS providers as OSGi components annotated @javax.ws.rs.ext.Provider whose bundle must carry the manifest header X-JAXRS-Provider: true; and (3) obtain the shared Jackson ObjectMapper via OSGi filter (&(source=judo-services-jackson-objectmapper)(type=extended)).
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/06_rest_customization.adoc:36', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/06_rest_customization.adoc:18', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/06_rest_customization.adoc:54', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/06_rest_customizati

## BA-008 [missing-how-to] QueryCustomizer builder fields for low-level DAO calls
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: QueryCustomizer is a Lombok @Builder with fields: filter (String, a JQL expression), orderByList (@Singular 'orderBy'), seek, withoutFeatures, mask, parameters and instanceIds, and exposes an orderBy(OrderBy) adder. OrderBy.attribute is @NonNull (EAttribute), so the builder rejects null with NullPointerException. Custom customizers are passed to low-level DAO operations (range/search/count/static operations) when a developer needs control beyond the generated fluent SDK (`).
- evidence: ['judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/DAO.java:626', 'judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/DAO.java:600']

## BA-009 [missing-how-to] Filestore S3/GCS backend configuration and access-URL semantics
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The FileStoreService has filesystem, RDBMS and S3-compatible backends. Beyond the env-var surface (JUDO_PLATFORM_FILESTORE=s3, JUDO_PLATFORM_FILESTORE_S3_BUCKET), the S3/GCS backend component (S3FileStoreService) requires config keys protocol, bucketName, accessKey and secretKey, with endpoint defaulting to empty (AWS; a trailing slash is appended) and region defaulting to us-east-1. Uploads of >=5 MiB use multipart (MULTIPART_THRESHOLD = 5*1024*1024). Crucially, getAccessUrl() returns an internal `<protocol>:<fileId>-<filename>` URL resolved by the OSGi URL stream handler - not a public or signed link - so downloads flow through the Karaf servlet. The S3 backend has no metadata cache: every getMimeType/getFileName/getSize/getCreateTime issues a HEAD request.
- evidence: ['osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:42', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:94', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:153', 'osgi-filestore@937a4ae:filestore-s3/src/main/java/hu/blackbelt/o

## BA-010 [missing-how-to] OpenAPI / Swagger API documentation generation
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated REST module can emit an OpenAPI spec: when the isGenerateOpenApiAnnotations generator parameter (or input variable ignoreOpenAPI=false) is set, generateOpenApiAnnotations becomes true and the swagger-maven-plugin resolves the spec to target/api-documentation-swagger as both openapi.json and openapi.yaml; swagger-annotations 2.2.8 is also added to the Karaf feature. This is the only documented way to produce machine-readable API docs for the generated JAX-RS endpoints.
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/rest/pom.xml.hbs:152', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/karaf-features/src/main/feature/feature.xml.hbs:20']

## BA-011 [missing-how-to] OIDC logout, profile popup, and signed-in gating
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: Authenticated frontend behavior: logout calls signoutRedirect with post_logout_redirect_uri set to the current URL without its hash fragment; the avatar/profile popup (HeaderProfile + ProfilePopup) is generated only when application.authentication is on, and the profile page opens as a dialog when application.profilePage and openInDialog are set. The layout also blocks rendering until principal.__signedIdentifier exists and maps error code AUTHENTICATED_ENTITY_NOT_FOUND to a 'User not found' message.
- evidence: ['judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/Header/HeaderContent/HeaderProfile/index.tsx.hbs:64', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/ProfilePopup/index.tsx.hbs:34', 'judo-ui-react-template@af315252:judo-ui-react/src/main/resources/actor/src/layout/index.tsx.hbs:42', 'judo-ui-react-template@af315252:judo-ui-reac

## BA-012 [missing-how-to] Customizing the JUDO Keycloak auth theme (login/account/email)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO ships a custom Keycloak theme (judo-keycloak) that overrides the stock `keycloak` theme via `parent=base` + `import=common/keycloak` and defines the branded login/account/admin/welcome/email templates as FreeMarker files (login.ftl, template.ftl, welcome/index.ftl). A developer who wants to brand the authentication screens must edit these templates and the theme.properties CSS-class mapping keys (kcButtonClass, kcButtonPrimaryClass, kcInputClass, kcFormCardClass, kcHeaderWrapperClass, kcInputErrorMessageClass), understand the `registrationLayout` macro's nested sections (header/form/info/show-username), and the realm-driven label logic in login.ftl (username/email/usernameOrEmail, rememberMe, resetPasswordAllowed).
- evidence: ['judo-keycloak@e159f55d4b:keycloak/login/theme.properties:1', 'judo-keycloak@e159f55d4b:keycloak/login/theme.properties:34', 'judo-keycloak@e159f55d4b:keycloak/login/template.ftl:42', 'judo-keycloak@e159f55d4b:keycloak/login/login.ftl:100', 'judo-keycloak@e159f55d4b:openspec/specs/login-theme/spec.md:14']

## BA-013 [missing-how-to] JSL editor / IDE tooling (VS Code extension and TextMate bundle)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: JUDO models are authored in JSL (.jsl files). Two artifacts provide IDE support: the JUDO JSL VS Code extension (lazy `onLanguage:jsl` activation, registers language id `jsl`, grammar scope `source.jsl`, embeds a Java language server `jsl-standalone`/`jsl-standalone.bat` that runs over LSP stdio, packaged as jsl-language.vsix) and the JSL TextMate bundle (judo-jsl-tmbundle) for VS Code/JetBrains/Sublime, installable in IntelliJ via the TextMate Bundles plugin pointing at the cloned bundle directory with `*.jsl` association. JSL grammar scopes follow TextMate conventions like `storage.types.class.jsl` and `keyword.operator.comparison.jsl`.
- evidence: ['judo-jsl-vscode@85e2e53:package.json:22', 'judo-jsl-vscode@85e2e53:README.md:28', 'judo-jsl-tmbundle@f129e20:pom.xml:50', 'judo-jsl-tmbundle@f129e20:doc/install-idea.md:10']

## BA-014 [missing-how-to] Local SMTP testing for invitation emails: mailpit + Keycloak realm SMTP
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: User-invitation e-mails are sent by Keycloak, not by the application, so JUDO_PLATFORM_MAIL_SMTP_* only covers app mail. On every Karaf start the Keycloak connector rewrites the DEFAULT realm's SMTP settings from the JUDO_PLATFORM_MAIL_SMTP_* values, so the KEYCLOAK_SMTP_* lines alone do not route invitations. To test invitations locally run a mailpit container (SMTP 1025, web inbox 8025) matching the platform SMTP host/port, then verify the Keycloak realm SMTP points at it.
- evidence: ['rackinspect-sessions-...feature-guard-user-management-by-role: [A!] "No past session set up a mailpit for rackinspect\'s local Karaf. ... The recipe comes from park-here ..."', 'rackinspect-sessions-...feature-guard-user-management-by-role: [A!] "Invitation e-mails: these are sent by Keycloak, not by the app. ... On every Karaf start, the Keycloak connector code rewrites the DEFAULT realm\'s SMT

## BA-015 [missing-pattern] E2E baseline orchestration: prepared DB dump (incl. Keycloak users) built once, parallel stacks on distinct ports
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: For E2E suites the team wanted a reusable prepared dump produced by judo.sh containing all test data and base roles together with Keycloak users (Keycloak shares the backend DB), rebuilt once, and a flow that recreates it when it goes stale. Because cold app start is ~10 minutes, the dump/image must be built once and reused across runs; parallel E2E groups run full stacks on different ports to avoid collisions, and host-machine images are reused.
- evidence: ['rackinspect-sessions-20261103__--Users-gaborflorian-projects-rackinspect--__2026-09-16T20-36-39-237Z_01a0abef-90c4-74f5-9fa9-3fea0b4ecf3a.jsonl : i want to run the test on a mode where we use a prepared dump which created bz the judo.sh and all the test data and base roles are there with kezcloak users (keycloak use the smae db as the backend) so we use the dump as a base start four our test, at

## BA-016 [missing-topic] Automated API-level testing of generated services (Postman / OpenAPI)
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The generated application ships Postman collections (v2.1.0) that exercise the REST API against a running instance (local Karaf on http://localhost:8181), asserting status codes, error codes and response shapes. The service is annotated with swagger-annotations and generation exposes an OpenAPI toggle (ignoreOpenAPI). Developers need a documented workflow for obtaining and iterating on the OpenAPI spec of their generated service and for running/adapting Postman collections, including environment variables that hold signed identifiers ({{...SignedId}}) used in ~set/~add bodies.
- evidence: ['judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:48', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:535', 'judo-tatami-tests@80e27d28:models/CRUDActionsTest/postman/CRUDActionsTest.postman_collection.json:596', 'judo-tatami-tests@80e27d28:models/DebateTest/pom.xml:196', 'judo-tatami-tests@80e27d

## BA-017 [missing-topic] Custom Keycloak login theme development
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The fullstack template ships a generated keycloak-theme Maven module (src/main/resources/themes/keycloak-theme/) containing FreeMarker login pages (login.ftl, register.ftl, error.ftl, template.ftl with the registrationLayout macro), a theme.properties (parent=base, import=common/keycloak, styles=css/login.css), a PatternFly-based login.css, a TEST_USERS test realm (test-users-realm.json, import via --import-realm) and a test-theme-with-compose.sh script that unzips the built <artifactId>-<version>-assets.zip into ./keycloak-themes and starts Keycloak on port 8080. The login theme name must exactly match the realm's loginTheme value ('<lowercase model.name><projectPostfix>-theme').
- evidence: ['judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/template.ftl.hbs', 'judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-application/src/main/resources/keycloak-theme/src/main/resources/themes/keycloak-theme/login/theme.properties.hbs:1', 'judo-e

## BA-018 [missing-topic] Guice provider module generation for generated SDK DAOs
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The guice module of the SDK generator emits one com.google.inject.AbstractModule per model (<Model>DaoModules, e.g. Northwind -> NorthwindDaoModules) with one @Provides method per DAO implementation, static navigation and static data DAO (named provide__<FqName> with dots replaced by __). Each provider takes a generic hu.blackbelt.judo.dao.api.DAO, hu.blackbelt.judo.meta.asm.runtime.AsmModel and hu.blackbelt.judo.dao.api.PayloadValidator and injects them via setDao/setAsmModel/setPayloadValidator.
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-guice/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/guice/GuiceHelper.java:48', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-guice/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/guice/GuiceHelper.java:52', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-guice/src/main/resources/g

## BA-019 [missing-topic] Generating OSGi Declarative Services REST clients from OpenAPI specs
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The openapi-generator-cxf-jaxrs-client-osgi-ds generator (generator name `jaxrs-cxf-client-osgi-ds`) produces a CXF JAX-RS client that is packaged as an OSGi bundle with a Declarative Services activator. From an OpenAPI spec it emits API/model packages plus a `ClientApiServiceActivator` with @ObjectClassDefinition config properties: endPoint (default basePath), log_payload, log_payload_limit (1000), connection_timeout (10000 ms), receive_timeout (15000 ms). Config options: activatorPackage (default org.openapitools.activator), activatorDsConfigurationRequired (false), useGzipFeature, useLoggingFeature; activatorDsConfigurationRequired=true emits configurationPolicy=REQUIRE.
- evidence: ['openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:README.md:158', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:README.md:70', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:src/main/java/hu/blackbelt/openapi/codegen/JavaCXFClientOsgiDsCodegen.java:54', 'openapi-generator-cxf-jaxrs-client-osgi-ds@9feeefa:openspec/specs/codegen/spec.md:76']

## BA-020 [missing-topic] Keycloak-managed user sync: user in Keycloak but missing from DB
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: For a managed actor (HUMAN, managed=true) the runtime bridges Keycloak and the entity store through UserManager/UserManagedWrappedDao: the Keycloak user is the source and the DB row is created/synced via the wrapped DAO (with password policy checks, required actions, and convertPrincipalToActor mapping). Because these two stores can drift, an admin user can exist in Keycloak while its entity row is absent from the database — so invitation/init flows must verify and create the DB-side row, not assume Keycloak membership implies an entity exists.
- evidence: ['rackinspect 2026-10-05 : "the user is not generated in the project when i want to sent the invitation email"', 'rackinspect 2026-10-09 : "check me why the admin users are not created on the db now a local host rackinpect is running the mate is on the keycloak butn ot inthe database"', 'rackinspect 2026-10-09 : "the user in the keycloak but not in the databas"']

## BA-021 [wrong-fact] dao-rdbms skill name prefix inconsistent
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: INSTALL.md uses /judo-dao-rdbms: prefix
- fact: plugin.json manifest uses the judo-runtime: prefix for skill names; the two disagree.
- evidence: session C141

## BA-022 [wrong-fact] testkit api-reference.md errors
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: modelName defaults 'exa'; resolveDialect public static; tearDown cleans resources; @Reference/@Inject select targets
- fact: JudoTest.java:44 default is 'example'; resolveDialect is package-private (JudoRuntimeFixture.java:229); tearDown only rolls back an open transaction; ReferenceInjector injects every eligible field and set* method and ignores those annotations.
- evidence: session C149

## BA-023 [wrong-fact] submodule-agent-docs design stale
- target: agent-docs/(general) | src: session:jb-011.json | status: reported-unvalidated
- claim: agent-docs under src/main/resources; webhook-interceptor.java marked done
- fact: Dispatcher pom copies from ${basedir}/agent-docs (submodule root); file on disk is webhook-interceptor.java.example.
- evidence: session C164

## BA-024 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:283
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ThreadLocalContextHolder.clearContext() clears the thread-local context.
- fact: No clearContext method exists in ThreadLocalContextHolder; the class has only getContextLocal, bindContext and getVariable.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:283

## BA-025 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:277
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: getVariable returns the variable value or null.
- fact: getVariable throws RuntimeException('Could not retrieve contextLocal') when no context is bound on the current thread; null is returned only
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:277

## BA-026 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:38
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: createGeneratorContext takes six parameters (templateLoader, uriResourceResolver, generatorModel, helpers, valueResolvers, contextAccessor).
- fact: createGeneratorContext takes a single CreateGeneratorContextArgument argument.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:38

## BA-027 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:111
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorParameter.extraContextVariables(map) takes a Map<String, Object>.
- fact: extraContextVariables is a Supplier<Map<String, ?>> with a default of ImmutableMap.of().
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:111

## BA-028 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:232
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: public static Collection<Class<?>> collectHelpers(String packageName, ClassLoader classLoader) returns helper classes.
- fact: collectHelpers(Collection<String> acceptedPackages, ClassLoader...) returns Collection<String> of class names; the Class-returning variant i
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:232

## BA-029 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:202
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ChainedURLTemplateLoader.createFromURIs(List<URI> uris, String prefix).
- fact: createFromURIs takes a single Collection<URI> argument; there is no prefix parameter.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:202

## BA-030 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:408
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ContentComparator.areEquivalent(byte[] content1, byte[] content2, String extension).
- fact: ContentComparator has compareNormalized(String filePath, byte[] contentA, byte[] contentB); areEquivalent does not exist.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:408

## BA-031 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:432
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: FileNormalizerRegistry.forExtension(String extension) returns Optional<FileTypeNormalizer>.
- fact: The method is getNormalizer(String extension); forExtension does not exist.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:432

## BA-032 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:448
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: FileNormalizerRegistry.registerPreset(String preset) registers a built-in preset.
- fact: No registerPreset method exists; the registry has register(FileTypeNormalizer normalizer).
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:448

## BA-033 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:189
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorTemplate.templateContext is a List<TemplateSpringELExpression>.
- fact: templateContext is declared as Collection<TemplateSpringELExpression>, initialised to a HashSet.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:189

## BA-034 [wrong-fact] src/main/resources/agent-docs/guides/user-guide.md:60
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: GeneratorModel.loadYamlURL(templateYamlUrl) with a single URL argument.
- fact: loadYamlURL requires (String originalUri, URL yaml, CreateGeneratorContextArgument args).
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/user-guide.md:60

## BA-035 [wrong-fact] src/main/resources/agent-docs/guides/user-guide.md:116
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: A top-level templateContext list in the YAML descriptor defines global variables.
- fact: GeneratorModel has no templateContext property (its fields are name, permission, templates, normalizeContent and fileNormalizers). templateC
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/user-guide.md:116

## BA-036 [wrong-fact] src/main/resources/agent-docs/guides/user-guide.md:222
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: ChainedURLTemplateLoader.createFromURIs(Arrays.asList(overrideUri, baseUri), 'templates').
- fact: createFromURIs takes only Collection<URI>.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/user-guide.md:222

## BA-037 [wrong-fact] src/main/resources/agent-docs/guides/api-reference.md:199
- target: agent-docs/(general) | src: judo-ng-read | status: validated
- claim: createFromURIs(List<URI> uris, String prefix) with 'first has highest priority'.
- fact: The real method is createFromURIs(Collection<URI> uris) with one argument, no prefix. The last URI in the list gets the highest priority.
- evidence: runtime/judo-generator-commons:src/main/resources/agent-docs/guides/api-reference.md:199

## BA-038 [mention-only] Request exchange-ID tracing (X-Exchange-Id header, MDC correlation)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A CXF interceptor pipeline decorates each HTTP request with a UUID exchange id: ExchangeIdDecorator stores it on the CXF Exchange under key 'exchangeId' and publishes it into the SLF4J MDC under key 'RequestExchangeId'; ExchangeIdResponseWriter echoes it back as the X-Exchange-Id response header (including on fault responses). It enables correlating server logs with client requests end-to-end.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-jaxrs-cxf/src/main/java/hu/blackbelt/judo/runtime/core/jaxrs/cxf/interceptors/ExchangeIdDecorator.java:38', 'judo-runtime-core@b34d8ea1:judo-runtime-core-jaxrs-cxf/src/main/java/hu/blackbelt/judo/runtime/core/jaxrs/cxf/interceptors/ExchangeIdDecorator.java:49', 'judo-runtime-core@b34d8ea1:judo-runtime-core-jaxrs-cxf/src/main/java/hu/blackbelt/judo/run

## BA-039 [mention-only] Choice/range retrieval operations (getRangeFor + _GetRangeInput input type)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Transfer actions and relations with a ChoiceModifier generate GET_RANGE range-lookup operations named `getRangeFor<Name>` (immutable, `_`-prefixed on collision). Their input is a synthesized `_GetRangeInput` unmapped transfer object type (named `_GetRangeInput`+Model+Transfer+Name) carrying an `owner` relation and, for mapped reference types, a `queryCustomizer` relation; the output returns the reference transfer type at cardinality 0..*.
- evidence: ['judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/action/relationGetRangeReferenceBehaviour.etl:40', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/action/relationGetRangeReferenceBehaviour.etl:214', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/java/hu/blackbelt/judo/tatami/jsl/jsl2psm/zeta/

## BA-040 [mention-only] Running Liquibase changelogs from OSGi bundles (LiquibaseExecutor)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: osgi-liquibase exposes a LiquibaseExecutor service with executeLiquibaseScript(Connection, scriptPathInBundle, Bundle) and an overload taking a Map<String,Object> of changelog parameters. DefaultLiquibaseExecutor is an immediate DS component that swaps the thread-context classloader, enters a Liquibase Scope with the Slf4jLogService, resolves changelog resources via BundleResourceAccessor, and applies parameters via setChangeLogParameter before update. Only LiquibaseException is rethrown; any other exception is swallowed so the caller sees success. The SPI logging service Slf4jLogService has default priority 5, overridable via system property hu.blackbelt.osgi.liquibase.logging.Slf4jLogService.priority.
- evidence: ['osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/LiquibaseExecutor.java:38', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/LiquibaseExecutor.java:48', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/impl/DefaultLiquibaseExecutor.java:99', 'osgi-liquibase@54cddcd:src/main/java/hu/blackbelt/osgi/liquibase/logging/Slf4jLogService.java:35']

## BA-041 [mention-only] JUDO list query without seek returns all rows
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A simple JUDO list call without an explicit seek/pagination returns all matching rows; pagination is an opt-in feature (the runtime has a separate seekBuilder). For small per-user datasets (e.g. 5–20 assigned jobsheets) a full pull without seek is fine, and there is no built-in truncation to worry about.
- evidence: ['judo-cli-sessions 2026-08-05T13-50 : [U] "#3 — JUDO list pagination, explained simply: SImple list call withouth seek will return all row i think"', "judo-cli-sessions 2026-08-05T13-50 : [DIG>] grep -rn 'seek' ~/.m2/repository/hu/blackbelt/judo/runtime ... seekBuilder_from_query_customizer"]

## BA-042 [mention-only] required="true" model attribute exposes a plain getter (no Optional/null-guard)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: For a model attribute declared `required="true"`, the generated service input/transfer class exposes a plain non-`Optional` getter (e.g. `Boolean getMinimumOfferPriceEnabled()`), so a null read means the caller omitted the field - not that it is a valid empty value. You read it directly and rely on the model-enforced required contract instead of adding Java-side null-guard workarounds.
- evidence: ["rackinspect 2026-05-06T18-58 session : [U] // Read the per-offer minimum-price toggle from the input. The model attribute is required with default=true so the SDK exposes a plain Boolean getter; null means the caller did not supply the field, in which case we fall through to the entity attribute's own default=true on create.", 'rackinspect 2026-05-06T18-58 session : [A!] Since OfferDetailsUpdate

## BA-043 [mention-only] Business error TO: both message and location should be i18n-localized
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A modeled business-error transfer object (e.g. FaultRegistryUploadError) carries both a `message` and a `location`; for user-facing upload errors both fields should be i18n-aware, with the backend language deciding the active locale. Error services should surface a localized, locatable error TO (with local-id fields) instead of a raw exception so the client (e.g. a mobile/voice app) can render the translated message at the offending location.
- evidence: ['rackinspect 2026-06-11T14:19 : [U] message should be i18n aware, location also should be i28n aware', 'rackinspect 2026-06-11T14:19 : [U] backend laguage should be used to decide, message should be i18n aware, location also should be i28n aware', 'rackinspect 2026-05-17T16:33 : [U] createBusinessErrorException should be backed localiyed']

## BA-044 [missing] Backend generator fragment override layouts
- target: agent-docs/backend | src: session:jb-001.json | status: reported-unvalidated
- claim: n/a
- fact: Generator scans two equivalent fragment-file layouts (project may mix): Layout A sibling: application/karaf-features/src/main/feature/feature.xml.<slot>.fragment.hbs and application/<module>/pom.xml.<slot>.fragment.hbs; second layout also supported. Slots: feature.xml: extra-repositories, extra-bundles, model-bundles; each pom.xml: project-definition, properties-definition, extra-plugin-management, extra-plugins, extra-dependencies; app-root pom: extra-modules. Slot names come from '<!-- To define create ...fragment.hbs file -->' markers. Analyzer should glob *.fragment.hbs.
- evidence: cciu-model-patterns .claude/agents/judo-backend-analyzer.md

## BA-045 [missing] Where JUDO project custom code lives (rackinspect conventions)
- target: agent-docs/backend | src: session:jb-005.json | status: reported-unvalidated
- fact: Interceptors: application/interceptors/src, Java classes `implements OperationCallInterceptor` (66; methods getName, ignoreDecoratedCall, preCall, postCall(EOperation, parameterPayload, returnPayload)) annotated `@Component(property={"judo.model.name=<model>"})` or with service=OperationCallInterceptor.class. Guards: `implements WriteGuard` (11; permitted() -> Set<ActorRole>, operations() -> List<String>, preCall). Custom backend operation code in application/app/src/main/java/.... Custom frontend: application/frontend-react/<app>/src/custom/ (application-customizer.tsx registers ~275 register*Hook and ~63 register*CustomImplementation calls, matched to pages via generated interface keys like KEY *_ACTIONS_HOOK; hooks/ dirs ViewEditActionHooks, FormActionsHooks, TableRowHighlightingHooks, containers, custom-implementations; components/). Generator overrides: application/frontend-react/generator-overrides/ui-react/actor/public/... (e.g. i18n/application_default_extra.fragment.hbs).
- evidence: Rackinspect/rackinspect@3954a (session 2026-11-03T15:10:08-15:10:27, agent git ls-files)

## BA-046 [missing] Custom operation implementations map to model operations via interface path
- target: agent-docs/backend | src: session:jb-006.json | status: reported-unvalidated
- fact: Each ...CustomImplementation.java implements an interface `...operation.<model>.<path>.<Op>`; that path names the model operation. Interceptors (66 OperationCallInterceptor, 11 WriteGuard with allowed roles + operations() list) map to operations via operations() lists. Frontend: 856 generated customization.ts files declare hook interfaces; application-customizer.tsx in src/custom registers ~370 hooks.
- evidence: rackinspect@3954ae1; session 2026-11-03 agent

## BA-047 [missing] Optimistic lock only on meta UPDATE
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Doc describes optimistic lock without saying where
- fact: The VERSION predicate exists only in the meta UPDATE (line 148); the attribute UPDATE (lines 176-178) has no version check.
- evidence: UpdateStatementExecutor.java:148,176-178, session C138

## BA-048 [missing] Keycloak defaults and qualifier count
- target: agent-docs/backend | src: session:jb-011.json | status: validated
- claim: DOX row says 21 qualifiers
- fact: 22 qualifiers (JudoKeycloakModuleConfiguration lines 17-143); keycloakServerUrl default http://localhost:8080/auth (line 17), keycloakAdminPassword default 'judo' (line 26).
- evidence: session C147 validation

## BA-049 [missing] REST operation URL suffixes and response DTO metadata
- target: agent-docs/backend | src: session:jb-020.json | status: reported-unvalidated
- fact: REST operation path suffixes: ~create, ~list, ~range, ~upload-token, etc. Response DTO metadata fields: __identifier, __signedIdentifier, __version, __deleteable, __entityType, __referenceId. Wire conversion: enums as ordinals, binaries as filestore tokens.
- evidence: gaps P30-03, P30-04, P16-05

## BA-050 [missing] Query-customizer filter operator codes and query-mask wire syntax
- target: agent-docs/backend | src: session:jb-020.json | status: reported-unvalidated
- fact: Document filter operator codes and query mask wire syntax; classes QueryMaskStringParser, error INVALID_QUERY_MASK.
- evidence: gap P16-08

## BA-051 [missing] Platform EXPORT operation and Excel Export SPI
- target: agent-docs/backend | src: session:jb-020.json | status: reported-unvalidated
- fact: Platform has an EXPORT operation and Excel Export SPI: JxlsExport, UnsupportedExportImpl, bound in JudoDefaultModule.
- evidence: gap P16-03

## BA-052 [missing] BasicApplication configuration keys and deferred startup
- target: agent-docs/backend | src: session:jb-020.json | status: reported-unvalidated
- fact: BasicApplication config keys (e.g. jaxrs.resource.components) and deferred startup behaviour need documenting.
- evidence: gap P11-02

## BA-053 [missing] Top gaps: platform behaviour absent from agent-docs
- target: agent-docs/backend | src: session:jb-021.json | status: reported-unvalidated
- claim: Catalog lacks these topics entirely
- fact: Missing: signed identifiers (change on every update, cannot be minted, need a stable secret), optimistic locking, REST contract, upload-token flow, which operations interceptors fire on, time zones; no JQL function reference and no JCL reference; UI-model values that break the generator; surprising DAO calls; production config: MUI license, Jasypt ENC() secrets, Keycloak login theme, S3/GCS filestore settings, CORS, local mail testing.
- evidence: session 2026-11-06T09:39:57, agent (knowledge-gaps-report.md)

## BA-054 [missing] Dispatcher refuses operations on immutable bound instances
- target: agent-docs/backend | src: session:jb-029.json | status: reported-unvalidated
- fact: The JUDO dispatcher signs bound-instance identifiers and carries an immutable flag inside the signed identifier; operations on immutable bound instances throw AccessDeniedException (S05-01).
- evidence: knowledge-gaps-report.md, session 2026-11-09T09:28:37Z

## BA-055 [missing] Validation message interpolation and localization pipeline
- target: agent-docs/backend | src: session:jb-029.json | status: reported-unvalidated
- fact: JUDO delegates bean validation to a Hibernate Validator OSGi component whose MessageInterpolator resolves messages at runtime: I18nService.getTemplate(message) returns the localized template (raw message used if null), then parameter tokens are interpolated (P29-03).
- evidence: knowledge-gaps-report.md, session 2026-11-09T09:28:37Z

## BA-056 [missing] Relation setter set<Relation> needs a value; use unset<Relation> to clear
- target: agent-docs/backend | src: session:jb-030.json | status: validated
- claim: Report claimed: generated relation setters NPE on null relatedObject
- fact: Only single-relation set<Relation>(object, relatedObject) calls relatedObject.identifier() without null check (fragment.dao.single.relation.implementation.mapped.java.hbs:193). Clearing is via unset<Relation>(object) (line 202, generated when unset allowed). add/remove on multi relations call identifier() per element so null elements fail. This is by-design: null/absent/empty are distinct in JUDO; document 'set needs a value, use unset', not 'setters throw on null'.
- evidence: template__judo-psm-generator-sdk-core/.../fragment.dao.single.relation.implementation.mapped.java.hbs:193,202

## BA-057 [missing] BooleanFilter has no isUndefined; use filterBy(String customFilter) with JQL !isUndefined()
- target: agent-docs/backend | src: session:jb-030.json | status: validated
- claim: 'No is-unset filter for nullable booleans; query cannot be expressed'
- fact: Typed BooleanFilter only has isTrue() ({0}) and isFalse() ((not {0})) (judo-sdk-common BooleanFilter.java/BooleanOperation.java). Escape hatch: query builder filterBy(String customFilter) takes raw JQL, which has !isUndefined()/!isDefined(). Boolean is three-state: absent/null/value.
- evidence: runtime__judo-sdk-common/.../query/BooleanFilter.java; fragment.querycustomizer.builder.java.hbs:45

## BA-058 [missing] Absent vs null vs empty are distinct states in JUDO generated API
- target: agent-docs/backend | src: session:jb-030.json | status: operator-stated
- claim: Reference for generated getter semantics
- fact: Generated getters depend on required: required=true -> plain type getter (Boolean getMinimumOfferPriceEnabled()), where null means caller omitted the field (error); required=false -> Optional<T> getter (Optional<FileType> getReviewReportMarkdownTemplate()). DTO getters check containsKey, so key-missing vs present-null differ. Null is not empty; empty is a value.
- evidence: dto.java.hbs:256; operator 2026-11-09T12:18

## BA-059 [missing] Static (unmapped) data accessors: selectValue()/query()/selectOne()
- target: agent-docs/backend | src: session:jb-030.json | status: operator-stated
- claim: Unmapped attributes/relations read like normal getters
- fact: Unmapped data comes via generated static-data DAO interfaces: selectValue() (or selectValue(param) if the query has a parameter) returns attribute primitive type; query() for collection navigation, selectOne() for single. Operator: 'very important'.
- evidence: session part 30, operator 2026-11-09T12:18

## BA-060 [missing] Payload typed map API
- target: agent-docs/backend | src: session:jb-030.json | status: operator-stated
- claim: Payload is just a Map
- fact: Payload is Map<String,Object> with static factories asPayload(map), map(k1,v1,...) overloads for 1-20 pairs, map(Entry...), entry, and typed accessors getAs(Class<T>,String), getAsPayload(String), getAsCollectionPayload(String). Operator: 'great find'.
- evidence: session part 30, operator 2026-11-09T12:18

## BA-061 [missing] CRUD only on mapped, non-abstract transfer objects
- target: agent-docs/backend | src: session:jb-030.json | status: operator-stated
- claim: Unmapped/abstract types lack create etc.
- fact: Generated DAO interface emits create/createAll (with/without Mask), getById/existsById/getAll/countAll/delete, query() and per-relation create/set/unset/add/remove/range only when self.isMapped (plus relation allowed-operation flags, abstract excluded). Operator: 'important'.
- evidence: session part 30

## BA-062 [missing] Custom operation must declare <faults> or SDK lacks throws clause
- target: agent-docs/backend | src: session:jb-032.json | status: reported-unvalidated
- claim: Docs have zero hits for faults/throws
- fact: A custom-implemented operation needs an explicit fault parameter (<faults> targeting the fault TO) in the ESM model; without it the generated SDK omits `throws BusinessErrorException` and Maven fails with 'not compatible with throws clause'. Rules were only discoverable from generated SDK source. Also: operation whose output DTO matches the action-container view root breaks frontend generator (nonexistent *OutputView); fix by dropping output / making void.
- evidence: judo-blueprint/target/gap-mining/out/S09.json:5-14,21; S02.json:25-39

## BA-063 [missing] Interceptors cannot throw modeled faults; wrap in InterceptorCallBusinessException
- target: agent-docs/backend | src: session:jb-032.json | status: validated
- claim: Interceptors can throw business faults
- fact: Interceptors throw ValidationException (field rule, location = attribute name), InterceptorCallBusinessException(type, code, Map.of("message",..), null, locale) for permission/business refusals, never BusinessErrorException/GenericOperationErrorException; caught BusinessErrorException from services is rethrown as IBCE (ElementFaultUpdateInterceptor:82, ErrorQualificationInstanceDeleteInterceptor:110, RegistryHeaderUpdateInterceptor:69). WriteGuardSupport.requirePermitted uses ERROR_CODE=MASTER_DATA_WRITE_FORBIDDEN. Runtime turns IBCE into a _fault payload, DefaultDispatcher.java:764 converts to BusinessException. Rackinspect passes the interceptor/guard name as `type`, which matches no frontend translation; recommended: put the fault FQN as type and code+message in details so generated fault dialog works.
- evidence: Rackinspect:interceptors/.../access/WriteGuardSupport.java:32,141; judo-runtime-core DefaultDispatcher.java:764

## BA-064 [missing] OperationCallInterceptors do not fire on custom/mapped operations
- target: agent-docs/backend | src: session:jb-032.json | status: validated
- claim: Interceptors/write guards protect all operations
- fact: Interceptors (incl. write guards) fire only for behaviour operations (CRUD/list/refresh/range/reference). Custom and MAPPED operations (User.toggleActive, createUser, resendInvitation, changeRoles) bypass them; guards must sit inside each *CustomImplementation. Hiding UI buttons does not protect either.
- evidence: gap-mining out/S26.json:9

## BA-065 [missing] Interceptor combination semantics, range interceptors as security boundary
- target: agent-docs/backend | src: session:jb-032.json | status: reported-unvalidated
- claim: n/a
- fact: Multiple OperationCallInterceptors on one operation: each preCall receives original payload, sees others' in-place payload mutations, return value accumulated last-non-null-wins. Range interceptors only fire on _getRangeReference* ops (not plain list/query ops like Rack/availableRackElements/~list); they are the security boundary for rangeType=ANY lean TOs since read-only attrs don't stop enumeration (incl. AI actor). Model min/max bounds are UI-only and don't reject server updates.
- evidence: judo-doc-problems.md Part B excerpts in session

## BA-066 [missing] Known generated DAO bugs: query<Attribute>() on enum, derived attribute via inherited member missing JOIN
- target: agent-docs/backend | src: session:jb-032.json | status: reported-unvalidated
- claim: n/a
- fact: query<Attribute>() on an enumeration attribute always throws (enum ordinal/cast bug; workaround read via DTO or <Enum>.getByOrdinal; fix: apply ordinal conversion in query fragment). A derived attribute navigating through an inherited member produces a missing JOIN. Absent/null/empty: set<Relation> needs an object and unset clears; filter 'not set' with JQL !isUndefined(); getters follow `required`. Full CRUD DAO only generated for mapped non-abstract types.
- evidence: session 2026-11-09T13:37, agent doc update; Rackinspect 24afac9 (enum-vs-ordinal bug in OperationCallInterceptor)

## BA-067 [missing] Enum query<Attribute>() always throws; derived attribute via inherited member lacks JOIN
- target: agent-docs/backend | src: session:sweep-012.json | status: reported-unvalidated
- claim: (n/a)
- fact: Known bugs in generated DAO: query<Attribute>() on enumeration attribute throws (ordinal cast, workaround read via DTO or <Enum>.getByOrdinal); derived attribute navigating through inherited member produces query missing JOIN. Set<Relation>(null) semantics corrected: set needs object, unset clears; filter 'not set' via JQL !isUndefined(); CRUD only on mapped non-abstract types.
- evidence: judo-doc-problems.md Topic 1 rewrite, session 13:37

## BA-068 [missing-how-to] Custom JQL variable providers and built-in categories
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JQL getVariable('CATEGORY','key') resolves request-scoped variables from platform categories SYSTEM, ENVIRONMENT, REQUEST, ACTOR, PRINCIPAL and SEQUENCE. Developers can register NEW variable providers as OSGi components with property judo.environment-variable-provider=true plus a category property; a provider with a key must be registered as java.util.function.Supplier, one without a key as Function; providers that depend on request context must set cacheable=false. SYSTEM shortcuts are current_date, current_timestamp, current_time (Date!now(), Timestamp!now(), Time!now()). Java operations resolve variables via hu.blackbelt.judo.dispatcher.api.VariableResolver.resolve(Integer.class,'SYSTEM','random').
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/02_jql_variables.adoc:60', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/02_jql_variables.adoc:63', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/02_jql_variables.adoc:51', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/02_jql_variables.adoc:27', 'docume

## BA-069 [missing-how-to] Custom Sequence SPI
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Application-generated identifiers can come from custom Sequence implementations: an OSGi component implementing hu.blackbelt.judo.dispatcher.api.Sequence (methods getNextValue(String sequenceName), getCurrentValue(String sequenceName)) registered with the property Sequence.TYPE_KEY; the default uses database sequences. A component example uses ConfigurationPolicy.REQUIRE + @Designate(ocd = TransientSequence.Config.class) with start (default 1L) and increment (default 1L) attributes, configured via KARAF_HOME/etc/sample.TransientSequence.cfg. The platform parameter sequenceType selects rdbms (default) or transient; transient sequences are not supported on multi-node deployments. Sequences may have gaps (rolled-back transaction values are not reused).
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/07_custom_sequence.adoc:12', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/07_custom_sequence.adoc:56', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/07_custom_sequence.adoc:37', 'documentation@3eec62f:docs/modules/ROOT/pages/administrator-guide/platform_parameters/07_other.ado

## BA-070 [missing-how-to] GenModel generator configuration and output control
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The MWE2/Xtext generator is configured by a RuntimeModelGeneratorConfig: resolveModelName and resolveModelVersion (when blank, the generated code exposes name/version as settable fields; when set, getName()/getVersion() return the literal value and no setter is generated), genModelNames (empty list = generate every GenModel), and printXmlOnError (when true the generated ValidationException message appends asString()). The MWE2 workflow defaults javaPath=src and javaGenPath=src-gen, runs a DirectoryCleaner that deletes javaGenPath before each run, splits a 'gen-once' outlet into javaPath, and requires modelDir to be supplied by the caller.
- evidence: ['judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/generator/runtimemodel/templates/RuntimeModel.xtend:14', 'judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/generator/runtimemodel/engine/RuntimeModelGeneratorConfig.xtend:10', 'judo-genmodel-generator@2c69d4c:runtimemodel/src/hu/blackbelt/judo/eclipse/emf/genmodel/genera

## BA-071 [missing-how-to] Runtime tuning system properties (EsmModelCacheExpiration, templateDebug)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Two JVM system properties control model/engine behaviour: EsmModelCacheExpiration (seconds, default 5) sets the expireAfterAccess window of the per-ResourceSet EsmModelCache LoadingCache; the templateDebug property enables template debugging (TEMPLATE_DEBUG) in the generator context.
- evidence: ['judo-meta-esm@65b02f94:model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmModelCache.java:128', 'judo-meta-esm@65b02f94:generator-engine/src/main/java/hu/blackbelt/judo/meta/esm/generator/engine/EsmGenerator.java:59']

## BA-072 [missing-how-to] JSL error declarations and transfer action throws clause
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Errors are declared as `error Name { field <Primitive> <name> [default:<expr>] [required]; ... }` (body optional; a body may include an `event initialize` member). A transfer action declares the errors it can throw with a `throws ErrA, ErrB` clause listing ErrorDeclaration names, on syntax `action <Output|void> name(<TransferType> <paramName> [choices:...]) [throws ...]` with modifiers enabled/static/update/delete. Errors are used through the Java API.
- evidence: ['judo-meta-jsl@b7a5245b:model/src/main/java/hu/blackbelt/judo/meta/jsl/JslDsl.xtext:194', 'judo-meta-jsl@b7a5245b:model/src/main/java/hu/blackbelt/judo/meta/jsl/JslDsl.xtext:195', 'judo-meta-jsl@b7a5245b:model/src/main/java/hu/blackbelt/judo/meta/jsl/JslDsl.xtext:705', 'judo-meta-jsl@b7a5245b:model/src/main/java/hu/blackbelt/judo/meta/jsl/JslDsl.xtext:709', 'judo-meta-jsl@b7a5245b:model/src/main/

## BA-073 [missing-how-to] Bound operation implementation rules (stateful and parameter compatibility)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A bound operation binding to an entity operation must keep parameters compatible with every inherited operation of the same name (psmUtils.parametersAreCompatible); overriding an inherited operation must keep parameters compatible. An implementation of an inherited abstract operation must set implementation.stateful = true, and the stateful flag must equal the flag of every overloaded operation that has an implementation. Abstract operations may have no implementation, and an abstract bound operation must not override a non-abstract inherited operation.
- evidence: ['judo-meta-psm@101fe64:model/src/main/epsilon/validations/data/boundOperation.evl:20', 'judo-meta-psm@101fe64:model/src/main/epsilon/validations/data/boundOperation.evl:28', 'judo-meta-psm@101fe64:model/src/main/epsilon/validations/data/boundOperation.evl:34']

## BA-074 [missing-how-to] BasicApplication configuration keys and deferred startup behaviour
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: BasicApplication is an OSGi DS component implementing javax.ws.rs.core.Application, configured by a factory configuration. A: 'jaxrs.resource.classes' (comma-separated FQNs, loaded with Class.forName; load failures are logged and skipped) and 'jaxrs.resource.components' (an OSGi LDAP filter over resource services; add/remove of a matching service updates a __lastChangedResources marker that triggers the application to restart). Resource changes are signalled by writing __lastChangedResources (System.currentTimeMillis()) into the application's own factory configuration, which ApplicationStore/CxfServerManager use to decide on updates.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/application/BasicApplication.java:180', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/application/BasicApplication.java:205', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/application/BasicApplication.java:238']

## BA-075 [missing-how-to] Registering custom JAX-RS providers and the X-JAXRS-Provider contract
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Custom JAX-RS providers (a service whose class is annotated @Provider) are only tracked by SharedProviderStore if the bundle's manifest header X-JAXRS-Provider is true. Providers without an 'applications.filter' property are global (applied to every application); with one, they are shared only with the Application services matching that LDAP filter. Applications also get class-based providers from 'jaxrs.provider.classes' and component-based providers listed in 'jaxrs.provider.components' (each name used as a Configuration Admin factory PID). Providers generated by ApplicationStore are tagged __generated.by and ignored by SharedProviderStore; the 'application.id' property is reserved.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/SharedProviderStore.java:96', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/SharedProviderStore.java:115', 'cxf-jaxrs-application-manager@9d3737e:pom.xml:165', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/ApplicationStore.java:265']

## BA-076 [missing-how-to] Jackson JSON provider configuration and date parameter conversion
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JacksonProvider builds a CXF JacksonJaxbJsonProvider from configuration keys JacksonProvider.SerializationFeature.<NAME> and JacksonProvider.DeserializationFeature.<NAME> (Boolean.parseBoolean; unknown enum names are logged and skipped), and JacksonProvider.ObjectMapper.modules (comma-separated Jackson Module class names). Defaults applied before config: INDENT_OUTPUT false, WRITE_DATES_AS_TIMESTAMPS false, FAIL_ON_UNKNOWN_PROPERTIES false. An optional GREEDY ObjectMapper service reference binds any registry mapper (e.g. from ExtendedObjectMapperProvider, which registers an ObjectMapper with findAndRegisterModules + ParameterNames/Jdk8/JavaTime/JSR353 modules and NON_NULL inclusion). ISO8601DateParamHandler converts java.util.Date request parameters using the config key ISO8601DateParamHandler.DATE_FORMAT (default yyyy-MM-dd); it only converts the exact java.util.Date type and shares a non-thread-safe SimpleDateFormat.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/providers/JacksonProvider.java:68', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/providers/JacksonProvider.java:84', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/providers/ExtendedObjectMapperProvider.java:44', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackb

## BA-077 [missing-how-to] CxfContext / CXF bus and interceptor wiring for applications
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: CxfContext is a DS component (factory configuration) that creates a CXF Bus with a required 'busId' (throws NullPointerException if unset; the value becomes the Bus service id), optional IN/OUT/FAULT interceptor trackers driven by LDAP filter fragments 'interceptors_in_components', 'interceptors_out_components', 'interceptors_fault_components' (each tracker filter is (&(objectClass=org.apache.cxf.interceptor.Interceptor)<fragment>)), and flags skipDefaultJsonProviderRegistration, wadlServiceDescriptionAvailable, metrics_enabled, logging_enabled. CxfServerManager always creates a default CxfContext with busId DEFAULT_CXF_BUS_FOR_JAXRS_APPLICATIONS; an application selects its context via the cxf.context property (BasicApplication.CONTEXT_PROPERTY_KEY) whose bus and interceptors are applied to the server factory.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/CxfContext.java:117', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/CxfContext.java:312', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/CxfServerManager.java:91', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/CxfServerManager.java:193']

## BA-078 [missing-how-to] Exchange-id request/response correlation for log tracing
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Two built-in CXF interceptors provide per-request correlation: ExchangeIdDecorator (IN, Phase.RECEIVE) assigns a UUID to each Exchange under the 'exchangeId' key and puts it into the SLF4J MDC under key 'RequestExchangeId'; ExchangeIdResponseWriter (OUT, Phase.POST_LOGICAL) writes that ID into the 'X-Exchange-Id' response header, and handleFault delegates to handleMessage so error responses carry the header too. The exchange ID is the same value used by the CXF logging feature.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/interceptors/ExchangeIdDecorator.java:42', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/interceptors/ExchangeIdDecorator.java:53', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/interceptors/ExchangeIdResponseWriter.java:42', 'cxf-jaxrs-application-manager@9d3737e:src/main/j

## BA-079 [missing-how-to] Extending expression variable resolver categories (VariableResolverManager)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The runtime registers expression variable providers via VariableResolverManager.registerFunction(category, provider, ...) and registerSupplier for SYSTEM/current_date, current_time, current_timestamp, and categories USER (access-token), ACTOR, ENVIRONMENT, PRINCIPAL, REQUEST, SEQUENCE. A developer can register custom categories/functions this way for use in model expressions via !getVariable(category, name).
- evidence: ['judo-platform@2d22cf41:judo-platform-services/judo-services-dispatcher-osgi/src/main/java/hu/blackbelt/judo/services/dispatcher/osgi/component/DefaultAccessTokenVariableResolverComponent.java:46', 'judo-platform@2d22cf41:judo-platform-services/judo-services-dispatcher-osgi/src/main/java/hu/blackbelt/judo/services/dispatcher/osgi/component/DefaultCurrentDateVariableResolverComponent.java:62', 'ju

## BA-080 [missing-how-to] Optimistic locking and __version semantics
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JUDO's RDBMS DAO implements optimistic locking through the reserved __version payload key. The version check runs ONLY when the update payload contains __version: it must equal the original __version or UpdatePayloadDaoProcessor throws IllegalArgumentException 'Outdated instance to update'; if __version is absent from the update payload, no check is made. At the executor level, the VERSION predicate is added only to the meta UPDATE (WHERE ID AND VERSION = :__version), and a stale version fails the checkState 'There is illegal state, no records updated' rather than silently updating nothing. A developer must know that omitting __version silently disables the optimistic-lock guard.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:147', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/executors/UpdateStatementExecutor.java:148', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/jud

## BA-081 [missing-how-to] Optimistic locking defaults and stale-version errors
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The RDBMS runtime hardwires optimistic locking ON (optimisticLockEnabled=true). Updates compare the incoming payload's __version against the stored row: a stale version makes UpdatePayloadDaoProcessor throw IllegalArgumentException 'Outdated instance to update' (only when optimistic locking is enabled and the payload carries a version). Inserts set version=1. Developers must therefore manage the __version field (echo it back, treat it as a concurrency token) and handle the stale-update error in clients.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-spring/src/main/java/hu/blackbelt/judo/runtime/core/spring/JudoDefaultSpringConfiguration.java:213', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:148', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/

## BA-082 [missing-how-to] REST date parameters are parsed as yyyy-MM-dd
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JAX-RS request query/path parameters of type java.util.Date are handled by ISO8601DateParamHandler, which parses and formats them strictly with the SimpleDateFormat pattern yyyy-MM-dd (no time component); a parse failure throws IllegalArgumentException 'Invalid date parameter: ...'. Other parameter types are untouched.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-jaxrs/src/main/java/hu/blackbelt/judo/runtime/core/jaxrs/providers/ISO8601DateParamHandler.java:44', 'judo-runtime-core@b34d8ea1:judo-runtime-core-jaxrs/src/main/java/hu/blackbelt/judo/runtime/core/jaxrs/providers/ISO8601DateParamHandler.java:66']

## BA-083 [missing-how-to] Embedding the ESM→UI transformation programmatically (Esm2Ui API)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The transformation can be invoked from Java via `Esm2Ui.executeEsm2UiTransformation(Esm2UiParameter)` built with `esm2UiParameter()` (defaults: transformationMode ETL, parallel=false, applicationType "default", applicationColumns 12, useCache=true), or as a workflow work unit `Esm2UiWork` / `Esm2UiWorkParameter` run inside a `TransformationContext`. `calculateEsm2UiTransformationScriptURI()` resolves the script root from jar/bundle/directory sources; ETL runs `esmToUi.etl` once per ActorType with context vars `actorType/esmUtils/uiUtils/applicationType/applicationColumns`. A developer embedding generation in custom tooling needs this API surface.
- evidence: ['judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2Ui.java:109', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2Ui.java:63', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2UiWork.java:46', 'judo-tatami-client@c0d1a6a6e:judo-tatami-esm2ui/src/main/

## BA-084 [missing-how-to] Transformation mode switching (ETL vs ZETA vs DUAL)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The tatami-core transformation engine can run in ETL (Epsilon), ZETA (Java), or DUAL (run both and compare) modes, selected via the `judo.transformation.mode` system property (e.g. `-Djudo.transformation.mode=ETL`). The default is ZETA since the mode flip; an explicit `transformationMode(TransformationMode.ETL)` work parameter overrides on a per-step basis, and DUAL runs both engines to compare output. A developer must know how to choose and pass the mode when running a model build.
- evidence: ['judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationMode.java:86', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationMode.java:122', 'judo-tatami-core@a81a4bf0:openspec/changes/change-default-transformation-mode/proposal.md:107']

## BA-085 [missing-how-to] Composable workflow engine API (Sequential/Parallel/Conditional/Repeat flows)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The tatami-core workflow engine composes transformation steps into flows through builders: `WorkFlowEngineBuilder.aNewWorkFlowEngine().build()`, `SequentialFlow.Builder.aNewSequentialFlow()`, `ParallelFlow`, `ConditionalFlow.Builder.aNewConditionalFlow().execute(w1).when(WorkReportPredicate.COMPLETED).then(w2).otherwise(w3)`, and `RepeatFlow` with `.repeat(work).times(n)`/`.until(...)`. Work flows nest (WorkFlow extends Work), the name must be unique per workflow, and each Work must catch exceptions and report WorkStatus.FAILED.
- evidence: ['judo-tatami-core@a81a4bf0:README.md:318', 'judo-tatami-core@a81a4bf0:documentation/workflow.md:156', 'judo-tatami-core@a81a4bf0:documentation/workflow.md:238', 'judo-tatami-core@a81a4bf0:AGENTS.md:161']

## BA-086 [missing-how-to] Transformation trace service (navigating the model trace chain)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: TransformationTraceService is an OSGi service that registers TransformationTrace objects per model name and lets callers navigate the transformation chain in both directions from a single EObject: ascendants/descendants via `getAscendantsOfInstanceByModelType`, `getRootAscendantsOfInstance`, and `getTraceEntriesForInstance(modelName, instance)` (multi-source, carrying ruleName/discriminator). Element identity is by resource URI + URI fragment, and queries throw IllegalArgumentException when the model name was never registered.
- evidence: ['judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceService.java:195', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceService.java:135', 'judo-tatami-core@a81a4bf0:src/main/java/hu/blackbelt/judo/tatami/core/TransformationTraceServiceImpl.java:286']

## BA-087 [missing-how-to] Runtime validation-message interpolation and localization (Hibernate MessageInterpolator pipeline)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JUDO delegates bean validation to a Hibernate Validator OSGi component whose MessageInterpolator resolves each validation message at runtime: I18nService.getTemplate(message) returns the localized template (raw message used as-is when it returns null), then it interpolates parameter tokens like {min}/{max}, evaluates EL expressions such as ${validatedValue}, and finally replaces escaped literals \{ \} \\ \$ with literal { } \ $. Locale resolution priority is LocaleProvider.getLocale() if present, else the configured defaultLocale (Metatype Config.defaultLocale()), else Locale.getDefault(). A malformed format falls back to the original message with a warning.
- evidence: ['osgi-validator@aa24735:hibernate-validator/src/main/java/hu/blackbelt/osgi/hibernate/MessageInterpolator.java:85', 'osgi-validator@aa24735:hibernate-validator/src/main/java/hu/blackbelt/osgi/hibernate/MessageInterpolator.java:77', 'osgi-validator@aa24735:hibernate-validator/src/main/java/hu/blackbelt/osgi/hibernate/MessageInterpolator.java:135', 'osgi-validator@aa24735:hibernate-validator/src/ma

## BA-088 [missing-how-to] JAX-RS service layer + Dispatcher call contract and HTTP behaviours
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Each generated REST service interface is `@javax.ws.rs.Path('/')`, declares `__bindDispatcher`/`__unbindDispatcher(Dispatcher)`, and every operation method is annotated `@hu.blackbelt.judo.dispatcher.api.JudoOperation(operationAsmFqName)` with `Map`/`List<Map>` input. The impl forwards each call to `Dispatcher.callOperation('<operationAsmFqName>', parameters)` where parameters always include `__exposed=TRUE` plus header-derived `__countRecords`, `__mask`, `__locale`, `__requestParameters`, `__principal`. Result behaviours: no bound Dispatcher → HTTP 503; malformed request-params → 400; no output type → 204; export operations stream to a UUID temp file with `Content-Disposition` (inline vs attachment).
- evidence: ['judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:71', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:22', 'judo-psm-generator-jaxrs@3883ae1:judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:76']

## BA-089 [missing-how-to] Static (unmapped) data and navigation accessors
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Unmapped attributes and relations are served through generated static-data DAO interfaces: the static query data interface exposes selectValue() (or selectValue(<parameter>) when the query has a parameter) returning the attribute's primitive/static type, and static navigations expose query() (collection) or selectOne() (single) with parameter overloads when hasParam. On the backend, unmapped attribute queries resolve the EAttribute via asmUtils.resolveAttribute("<asm name>#<attribute>").get() and call dao.getStaticData(attribute) or dao.getParameterizedStaticData(attribute, parameter.toMap()); a missing value yields null via Optional.orElse(null).
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/static.query.data.java.hbs:20', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/static.query.navigation.java.hbs:28', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/static.query.navigation.java.hbs:13', 'ju

## BA-090 [missing-how-to] Mapped vs unmapped transfer-object API surface boundaries
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The generated DAO interface only emits full CRUD on mapped, non-abstract types: create/createAll (with and without Mask), getById/existsById/getAll/countAll/delete, query() and per-relation create/set/unset/add/remove/range methods are all gated behind self.isMapped (plus relation allowed-operation predicates like isCreateAllowed/isSetAllowed/isAddAllowed/isRemoveAllowed and relationHasRange). Unmapped DTOs and unmapped single relations get only query<...>() accessors and no create/delete/getById/set/unset/range methods.
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dao.java.hbs:122', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dao.java.hbs:22', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dao.java.hbs:67', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-

## BA-091 [missing-how-to] Generated relation-setter DAOs NPE on null relatedObject
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Generated JUDO DAO relation setters (e.g. `setErrorReplacement(entity, relatedObject)`) call `relatedObject.identifier()` unconditionally, so passing `null` throws a NullPointerException. Optional references therefore cannot be cleared through these generated setters, and the failure is invisible because it lives in generated code (under target/, not in git).
- evidence: ['judo-cli-sessions 2026-09-08T14-50 : [A!] "line 731, in a generated file (under target/, so it\'s not in git...) ElementFaultDaoImpl.java:731 dao.setReference(... object.identifier().getIdentifier(), Arrays.asList((Serializable) relatedObject.identifier().getIdentifier())); ... That trailing relatedObject.identifier() is the crash."', 'judo-cli-sessions 2026-09-02T14-27 : [U] "But where we use t

## BA-092 [missing-how-to] ValidationException multi-result vs single-fault error shape
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A JUDO ValidationException can carry multiple ValidationResults, but if a custom operation swallows it and rethrows a single-fault BusinessError (e.g. `createFaultRegistryUploadError`), the per-row gap list is lost. To surface a row-oriented validation/error list to the client, keep the multi-result shape instead of collapsing everything into one fault code.
- evidence: ['judo-cli-sessions 2026-09-08T14-50 : [A!] "Spec HU says the multi-result gap list comes free from ExceptionUtils.createValidationException(results). It doesn\'t. That helper exists, but the conversion op deliberately throws it away: CreateCompleteFaultRegistryCustomImplementation.java:527 ... Every throw in that file is createFaultRegistryUploadError — a single-fault shape."']

## BA-093 [missing-how-to] Runtime payload validation semantics: required relations vs required attributes, and which relations are skipped
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The generated runtime validator (DefaultPayloadValidator) enforces required fields during update/create: a mandatory attribute raises `MISSING_REQUIRED_ATTRIBUTE`, a mandatory one-way relation raises `MISSING_REQUIRED_RELATION` (carrying `__referenceId`), and DERIVED reference members are skipped by update validation while embedded references are traversed. The dispatcher itself enforces required relations (the agent removed a `missingLocation` guard because 'dispatcher enforces' it), so custom code should not duplicate that check.
- evidence: ['judo-cli-sessions__2026-09-28T18-23 : grep -rl "MISSING_REQUIRED_RELATION" . | head -> ./judo-runtime-core-validator/.../DefaultPayloadValidator.class', 'judo-cli-sessions__2026-10-01T11-24 : unzip -p $x \'*.class\' | strings | grep -E "^MISSING_REQUIRED|REQUIRED_RELATION" | sort -u', 'judo-cli-sessions__2026-10-01T11-24 : "Partner create: missingLocation guard -> removed (dispatcher enforces), 

## BA-094 [missing-how-to] JUDO timestamp/timezone semantics (Timestamp!now vs LocalDateTime.now vs DB UTC)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JUDO has two different clocks that do NOT agree. `Timestamp!now()` (the model expression) resolves through `CurrentTimestampProvider`/`DefaultVariableResolver` and is controlled by the `JUDO_PLATFORM_DEFAULT_ZONE_ID` OSGi/env variable (default e.g. Europe/Budapest), not by the JVM timezone. Plain `LocalDateTime.now()` in custom Java follows the JVM `TZ`/`user.timezone`. The mapper/DB layer converts to UTC (e.g. `OffsetDateTimeToLocalDateTimeConverter` uses `ZoneOffset.UTC`), and the Jackson layer serializes as ISO offset/UTC. So a field written as UTC and later compared against `LocalDateTime.now()` in local time yields a fixed offset (2h in summer for Budapest) that silently breaks any age/duration limit. Rule: pick one clock for both write and compare, or compare in the same zone.
- evidence: ["judo-cli-sessions__sessions__2026-10-06T11-45-37-048Z : [A!] 'Az oszlopot UTC-ben írja a kód, de a JVM helyi idejével hasonlítja össze: írás: DefectTicketUpload:300 TemporalUtils.timestampNow() -> 11:36:24 (UTC); olvasás: PhotoHelpReaperJob:94 LocalDateTime.now() -> 13:36:30 (TZ = Budapest); kor = 2óra0mp > 300mp -> HARD_MAX'", "judo-cli-sessions__sessions__2026-10-06T11-45-37-048Z : [U] 'Szoval

## BA-095 [missing-how-to] Querying unset/null optional booleans with BooleanFilter
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: JUDO's generated DAO BooleanFilter only exposes isTrue()/isFalse() — there is no "is unset" filter for an optional (nullable) boolean column. To detect faults where an optional boolean (e.g. withMaterial) is not set, you must either count all rows minus isTrue minus isFalse (three count queries), or load one masked selectList() carrying both the boolean and the related picture IDs and check in Java. This avoids adding derived model members.
- evidence: ['rackinspect 2026-10-04T16-10-56 : "You\'re right: we don\'t need the derived members... `filterByWithMaterial` exists, but `BooleanFilter` only has `isTrue()` and `isFalse()`. There\'s no "is unset" filter. Unset faults can still be found by counting: all faults, minus `isTrue`, minus `isFalse`. That\'s three count queries and no model change."']

## BA-096 [missing-how-to] Querying an enumeration-typed relation can return raw Integer (ClassCastException)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: When a generated relation/navigation returns an enumeration-typed value (e.g. partnerAffiliation), the runtime may deliver it as a raw Integer ordinal rather than the enum instance, producing ClassCastException in the generated DAO impl if you treat the result as the enum. Validate the result casting (and that the generated getter names, e.g. getAffiliationHidden, actually exist) before relying on a newly added enum attribute on a relation.
- evidence: ['rackinspect 2026-10-09 : "java.lang.ClassCastException: class java.lang.Integer cannot be cast to class hu.blackbelt.rackinspect.rackinspect.api.rackinspect.entities.partneraffiliation.PartnerAffiliation ... at ...PartnerDaoImpl.lambda$48(PartnerDaoImpl.java:4323)"', 'rackinspect 2026-10-09 : "The method getAffiliationHidden() is undefined for the type ...Partner"']

## BA-097 [missing-how-to] ResponseConverter outbound payload conversion O(keys × F²) bottleneck and fix
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The JUDO runtime ResponseConverter.convert() had to recompute the returnable property set for every key of every row: it scanned all structural features twice (nested streams, ~F²) and called AsmUtils.getExtensionAnnotationValue(d,"default") per candidate, so list endpoints cost O(rows × keys × F²). The fix is to compute the allowed-name set once per type per convert() call into a local map keyed by EClass (no cache, no global state), giving ~86× speedup on partners/~list and ~1.9× average over 40 endpoints. The "default" extension annotation marks hidden default-value companion fields that must be excluded from response keys; that is why the lookup exists.
- evidence: ['rackinspect-sessions-...2026-10-15T19-33-24Z : "the JUDO runtime `ResponseConverter.convert` (keys × F² annotation lookups per row)"', 'rackinspect-sessions-...2026-10-15T19-33-24Z : "why this look up is so complicated why the getExtentionAnnotaion is needed"', 'rackinspect-sessions-...2026-10-15T19-33-24Z : "Compute it once per convert() call, in a local map (recommended)"', 'rackinspect-sessio

## BA-098 [missing-how-to] Reading principal/actor inside interceptors via dispatcher exchange keys
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: To inspect the calling user/actor inside an OperationCallInterceptor use the dispatcher exchange map constants: PRINCIPAL_KEY ("__principal"), ACTOR_KEY ("__actor"), INSTANCE_KEY_OF_BOUND_OPERATION ("__this") and "__entityType" (from hu.blackbelt.judo.dispatcher.api.Dispatcher / judo-dispatcher-api jar). The signed identifier of the instance is read from the "__signedIdentifier" payload key by DefaultIdentifierSigner. These boundary/principal constants are not documented in the catalog and had to be reverse-engineered with javap on the runtime jars.
- evidence: ['rackinspect-sessions-...feature-guard-user-management-by-role: [DIG>] "public static final java.lang.String INSTANCE_KEY_OF_BOUND_OPERATION = "__this"; ... PRINCIPAL_KEY = "__principal"; ACTOR_KEY = "__actor";" (javap -constants judo-dispatcher-api jar)', 'rackinspect-sessions-...feature-guard-user-management-by-role: [DIG>] DefaultIdentifierSigner bytecode: "// String __signedIdentifier" and ma

## BA-099 [missing-pattern] Custom JAX-RS REST resources in a JUDO application
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A JUDO application developer can expose custom REST endpoints inside the running Karaf app by writing an OSGi Declarative Services component that is also a JAX-RS root resource: annotate the class with @Path (and use @GET/@Post/... with @QueryParam etc.), register it as a service with a discriminator property (e.g. appName=poc), then bind it into a BasicApplication via the 'jaxrs.resource.components' LDAP filter (matching services become singletons) or a 'jaxrs.resource.classes' comma-separated FQN list (loaded with Class.forName). The application address comes from the applicationPath property or @ApplicationPath.
- evidence: ['cxf-jaxrs-application-manager@9d3737e:examples/echo/Echo.java:13', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/application/BasicApplication.java:205', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/application/BasicApplication.java:180', 'cxf-jaxrs-application-manager@9d3737e:src/main/java/hu/blackbelt/jaxrs/CxfServerManager.java:187']

## BA-100 [missing-topic] Transfer-object immutability and lifecycle semantics
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The immutable/mutable copy model of JUDO transfer objects: the 'immutable' keyword creates a detached copy of a TO/entity/list/relation (requires 'var immutable <Type>' in the declaration); the 'mutable <immutableValue>' keyword reloads the entity from the database by identifier only (attributes/relations of the copy are not written back). Immutable objects cannot be returned from operations, cannot have operations called on them, cannot be deleted, and cannot navigate non-aggregation/composition associations. Each script call starts a new transaction (read committed by default, reused if invoked from a running script); mapped TOs share identity with their target entity; optimistic locking increments a version field on every write and a save with a stale version is declined.
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/user-guide/application_modeling/05_transfer_object_lifecycle.adoc:426', 'documentation@3eec62f:docs/modules/ROOT/pages/user-guide/application_modeling/05_transfer_object_lifecycle.adoc:526', 'documentation@3eec62f:docs/modules/ROOT/pages/user-guide/application_modeling/05_transfer_object_lifecycle.adoc:537', 'documentation@3eec62f:docs/modules/ROOT/p

## BA-101 [missing-topic] OSGi Configuration Mapper for custom application parameters
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Application-level configuration for JUDO additions is defined through the OSGi Configuration Mapper: a configset declares templatePath (classpath folder with *.template FreeMarker files), envPrefix (e.g. MY_APP_), and variableScopePreference (osgi,environment,system). Each *.template file name (without extension) becomes a configuration PID, e.g. ApplicationConfiguration.template -> PID ApplicationConfiguration. With envPrefix=MY_APP_, env var MY_APP_PROP_NAME is referenced in templates as propName; templates are processed with FreeMarker and can pull from environment, system properties or application parameters. Consumers read the PID via ConfigurationAdmin.getConfiguration("ApplicationConfiguration").
- evidence: ['documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/09_define_custom_application_parameters.adoc:31', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/09_define_custom_application_parameters.adoc:40', 'documentation@3eec62f:docs/modules/ROOT/pages/developer-guide/backend/09_define_custom_application_parameters.adoc:46', 'documentation@3eec62f:docs/modules/

## BA-102 [missing-topic] Model/metamodel cache TTL system properties
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: Several platform caches are tuned only via system properties read at class load: EsmModelCacheExpiration (seconds, default 5) controls the Guava-backed EsmModelCache, invalidated through an EContentAdapter; EsmUtilsCacheExpiration (seconds, default 60) sets expireAfterAccess for the per-ResourceSet AsmUtilsCache; FqnCacheExpiration (seconds, default 300) sets the expireAfterAccess window of the FQN cache, where expiry is idle-based (not a fixed TTL) and the forward index is never expired (only clear() empties it). AsmUtilsCache.clear() clears FQ-name, element-by-type, mapped-type and binding maps but not annotationsByModelElementAndName.
- evidence: ['judo-meta-esm@65b02f94:openspec/specs/esm-model-runtime/spec.md:110 — EsmModelCache expiry is set by the system property EsmModelCacheExpiration, default 5 seconds. The cache is invalidated through an EContentAdapter.', 'judo-meta-asm@a3b7846:model/src/main/java/hu/blackbelt/judo/meta/asm/runtime/AsmUtilsCache.java:48 — System property AsmUtilsCacheExpiration (seconds, default 60) sets the expir

## BA-103 [missing-topic] IdentifierProvider pluggable identifier generation extension point
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: IdentifierProvider is a public interface for pluggable identifier generation: get() returns the identifier value, getType() its Serializable class, getName() its name. This module (judo-dao-api) declares the interface but provides no implementation; concrete identifier generation comes from JUDO runtime modules, and a developer can implement IdentifierProvider to change how identifiers are produced.
- evidence: ['judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/IdentifierProvider.java:26', 'judo-dao-api@7e7131d:src/main/java/hu/blackbelt/judo/dao/api/IdentifierProvider.java:25']

## BA-104 [missing-topic] REST transport protocol (signed identifiers, partial update, list query contract)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The generated backend exposes a JSON-over-HTTP CRUD/operation API rooted at /api/<Model>/Actor/... with resource verbs ~create/~list/~update/~delete/~get/~validate (instance writes identified by the X-Judo-SignedIdentifier request header, responses carrying __identifier/__signedIdentifier). List/query bodies combine _orderBy with a _seek keyset cursor (lastItem:{__signedIdentifier,<sort key>}, limit, offset, reverse) and per-attribute filter operators; ~update is partial, i.e. fields omitted from the body are left unchanged. There is no consolidated reference describing this wire contract for a developer building a custom client or debugging the generated one.
- evidence: ['judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Object.postman_collection.json:44', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Object_Inheritance_mixin_mapped.postman_collection.json:369', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Object_Operations_newcrud.postman_collection.json:22', 'judo-platform@2d22cf41:judo-platform-ites

## BA-105 [missing-topic] Missing API error codes (actor-bound ops, optional params, ranges)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The runtime returns specific error codes not present in the catalog's error reference: AUTHENTICATED_ENTITY_NOT_FOUND (403), ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION (403), MISSING_REQUIRED_PARAMETER (400) and NOT_ACCEPTED_BY_RANGE (400).
- evidence: ['judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Special_FilteredAccess.postman_collection.json:547', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Special_FilteredAccess.postman_collection.json:735', 'judo-platform@2d22cf41:judo-platform-itest/itests/collections/CRUD_Object_Operations_single.postman_collection.json:295', 'judo-platform@2d22cf41:judo-platf

## BA-106 [missing-topic] Reserved payload keys used by DAO payload processors
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The DAO payload processors reserve specific payload map keys that developers must not reuse as model features: __referenceId (client reference identifier), __entityType (entity type marker), __version (optimistic lock), and __selected (selected-item marker in the select path). Payload authors must avoid these names for model features. PayloadDaoProcessor also defines the public constants MEASURE_CONVERTING_SCALE = 20 used when converting transfer values between measure units.
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/PayloadDaoProcessor.java:57', 'judo-runtime-core@b34d8ea1:judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/executors/StatementExecutor.java:71']

## BA-107 [missing-topic] PayloadTraverser: walking payload trees with a processor/predicate
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: PayloadTraverser is a builder-configured walker over a Payload tree: traverse(Payload, EClass) visits each payload that passes a predicate on its EReferences, calls a BiConsumer processor with a PayloadTraverserContext (type + path), and can gate descent per reference item via referenceItemTravesePredicate. getPathAsString() joins segments with '.' and adds [index] for many-valued references. It is the reusable utility for nested/recursive payload processing in custom operations (e.g. deep validation, copying, masking).
- evidence: ['judo-runtime-core@b34d8ea1:judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/PayloadTraverser.java:58', 'judo-runtime-core@b34d8ea1:judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/PayloadTraverser.java:49', 'judo-runtime-core@b34d8ea1:judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/PayloadTraverser.java:126']

## BA-108 [missing-topic] Binary upload-token capability (getUploadTokenFor operation and UploadToken type)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: A transfer field that reads and maps a binary (BinaryType) primitive on a create-capable transfer automatically gets a `getUploadTokenFor<Field>` unbound operation (GET_UPLOAD_TOKEN behaviour) returning a synthesized `UploadToken` unmapped transfer object type holding one required `token` string attribute (UploadTokenStringType, maxLength 2048). The operation's output parameter is named `output`, typed UploadToken, cardinality 1..1.
- evidence: ['judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/action/getUploadTokenBehaviour.etl:56', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/action/getUploadTokenBehaviour.etl:76', 'judo-tatami-jsl@c1693a5b:judo-tatami-jsl-jsl2psm/src/main/epsilon/transformations/psm/modules/action/getUploadTokenBehaviour.etl

## BA-109 [missing-topic] Generation feature switches and their defaults (generateActors/generateOperations/generateBehaviours/generateTransferObjectTypes/generateDefaultTransferObjectTypes, stringMaxLength)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The ESM-to-PSM transformation is gated by five boolean switches carried on every parameter builder: generateActors, generateOperations, generateBehaviours, generateTransferObjectTypes and generateDefaultTransferObjectTypes, all defaulting to true, plus stringMaxLength (default 65536) which controls the generated _StringType. The switches are not uniform: e.g. the _...ForDefaultTransferObjectType attribute rules are gated by generateDefaultTransferObjectTypes (not generateTransferObjectTypes), and the query-customizer/ordering/filter families are gated by generateBehaviours.
- evidence: ['judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/Esm2PsmZeta.java:122', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/Esm2PsmWork.java:58', 'judo-tatami@13186706:judo-tatami-esm2psm/src/main/epsilon/transformations/psm/modules/service/transferAttribute.etl:82']

## BA-110 [missing-topic] Type-coercion mapper library (Coercer/Converter/Formatter)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: hu.blackbelt.mapper is a pluggable Converter<S,T> type-coercion library. Coercer.coerce(source, targetClass|targetClassName) resolves an exact source-type converter, then the first converter with an assignable source type, then falls back to a two-step source->String->target conversion via Formatter<T>; primitive targets are resolved to their wrapper types first. Java8Module registers 56 built-in converters plus formatters; JodaTimeModule extends the set (JodaTimeModule / decorateWithJodaTime); ExtendableCoercer.getConverterFactory() exposes the converter registry so code can inspect or replace converters by calling ConverterRegistry.registerConverter/unregisterConverter. Failures surface as UnsupportedOperationException ("Failed to convert ...") or ConverterException (unchecked).
- evidence: ['mapper@75435c8:mapper-api/src/main/java/hu/blackbelt/mapper/api/Coercer.java:37', 'mapper@75435c8:mapper-api/src/main/java/hu/blackbelt/mapper/api/Converter.java:31', 'mapper@75435c8:mapper-impl/src/main/java/hu/blackbelt/mapper/impl/DefaultCoercer.java:85', 'mapper@75435c8:mapper-impl/src/main/java/hu/blackbelt/mapper/impl/DefaultCoercer.java:164', 'mapper@75435c8:mapper-impl/src/main/java/hu/b

## BA-111 [missing-topic] JUDO SDK generator template parameters (apiPrefix / generateOptionalTypes / generatePayloadValidator / debugPrint / identifierType)
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The judo-psm-generator-sdk-core generator reads five Handlebars template variables (set as Maven plugin <parameters> / generator-parameter.properties values and read through StoredVariableHelper from a ThreadLocal while templates execute): apiPrefix (string package prefix prepended to generated API package names), generateOptionalTypes (boolean; when true, non-required attributes and relations are wrapped in java.util.Optional), generatePayloadValidator (boolean; gates payload validation via validatePayload in the generated DAO impls), debugPrint (boolean; adds debug comment banner lines), and identifierType (the Java type used for identifiers in generated DAO/DTO code, e.g. java.io.Serializable). These flags change the shape of the generated SDK API a developer writes against.
- evidence: ['judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/api/StoredVariableHelper.java:48', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/api/StoredVariableHelper.java:60', 'judo-psm-generator-sdk-core@7d2e251:judo-psm-generator-sdk-core-api/src/main/jav

## BA-112 [missing-topic] Built-in optimistic locking & the VERSION field on updates
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: The JUDO RDBMS DAO enables optimistic locking by default (`rdbmsDaoOptimisticLockEnabled` defaults to true). Every entity carries a `VERSION` field; `UpdatePayloadDaoProcessor` reads `originalVersion` from the stored payload and `updateVersion` from the submitted payload and refuses a stale write if they differ, and `DefaultIdentifierSigner` folds the version into signed identifiers. Custom update operations that rebuild payloads must carry the current VERSION or they trigger optimistic-lock collisions / version errors; the version is a concurrency guard, not an app concern.
- evidence: ["judo-cli-sessions__sessions__2026-10-02T14-00-50-847Z : [DIG>] 'final Integer originalVersion = originalPayload.getAs(Integer.class, VERSION);'", "judo-cli-sessions__sessions__2026-10-02T14-00-50-847Z : [DIG>] 'Boolean rdbmsDaoOptimisticLockEnabled = JudoDefaultModuleConfiguration.DEFAULT.getRdbmsDaoOptimisticLockEnabled();' '(default true)'", "judo-cli-sessions__sessions__2026-10-02T14-00-50-84

## BA-113 [missing-topic] Native SQL / JDBC / DataSource query from a JUDO custom service
- target: agent-docs/backend | src: gap-mining | status: mined
- fact: To look up rows that JQL and the generated QueryCustomizer cannot express (e.g. finding the owning JobSheetItem of a picture via the join table j_entities_job_sheet_item_pictures), a service needs to run a native SQL query. That requires injecting a JDBC DataSource into an OSGi declarative-service component (a new DataSource @Reference) and wiring the test kit to bind it — there is no working precedent in this repo, the blueprint, or the catalog for how to add and test a native-SQL/DataSource path inside a custom service layer.
- evidence: ['judo-cli-sessions__2026-10-28 : [CAT] ask_user "6.4 owner lookup (picture -> owning JobSheetItem). JQL cannot filter JobSheetItem by a contained picture\'s id (no navigation in filterBy, no typed relation filter). D8 then prescribes a native lookup on j_entities_job_sheet_item_pictures — but there is NO native-SQL / DataSource precedent in this repo or the blueprint (new OSGi DataSource referenc

## BA-114 [wrong-fact] G E N E R A T E D header does not mean untouched
- target: agent-docs/backend | src: session:jb-006.json | status: reported-unvalidated
- claim: Files with the 'G E N E R A T E D' header are generated and untouched.
- fact: 57 of 192 tracked *CustomImplementation.java still carry the stub 'G E N E R A T E D' header but are fully implemented. The *.java.default stubs (245) just throw UnsupportedOperationException; 53 model operations have only the stub (no implementation). Compare against the .default sibling instead of the header.
- evidence: rackinspect@3954ae1 application/app/src/main/java

## BA-115 [wrong-fact] backend interceptors: OperationCallInterceptor signatures
- target: agent-docs/backend | src: session:jb-007.json | status: validated
- claim: Example uses no-arg getOperations() and postCall(Payload, ...); interface snippet lists no async()/terminateOnException()/ignoreDecoratedCall().
- fact: Source has getOperations(AsmModel) and postCall(EOperation, Object, Object); interface also has async(), terminateOnException(), ignoreDecoratedCall() whose behaviour is undocumented.
- evidence: judo-runtime-core@b9bd93e8 (BE-001..004)

## BA-116 [wrong-fact] AccessValidationDao does not exist
- target: agent-docs/backend | src: session:jb-007.json | status: validated
- claim: AccessValidationDao appears in three backend docs (BE-005/006/007).
- fact: Class exists in no judo-ng module nor rackinspect.
- evidence: re-grepped all judo-ng and rackinspect (session 2026-11-04T08:53)

## BA-117 [wrong-fact] Business errors: ExceptionUtils/BusinessErrorException are not platform classes
- target: agent-docs/backend | src: session:jb-007.json | status: validated
- claim: throw ExceptionUtils.createBusinessErrorException(...); GenericOperationErrorException and BusinessErrorException are runtime exception types. Subagent's proposed fix: use runtime ValidationException/AccessDeniedException/NotFoundException.
- fact: ExceptionUtils is rackinspect project code (hu.blackbelt.rackinspect.common.utils); BusinessErrorException is generated from the project's own model (e.g. rackinspect api...error_services.businesserror.BusinessErrorException). JUDO way: model business errors as operation faults (esm.ecore:584); the generator creates the exception class. Runtime exceptions ValidationException, AccessDeniedException, NotFoundException exist in judo-runtime-core .../runtime/core/exception/. The subagent's proposed text was wrong.
- evidence: rackinspect DefectTicketUpload.java:244; esm.ecore:584 (BE-008/009)

## BA-118 [wrong-fact] EmptyMapIntstanceCollector name
- target: agent-docs/backend | src: session:jb-008.json | status: reported-unvalidated
- claim: agent-docs/README.md row says `EmptyMapInstanceCollector`.
- fact: The class in dao-core is spelled `EmptyMapIntstanceCollector` (typo is real, referenced in dao-core collectors/AGENTS.md).
- evidence: session 2026-11-04T09:47, subagent reader B098 (judo-runtime-core-dao-core)

## BA-119 [wrong-fact] max_uuid returns first arg
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: AGENTS row says max_uuid returns the larger value
- fact: In create-min-max.sql lines 77-81 both branches return $1, so max(uuid) returns the first argument, not the larger one (also a code bug).
- evidence: session 2026-11-04T13:22, subagent C134 (create-min-max.sql:77-81)

## BA-120 [wrong-fact] Oracle dialect does not exist
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Row lists an oracle dialect bundle among Dialect implementations
- fact: Only hsqldb and postgresql implement Dialect in this checkout; no Oracle bundle.
- evidence: session 2026-11-04T13:22, subagent C134

## BA-121 [wrong-fact] SelectStatementExecutor constructor responsibilities
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Constructor sets up METRICS scopes and getConstantFields() set/remove
- fact: Constructor only registers expression translators; METRICS scope/constant fields handling happens in selectMetadata, executeSelect and countSelect.
- evidence: session 2026-11-04T13:22, subagent C137

## BA-122 [wrong-fact] dispatcher extension-points.md signatures
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: Signatures for ActorResolver, VariableResolverManager, DispatcherFunctionProvider, IdentifierSigner and Export
- fact: These signatures do not match the code.
- evidence: session C141

## BA-123 [wrong-fact] postCall interceptor order
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: postCall runs in reverse order
- fact: postCallInterceptors iterates in the same order as preCallInterceptors.
- evidence: CallInterceptorUtil.java, session C141

## BA-124 [wrong-fact] custom-queries SKILL uses nonexistent translator.register
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: uses translator.register(...) and lists FilterMapper class
- fact: No register method exists (map reachable only via getTranslators()); FilterMapper class is not in the repo.
- evidence: session C141, C145 (Translator has no register; custom-functions skill line 82)

## BA-125 [wrong-fact] query-debugging SKILL rdbmsReference
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: calls resolver.rdbmsReference(...)
- fact: Does not exist; M:N lookup is rdbmsJunctionTable(EReference).
- evidence: session C141

## BA-126 [wrong-fact] getTransferObjectGraph return type in expression docs
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: returns bare type
- fact: Code returns Optional.
- evidence: session C145

## BA-127 [wrong-fact] debug-operations skill log strings
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: lists log strings 'Dispatching operation:', 'Resolved actor:'
- fact: Not in source; only 'Operation {} completed in {} ms' (DefaultDispatcher.java:821) and 'Unable to rollback transaction' (TransactionalOperationCall.java:77) exist. Also create-interceptor skill claims Multibinder wiring but OperationCallInterceptorProviderProvider builds a list.
- evidence: session C145

## BA-128 [wrong-fact] FeatureFactory '~90 converters'
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: ~90 converters
- fact: FeatureFactory registers 78 converters.put calls; feature/AGENTS.md lists 72 converter files.
- evidence: session C156

## BA-129 [wrong-fact] Converter AGENTS rows wrong
- target: agent-docs/backend | src: session:jb-011.json | status: reported-unvalidated
- claim: StringAggregated handles concatenate; Matches adds one operand parameter
- fact: StringAggregatedExpressionToFeatureConverter switch handles only MIN and MAX; MatchesToFeatureConverter adds two parameters (STRING and PATTERN).
- evidence: session C157/C158

## BA-130 [wrong-fact] transferObjectType.etl generateBehaviours guard
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: The doc says the whole family of rules is generateBehaviours-guarded.
- fact: `CreateQueryOrderingType`, `CreateQueryFilterType`, `CreateQuerySeekingType`, the get-range input rules and `CreateUploadTokenType` have no such guard.
- evidence: batch C371

## BA-131 [wrong-fact] Asm2Keycloak AGENTS.md claims
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: ClientRules.java.AGENTS.md says `createKeycloakClientClaim` reads `keycloakResource`. Asm2Keycloak.java.AGENTS.md claims MD5 keying for script URIs. Asm2KeycloakRuleNames AGENTS.md says `CreateRealm` is an ETL rule name.
- fact: All three claims are wrong. The code does not read `keycloakResource` there, does no MD5 keying, and `realm.etl` has no `CreateRealm` rule.
- evidence: batch C389

## BA-132 [wrong-fact] asm2rdbms zeta rules AGENTS.md counts and perf test sizes
- target: agent-docs/backend | src: session:jb-015.json | status: reported-unvalidated
- claim: zeta/rules/AGENTS.md:8: 'ten eClassToTable*Field rules'. The perf test sizes are 10/50/100.
- fact: ClassRules.java has nine eClassToTable*Field rules plus eClassToRdbmsTable, ten @TransformRule methods in total. The perf test sizes in code are 100/500/1000. In `ReferenceRules.java:558`, `fk2.setSqlName` runs only if the source table and PK exist, but fk2 is still added to the junction table and traced, so its sqlName may be null with no warning.
- evidence: batch C392

## BA-133 [wrong-fact] Backend API corrections in catalog docs (interceptor, errors, expressions)
- target: agent-docs/backend | src: session:jb-029.json | status: reported-unvalidated
- claim: Docs use ExceptionUtils.createBusinessErrorException, GenericOperationErrorException, Translator.register(), interceptor getOperations without AsmModel
- fact: Interceptor getOperations(AsmModel) returns operations; postCall runs in registration order. Business errors are modeled faults -> generated <Name>Exception (BusinessErrorException generated per project); ValidationException/AccessDeniedException/NotFoundException are platform errors; ExceptionUtils.createBusinessErrorException and GenericOperationErrorException do not exist. getTransferObjectGraph/getTransferObjectBindings return Optional<...>; EntityTypeExpressions fields are getterAttributeExpressions/getterReferenceExpressions; Translator has no register(), use getTranslators() map. DI via @Reference and @Inject.
- evidence: session 2026-11-09T09:31:53Z, agent output from catalog-update-report.md §3.1

## BA-134 [wrong-fact] Interceptor postCall order is forward, not reverse
- target: agent-docs/backend | src: session:jb-030.json | status: validated
- claim: 'FOR EACH interceptor (REVERSE order): interceptor.postCall(...)' (line 42) and '@JudoTest example comment: Both interceptors invoked in REVERSE order for postCall' (line 86)
- fact: postCall is dispatched in the same forward registration order as preCall; postCallInterceptors iterates getInterceptorsForOperation(...) in registration order.
- evidence: judo-runtime-core-guice-testkit/agent-docs/interceptor-testing.md:42,86; findings_rows.json

## BA-135 [wrong-fact] Interceptor example incomplete (getOperations / getIdOf)
- target: agent-docs/backend | src: session:jb-030.json | status: validated
- claim: Example getOperations uses asmUtils::resolveOperation and postCall uses getIdOf(...)
- fact: Neither asmUtils nor getIdOf is declared/imported in the example. The shipped interceptor template declares `private AsmUtils asmUtils` (@Reference or constructed AsmUtils); show the field and the getIdOf helper.
- evidence: judo-doc-problems.md Part A, session part 30

## BA-136 [wrong-fact] Custom implementation example, line 251
- target: agent-docs/backend/custom-operations.md | src: agent-docs-review:backend.json | status: reported
- claim: @Reference AccessValidationDao accessValidationDao;
- evidence: judo-runtime-core@b9bd93e8: no class or interface AccessValidationDao defined in any module (rg across repo returns no match)

## BA-137 [missing] Generated relation-setter DAOs NPE on null
- target: agent-docs/backend/data-access-guide.md | src: session:jb-020.json | status: reported-unvalidated
- fact: Generated DAO relation setters (e.g. setErrorReplacement(entity, relatedObject)) call relatedObject.identifier() unconditionally, so passing null throws NullPointerException; unset must be used instead.
- evidence: gap S01-06

## BA-138 [missing] Mapped vs unmapped transfer-object DAO API surface
- target: agent-docs/backend/data-access-guide.md | src: session:jb-020.json | status: reported-unvalidated
- fact: Generated DAO interface emits full CRUD (create/createAll with/without Mask, getById/existsById/getAll/countAll/delete, query(), per-relation create/set/unset/add/remove/range) only on mapped, non-abstract types, gated behind self.isMapped (plus relation allowed-operations). Also payload helper has Map.of-style overloads for 1-20 pairs, getAs(Class,String), getAsCollectionPayload, getAsPayload.
- evidence: gap P32-05

## BA-139 [missing] Mask best practices answer location
- target: agent-docs/backend/data-access-guide.md | src: session:jb-023.json | status: reported-unvalidated
- fact: Masks documented in data-access-guide.md 'Using Masks (Projections)' (line ~361-480): [Entity]Mask.entityMask().withX(); empty mask = existence check; nested masks for relationships; masks in dao.update for partial update; unmasked field access returns null with no error (most common bug; also Anti-Pattern 9 in integration-testing/best-practices.md). Operator asked for this, suggesting a discoverable mask how-to/best-practice entry in catalog/best-practices is missing (only agent-docs).
- evidence: session 2026-11-06T10:44, operator question + agent kb_search

## BA-140 [missing] Generated relation-setter DAOs NPE on null relatedObject
- target: agent-docs/backend/data-access-guide.md | src: session:jb-029.json | status: reported-unvalidated
- fact: Generated JUDO DAO relation setters (e.g. setErrorReplacement(entity, relatedObject)) call relatedObject.identifier() unconditionally; passing null throws NullPointerException.
- evidence: knowledge-gaps-report.md §2 (S01-06); judo-psm-generator-sdk-core, judo-dao-api

## BA-141 [missing] BooleanFilter has no 'is unset' filter for optional booleans
- target: agent-docs/backend/data-access-guide.md | src: session:jb-029.json | status: reported-unvalidated
- fact: SDK BooleanFilter only exposes isTrue()/isFalse(); there is no filter for null/unset optional booleans.
- evidence: knowledge-gaps-report.md (session excerpt, 2026-11-09T09:28:59Z)

## BA-142 [correction] Operator: not all business errors are modeled exceptions, not all errors map to attributes, interceptors cannot send faults
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: operator-stated
- claim: Agent Part A line 'business errors are modeled faults'.
- fact: The operator pointed out that: (1) not all business errors are modeled exceptions; (2) not all errors connect to model attributes; (3) a modeled fault cannot be sent from an interceptor; (4) interceptors do not handle business problems. Source checks confirmed all of them, so the Part A error-handling item needed a rewrite. Distinguish platform errors (ValidationException, 400, location optional) from modeled faults (422, checked exception).
- evidence: session 2026-11-06T10-49-13-527Z, operator, about 2026-11-09T13:10

## BA-143 [decision] Business errors from interceptors must be wrapped in a business exception; ValidationException not for interceptors
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-030.json | status: operator-stated
- claim: Docs tell interceptors to throw ValidationException/faults
- fact: Operator: validation exceptions in business errors are not all modeled exceptions; a modeled fault can't be sent from interceptors; not all exceptions connect to model attributes because they don't come from the model; interceptors don't handle business problems, so the business error should be wrapped in the interceptor (e.g. InterceptorCallBusinessException/BusinessException). Operator asked for parallel exploration (5 explore subagents).
- evidence: session 2026-11-09T13:06:35, operator

## BA-144 [missing] JUDO runtime exception hierarchy and HTTP mapping
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-030.json | status: reported-unvalidated
- claim: ValidationException in business-error docs as modeled/connected to attributes
- fact: ClientException (abstract, RuntimeException; getStatusCode/getDetails, runtime-core exception package): ValidationException 400 (Collection<ValidationResult>), AccessDeniedException 403, AuthenticationRequiredException 401, NotFoundException 404 (single ValidationResult). ClientExceptionMapper returns getStatusCode (400 if null) with getDetails() JSON. BusinessException (judo-dispatcher-api, RuntimeException, NOT ClientException; fields type, errorCode, details, throwable, locale) -> 422 with header X-Fault:<type>, body {<faultFQN>:{details w/o '_' keys & nulls}, code:errorCode}; cause only if includeBusinessCause. InterceptorCallBusinessException extends BusinessException. Other exceptions -> 500 {level:ERROR, code:INTERNAL_SERVER_ERROR, details:{}}; stack trace details.exception when returnRuntimeExceptions (not for BusinessException). InternalServerException -> 500. There's no FeedbackItem class; equivalent is hu.blackbelt.judo.dao.api.ValidationResult (code, Level ERROR|WARNING, Object location, Map details).
- evidence: RC/.../exception/*.java; RuntimeExceptionMapper.java:68-110; ClientExceptionMapper.java:33-47; BusinessException.java:29-31; subagent explore

## BA-145 [missing] ValidationException is a platform exception; ValidationResult location need not be a model attribute
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-030.json | status: reported-unvalidated
- claim: Validation errors map to model attributes
- fact: ValidationException is a platform ClientException, not generated. ValidationResult.location can be absent (DefaultDispatcher.java:305-309,320), free strings like '_mask'/'_identifier' (QueryCustomizerParameterProcessor.java:296,325), parameter name or '', or global access errors with only code/level (DefaultAccessManager.java:106-130).
- evidence: runtime__judo-dao-api ValidationResult.java:31-44

## BA-146 [missing] Modeled faults generate checked <Fault>Exception; dispatcher translates BusinessException
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-030.json | status: reported-unvalidated
- fact: dao.fault.java.hbs:8 generates <Fault>Exception extends java.lang.Exception (checked, not BusinessException) with typed details, errorCode as message, ctors (details),(errorCode,details),(errorCode,details,cause). dto.dispatcher.wrapper.java.hbs:43-54 catches BusinessException, matches ex.getType() to fault ASM name and throws <Fault>Exception, else IllegalStateException. DefaultDispatcher.java:408-414 creates BusinessException from operation result FAULT map (FAULT_TYPE, FAULT_DETAILS, FAULT_ERROR_CODE, FAULT_CAUSE).
- evidence: template__judo-psm-generator-sdk-core dao.fault.java.hbs; DefaultDispatcher.java:408-414

## BA-147 [missing] Dispatcher rewraps non-client RuntimeExceptions as InternalServerException; nested ClientException/BusinessException becomes 500
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-030.json | status: reported-unvalidated
- fact: DefaultDispatcher.java:812-814 rethrows ClientException and BusinessException unwrapped; every other RuntimeException/ExecutionException becomes InternalServerException('Operation failed', ex) (:815-816). No recursive getCause unwrapping in mappers or FaultInterceptor, so a client/business exception buried in a cause chain surfaces as generic 500. FaultInterceptor (CXF PRE_STREAM) only sets HTTP status, no body; auto-unboxes getStatusCode (NPE for null custom subclass).
- evidence: DefaultDispatcher.java:812-816; FaultInterceptor.java:51-108

## BA-148 [missing] Fault type string not validated; use modeled fault FQN
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: validated
- claim: No guidance on what type string to use.
- fact: Neither type nor details are validated against the model or the operation's declared faults (the dispatcher never checks them). Use the ASM FQN of a modeled fault transfer object (e.g. northwind.services.AlreadyShipped) as type, even if no operation declares it. The frontend translation keys faults.<fqn>.<attr> depend on it; a typo still gives a 422 but the dialog falls back to raw attribute names. Null details would NPE in the mapper (RuntimeExceptionMapper ~L88-90).
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore

## BA-149 [missing] Fault handling and declared-fault filtering in SDK wrapper
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: validated
- claim: Implicitly that the dispatcher checks faults against the declaration.
- fact: The dispatcher does not check faults against the operation. The only check is in the generated SDK client wrapper (dto.dispatcher.wrapper.java.hbs:43-55): it matches BusinessException.getType() against declared faults and rethrows the typed <Name>Exception, else IllegalStateException. If the operation declares no faults the raw BusinessException passes through. Over REST, any fault type string works (422 with X-Fault).
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore

## BA-150 [missing] ValidationResult.location is optional
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: validated
- claim: error-handling-guide.md:73-80 and :119 present ValidationException as field-bound input errors; 03_business_fault.adoc:133 says validation is based on model elements.
- fact: ValidationResult {code, level, location, details} has location of type Object and optional (ValidationResult.java:33-38). The platform itself emits errors without location (ERROR_INVALID_IDENTIFIER, ACCESS_DENIED) or with non-field locations (_mask, _identifier). The official docs example throws ValidationException with only a code (SHIPPED_TIME_MUST_AFTER_ORDER_TIME). Not all errors map to model attributes.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore + operator point

## BA-151 [missing] Exception mapping HTTP details
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: validated
- fact: RuntimeExceptionMapper.java:60-119: BusinessException maps to 422, X-Fault: <type>, body {<type>: details minus _-keys and nulls, code, cause only if includeBusinessCause}. Other RuntimeException maps to 500 code INTERNAL_SERVER_ERROR. In the dispatcher outer catch (:812-816) ClientException/BusinessException are rethrown, other RuntimeException/ExecutionException become InternalServerException('Operation failed'). FaultInterceptor (jaxrs-cxf) handles only exceptions escaping the mapper. ValidationException extends ClientException (ValidationException.java:28). For exposed operations the dispatcher validates parameters in a transaction that is rolled back (:696-714) with no interceptors.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore

## BA-152 [wrong-fact] ExceptionUtils and GenericOperationErrorException exist only in docs
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: reported-unvalidated
- claim: error-handling-guide.md:36 'ExceptionUtils recommended way': createBusinessErrorException, createValidationResult, createValidationException, createBusinessException; :121 GenericOperationErrorException (BusinessException) 500; also in interceptors.md, internationalization-guide.md, advanced-patterns.md.
- fact: No ExceptionUtils class or GenericOperationErrorException exists in any platform or template source under wt/ (no .java, .hbs). They only appear as call sites in agent-docs. They may be in a runtime jar or per-project code, which is unverified. Treat them as unconfirmed and do not teach them as platform API.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore Where ExceptionUtils comes from

## BA-153 [wrong-fact] BusinessErrorException is not a platform type
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: reported-unvalidated
- claim: error-handling-guide: BusinessErrorException is 'modeled, type-safe business rule violations' with 422; template says 'model custom fault types (BusinessError)'.
- fact: No BusinessErrorException Java class or BusinessError fault exists in the platform. It is generated per project from a user-modeled fault TO named BusinessError via dao.fault.java.hbs (<ClassName>Exception). The docs must say the project has to model it.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore, template__judo-esm-fullstack-project-template error-handling-guide.md.hbs:27,47,120

## BA-154 [wrong-fact] Catalog/template/official docs disagree on business-rule error type and status
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-031.json | status: reported-unvalidated
- claim: error-handling-guide.md:121 GenericOperationErrorException 500; template .hbs: ValidationException with ERR_ prefix, 400; official 03_business_fault.adoc:24: modeled fault 422.
- fact: The three sources give three answers. Correct: platform errors (ValidationException 400, AccessDenied 403, AuthenticationRequired 401, NotFound 404) are ClientException subclasses; modeled faults give 422 plus X-Fault. Also: generalization-guide.md:196 uses new ValidationException(String), which the template says does not exist; NotFoundException/AccessDeniedException need a ValidationResult constructor. Template says 'no BusinessException class in runtime-core' but judo-dispatcher-api has BusinessException. validation-exception-hierarchy.md:48 wraps Exception into createBusinessErrorException('UNEXPECTED') making bugs 422.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore docs-vs-docs comparison

## BA-155 [wrong-fact] Project service helpers presented as platform API in agent-docs
- target: agent-docs/backend/error-handling-guide.md | src: session:jb-038.json | status: validated
- claim: ExceptionUtils / GenericOperationErrorException / BusinessErrorException are documented as platform API.
- fact: They are project code, not platform API. Still wrong in catalog/agent-docs/frontend/advanced-patterns.md, backend/internationalization-guide.md, backend/interceptors.md and backend/error-handling-guide.md. Blueprints now label such classes as example project code. Business faults are modeled as 422 ValidationException, 400 for others (per agent search).
- evidence: grep in catalog/agent-docs at session 15:55; agent report bp08b

## BA-156 [wrong-fact] ExceptionUtils / GenericOperationErrorException are not platform classes
- target: agent-docs/backend/error-handling-guide.md | src: session:sweep-012.json | status: validated
- claim: Docs teach ExceptionUtils.createBusinessException/createValidationException and GenericOperationErrorException as platform API (error-handling-guide, interceptors, internationalization-guide).
- fact: No source or template in judo-ng defines them (only doc references). In Rackinspect they are project code (common/.../utils/ExceptionUtils.java) wrapping generated fault exceptions from the project's own fault TOs (BusinessError -> BusinessErrorException, GenericOperationError -> GenericOperationErrorException, 422). Label as example project code to copy.
- evidence: judo-ng template agent-docs grep; Rackinspect common/src/main/java/hu/blackbelt/rackinspect/common/utils/ExceptionUtils.java:16-50

## BA-157 [wrong-fact] Docs give three contradictory answers for business rule violation
- target: agent-docs/backend/error-handling-guide.md | src: session:sweep-012.json | status: validated
- claim: Official docs: modeled fault 422; catalog: GenericOperationErrorException 500; template: ValidationException with ERR_ code 400. Catalog interceptor examples throw raw RuntimeException (user sees 500).
- fact: Two distinct kinds: platform errors (ValidationException 400, AccessDeniedException 403, AuthenticationRequiredException 401, NotFoundException 404; unchecked ClientException, payload list of ValidationResult{code,level,location,details}) vs modeled faults (generated checked <Fault>Exception, 422 + X-Fault header = fault FQN). Field/input problem -> ValidationException; business rule -> modeled fault. Never RuntimeException for user-facing errors.
- evidence: session 2026-11-09T13:11:53 assistant synthesis of source-reading agents

## BA-158 [wrong-fact] Business exception example, line 50
- target: agent-docs/backend/error-handling-guide.md | src: agent-docs-review:backend.json | status: reported
- claim: throw ExceptionUtils.createBusinessErrorException(...)
- evidence: judo-runtime-core@b9bd93e8: no definition of createBusinessErrorException or ExceptionUtils in any module (rg across repo returns no match); exception classes live in judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/exception/

## BA-159 [wrong-fact] Exception table, line 102 and 120
- target: agent-docs/backend/error-handling-guide.md | src: agent-docs-review:backend.json | status: reported
- claim: GenericOperationErrorException (line 102) and BusinessErrorException (table row, line 120) are runtime exception types
- evidence: judo-runtime-core@b9bd93e8: no class named GenericOperationErrorException or BusinessErrorException in any module; existing runtime exceptions are judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/exception/{ValidationException,AccessDeniedException,NotFoundException}.java

## BA-160 [wrong-fact] PerformOperation example, line 42
- target: agent-docs/backend/error-handling-guide.md | src: agent-docs-review:backend.json | status: reported
- claim: @Component(service = PerformOperation.class) public class PerformOperationCustomImplementation implements PerformOperation
- evidence: judo-psm-generator-sdk-core@e4dd344: no PerformOperation type found; it is only valid if the example model defines an operation named PerformOperation

## BA-161 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/interceptors.md.hbs:391
- target: agent-docs/backend/interceptors.md | src: judo-ng-read | status: validated
- claim: In the doc's sample code (not compiled), if (!input.getAs(Boolean.class, ...)) unboxes the result; if the key is absent getAs returns null, 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/interceptors.md.hbs:391

## BA-162 [missing] Document that interceptors apply only to built-in operations
- target: agent-docs/backend/interceptors.md | src: session:jb-031.json | status: reported-unvalidated
- claim: Catalog interceptors.md does not say which operations are intercepted.
- fact: State that interceptors never fire for custom/SDK/script operations. Range interceptors fire only on _getRangeReference*/range calls. With several interceptors each preCall gets the original payload and sees peers' in-place mutations; the return value is last-non-null-wins (gap report S26-01, S05-03, S04-02).
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore, knowledge-gaps-report.md:270-272

## BA-163 [missing] Throwing a business error from an interceptor: InterceptorCallBusinessException
- target: agent-docs/backend/interceptors.md | src: session:jb-031.json | status: validated
- claim: Catalog interceptor examples throw raw RuntimeException (recaptcha-waf-interceptor/backend.md:19,26) or wrap GenericOperationErrorException in RuntimeException (interceptors.md:234,294,479). A raw RuntimeException gives a 500.
- fact: preCall/postCall are declared throws InterceptorCallBusinessException(String type, String errorCode, Map<String,Object> details, Throwable throwable, Locale locale), a BusinessException subclass (behaviours/InterceptorCallBusinessException.java:8-11). The dispatcher converts it to a _fault payload and then a BusinessException (DefaultDispatcher.java:764-771, 402-414). REST returns 422 with X-Fault: <type>, and a body {<type>: details without _-keys/nulls, code: errorCode}. Interceptors run inside the behaviour's transaction, so the throw rolls back the DAO write, including from postCall. Any other RuntimeException becomes InternalServerException and a 500. Locale is replaced by the dispatcher's locale. A generated checked <Fault>Exception cannot be thrown from an interceptor.
- evidence: session 2026-11-06T10-49-13-527Z part 31, subagent explore, RuntimeExceptionMapper.java:60-119

## BA-164 [missing] judo-doc-problems.md lists unapplied wrong facts for agent-docs
- target: agent-docs/backend/interceptors.md | src: session:jb-038.json | status: reported-unvalidated
- claim: Interceptors doc: reverse postCall order; example incomplete (getOperations / getIdOf); interceptor contract flags.
- fact: judo-doc-problems.md Part A sections include: interceptors run only on built-in operations, never custom/script operations; postCall in registration order; the contract of each flag; example missing getOperations/getIdOf; UI model values that break the generator; binary upload/download two-phase token flow; SYSTEM/non-principal actors (exposure, transfer-object closure, realm); multi-module build order and stale artifacts; JQL/derived-member rules that fail late; absent/null/empty SDK behaviour. Still to be applied to catalog/agent-docs.
- evidence: openspec/changes/restructure-blueprints-for-kb/judo-doc-problems.md headings (lines ~452-483)

## BA-165 [missing] Write guards must live in custom operations; range interceptors only on _getRangeReference
- target: agent-docs/backend/interceptors.md | src: session:sweep-012.json | status: reported-unvalidated
- claim: (n/a)
- fact: Custom and MAPPED ops (User.toggleActive, createUser, resendInvitation) bypass interceptors; range interceptors only fire on _getRangeReference* not plain list ops; multiple interceptors for same operation see each other's in-place payload mutations, return last-non-null-wins; range interceptors are the security boundary for rangeType=ANY lean TOs; model min/max range bounds are UI-only.
- evidence: judo-doc-problems.md Part B; session S26

## BA-166 [wrong-fact] Interceptor API claims in agent-docs backend/interceptors
- target: agent-docs/backend/interceptors.md | src: session:jb-019.json | status: reported-unvalidated
- claim: `@Override public List<String> getOperations()` (no-arg); `@Override public Payload postCall(Payload result, ...)`; interface snippet lists only getName, getOperations(AsmModel), preCall, postCall with no throws clause
- fact: Pass-1 review findings BE-001/BE-002 (wrong, high) and BE-003 (outdated): getOperations takes AsmModel, postCall signature differs, throws clauses exist. BE-004: doc never describes async, terminateOnException or ignoreDecoratedCall behaviour. The postCall ordering claim (reverse order) was also flagged. Same wrong getOperations() appears in 1 agent-doc, 1 best practice, 4 blueprints.
- evidence: session 2026-11-06T08:27:30, agent-docs-review/review.md BE-001..BE-004; grep counts

## BA-167 [wrong-fact] postCall runs in registration order, not reverse
- target: agent-docs/backend/interceptors.md | src: session:jb-038.json | status: reported-unvalidated
- claim: Interceptors are invoked in reverse order for postCall.
- fact: postCall is dispatched in registration order, not reverse. The agent-docs interceptors.md still carries the wrong claim, and openspec judo-doc-problems.md Part A lists it. The blueprint operation-call-logging-interceptor already says registration order.
- evidence: openspec/changes/restructure-blueprints-for-kb/judo-doc-problems.md, 'postCall runs in registration order, not reverse'; session line ~290

## BA-168 [wrong-fact] Interceptors run only for built-in operations, not custom/script operations
- target: agent-docs/backend/interceptors.md | src: session:sweep-012.json | status: validated
- claim: Interface Javadoc: supports script operations and SDK implementations; empty getOperations means all operation calls intercepted.
- fact: OperationCallInterceptors fire only on built-in behaviour operations (create, update, delete, list, refresh, set/add/remove reference, range, getTemplate, export, validate). Custom (SDK), MAPPED and script operations never hit interceptors (all 20 call sites in behaviours/*Call.java; DefaultDispatcher.java:716-737). Guards for custom ops must be inside each *CustomImplementation. Javadoc is wrong too.
- evidence: DefaultDispatcher.java:716-737; Rackinspect session out/S26.json:9

## BA-169 [wrong-fact] Interceptors cannot throw the generated fault; wrap in InterceptorCallBusinessException
- target: agent-docs/backend/interceptors.md | src: session:sweep-012.json | status: validated
- claim: Interceptor examples throw <Fault>Exception/RuntimeException.
- fact: preCall/postCall declare throws InterceptorCallBusinessException only; <Fault>Exception is checked so it won't compile. Use new InterceptorCallBusinessException(type, errorCode, Map details, cause, locale): dispatcher converts to BusinessException -> 422 + X-Fault header; frontend fault dialog translates details by faults.<type>.<attribute>; runs in the operation transaction (rollback). Recommended: type = modeled fault FQN (Rackinspect uses guard name, so no translation matches and it had to override frontend). type/details not validated against model (typo falls back to raw attribute names); null details NPEs in mapper.
- evidence: DefaultDispatcher.java:764-770,402-414; RuntimeExceptionMapper.java; session 13:11 assistant

## BA-170 [wrong-fact] Interceptor example (MyTransientEnricher), line 32
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: @Override public List<String> getOperations() - no-arg method returning List<String>
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/OperationCallInterceptor.java:34

## BA-171 [wrong-fact] Interceptor example (MyTransientEnricher), line 36
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: @Override public Payload postCall(Payload result, ...)
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/OperationCallInterceptor.java:83

## BA-172 [wrong-fact] OperationCallInterceptor Interface (line ~137)
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: Interface snippet lists only getName, getOperations(AsmModel), preCall, postCall with no throws clause
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/OperationCallInterceptor.java:44

## BA-173 [wrong-fact] OperationCallInterceptor Interface
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: Doc never describes async, terminateOnException or ignoreDecoratedCall behaviour
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/OperationCallInterceptor.java:38-60

## BA-174 [wrong-fact] Authentication/Interceptor example, line 472
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: @Reference AccessValidationDao accessValidationDao;
- evidence: judo-runtime-core@b9bd93e8: no class or interface AccessValidationDao defined in any module (rg across repo returns no match)

## BA-175 [wrong-fact] Ancillary ServiceContext operation reference, line 224
- target: agent-docs/backend/interceptors.md | src: agent-docs-review:backend.json | status: reported
- claim: asmUtils.resolveOperation('<model>.services.ServiceContext#_createInstanceEntities')
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/ServiceContext.java:19 (class exists; the _createInstanceEntities operation is model-generated and was not found in the sources checked)

## BA-176 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/internationalization-guide.md.hbs:172
- target: agent-docs/backend/internationalization-guide.md | src: judo-ng-read | status: validated
- claim: The duplicate check queries EnumerationFilter.equalTo(RecordingMethod.AUTO), but the same operation creates records with RecordingMethod.MAN
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/internationalization-guide.md.hbs:172

## BA-177 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/internationalization-guide.md.hbs:197
- target: agent-docs/backend/internationalization-guide.md | src: judo-ng-read | status: validated
- claim: The check rejects amounts where compareTo(BigDecimal.ONE) < 0, i.e. values below 1, but the error reported is value_must_be_positive_number,
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/internationalization-guide.md.hbs:197

## BA-178 [wrong-fact] Custom data type registration, line ~166
- target: agent-docs/backend/patterns-and-best-practices.md | src: agent-docs-review:backend.json | status: reported
- claim: @Reference(target = '(judo.model.name=...)') on DataTypeManager
- evidence: judo-runtime-core@b9bd93e8:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/core/DataTypeManagerProvider.java:29 (provider exists; its service properties not checked)

## BA-179 [missing] Signed identifier cannot be minted by client/server code
- target: agent-docs/backend/signed-identifiers.md | src: session:jb-020.json | status: reported-unvalidated
- fact: The runtime only mints a __signedIdentifier while serving a REST response; there is no reachable plain mint API. Code needing a ticket's __signedIdentifier cannot create one itself. Signed ids can differ from locally stored ones when the JUDO side updates the entity (signed id changes after update). Propose new agent-docs/backend/signed-identifiers.md, linked from frontend/advanced-patterns.md.
- evidence: session judo-cli-sessions 2026-09-19T17-24-47 and 2026-08-05T13-50 (S01-04), agent

## BA-180 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/testing-guide.md.hbs:87
- target: agent-docs/backend/testing-guide.md | src: judo-ng-read | status: validated
- claim: Integration tests run with mvn clean install -Pintegration-tests (an integration-tests Maven profile).
- fact: No pom template in this repository defines a profile with id integration-tests; the profiles that exist are build-model, build-schema, build
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/testing-guide.md.hbs:87

## BA-181 [wrong-fact] Test example, line 32
- target: agent-docs/backend/testing-guide.md | src: agent-docs-review:backend.json | status: reported
- claim: private AccessValidationDao accessValidationDao;
- evidence: judo-runtime-core@b9bd93e8: no class or interface AccessValidationDao defined in any module (rg across repo returns no match)

