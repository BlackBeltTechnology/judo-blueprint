# Missing knowledge: agent-docs, best practices, model blueprints

What the catalog does not contain at all, as opposed to what it contains but search fails to find. Each item is backed by judo-ng source or by real development sessions, and was checked against all 565 catalog files.

`catalog-update-report.md` covers what is **wrong** in the catalog. This report covers what is **missing**.

## 1. Summary

- **324 validated gaps in 72 topics.** Of 420 mined candidates, 16 were already covered (a findability issue), 79 are not needed by application developers, and 1 could not be verified. They are listed in section 6.
- **The biggest holes are platform runtime behaviour that developers had to dig for:**
  - signed identifiers;
  - optimistic locking;
  - the REST contract;
  - the upload-token flow;
  - interceptor scope;
  - time zones;
  - which DAO calls surprise you.

  Developers in the sessions read jars and generated code to learn these.
- **The model languages have no reference.** There is no JQL function table (temporal, collection, aggregation, string), no JCL reference, and no list of the derived-member rules that only fail at build or run time.
- **Model changes break the frontend in ways nobody documented.** Renaming or removing attributes and operations breaks custom TS, leaves stale hooks, and some UI-model values break the generator. This is one of the most frequent session themes.
- **Configuration that every production app needs is absent:**
  - MUI license;
  - Jasypt `ENC()` secrets;
  - the Keycloak login theme;
  - a stable identifier-signer secret;
  - S3/GCS filestore settings;
  - CORS;
  - local mail testing.
- **Testing knowledge is thin.** The catalog does not cover:
  - testkit caching (`BY_CLASS`, `shareInjector`);
  - choosing the test DB (PostgreSQL/Yugabyte containers);
  - API-level tests;
  - multi-JVM heap failures that silently skip classes;
  - an E2E baseline-dump method.
- **Domain knowledge:** seven reusable domains from the rackinspect sessions have no blueprint:
  - inspection fault registry / ticketing;
  - offer pricing;
  - job sheet → work report → certificate;
  - partner-scoped multi-role users;
  - offline mobile ingest;
  - typed media attachments;
  - retention.

  They come from one project, so they must be generalised before they become blueprints.

| Target | High | Medium | Low |
|---|---|---|---|
| agent-docs | 25 | 18 | 6 |
| best-practices | 8 | 7 | 0 |
| model-blueprints | 6 | 1 | 0 |
| cli | 1 | 0 | 0 |

**Priority:**
- **High:** seen in at least 3 sessions, or at least 6 independent findings.
- **Medium:** seen in 1 or 2 sessions, or at least 3 findings.
- **Low:** the rest.

### Scope decisions needed

Three topics only matter if the catalog targets that stack:
- **JSL** (textual model language);
- **Spring Boot** runtime;
- **Flutter** frontend.

The current catalog is ESM / Karaf / React. Decide before writing them.

### How to read an item

Each topic gives four things:
- the priority and its evidence;
- where the knowledge should go;
- what the catalog has today, when there is a partial mention;
- the facts to add.

Every fact keeps its gap id (`P..` = judo-ng platform source, `S..` = session logs). Look the id up in `target/gap-mining/all_gaps.json` for the full text, evidence citations and the miner's catalog searches.

## Method

1. **Mining.** 60 parallel read-only subagents on `@free` (`inception/mercury-3`) did the mining:
   - 34 subagents read the validated judo-ng digests of 103 repos. Agent tooling, tests and changelogs were stripped first.
   - 26 subagents read condensed logs of 544 development sessions (rackinspect and judo-cli).

   The condensed logs keep user messages, catalog lookups, digs into jars, generated code or platform source, and agent statements admitting missing knowledge. Each miner had to search the catalog with at least 3 terms before keeping a gap.
2. **Validation.** I validated the gaps myself in the main session, with no subagents:
   - **Evidence:** 419 of 420 cited sources resolve, either to a real judo-ng file near the cited line or to a quote in the session logs.
   - **Absence:** every identifier in each gap was searched across all 565 catalog files. About 60 topics also got concept-level searches, and 25 partial hits were read in full to decide covered, mention-only or missing.
   - **Truth:** I checked a sample of 10 platform claims against the source. All 10 held, e.g. `UpdatePayloadDaoProcessor` checking `__version`, the `getUploadTokenFor<Field>` generation, `VITE_MUI_LICENSE_KEY`, `AcceptableClientsParser`, the JSL `event` grammar, `StaticNavigation`, the `dialect`/`container` test properties, and `ENC(...)`.
   - **Relevance:** I removed platform internals and one-project specifics.
3. **Grouping.** Duplicates and near-duplicates were grouped into topics; the verdicts are in `target/gap-mining/verdicts.py`.

### Limits

- Session counts come from the miners and may overcount.
- The session corpus is two developers on one project.
- The fact text is the miner's wording; only the sampled claims were checked against source line by line.
- Confirm each topic against source when you write the entry, as the catalog's own validation rule requires.

## 2. agent-docs: missing platform knowledge

### Generated DAO/SDK behaviour that surprises developers (known issues)

- **Priority:** High · **Area:** backend · **Evidence:** 12 session(s); judo-ng: `judo-psm-generator-sdk-core`, `judo-dao-api`
- **Put it in:** agent-docs/backend/data-access-guide.md (known issues)
- **What to add:**
  - **Generated relation-setter DAOs NPE on null relatedObject** (how-to, `S01-06`). Generated JUDO DAO relation setters (e.g. `setErrorReplacement(entity, relatedObject)`) call `relatedObject.identifier()` unconditionally, so passing `null` throws a NullPointerException.
  - **Querying an enumeration-typed relation can return raw Integer (ClassCastException)** (how-to, `S19-08`). When a generated relation/navigation returns an enumeration-typed value (e.g. partnerAffiliation), the runtime may deliver it as a raw Integer ordinal rather than the enum instance, producing ClassCastException in the generated DAO impl if you treat the result as the enum.
  - **Querying unset/null optional booleans with BooleanFilter** (how-to, `S19-01`). JUDO's generated DAO BooleanFilter only exposes isTrue()/isFalse() — there is no "is unset" filter for an optional (nullable) boolean column. To detect faults where an optional boolean (e.g.
  - **Querying unset/null booleans: no is-unset filter** (how-to, `S24-04`). The SDK BooleanFilter only exposes isTrue() and isFalse() — there is no "is unset" filter for optional/ nullable booleans.
  - **Derived attribute traversing an inherited member makes the RDBMS query generator emit a missing JOIN** (pattern, `S12-05`). A derived attribute that navigates through an inherited attribute can break JUDO's RDBMS query generator: `lastWorkReport : Binary = self.workReports!any().lastDocument.document` (where `lastDocument` is inherited on `Task`, not declared on `WorkReport`) produced SQL that joined the …
  - **required="true" model attribute exposes a plain getter (no Optional/null-guard)** (mention-only, `S10-03`). For a model attribute declared `required="true"`, the generated service input/transfer class exposes a plain non-`Optional` getter (e.g. `Boolean getMinimumOfferPriceEnabled()`), so a null read means the caller omitted the field - not that it is a valid empty value.
  - **Generated SDK TO accessors: required=false Optional getters, DTO-direct context vs Map, Optional handled in helpers** (how-to, `S16-05`). JUDO generated transfer-object accessors follow the model's required flag: a required attribute generates a plain-typed getter (e.g. getReviewReportTemplate(): FileType), while a non-required (optional) attribute generates Optional<T> (e.g. getReviewReportMarkdownTemplate(): Optional<FileType>).
  - **Static (unmapped) data and navigation accessors** (how-to, `P32-04`). Unmapped attributes and relations are served through generated static-data DAO interfaces: the static query data interface exposes selectValue() (or selectValue(<parameter>) when the query has a parameter) returning the attribute's primitive/static type, and static navigations expose query() (collection) or selectOne() (single) with parameter overloads when hasParam.
  - **Payload transfer-object library (factories, typed accessors, transient keys)** (how-to, `P11-07`). Payload is a Map<String,Object> data-transfer type with static factories (asPayload(map), map(String k1, Object v1, ...) overloads for 1-20 pairs, map(Entry...), entry) and typed accessors (getAs(Class<T>, String), getAsCollectionPayload(String), getAsPayload(String)).
  - **Mapped vs unmapped transfer-object API surface boundaries** (how-to, `P32-05`). The generated DAO interface only emits full CRUD on mapped, non-abstract types: create/createAll (with and without Mask), getById/existsById/getAll/countAll/delete, query() and per-relation create/set/unset/add/remove/range methods are all gated behind self.isMapped (plus relation allowed-operation …

### UI model values that break the generator (known issues)

- **Priority:** High · **Area:** frontend · **Evidence:** 11 session(s)
- **Put it in:** agent-docs/frontend/esm-to-ui-mappings/ (known issues)
- **What to add:**
  - **UI widget/layout values that break the generator (SWITCH widget, TabRef columns on unmapped input TOs, ActionGroup-wrapped OperationForms)** (how-to, `S12-06`). Several ESM UI-layer values silently break frontend generation: `booleanWidget: "SWITCH"` does not exist (the Handlebars generator has no `switch.hbs` partial, so use `CHECKBOX`/`COMBO`);
  - **Misleading UiValidationException "All constraints have been satisfied" gives zero diagnostics; binary-search UI layout groups** (how-to, `S12-04`). A frontend model/build failure can surface as `UiValidationException: All constraints have been satisfied` — an ERROR that reports no actual failed constraint, forcing a slow bisect.
  - **Self-referential/recursive relation pages drop targetPageDefinition, NPE'ing the React generator** (pattern, `S12-01`). The ESM→UI ETL (Esm2UiWork) drops `targetPageDefinition` on actions transcluded into self-referential page contexts: when a relation is recursive (e.g.
  - **Operation generator gotchas: output type matching view root breaks frontend; explicit <faults> needed for throws BusinessErrorException** (how-to, `S09-01`). In JUDO, an operation whose `output` DTO matches the action-container view's root type makes the frontend generator emit references to a non-existent `*OutputView` dialog (e.g. openServicesOffer_servicesOfferOffer_View_EditUpdateOfferDetailsOutputView), breaking the TS build;
  - **TabularReferenceField with representationComponent="button" still requires <columns>** (how-to, `S11-09`). A TabularReferenceField rendered as a button (representationComponent="button") still triggers the validator warning 'Columns are not defined for viewable table' unless its <columns> are populated in the model; the button representation does not remove the columns requirement.
  - **Frontend action-hook pitfalls: clearing fields & dialog reopen traps** (pattern, `S24-08`). In custom action hooks, clearing an optional field via storeDiff('field', undefined) can wipe a default value the form relies on — re-assign the default when intentionally clearing.

### Binary upload/download: two-phase token flow

- **Priority:** High · **Area:** integration · **Evidence:** 8 session(s); judo-ng: `osgi-filestore`, `judo-tatami-jsl`, `judo-ui-typescript-rest-template`, `judo-ui-react-template`
- **Put it in:** agent-docs/backend/file-upload-download.md (new); best-practices/backend/filestore-mediated-file-transfer.md links to it
- **Catalog today:** No file mentions an upload token. `FileStoreService` is used in project patterns only.
- **What to add:**
  - **Binary upload-token capability (getUploadTokenFor operation and UploadToken type)** (topic, `P22-02`). A transfer field that reads and maps a binary (BinaryType) primitive on a create-capable transfer automatically gets a `getUploadTokenFor<Field>` unbound operation (GET_UPLOAD_TOKEN behaviour) returning a synthesized `UploadToken` unmapped transfer object type holding one required `token` string attribute (UploadTokenStringType, maxLength 2048).
  - **Binary file upload/download two-phase token flow** (how-to, `P33-03`). File upload/download over REST is a two-phase, token-gated protocol: uploadFile first POSTs '<attributePath>/~upload-token' to obtain a token, then POSTs multipart data to the upload path with an X-Token header;
  - **JUDO's authenticated two-phase file upload: token issuance, servlet claims, and FileType transfer-serialization** (how-to, `S23-02`). Binary upload is a two-phase JWT flow: the client obtains an upload token (GetUploadTokenCall payload, claims named FILE_ID → JWT `sub`, FILE_NAME → `fileName`, FILE_MIME_TYPE, FILE_SIZE) from the filestore TokenIssuer, then POSTs the file to the filestore servlet which validates the token and MIME type and returns JSON file metadata;
  - **Filestore upload token flow and concurrency safety internals** (how-to, `S26-06`). The file-upload path uses GetUploadTokenCall (which issues a signed upload token via TokenIssuer, key __uploadToken), the Filestore UploadServlet (tokenRequired, maxSize/maxFileSize, noDataTimeout, uploadDelay, CORS processor), and DefaultTokenIssuer (JWT algorithm, keyProvider, expectedIssuers, expirationTimeInMinutes).
  - **Filestore HTTP upload/download servlets and JWT token security** (how-to, `P27-04`). UploadServlet and DownloadServlet register at a required servletPath and secure file transfers with JWTs carried in the X-Token header. The security stack: DefaultKeyProvider dispatches on algorithm prefix HS/RS/PS/ES and reads config 'secret' (base64 HMAC) or 'keys' (base64 JWK);
  - **Filestore hardened security defaults (token expiry, clock skew, CORS)** (domain, `S21-04`). The hardened filestore servlet/token defaults: token expiry defaults to 1440 minutes, allowedClockSkew defaults to 60 s, and a wildcard CORS origin is no longer allowed to grant credentials.
  - **FileStoreService.put() sizes the BLOB from InputStream.available() — buffering/streaming gotcha** (how-to, `S16-03`). JUDO's RdbmsFileStoreService.put(InputStream, fileName, mimeType) does NOT buffer the stream; it stores the InputStream by reference and records size = in.available() (narrowed to int), then writes via LobCreator.setBlobAsBinaryStream(ps, 6, stream, len).

### SYSTEM / non-principal actors: exposure, transfer-object closure, realm

- **Priority:** High · **Area:** security · **Evidence:** 10 session(s)
- **Put it in:** agent-docs/model/system-actors.md (new)
- **What to add:**
  - **Authorizing a SYSTEM/non-principal actor: bound-operation gating via exposedBy on the producing TO** (pattern, `S03-01`). To restrict an AI/system actor in JUDO you must understand how operations are actually gated: a bound operation like deleteRack is NOT reached through an access at all — it lives on the mapped transfer object (services/rack_service/Rack/~deleteRack) and its guard tests `exposedBy` on the producing TO, not the access getter and not the CRUD flags.
  - **Transfer-object closure decision procedure: when a restricted actor needs a NEW TO vs reusing an existing one** (how-to, `S03-02`). There is a repeatable decision procedure for whether an AI/system actor can reuse an existing transfer object input/output or needs a new one: enumerate the operation closure of the candidate TO (its own ops plus ops reachable through its relations and derived relations), and if that closure contains any mutating operation (delete/update/remove, e.g.
  - **Modeling a non-principal SYSTEM actor: realm=DEFAULT behavior, no menu items, no principal** (topic, `S03-07`). A SYSTEM actor without a principal (e.g.

### Multi-module build order and stale artifacts

- **Priority:** High · **Area:** deployment · **Evidence:** 10 session(s)
- **Put it in:** agent-docs/deployment/build-process.md (troubleshooting)
- **What to add:**
  - **Multi-module JUDO reactor: install model+schema before sdk; use -pl with -o and validateModels=false** (how-to, `S17-05`). A JUDO application is a Maven reactor of interdependent modules (model, schema, sdk, internal, app, common). Installing a single module (e.g. sdk) standalone fails with 'Could not collect dependencies ...
  - **Stale ~/.m2 model jar poisons the backend chain; mvnd may print BUILD SUCCESS while installing stale jars** (how-to, `S04-01`). In a multi-module JUDO build, the SDK pom regenerates at `generate-sources` FROM the installed model jar in `~/.m2`, not from the edited model source.
  - **Stale Maven SNAPSHOT jars in ~/.m2 vs generated sources; rebuild with ./judo.sh build -i** (how-to, `S05-05`). Tests can pass while the installed SNAPSHOT jars in ~/.m2 are stale — so unit tests compiled against fresh generated sources behave differently from the artifacts actually run.

### JQL/derived-member rules that fail late

- **Priority:** High · **Area:** model · **Evidence:** 5 session(s); judo-ng: `judo-jql-ide-eclipse`, `judo-tatami-base`, `judo-tatami-client`, `judo-platform`
- **Put it in:** agent-docs/model/jql-reference.md (rules and late failures)
- **What to add:**
  - **JQL: derived relation getter cannot reference `self` inside a global EntityType!filter lambda** (how-to, `S16-02`). A DERIVED relation getter CANNOT reference `self` inside a global `EntityType!filter(x | ... == self)` lambda — the Maven judo-tatami builder fails with 'Unknown symbol: self'.
  - **Derived attribute expression must not reference another derived attribute; editable derived via mapped transfer** (how-to, `S22-04`). A derived attribute's getter expression should not point to another derived attribute, a chained derived can be a performance killer. Derived attributes are read-only;
  - **Derived single-valued relation requires !any() narrowing** (how-to, `P12-04`). A DERIVED relation/aggregation with upper bound 1 must append '!any()' to its getter expression (narrowResult) so the member yields a single element instead of a collection; upper -1 collections get no suffix. Failing to narrow yields a collection where the model expects a scalar.
  - **JQL cannot filter a collection/contained child by its own id — need a derived container back-reference or native lookup** (mention-only, `S08-06`). The generated QueryCustomizer cannot filter a parent list by a contained child's identifier (no navigation inside filterBy, no typed relation filter).
  - **Model-annotation-driven derived field semantics (changeable vs read-only)** (how-to, `P19-08`). Derived PSM accessors become ASM EAttributes/EReferences with derived=true, volatile=true, and changeable only when a setterExpression exists (PrimitiveAccessor setter, or a binding to an Attribute/PrimitiveAccessor with a setter).
  - **What makes an attribute/relation orderable and filterable (capability rules)** (how-to, `P20-04`). Ordering and filtering are only available on references whose target is mapped and has at least one non-TRANSIENT attribute of a supported type: orderable attributes are string/numeric/date/timestamp/time/boolean; filterable adds enumeration; TRANSIENT members are excluded from both.
  - **Conditional confirmation condition: EVL requires a boolean attribute of the ROOT type (and the selector may list sibling entities)** (how-to, `S08-05`). When wiring a CONDITIONAL operation-form confirmation, the ESM `confirmationCondition` must be a boolean attribute that belongs to the operation's root type; otherwise model validation fails with 'Confirmation condition must be an attribute of the root type' (e.g.
  - **Design-time JQL expression validation contract (which members require which expression)** (mention-only, `P02-03`). The JUDO Designer validates model expressions with EVL constraints, each tied to a member kind: GetterExpressionIsValid runs on a DataMember only when memberType is DERIVED;

### Platform error codes and payload-validation semantics

- **Priority:** High · **Area:** backend · **Evidence:** 6 session(s); judo-ng: `judo-platform`, `osgi-validator`
- **Put it in:** agent-docs/backend/error-handling-guide.md (platform error-code table)
- **Catalog today:** error-code-enum is a project blueprint; no platform error-code list.
- **What to add:**
  - **Missing API error codes (actor-bound ops, optional params, ranges)** (topic, `P12-08`). The runtime returns specific error codes not present in the catalog's error reference: AUTHENTICATED_ENTITY_NOT_FOUND (403), ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION (403), MISSING_REQUIRED_PARAMETER (400) and NOT_ACCEPTED_BY_RANGE (400).
  - **Runtime payload validation semantics: required relations vs required attributes, and which relations are skipped** (how-to, `S06-01`). The generated runtime validator (DefaultPayloadValidator) enforces required fields during update/create: a mandatory attribute raises `MISSING_REQUIRED_ATTRIBUTE`, a mandatory one-way relation raises `MISSING_REQUIRED_RELATION` (carrying `__referenceId`), and DERIVED reference members are skipped by update validation while embedded references are traversed.
  - **ValidationException multi-result vs single-fault error shape** (how-to, `S01-07`). A JUDO ValidationException can carry multiple ValidationResults, but if a custom operation swallows it and rethrows a single-fault BusinessError (e.g. `createFaultRegistryUploadError`), the per-row gap list is lost.
  - **Runtime validation-message interpolation and localization (Hibernate MessageInterpolator pipeline)** (how-to, `P29-03`). JUDO delegates bean validation to a Hibernate Validator OSGi component whose MessageInterpolator resolves each validation message at runtime: I18nService.getTemplate(message) returns the localized template (raw message used as-is when it returns null), then it interpolates parameter tokens like …
  - **JUDO dispatcher refuses operations on immutable bound instances (AccessDeniedException)** (pattern, `S05-01`). The JUDO dispatcher signs bound-instance identifiers and carries an `immutable` flag inside the signed identifier.

### Custom operation runtime contract (no impl bundle, customImplementation=false, stateful ops)

- **Priority:** High · **Area:** backend · **Evidence:** 5 session(s); judo-ng: `judo-meta-esm`, `judo-tatami-base`, `judo-meta-psm`, `judo-runtime-core`
- **Put it in:** agent-docs/backend/custom-operations.md
- **What to add:**
  - **Custom-operation implementation with no impl bundle: runtime behavior undocumented; modeled fault must be declared to compile a checked BusinessErrorException** (topic, `S02-02`). For a custom-implementation operation whose implementation bundle is absent (not generated/registered), there is no documented behavior — the agent could not assume safe failure.
  - **customImplementation=false footgun: default body is only a //sdk comment so the operation silently runs and does nothing** (how-to, `S18-03`). When an operation is modeled with customImplementation=false and no Java implementation pair is written, the generated body is just a //sdk comment placeholder with an empty fallback; the operation therefore starts and returns successfully doing nothing, which is easy to misread as implemented.
  - **Stateless vs stateful operation guard and context keys** (how-to, `P15-06`). Operations model a stateful flag (operation.md: stateful=true means the operation can modify system state; false means a query with no side effects).
  - **Stateful operation semantics driven by behaviour type and implementation** (how-to, `P19-09`). An operation's `stateful` EAnnotation is produced from mutually exclusive rules: with an implementation it reflects implementation.isStateful();
  - **Bound operation implementation rules (stateful and parameter compatibility)** (how-to, `P08-08`). A bound operation binding to an entity operation must keep parameters compatible with every inherited operation of the same name (psmUtils.parametersAreCompatible); overriding an inherited operation must keep parameters compatible.
  - **Operation naming and shape constraints (reserved getter/setter names, stateful, initializer, fault cardinality)** (how-to, `P03-06`). Operation names may not equal 'set'/'get' + an attribute or relation name (case-insensitive) because those are reserved for generated accessors; an INSTANCE operation's stateful flag must match every inherited non-abstract operation of the same name;

### Principal-to-actor resolution and multi-client Keycloak mapping

- **Priority:** High · **Area:** security · **Evidence:** 3 session(s); judo-ng: `judo-runtime-core`, `judo-services`, `judo-tatami-base`, `judo-platform`
- **Put it in:** agent-docs/backend/authentication-guide.md
- **What to add:**
  - **Actor resolution claim-mapping lookup order and checkMappedActors** (how-to, `P15-08`). DefaultActorResolver maps a JudoPrincipal to an actor entity. getActorByClaims picks the lookup attribute in this order: the USERNAME-claim attribute if its claim is present, then the EMAIL-claim attribute, then the first identifier attribute (sorted by name) present in claims;
  - **ActorResolver SPI: custom principal-to-actor resolution** (how-to, `P16-02`). ActorResolver is the security SPI that maps an authenticated JudoPrincipal or token claims to a persisted actor Payload.
  - **Engine principal-to-actor resolution (getActorByClaims) and its latency** (topic, `S19-02`). Under the hood the dispatcher resolves an authenticated principal into the actor payload via DefaultActorResolver.getActorByClaims: it picks the actor type EClass, finds the attribute annotated with claim=USERNAME, then calls dao.search(...) on that actor type with the claim value — the actor (and its DB read) is resolved on every principal-bearing request.
  - **Multi-client Keycloak whitelist (JUDO_PLATFORM_ACCEPTABLE_CLIENTS)** (how-to, `P18-02`). When several Keycloak clients (frontends) authenticate against the same realm, JUDO maps the token's azp claim to an actor type. By default the client name is derived from azp by replacing '-' with '.'; if a frontend client's name does not match an actor FQN, the actor cannot be resolved.
  - **Per-model Keycloak connector configuration: acceptableClients actor-to-client map, access types, and user-manager toggle** (how-to, `P14-03`). The KeycloakSecurityActivator creates per-Keycloak-model components whose config keys include serverUrl, publicUrl, adminUser, adminPassword, clientSecret (on KeycloakConnectorComponent) and updateExistingUsers, requiredActions, enabled (on KeycloakUserManagerComponent).
  - **Keycloak runtime connector, realm and client-type configuration** (how-to, `P21-06`). The runtime Keycloak integration is configured per model: KeycloakConnectorComponent takes serverUrl, publicUrl, adminUser, adminPassword (PASSWORD), clientSecret (optional). Management components are only provisioned when managementEnabled=true (default false, connector-only).
  - **Keycloak client access-type and user-provisioning defaults** (how-to, `P18-08`). The KeycloakRealmSynchronizer provisions realms/clients from the keycloak metamodel with defaults: systemDefaultAccessType=CONFIDENTIAL for system actors and humanDefaultSystemAccessType=BEARER_ONLY for actors with @actorType kind HUMAN (a client's own publicClient/bearerOnly overrides).
  - **Model-annotation-driven Keycloak realm/client generation and claim mapping** (how-to, `P19-05`). The ASM→Keycloak transformation generates Keycloak realms and clients from the model itself: each distinct non-blank `realm` EAnnotation value across actor types becomes a realm (id=realm, enabled, loginWithEmailAllowed), and each actor type with a realm annotation becomes a client …
  - **Keycloak realm synchronization and auto-provisioning from the model** (topic, `P16-09`). JudoKeycloakModule wires a KeycloakRealmSynchronizer as an eager singleton, so synchronizeAllRealms() runs when the injector is created: realms, clients and users are provisioned from the model's asm2keycloak trace.
  - **Keycloak-managed user sync: user in Keycloak but missing from DB** (topic, `S19-03`). For a managed actor (HUMAN, managed=true) the runtime bridges Keycloak and the entity store through UserManager/UserManagedWrappedDao: the Keycloak user is the source and the DB row is created/synced via the wrapped DAO (with password policy checks, required actions, and convertPrincipalToActor mapping).

### JUDO testkit: runtime caching, DB selection, fixtures, Guice composition

- **Priority:** High · **Area:** testing · **Evidence:** 3 session(s); judo-ng: `judo-runtime-core-jsl`, `judo-runtime-core`, `osgi-utils`
- **Put it in:** agent-docs/integration-testing/getting-started.md + best-practices.md
- **Catalog today:** `JudoRuntimeFixture` is used; caching, `shareInjector` and DB selection are not documented.
- **What to add:**
  - **@JudoTest runtime caching (shareInjector, BY_CLASS/SINGLETON)** (how-to, `P15-05`). The @JudoTest testkit supports caching the derived runtime (QueryFactory, Liquibase execution, Guice Injector) across test methods via the boolean shareInjector() element (default false), active only for class-level BY_CLASS and SINGLETON test modes;
  - **Testkit runtime caching and env-var overrides for @JudoTest** (how-to, `P16-07`). The testkit caches heavy runtime components for speed: @JudoTest.shareInjector (default false) is only honoured for class-level dataSourceMode BY_CLASS or SINGLETON, and only when true are the Injector, QueryFactory, Liquibase executor and TxManager reused across methods.
  - **Modern JUDO integration-testkit configuration and performance (BY_CLASS, shareInjector, model-runtime cache)** (how-to, `S23-03`). The current `@JudoTest` testkit (judo-runtime-core-guice-testkit) has datasource modes BY_METHOD / BY_CLASS / SINGLETON and a `shareInjector` opt-in;
  - **Selecting the integration-test database via system properties (dialect/container/tz)** (how-to, `P17-02`). JudoDatasourceFixture selects the test database from system properties: `dialect` (hsqldb default | postgresql), `container` (none | yugabytedb, valid only with postgresql), and `tz` (default GMT). Only hsqldb and postgresql are accepted; anything else throws IllegalStateException.
  - **YugabyteDB / PostgreSQL TestContainers in JUDO test fixtures** (how-to, `P17-03`). Integration tests can run against a YugabyteDB container via `YugabytedbSQLContainer` (image `yugabytedb/yugabyte:2.1.8.2-b1`, PostgreSQL wire protocol, port 5433, default db/user/password `yugabyte`, fluent overrides withDatabaseName/withUsername/withPassword). Postgres tests use TestContainers.
  - **Running JUDO integration tests against real PostgreSQL via testcontainers for production-representative measurements** (how-to, `S20-02`). To reproduce production behavior (e.g. init/import timing), run JUDO @JudoTest suites against a real PostgreSQL using testcontainers (set the dialect, use the guice-testkit container support) instead of only the default in-memory HSQLDB.
  - **JUDO integration-test fixture transaction/savepoint semantics and silent failures** (pattern, `P17-06`). The JUDO test fixtures have important edge behavior: JudoDatasourceByClassExtension/SingletonExtension commit a PROPAGATION_MANDATORY transaction in afterEach and swallow any exception in an empty catch; afterAll teardown is a no-op in the singleton extension;
  - **Guice injector composition in tests (Modules.combine, init(module, testInstance))** (how-to, `P17-07`). JudoRuntimeFixture builds the Guice injector via `Modules.combine(module, judoDefaultModule, databaseModule)` and `init(Module, Object injectModulesTo)` injects fields into the test instance.
  - **Mocking environment variables in integration tests (EnvironmentVariableMocker / SystemStubs)** (pattern, `P17-04`). JUDO provides test utilities to override `System.getenv()`: `EnvironmentVariableMocker` (static mock over `java.lang.ProcessEnvironment`, with initMocked/deinitMocked, a stack of replacement maps via connect/pop/remove) and `EnvironmentVariables` (a SystemStubs resource with fluent `and(name,value)` / `set(name,value)`, activated in doSetup and removed in doTeardown).
  - **Unit-testing OSGi Declarative Services components without a running container (MockOsgi/BeanUtil)** (how-to, `P29-04`). The osgi-test library (osgi-utils) provides MockOsgi and BeanUtil to drive OSGi DS component lifecycle headlessly: MockOsgi.activate/deactivate invoke @Activate/@Deactivate methods via reflection, resolving parameter types (none, BundleContext, ComponentContext, Map/Dictionary), and …

### Signed identifiers: lifecycle, churn and secret

- **Priority:** High · **Area:** backend · **Evidence:** 4 session(s); judo-ng: `judo-runtime-core`, `documentation`
- **Put it in:** agent-docs/backend/signed-identifiers.md (new); link from frontend/advanced-patterns.md
- **Catalog today:** `__signedIdentifier` is used in frontend code samples; nothing says it changes on update, cannot be minted, or needs a stable secret.
- **What to add:**
  - **Signed identifier stability requires a configured @IdentifierSignerSecret** (how-to, `P16-04`). Entity identifiers exposed to clients are JWT/HMAC-signed (DefaultIdentifierSigner) and carried by clients as __signedIdentifier. The HMAC secret comes from an optional @IdentifierSignerSecret binding (Base64-decoded).
  - **Signed identifier / optimistic-lock version churns on server-side update** (how-to, `S01-04`). JUDO entities carry an identifier that includes a version; when a record is updated server-side its signed identifier (signedId) can change, so it no longer matches a locally cached signed id.
  - **Signed identifiers change whenever an object is updated and must be re-queried before use** (how-to, `S05-02`). In JUDO a bound operation's signed identifier (signedIdentifier) encodes the instance's current version/state; it is invalidated whenever the object is updated. A client (e.g.
  - **Signed identifiers: minted only while serving a REST response; there is no reachable plain mint API** (how-to, `S03-04`). Client/server code that must pass a ticket's `__signedIdentifier` cannot mint one itself with a normal API call: the runtime only mints a signed identifier while it is serving a REST response (i.e. when the AI queries the defect ticket and gets one back in the payload).
  - **Bound operations and signed identifier mechanics** (how-to, `P15-02`). Bound operations (on a specific instance) rely on a JWT-signed identifier. DefaultIdentifierSigner builds a compact JWS whose subject is the identifier, with claims ver (version), immutable, and issuer = FQName of the producing EReference/EOperation;
  - **Access-control runtime semantics: signed identifiers** (topic, `P01-09`). JUDO enforces access at runtime via signed identifiers: the signed identifier encodes the access/navigation edge used to obtain an instance, so an update is rejected when the instance was reached through an access that does not allow updates (e.g. ordersInMyRegion marked updatable vs not).

### Generated REST API contract (paths, headers, metadata fields, wire formats)

- **Priority:** High · **Area:** integration · **Evidence:** 1 session(s); judo-ng: `judo-psm-generator-jaxrs`, `judo-runtime-core`, `judo-platform`, `judo-tatami-tests` …
- **Put it in:** agent-docs/backend/rest-api-contract.md (new)
- **Catalog today:** `~list` appears only in e2e route matchers; `X-Judo-RequestParameters` in one pattern. No contract doc.
- **What to add:**
  - **REST transport protocol (signed identifiers, partial update, list query contract)** (topic, `P12-01`). The generated backend exposes a JSON-over-HTTP CRUD/operation API rooted at /api/<Model>/Actor/... with resource verbs ~create/~list/~update/~delete/~get/~validate (instance writes identified by the X-Judo-SignedIdentifier request header, responses carrying __identifier/__signedIdentifier).
  - **Generated REST API contract: tilde subresource verbs and signed identifiers** (how-to, `P25-01`). A generated JUDO application exposes a REST API under /api/<Model>/<Actor>/ whose operations are tilde-prefixed subresource verbs: ~create, ~update, ~delete on entities, ~list/~range for collections, and ~set/~add to mutate a many-relation.
  - **REST operation URL path suffixes (~create, ~list, ~range, ~upload-token, ...)** (how-to, `P30-03`). Every generated REST operation is routed on a `~`-suffixed path built by `OperationHelper.toJAXRSPath`: LIST maps to `~list` (cardinality -1) or `~get`, CREATE_INSTANCE to `~create`, and the full suffix set is `~create`, `~validate`, `~update`, `~delete`, `~set`, `~unset`, `~add`, `~remove`, …
  - **REST response DTO metadata fields (__identifier, __signedIdentifier, __version, __deleteable, ...)** (how-to, `P30-04`). Generated REST DTOs carry reserved double-underscore metadata fields on mapped transfer objects: response DTOs get `__deleteable` (Boolean), `__updateable` (Boolean), `__entityType` (String), `__identifier`, `__signedIdentifier`, `__version` (Integer) and `__referenceId` (String);
  - **X-Judo-* REST request protocol headers** (mention-only, `P30-05`). The generated REST operation signatures expect protocol headers `X-Judo-CountRecords` (→ `__countRecords`), `X-Judo-Mask` (→ `__mask`), `X-Judo-RequestParameters` (→ `__requestParameters`, parsed by `RestUtils.parseHeaderRequestParams` into a `Map`), `X-Judo-SignedIdentifier` (bound operations), and `X-Judo-MarkSelectedRangeItems` (range operations);
  - **X-Judo-* wire-protocol headers** (topic, `P33-02`). All generated REST services communicate via custom headers: X-Judo-SignedIdentifier (target signed id on commands), X-Judo-Mask (response projection on commands), X-Judo-CountRecords / X-Judo-Count (request/response total-count), and X-Judo-MarkSelectedRangeItems (marks already-attached items in range requests).
  - **REST wire conversion contract: enums as ordinals, binaries as filestore tokens** (topic, `P16-05`). On the wire, RequestConverter/ResponseConverter translate payloads for transfer types: enum attributes travel as integer ordinals (RequestConverter looks up the input literal via getEEnumLiteral and stores getValue();
  - **Query-customizer filter operator codes and query-mask wire syntax** (topic, `P16-08`). The query-customizer parameter processor maps a numeric filter operator code per attribute type: for strings 0 '<', 1 '>', 2 '<=', 3 '>=', 4 '==', 5 '!=', 6 '~' (matches), 7 'like'; numeric/date/time/timestamp use 0-5; boolean only 0 (EQ); enumeration only 0 (EQ) and 1 (NEQ).
  - **REST date parameters are parsed as yyyy-MM-dd** (how-to, `P18-09`). JAX-RS request query/path parameters of type java.util.Date are handled by ISO8601DateParamHandler, which parses and formats them strictly with the SimpleDateFormat pattern yyyy-MM-dd (no time component); a parse failure throws IllegalArgumentException 'Invalid date parameter: ...'.
  - **JAX-RS service layer + Dispatcher call contract and HTTP behaviours** (how-to, `P30-06`). Each generated REST service interface is `@javax.ws.rs.Path('/')`, declares `__bindDispatcher`/`__unbindDispatcher(Dispatcher)`, and every operation method is annotated `@hu.blackbelt.judo.dispatcher.api.JudoOperation(operationAsmFqName)` with `Map`/`List<Map>` input.
  - **JUDO list query without seek returns all rows** (mention-only, `S01-09`). A simple JUDO list call without an explicit seek/pagination returns all matching rows; pagination is an opt-in feature (the runtime has a separate seekBuilder). For small per-user datasets (e.g.
  - **Choice/range retrieval operations (getRangeFor + _GetRangeInput input type)** (mention-only, `P22-07`). Transfer actions and relations with a ChoiceModifier generate GET_RANGE range-lookup operations named `getRangeFor<Name>` (immutable, `_`-prefixed on collision).

### Which operations interceptors see, and how several compose

- **Priority:** High · **Area:** backend · **Evidence:** 5 session(s)
- **Put it in:** agent-docs/backend/interceptors.md (scope + composition section)
- **Catalog today:** interceptor-range-override.md names `_getRangeReference`, no scope rules.
- **What to add:**
  - **OperationCallInterceptors do not fire on custom/mapped operations** (how-to, `S26-01`). JUDO's OperationCallInterceptors (including write guards) fire only for behaviour operations (CRUD, list, refresh, range and reference operations). Custom and MAPPED operations such as User.toggleActive, resendInvitation, createUser and changeRoles never hit interceptors.
  - **Range interceptors only fire on _getRangeReference* operations, not on direct list/query operations** (pattern, `S05-03`). JUDO range interceptors are bound to the `_getRangeReference*` operations used by reference/autocomplete fields. When the frontend calls a plain list/query operation instead (e.g. `Rack/availableRackElements/~list`), the range interceptor never runs and its context filtering is bypassed.
  - **Multi-interceptor composition semantics: ordering, peer mutation visibility, last-non-null-wins return accumulation** (how-to, `S04-02`). When multiple `OperationCallInterceptor`s are registered for the same operation, they do not run in parallel: each preCall receives the original payload, interceptors see each other's in-place mutations to the payload, and the return value is accumulated last-non-null-wins (peers never see each other's return value).
  - **Range interceptors are the security boundary for rangeType=ANY lean transfer objects** (mention-only, `S03-09`). A lean transfer object with rangeType=ANY exposes the whole instance set to any caller (including the AI actor) unless a range interceptor scopes the enumeration; making the TO's relations/attributes read-only does not stop enumeration. Range interceptors (e.g.

### Schema migration: what needs manual steps, `.missing` review scripts, version checks

- **Priority:** High · **Area:** deployment · **Evidence:** 4 session(s); judo-ng: `documentation`, `judo-rdbms-schema`, `judo-services`
- **Put it in:** agent-docs/deployment/schema-evolution.md
- **Catalog today:** schema-evolution.md has "generate and review migration scripts" only.
- **What to add:**
  - **Schema evolution: additive stored model members need NO manual liquibase/schema-upgrade step — the generated changelog carries them** (how-to, `S03-06`). When a model change merely adds a stored member (attribute) to an entity, the schema migration is produced automatically: the model's generated liquibase changelog (application/model/target/generated-resources/model/rackinspect-liquibase_postgresql.changelog.xml) already contains the new column (e.g.
  - **Schema migration review-required .sql.missing workflow** (how-to, `P01-10`). JUDO RDBMS schema evolution distinguishes identical, applyable and review-required change types across base/update/incremental models.
  - **Incremental schema-migration review workflow: review scripts, .missing placeholders, applyable check, and the useXmiId/ignoreReview flags** (how-to, `P14-05`). The rdbms-schema generator produces an eight-phase set of changesets (check, backup, beforeIncremental, updateDataBeforeIncremental, incremental, updateDataAfterIncremental, aferIncremental [sic] -> script 07_aferIncremental, dropBackup) plus an aggregated 00_<model>_incremental_<dialect>.changeset.xml and a <model>-rdbms_<version>_<dialect>.model.
  - **Consolidating incremental schema migration folders into one continuous generated step** (mention-only, `S05-08`). When many model changes accumulate, instead of stacking per-snapshot migration folders (e.g.
  - **Runtime Liquibase model-store version enforcement and ignoreVersionCheck** (how-to, `P21-05`). Before a datasource is used, LiquibaseModelDataSourcePrehook either runs the Liquibase migration or checks/records the model version in the `JUDO_MODEL_VERSIONS` table and verifies the RDBMS model matches the database.

### Relation kinds, CRUD flags and the endpoints they generate

- **Priority:** High · **Area:** model · **Evidence:** 4 session(s); judo-ng: `judo-platform`
- **Put it in:** agent-docs/model/model-development.md (relations and CRUD flags)
- **What to add:**
  - **CRUD flags are declared on relations, not on the shared transfer object; REST/range endpoints are generated only for relations with C/U/D flags** (topic, `S03-03`). CRUD flags in JUDO are declared on the relation members themselves (a relation's create/update/delete flags), not once on a shared transfer object. There is no single 'CRUD flag' on the TO.
  - **Relation kind determines the generated relation endpoints and where delete lives (~add/~remove/~set vs ownership ops)** (pattern, `S08-04`). Whether a relation is an ASSOCIATION or a COMPOSITION at entity level determines which generic transfer endpoints are generated and therefore which operations exist for a client. An association `pictures` relation generates generic `~add`/`~remove`/`~set` endpoints;
  - **Mapped transfer-object relation-kind and binding rules** (how-to, `P12-05`). On a mapped transfer object an entity-side relation is exposed as AGGREGATION when the cardinality lower bound is 1 (else ASSOCIATION), and entity COMPOSITION/DERIVED ASSOCIATION also map to AGGREGATION on the TO.
  - **transfer_ prefix naming convention for mapped transfer-object members** (topic, `P12-06`). Attributes and derived members of mapped transfer objects are exposed with a transfer_ prefix, e.g. transfer_derivedAttribute and transfer_derivedEnum alongside the stored derivedAttribute/derivedEnum, and transfer objects expose the mapped entity's members under these names in list responses.

### Filestore on S3/GCS: configuration and access URLs

- **Priority:** High · **Area:** deployment · **Evidence:** 4 session(s); judo-ng: `osgi-filestore`
- **Put it in:** agent-docs/deployment/application-config.md (extend filestore section)
- **Catalog today:** application-config.md lists `JUDO_PLATFORM_FILESTORE_S3_BUCKET` only.
- **What to add:**
  - **Filestore S3/GCS backend configuration and access-URL semantics** (how-to, `P27-03`). The FileStoreService has filesystem, RDBMS and S3-compatible backends.
  - **Filestore S3/GCS backend config & servlet CORS semantics** (how-to, `S24-01`). Configure the JUDO filestore S3 backend via JUDO_PLATFORM_FILESTORE=s3 plus JUDO_PLATFORM_S3_BUCKET / JUDO_PLATFORM_S3_ENDPOINT / JUDO_PLATFORM_S3_REGION, and note that osgi-configuration-mapper strips the JUDO_PLATFORM_ prefix and converts UPPER_SNAKE_CASE to lowerCamelCase.
  - **GCS bucket as JUDO S3 filestore (HMAC + env config)** (how-to, `S19-07`). Google Cloud Storage exposes an S3-compatible XML API, so JUDO's S3FileStoreService works against GCS with no GCS-specific code or config: point the client at https://storage.googleapis.com using HMAC credentials (S3 config keys).

### Time zones and date/time wire format

- **Priority:** High · **Area:** backend · **Evidence:** 4 session(s)
- **Put it in:** agent-docs/backend/data-access-guide.md (time zones)
- **Catalog today:** No file mentions time zones, `ZONE_ID` or `user.timezone`.
- **What to add:**
  - **JUDO timestamp/timezone semantics (Timestamp!now vs LocalDateTime.now vs DB UTC)** (how-to, `S07-01`). JUDO has two different clocks that do NOT agree. `Timestamp!now()` (the model expression) resolves through `CurrentTimestampProvider`/`DefaultVariableResolver` and is controlled by the `JUDO_PLATFORM_DEFAULT_ZONE_ID` OSGi/env variable (default e.g. Europe/Budapest), not by the JVM timezone.
  - **JUDO LocalDateTime wire format and timezone normalization** (how-to, `S01-01`). JUDO REST serializes LocalDateTime as a string in ISO_OFFSET_DATE_TIME form `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` (offset always present; a zero offset is rendered as `Z`). When a client sends an OffsetDateTime, JUDO's mapper converts it to LocalDateTime via `atZoneSameInstant(UTC)` — i.e.

### JQL function reference: temporal, collection, aggregation, string, measured literals

- **Priority:** High · **Area:** model · **Evidence:** 1 session(s); judo-ng: `judo-meta-expression`, `judo-meta-jql`, `judo-tatami-jsl`, `judo-meta-expression-psm`
- **Put it in:** agent-docs/model/jql-reference.md (new; full function table)
- **Catalog today:** `!head`, `!lpad` and ternaries appear inside patterns; there is no function reference.
- **What to add:**
  - **Temporal/date-time functions in JQL** (topic, `P05-01`). The JUDO expression/JQL engine provides a full temporal function family that the catalog does not mention at all: current_date / current_timestamp / current_time (SYSTEM-category environment variables, NowFunctionTransformer); date/time/timestamp constructors (date(y,m,d) exactly 3 ints;
  - **JQL time/duration built-ins (e.g. elapsedTimeInMinutes) undocumented in the JQL reference** (topic, `S12-03`). JUDO's JQL includes built-in temporal helpers not listed in the model-development JQL reference: `self.<end>!elapsedTimeInMinutes(self.<start>)` computes a duration in minutes between two timestamps, and collection aggregation like `self.downtimes!sum(e | e.downtimeMinutes)` works on derived attributes.
  - **Collection functions head/tail/heads/tails, join, and boolean aggregators** (topic, `P05-04`). The JQL collection function reference omits several shipped functions: head/tail/heads/tails (ObjectSelector enum; HEAD/TAIL return a single element via MIN/MAX aggregate over the sort expression, HEADS/TAILS return a filtered collection; ANY wraps directly without a filter);
  - **Aggregation type constraints and round(scale)** (how-to, `P05-05`). The JQL aggregation functions have per-type restrictions not covered by the catalog's simple listing: sum supports only integer and decimal values (strings and temporal values throw 'Invalid expression for aggregation');
  - **String function variants lpad/rpad/ltrim/rtrim/capitalize/ilike** (mention-only, `P05-06`). The JQL string function reference is missing the lpad/rpad padding functions (padding type enum is misspelled PaddignType; default pad string is a single space), ltrim/rtrim, capitalize (UPPER(first char) + LOWER(remainder)), and a case-insensitive like variant.
  - **Built-in JSL function library (JQL translation and renaming)** (topic, `P22-01`). The JSL expression language is translated to JQL by Jsl2JqlFunction and JslExpressionToJqlExpression.
  - **Measured literal syntax and duration-addability rules** (how-to, `P05-03`). Measured literals are written as 'measure#unit' or just 'unit' (JqlMeasuredLiteralTransformer), not the '[kg]' bracket notation shown in the catalog.
  - **JQL grammar and operator quirks** (how-to, `P06-10`). JQL expression grammar specifics: the ternary `cond ? then : else` is right-associative; equality operators are only `==` and `!=` (there is no `=` or `<>`); enum literals use `Type#VALUE`; function calls use `expr!name(args)` and the result can be further navigated;

### Undocumented UI-model attributes

- **Priority:** High · **Area:** model · **Evidence:** judo-ng: `judo-tatami-client`, `judo-tatami-jsl`, `judo-ui-react-template`
- **Put it in:** agent-docs/model/esm_metamodel/ui.md
- **What to add:**
  - **Group layout inheritance and effective alignment rules** (how-to, `P23-09`). A Group whose layout is null/DEFAULT inherits the nearest ancestor Group layout (walking up the eContainer chain, stopping at a non-Group container), defaulting to HORIZONTAL if none is found.
  - **Table presentation attributes (tableRepresentation, isSmallTable, isExportable)** (topic, `P23-08`). Generated tables expose presentation/behaviour properties read from the ESM tabular element: `tableRepresentation` (e.g.
  - **additionalMaskAttributes / additionalMaskFeatures table mask projection** (how-to, `P23-07`). ESM Table/TabularReferenceField `additionalMaskFeatures` entries are mapped onto the generated UI Table as `additionalMaskAttributes` (attribute names matching the original ESM attribute names). This extends what data the table loads/renders beyond the plain columns.
  - **isInCard visual element card placement** (topic, `P23-06`). Visual elements (DataField, Divider, Group, etc.) carry an `isInCard` flag that the ESM2UI transformation uses to place the element inside a Card container.
  - **applicationColumns UI grid column configuration** (topic, `P23-05`). The `applicationColumns` context attribute controls the number of grid columns used by generated UI Flex/PageContainer layouts; it defaults to 12 when unset. Generated views/forms/tables derive their column spans from this value (e.g.
  - **applicationType / applicationColumns generation parameters** (topic, `P20-05`). The `Esm2UiParameter` / `Esm2UiWorkParameter` builders accept `applicationType` (default "default") and `applicationColumns` (default 12), which control the generated UI application layout (non-Component containers get `col = APPLICATION_COLUMNS`, i.e. 12.0, with stretch BOTH).
  - **Inline editing only works on eager tables (JNG-6043)** (how-to, `P24-02`). The generated Table's isInlineEditable flag is set equal to the relation's isEager flag (t.isInlineEditable = t.isEager). A TODO JNG-6043 comment notes the runtime only supports inline editing for eager tables. A developer must mark the relation eager to get an inline-editable table.
  - **Link representation column requires a string-typed field on the target** (pattern, `P24-03`). ViewLinkDeclarationRepresentationColumn derives the representation from the first primitive 'string'-typed field of the relation target's transfer declaration. If no such field exists the transformation logs an error and the representation column is omitted (ETL throws; Zeta returns null).
  - **Predictive modifier generates a type-ahead TextInput** (how-to, `P24-04`). A string widget whose transferred field carries a predictive modifier (PredictiveModifier present and not false) is generated as a TextInput with IsTypeAHeadField=true, enabling autocomplete from previously filled values. Boolean/other primitive widgets do not get type-ahead.
  - **Custom component annotation prefix ('use' annotations)** (how-to, `P31-02`). Model annotations with the default prefix `use` (configurable via the `customComponentAnnotationPrefix` template parameter, default 'use') wire a custom React component through the generator.

### JSL (textual model) language: events, errors, opposite-add, escaping, build constraints

- **Priority:** High · **Area:** model · **Evidence:** judo-ng: `judo-meta-jsl`
- **Put it in:** agent-docs/model/jsl/ (new; only if JSL projects are in scope)
- **What to add:**
  - **JSL transfer event handlers (event create|delete|fetch|initialize|update)** (topic, `P06-03`). Transfer objects declare lifecycle handlers with `event <create|delete|fetch|initialize|update> <name>;`. The grammar accepts no parameter list and no on:(before|after|instead) modifier (the OnModifier rule is commented out). Error bodies may also contain an `event initialize` member.
  - **JSL error declarations and transfer action throws clause** (how-to, `P06-08`). Errors are declared as `error Name { field <Primitive> <name> [default:<expr>] [required]; ... }` (body optional; a body may include an `event initialize` member).
  - **opposite-add: injecting a bidirectional back-reference into another model** (pattern, `P06-04`). A relation can declare its opposite side as `opposite-add: Name` (EntityRelationOppositeInjected), which injects a new relation into the referenced entity of another model without modifying that model's source, or as `opposite: Name` (EntityRelationOppositeReferenced) pointing at an existing relation.
  - **JSL reserved-word identifier escaping with backticks** (how-to, `P06-01`). JSL identifiers are ASCII letters/digits starting with a letter, but the grammar ID terminal also accepts a backtick-quoted name, which is how a reserved word such as `void`, `self`, `true`, `false` or `not` is used as an element name. The parser strips the backticks;
  - **JSL built-in judo::types and judo::functions libraries** (topic, `P06-02`). Every JSL model implicitly imports two framework-provided models. `judo::types` declares Boolean, Date, Time, Timestamp, Integer (numeric precision:9 scale:0), Long (numeric precision:15 scale:0) and String (min-size:0 max-size:4000).
  - **JSL collection iterator lambda restrictions** (pattern, `P06-05`). Collection iterator functions (first, last, front, back, filter, anyTrue/allTrue/anyFalse/allFalse, min, max, avg, sum) are declared as lambdas taking a single boolean or numeric expression. The lambda body may only select an immediate field of the iterator variable - multi-step navigation (e.g.
  - **JSL constraints that fail model builds (required/collection/abstract/eager/identifier)** (how-to, `P06-11`). Key JSL validator rules a developer must respect: a collection cannot be required; a bidirectional relation cannot be required on both ends; an abstract entity cannot be used as a field type (FieldTypeIsAbstractEntity) and can only be inherited;
  - **Binary field modifiers: mime-type and max-file-size with measure units** (how-to, `P06-07`). A binary primitive must declare both `mime-type:` (entries of form type/subtype, subtype may be `*`; keyword is singular `mime-type`, not `mime-types`) and `max-file-size:`.
  - **JSL actor declaration grammar limits** (how-to, `P06-09`). Actor declaration syntax is `actor Name [realm:"..."] [claim:"..."] [identity:Transfer::field] [guard <expr>] { access ... }`.

### Runtime/container configuration not covered (health checks, datasource, Karaf, Docker image)

- **Priority:** High · **Area:** deployment · **Evidence:** judo-ng: `judo-esm-fullstack-project-template`, `judo-services`, `judo-tatami-tests`, `documentation` …
- **Put it in:** agent-docs/deployment/production.md
- **What to add:**
  - **Custom health checks** (how-to, `P01-07`). JUDO registers Apache Felix health-check rules (ModelsCheck, OperationsCheck, PlatformComponentsCheck) and exposes a status page at http://localhost:8181/system/health?tags=<ModelName>.
  - **PostgreSQL bootstrap retry and pax-jdbc datasource configuration keys** (topic, `P21-08`). The PostgreSQL datasource tracker waits for the database with a resilience4j retry loop before creating an org.ops4j.datasource factory configuration: retryMaxAttempts (default 1000), retryExponentialBackoff (default true), retryWaitDuration (default 1000ms) and ignoreVersionCheck (default false).
  - **Karaf container administration for deployed apps (JAAS users, startup feature)** (how-to, `P25-03`). A deployed JUDO app runs in a Karaf container whose console access is configured through JAAS users.properties in the format USER=PASSWORD,_g_:GROUP, with roles (group, admin, manager, viewer, systembundles, ssh) granted per group;
  - **Docker image build customization (tags, base image, agents)** (how-to, `P28-06`). The generated docker module builds one image tar per architecture with jib-maven-plugin 3.3.2: x86_64/amd64/arm64 profiles write target/<artifactId>-<version>_docker_image_<arch>.tar, all using a hard-coded azul/zulu-openjdk-debian:21-latest base.
  - **Shipped Docker Compose environments and ./judo.sh env** (how-to, `P28-03`). The template ships two docker-compose profiles. compose-develop runs Traefik + Keycloak start-dev + the app on *.traefik.me over plain HTTP (proxy.traefik.me, auth.traefik.me:8080, app.traefik.me:8181) with JUDO_PLATFORM_FILESTORE=rdbms.
  - **Embedded HSQLDB server and per-model dev datasource configuration** (how-to, `P14-09`). HsqldbServer is an OSGi component that starts an HSQLDB TCP server and publishes a PAX-JDBC org.ops4j.datasource factory config; its config keys are dataSourceName (required), databaseName (required), databasePath (required), port (optional, default 9001); dynamic properties prefixed pax-jdbc.
  - **Embedded HSQLDB server provisioning and configuration** (how-to, `P21-09`). For local development and tests JUDO provisions an embedded HSQLDB TCP server per LiquibaseModel: HsqldbServer requires dataSourceName, databaseName and databasePath (all String, no default) with optional port (default 9001);
  - **Maven extension fragments for generated backend modules** (how-to, `P28-04`). Every generated Maven module (application root, app, interceptors, karaf-features, schema, e2e, web-root) includes empty extension fragments that are injected at fixed points of the generated POM: pom.xml.extra-dependencies.fragment.hbs into <dependencies>, pom.xml.extra-plugins.fragment.hbs into …
  - **Project generation toggles and single-actor vs multi-actor mode** (how-to, `P30-08`). Project generation is controlled by per-module flags (`shouldGenerate*`, sourced from `generator-parameter.properties`): model, sdk, application, rest, internal, frontend, docker, interceptor, schema, karaf, keycloak-theme, web-root, e2e and launcher.

### Generated database schema: naming, audit columns, indexes

- **Priority:** High · **Area:** model · **Evidence:** 1 session(s); judo-ng: `judo-tatami-base`, `judo-meta-rdbms`, `judo-tatami`, `judo-tatami-jsl`
- **Put it in:** agent-docs/deployment/schema-evolution.md (generated schema)
- **What to add:**
  - **Generated RDBMS schema SQL naming conventions** (how-to, `P09-03`). Generated RDBMS schema names follow two deliberately opposite SQL naming conventions enforced by validation: table names must match ^[A-Z][A-Z0-9_]*$ (UPPER_SNAKE, critique RdbmsTableNameConvention) while field/column names must match ^[a-z][a-z0-9_]*$ (lower_snake, critique RdbmsFieldNameConvention).
  - **Generated SQL identifier naming and per-dialect length budgets** (how-to, `P19-01`). The ASM→RDBMS generator derives every table/column/FK/junction SQL name from model names with deterministic abbreviation: AbbreviateUtils strips vowels then consonants in English-frequency order, and each dialect imposes length budgets (default tableNameMaxSize=62, columnNameMaxSize=58; Oracle 30/30;
  - **RDBMS naming-prefix controls for generated schemas (rdbmsTablePrefix/ColumnPrefix/ForeignKeyPrefix/InverseForeignKeyPrefix/JunctionTablePrefix, rdbmsColumnMaxNameSize)** (topic, `P26-04`). When the pipeline generates RDBMS models, table and column naming is controlled by prefix parameters with defaults T_ for tables, C_ for columns, FK_ for foreign keys, J_ for junction tables, and an inverse-foreign-key prefix; a value of "-" (after trimming and dash removal) means no prefix.
  - **RDBMS naming-prefix configuration for generated schema objects** (how-to, `P22-05`). Generated tables, columns, foreign keys, inverse foreign keys, and junction tables use configurable prefixes: T_, C_, FK_, FK_INV_, J_ respectively, each overridable with '-' to suppress the prefix. These prefixes are set in the workflow Maven plugin configuration.
  - **Automatic system/audit columns on every generated entity table** (topic, `P19-03`). Every entity table gets nine fixed system columns automatically, independent of the model: ID (java.util.UUID, the primary key), TYPE (mandatory String), VERSION, CREATE_USERNAME, CREATE_USER_ID, CREATE_TIMESTAMP, UPDATE_USERNAME, UPDATE_USER_ID, UPDATE_TIMESTAMP.
  - **Generated schema adds no indexes on m:n join-table FKs** (topic, `S19-06`). JUDO's generated liquibase changelog creates join tables for m:n relations but does not emit createIndex entries for their FK columns; for large partner/user-style junction relations this degrades the lookup/join queries. When a relation can grow large, verify the migration (e.g.

### Frontend OIDC metadata, logout and guest access

- **Priority:** High · **Area:** frontend · **Evidence:** judo-ng: `judo-ui-react-template`, `judo-runtime-core`, `judo-tatami-jsl`, `judo-tatami` …
- **Put it in:** agent-docs/frontend/authentication.md (new)
- **What to add:**
  - **GET_METADATA OpenID security descriptor for frontend login** (how-to, `P16-10`). The backend's GET_METADATA operation builds, for an actor type carrying a 'realm' extension annotation, an OpenID/OAuth security descriptor returned as the 'security' list.
  - **Actor SSO/security metadata (_metadata operation and _MetadataSecurityFor type)** (topic, `P22-03`). Every actor gets a `_metadata` unbound operation (GET_METADATA) returning a `_MetadataFor<Actor>` type, and actors with a principal additionally get a `_principal` operation returning the principal type.
  - **Model-driven actor OpenID Connect client configuration (generated _MetadataSecurityFor<actor> client fields)** (topic, `P26-07`). For each ESM actor with a mapped principal, the transformation generates an actor metadata transfer-object type _MetadataFor<actor> with an embedded security relation to _MetadataSecurityFor<actor>, which carries nine fixed transfer attributes: name, openIdConfigurationUrl, issuer, authEndpoint, …
  - **~meta security discovery and ~principal actor endpoints** (how-to, `P12-02`). Each Actor exposes GET /api/<Model>/Actor/<Actor>/~meta whose security[0] entry provides tokenEndpoint, clientId and openIdConfigurationUrl used to obtain an OAuth access_token for that Actor, and GET /api/<Model>/Actor/<Actor>/~principal returning the authenticated principal (email plus __identifier/__signedIdentifier).
  - **OIDC logout, profile popup, and signed-in gating** (how-to, `P33-05`). Authenticated frontend behavior: logout calls signoutRedirect with post_logout_redirect_uri set to the current URL without its hash fragment;
  - **Guest page and guest access mode** (how-to, `P31-03`). With `supportGuestAccess` enabled, an unauthenticated user is not redirected to signinRedirect; instead the Auth gate renders a Pandino-overridable guest page.

### JCL operation-body language reference

- **Priority:** High · **Area:** model · **Evidence:** judo-ng: `documentation`, `judo-meta-script`, `judo-meta-jcl`, `judo-jcl-ide-eclipse`
- **Put it in:** agent-docs/model/jcl-reference.md (new)
- **Catalog today:** Only operation.md says the body is a JCL script.
- **What to add:**
  - **JCL operation body language reference** (how-to, `P01-01`). JCL (JUDO Control Language) is the imperative scripting language used for operation bodies in the model: statements, blocks, variable declarations, assignment, if/for/while/return, new/delete/unset, reference-set += and -=, and subtype spawning via 'x as Type'.
  - **JCL operation-script language reference (operators, selectors, blocked functions)** (topic, `P09-01`). The JUDO script language used for Operation bodies (JCL/JSL, built by JclScriptBuilder) has its own semantics that diverge from JQL expressions, and there is no language reference for it in the catalog.
  - **JCL action-language syntax reference** (how-to, `P05-08`). Operation bodies are JCL scripts (the ESM operation model's body field is a JCL script when customImplementation=false; customImplementation=true switches to Java). The catalog only shows examples (script-driven-operations.md) and a one-line mention (operation.md).
  - **JCL operation-body validation and the customImplementation bypass** (how-to, `P02-04`). Operation bodies written in JCL are validated by an EVL constraint ScriptValid (severity ERROR) that runs the JCL build for each Operation whose script is not custom. The check calls the native JclEvlValidator and passes only when isOk(self) returns null;
  - **Transfer-object immutability and lifecycle semantics** (topic, `P01-02`). The immutable/mutable copy model of JUDO transfer objects: the 'immutable' keyword creates a detached copy of a TO/entity/list/relation (requires 'var immutable <Type>' in the declaration);
  - **Authenticated-actor access functions in operation scripts** (how-to, `P09-04`). Inside operation scripts the current authenticated actor is exposed through dedicated functions and navigation: `principal` and `iscurrentactor` are registered script functions, and a leading navigation name that resolves to an actor type becomes an ActorReference base expression rather than a data navigation.

### Frontend extension points not yet documented

- **Priority:** High · **Area:** frontend · **Evidence:** judo-ng: `judo-ui-react-template`
- **Put it in:** agent-docs/frontend/hooks/
- **What to add:**
  - **Extra routes extension point** (how-to, `P31-06`). The generated `src/extra-routes.tsx` exports an `extraRoutes: Array<{ path: string; element: ReactElement; exact?: boolean }>` array that the generated routes.tsx prepends to the generated routes.
  - **Multi-application switcher and alternative-app navigation** (topic, `P33-04`). The generated app supports switching between alternative applications: ProfilePopup shows an application switcher when otherApplicationsAvailable is true, driven by useApplicationSelector();
  - **Menu actions hook objectClass gotcha** (pattern, `P31-07`). The menu-actions customization hook is registered under the OSGi objectClass value 'MENU_ACTIONS_HOOK' — without the 'Hook' suffix used by every other hook key (CustomHeroPropsHook, CustomLogoPropsHook, FooterTextHook, MenuItemsCustomizerHook).
  - **Sub-theme hook registration API** (how-to, `P31-04`). A named sub-theme is registered by a generated `register<SubTheme>SubThemeHook(context)` which calls `context.registerService(SUB_THEME_HOOK_INTERFACE_KEY, fn, { name: '<toSafeCamelCase subTheme>' })`.
  - **Per-component MUI theme override fragments** (mention-only, `P33-08`). The generated theme (index.tsx.hbs) is assembled from a fixed set of per-component override fragments: …
  - **Operation fault dialog API** (mention-only, `P31-08`). `useFaultDialog()` returns `(faultObjectKey: string, payload: any) => void`, which opens an OperationFaultDialog in the StackableDialogProvider and renders the business-fault payload as translated key/value pairs.

### Custom JAX-RS resources and REST-only endpoints

- **Priority:** Medium · **Area:** backend · **Evidence:** 1 session(s); judo-ng: `cxf-jaxrs-application-manager`, `documentation`
- **Put it in:** agent-docs/backend/custom-rest-resources.md (new)
- **What to add:**
  - **Custom JAX-RS REST resources in a JUDO application** (pattern, `P11-01`). A JUDO application developer can expose custom REST endpoints inside the running Karaf app by writing an OSGi Declarative Services component that is also a JAX-RS root resource: annotate the class with @Path (and use @GET/@Post/...
  - **BasicApplication configuration keys and deferred startup behaviour** (how-to, `P11-02`). BasicApplication is an OSGi DS component implementing javax.ws.rs.core.Application, configured by a factory configuration. A: 'jaxrs.resource.classes' (comma-separated FQNs, loaded with Class.forName;
  - **Registering custom JAX-RS providers and the X-JAXRS-Provider contract** (how-to, `P11-03`). Custom JAX-RS providers (a service whose class is annotated @Provider) are only tracked by SharedProviderStore if the bundle's manifest header X-JAXRS-Provider is true. Providers without an 'applications.filter' property are global (applied to every application);
  - **CXF / JAX-RS REST customization** (how-to, `P01-06`). JUDO REST services are exposed through Apache CXF.
  - **REST-only custom operation (no web form) pattern for mobile endpoints** (pattern, `S07-04`). A custom operation that is meant for the phone (not the web UI) is modeled with no `OperationForm`, making it a REST-only endpoint. Precedent: `dispatchPhotoHelp` has no form and is REST-only.

### MUI X Pro/Premium license configuration

- **Priority:** Medium · **Area:** frontend · **Evidence:** 2 session(s); judo-ng: `judo-ui-react-template`
- **Put it in:** agent-docs/frontend/mui-license.md (new)
- **Catalog today:** No file mentions the MUI license.
- **What to add:**
  - **Enabling the MUI X Pro license in the generated React frontend** (topic, `S23-01`). The JUDO React generator reads a `muiLicensePlan` generator property (community|pro|premium) that is resolved by `ReactStoredVariableHelper.isMUILicensed()/isMUILicensePlanPro()` and drives template branches such as pinned-columns in LazyTable (`{{# if isMUILicensePlanPro }} initialState={ { pinnedColumns: { right: ['actions'] } } }`).
  - **MUI X license tier configuration** (topic, `P33-01`). The generated React frontend gates licensing-dependent behavior on the isMUILicensed / isMUILicensePlanPro flags and reads the MUI X license from the VITE_MUI_LICENSE_KEY environment variable at build time (LicenseInfo.setLicenseKey).
  - **MUI license plan, key and feature gating** (topic, `P31-01`). The React generator is parameterised by the `muiLicensePlan` template parameter (empty/community, pro, premium). The MUI license key is read at runtime from the Vite env var VITE_MUI_LICENSE_KEY (LicenseInfo.setLicenseKey in main.tsx);

### Test-suite memory: multi-JVM heap exhaustion hides unrun classes

- **Priority:** Medium · **Area:** testing · **Evidence:** 2 session(s)
- **Put it in:** agent-docs/integration-testing/best-practices.md
- **What to add:**
  - **E2E/integration suite multi-JVM heap: silent green with classes never run** (how-to, `S19-04`). The JUDO test suite forks several JVMs (each with its own heap, set in test/pom.xml); when a JVM OOMs halfway, every class still queued on that JVM never runs, yet surefire can still report '524 tests, 0 failures' — a misleading green. To get trustworthy results, raise the per-JVM heap (e.g.
  - **Full backend test suite memory: multi-JVM heap exhaustion** (how-to, `S24-05`). JUDO's test suite splits across multiple JVMs (e.g. 4), each with a fixed heap; when each JVM runs many classes the heap fills and the JVM dies, silently dropping every class still queued on it while the report can still look green (pass count with classes never run). Raise per-JVM heap (e.g.

### Local e-mail testing (Mailpit) incl. Keycloak realm SMTP

- **Priority:** Medium · **Area:** testing · **Evidence:** 2 session(s)
- **Put it in:** agent-docs/deployment/local-development.md
- **Catalog today:** SMTP env vars are documented; local testing is not.
- **What to add:**
  - **Local email testing with Mailpit vs production SMTP env-provided values** (how-to, `S06-07`). Email is tested locally with a catcher like Mailpit: SMTP host/port come from `judo-karaf.env` (`localhost:1025`, no auth/TLS) for local runs, while test/demo/prod read `JUDO_PLATFORM_MAIL_SMTP_*` (+ `_FROM`) from deployment env vars in `environments/<env>/app-compose/docker-compose.yml`.
  - **Local SMTP testing for invitation emails: mailpit + Keycloak realm SMTP** (how-to, `S26-03`). User-invitation e-mails are sent by Keycloak, not by the application, so JUDO_PLATFORM_MAIL_SMTP_* only covers app mail.

### Optimistic locking (`__version`) on updates

- **Priority:** Medium · **Area:** backend · **Evidence:** 1 session(s); judo-ng: `judo-runtime-core`
- **Put it in:** agent-docs/backend/data-access-guide.md (new section)
- **Catalog today:** Only a frontend sample compares `__version`; the server-side check is undocumented.
- **What to add:**
  - **Built-in optimistic locking & the VERSION field on updates** (topic, `S07-02`). The JUDO RDBMS DAO enables optimistic locking by default (`rdbmsDaoOptimisticLockEnabled` defaults to true). Every entity carries a `VERSION` field;
  - **Optimistic locking and __version semantics** (how-to, `P15-01`). JUDO's RDBMS DAO implements optimistic locking through the reserved __version payload key. The version check runs ONLY when the update payload contains __version: it must equal the original __version or UpdatePayloadDaoProcessor throws IllegalArgumentException 'Outdated instance to update';
  - **Optimistic locking defaults and stale-version errors** (how-to, `P18-05`). The RDBMS runtime hardwires optimistic locking ON (optimisticLockEnabled=true).

### Expression variable categories beyond ACTOR/PRINCIPAL, and custom providers

- **Priority:** Medium · **Area:** model · **Evidence:** judo-ng: `judo-runtime-core`, `documentation`, `judo-platform`, `judo-meta-expression`
- **Put it in:** agent-docs/model/model-development.md (variables section)
- **Catalog today:** ACTOR, PRINCIPAL and SEQUENCE are used in examples; no category list.
- **What to add:**
  - **Custom JQL variable providers and built-in categories** (how-to, `P01-03`). JQL getVariable('CATEGORY','key') resolves request-scoped variables from platform categories SYSTEM, ENVIRONMENT, REQUEST, ACTOR, PRINCIPAL and SEQUENCE. Developers can register NEW variable providers as OSGi components with property judo.environment-variable-provider=true plus a category property;
  - **Extending expression variable resolver categories (VariableResolverManager)** (how-to, `P12-07`). The runtime registers expression variable providers via VariableResolverManager.registerFunction(category, provider, ...) and registerSupplier for SYSTEM/current_date, current_time, current_timestamp, and categories USER (access-token), ACTOR, ENVIRONMENT, PRINCIPAL, REQUEST, SEQUENCE.
  - **Environment-variable categories SYSTEM and PARAMETER (and typed/measured env vars)** (how-to, `P05-02`). The catalog documents only two !getVariable(category, name) categories: PRINCIPAL (JWT claims) and ACTOR (persisted Actor entity).
  - **Built-in variable namespaces for expressions beyond ACTOR/PRINCIPAL** (how-to, `P16-01`). The runtime variable resolver pre-registers four extra namespaces usable in any JQL expression via !getVariable(category, key): SYSTEM (suppliers current_timestamp, current_date, current_time), ENVIRONMENT (maps to an env var, falling back to a JVM system property), SEQUENCE (advances a named …
  - **Reserved JQL variable categories and system functions** (how-to, `P18-07`). The runtime VariableResolver pre-registers reserved variable categories/functions usable inside JQL expressions: SYSTEM.current_timestamp, SYSTEM.current_date and SYSTEM.current_time suppliers, plus ENVIRONMENT, SEQUENCE and REQUEST functions (e.g.

### Type mapping and type-level constraints (precision→Java, enums, unsupported types)

- **Priority:** Medium · **Area:** model · **Evidence:** judo-ng: `judo-psm-generator-sdk-core`, `judo-meta-psm`, `judo-tatami-base`, `judo-psm-generator-jaxrs` …
- **Put it in:** agent-docs/model/esm_metamodel/type.md
- **What to add:**
  - **Numeric/Decimal precision mapping to Java types (Integer/Long/BigDecimal/Float/Double)** (how-to, `P30-09`). The generated REST/SDK Java types for NumericType depend on precision/scale: for Integer numerics, precision 1–9 → `java.lang.Integer`, 10–19 → `java.lang.Long`, otherwise `java.math.BigDecimal`;
  - **Precision/scale to Java type mapping for numeric attributes** (how-to, `P32-07`). The generator's JavaApiHelper maps NumericType to concrete Java types by precision/scale: integer numerics with precision 1-9 map to java.lang.Integer, 10-19 to java.lang.Long, otherwise java.math.BigDecimal;
  - **Enumeration modeling constraints (ordinal range, uniqueness, non-empty)** (how-to, `P06-06`). Enumeration ordinals must be 0..9999 (ENUM_LITERAL_ORDINAL_MAX_VALUE), literal names and ordinals must each be unique within an enum (names compared case-insensitively), and an enum must have at least one literal. Enum literals are referenced in JQL expressions with `Type#VALUE` syntax.
  - **Enumeration ordinal persistence (do not renumber)** (pattern, `P08-07`). Enumeration members persist by their ordinal value (e.g. Countries HU=0, AT=1, RO=2, SK=3; Titles MS=0...DR=3). Because ordinals are the persisted form, reordering, inserting, or deleting members changes stored values and corrupts existing data.
  - **Password and XML data types are unsupported and abort transformation** (mention-only, `P19-04`). The PSM→ASM type rules contain CreatePasswordType and CreateXMLType, which throw 'not supported yet' and emit no EDataType; the Zeta TypeRules likewise exclude them (isCustomTypeGuard).

### Parameterized queries and parameter ranges

- **Priority:** Medium · **Area:** model · **Evidence:** judo-ng: `judo-meta-script`, `judo-platform`, `judo-runtime-core-jsl`, `judo-tatami-jsl`
- **Put it in:** agent-docs/model/model-development.md (parameterized queries)
- **What to add:**
  - **Parameterized queries with default arguments and derived relations that call them** (how-to, `P17-01`). A JSL entity can declare a query that takes parameters with default values, e.g. `query Lead[] leadsOver(Integer limit = 100)` on SalesPerson, and a derived relation can invoke it: `SalesPerson.leadsOver10 = self.leadsOver(limit = 10)`.
  - **Parameterized query modeling and call semantics** (how-to, `P09-02`). Parameterized queries (derived features taking an input TransferObjectType) are wired by tagging a feature with a `parameterized` extension annotation (EAnnotation whose source ends in 'parameterized' with detail 'true').
  - **Parameterized static queries generate unmapped parameter objects** (topic, `P22-06`). A static JSL query with parameters produces an unmapped transfer object type named `_<EntityOrContainer>_<Query>Parameters` (defaultParameterNamePrefix + (entity|container name) + midfix + query name + postfix), annotated `OriginalSource` and `ParameterObject` (with an OriginalName detail).
  - **Operation input parameter range expressions and the ~range endpoint** (how-to, `P12-03`). An operation's input parameter can carry a range via ParameterBuilder.withRangeType(RangeType.DERIVED | RangeType.ANY) plus withRangeExpression("self.creatures"), restricting the values a caller may pass.

### Measures and units: store unit, precision, conversion

- **Priority:** Medium · **Area:** model · **Evidence:** judo-ng: `judo-meta-psm`, `judo-meta-measure`, `judo-runtime-core`
- **Put it in:** agent-docs/model/esm_metamodel/other.md (measures)
- **What to add:**
  - **Derived measures and unit conversion rates** (how-to, `P08-03`). Measures are either base measures (e.g. Mass with kilogram) or derived measures defined as terms of other measures with exponents, e.g. Acceleration = Velocity.metrePerSecond × Time.second^-1, Area = Length.metre^2 (withExponent(2)); a derived measure may not reference itself recursively.
  - **Measure unit conversion contract between transfer and entity values** (how-to, `P15-07`). When a payload value moves between a transfer object and an entity, the DAO converts between measure units using the rateDividend/rateDivisor of both units, rounds to scale 20 with HALF_UP (MEASURE_CONVERTING_SCALE = 20), and returns a BigInteger when the entity attribute type is an integer type.
  - **MeasuredType store-unit selection and precision semantics** (mention-only, `P08-04`). A MeasuredType ties a NumericType to a stored unit: e.g. MassStoredInKilograms (precision 15, scale 4) with storeUnit $mass.kilogram, MassStoredInGrams with $mass.gram, TimeStoredInMonths (precision 9, no scale) with storeUnit $moMonthBasedTime.month, VolumeStoredInLitre with $volume.litre.
  - **Defining unit conversion rates (rateDividend/rateDivisor) relative to a base unit** (mention-only, `P07-02`). In the ESM measure package, a Measure groups Units; the base unit is the conversion anchor and every other unit carries a rational conversion pair rateDividend/rateDivisor (EBigDecimal, lowerBound 1) relative to that base unit.

### Frontend build properties, environment variables and base path

- **Priority:** Medium · **Area:** frontend · **Evidence:** judo-ng: `judo-esm-fullstack-project-template`, `judo-ui-react-template`, `judo-jsl-fullstack-karaf-project-template`
- **Put it in:** agent-docs/frontend/development-workflow.md (env and build properties table)
- **What to add:**
  - **Full frontend environment-variable reference** (topic, `P33-07`). The generated frontend consumes a specific env-var set: VITE_API_DEFAULT_BASE_URL (fallback window.location.origin), VITE_API_RELATIVE_PATH (fallback '/api'), VITE_FILE_DEFAULT_BASE_URL (fallback the API base URL), and optionally VITE_MUI_LICENSE_KEY.
  - **Frontend Maven build modes and module properties (frontend-build-type, muiLicensePlan, override-dir)** (how-to, `P30-11`). The generated React frontend actor POM selects a build strategy via `frontend-build-type`: default `full` (pnpm install/format/build/test), `CI` (install/build/test), `quick` (format + build:reckless).
  - **Frontend context path and multi-actor routing / base href** (how-to, `P28-05`). Each actor's React frontend is hosted at an OSGi Web-ContextPath of /<model-name><frontend postfix>/<actor-name> for multi-actor apps (or singleApplicationPath / '/' for a single-actor app).
  - **Node/pnpm version pinning and automatic toolchain bootstrap** (how-to, `P28-08`). Node and pnpm versions are pinned by template parameters (defaults node-version 24.13.1, pnpm-version 10.15.0; frontend-maven-plugin version fixed at 1.12.1).

### Forcing regeneration: `.generator-checksum-ignore`, Biome false positives

- **Priority:** Medium · **Area:** frontend · **Evidence:** 1 session(s); judo-ng: `judo-meta-ui`
- **Put it in:** agent-docs/frontend/development-workflow.md
- **What to add:**
  - **.generator-checksum-ignore: forced regeneration of manually modified files** (topic, `P10-02`). The generator supports a .generator-checksum-ignore file whose .gitignore-style globs mark files that skip checksum validation and are always regenerated, even when manually modified. This is distinct from .generator-ignore (which prevents files from being written/indexed/deleted at all).
  - **Second frontend build false-positive 'manually changed' files: Biome reformat runs after checksum capture** (how-to, `S25-02`). In a JUDO generated frontend the build pipeline records checksums of generated files (`generated-files-genericuser`) and THEN the default `build-frontend-full` profile runs `pnpm run format` (`biome format ./src --write && biome check --write ./src`), which rewrites those very files after the checksum was taken.

### Running JUDO on Spring Boot

- **Priority:** Medium · **Area:** deployment · **Evidence:** judo-ng: `judo-runtime-core`, `judo-psm-generator-sdk-core`, `judo-spring-maven-plugin`, `judo-runtime-core-jsl`
- **Put it in:** agent-docs/deployment/spring-boot.md (new; only if the Spring stack is in scope)
- **What to add:**
  - **Running JUDO on Spring Boot (autoconfiguration, model discovery)** (topic, `P18-03`). JUDO provides a full set of Spring Boot autoconfiguration modules (judo-runtime-core-spring, spring-hsqldb, spring-postgresql) that assemble the RDBMS runtime (DAO, dispatcher, query factory, variable resolver, identifier signer) without OSGi/Karaf.
  - **Spring Boot application wiring keys (spring.datasource.*, spring.liquibase.change-log, judo.modelName)** (how-to, `P17-05`). A JUDO Spring Boot app is configured via `application.properties`: `spring.datasource.url`/`username`/`password`, `spring.liquibase.change-log=classpath:model/<Model>-liquibase_hsqldb.changelog.xml`, and `judo.modelName=<Model>` to select the JUDO model.
  - **Spring Boot auto-configuration of generated SDK DAOs** (topic, `P32-02`). The spring module of the SDK generator emits one Spring @Configuration class per model (<Model>DaoModules in the springPrefix package) with three @Autowired fields (DAO, AsmModel, PayloadValidator) and one @Bean method per DAO, static navigation and static data (allDaoTransferObjectType / …
  - **judo-spring-maven-plugin transformerWorkflow configuration (dialect auto-detection, SDK template cartridges, skip flags)** (how-to, `P29-02`). The build runs the judo-spring-maven-plugin goal `transformerWorkflow` bound to generate-sources. Key parameters a developer configures: `dialects` (auto-detected from project dependencies - hsqldb when org.hsqldb:hsqldb present, postgresql when org.postgresql:postgresql present;

### OpenAPI: generating and serving API docs, generating clients

- **Priority:** Medium · **Area:** integration · **Evidence:** judo-ng: `openapi-generator-cxf-jaxrs-client-osgi-ds`, `judo-services`, `judo-psm-generator-jaxrs`, `judo-esm-fullstack-project-template` …
- **Put it in:** agent-docs/deployment/application-config.md + agent-docs/backend/rest-api-contract.md
- **What to add:**
  - **OpenAPI/Swagger documentation generation of the REST API** (mention-only, `P30-10`). When `generateOpenApiAnnotations=true`, the rest module runs swagger-maven-plugin (resolve) writing OpenAPI JSON/YAML under `target/api-documentation-swagger`, embedded into the bundle via Include-Resource/Openapi-Content, and every service/DTO carries `@Schema`/OpenAPI annotations.
  - **OpenAPI / Swagger API documentation generation** (how-to, `P28-02`). The generated REST module can emit an OpenAPI spec: when the isGenerateOpenApiAnnotations generator parameter (or input variable ignoreOpenAPI=false) is set, generateOpenApiAnnotations becomes true and the swagger-maven-plugin resolves the spec to target/api-documentation-swagger as both openapi.json and openapi.yaml;
  - **OpenAPI/Swagger UI serving location per model (/api-spec/<model>)** (mention-only, `P21-07`). A SwaggerUIServlet is registered per OpenapiModel on the HttpService at `/api-spec/<model name>` (API_SPEC_URL + '/' + name). The `apiRoot` config key defaults to `/api` and becomes the swagger.json basePath prefix: basePath = apiRoot + '/' + model name;
  - **Generating OSGi Declarative Services REST clients from OpenAPI specs** (topic, `P34-06`). The openapi-generator-cxf-jaxrs-client-osgi-ds generator (generator name `jaxrs-cxf-client-osgi-ds`) produces a CXF JAX-RS client that is packaged as an OSGi bundle with a Declarative Services activator.

### Custom application parameters (OSGi Configuration Mapper) and encrypted values

- **Priority:** Medium · **Area:** backend · **Evidence:** judo-ng: `osgi-encryption`, `documentation`, `karaf-jasypt-support`
- **Put it in:** agent-docs/deployment/application-config.md (custom parameters, ENC())
- **Catalog today:** No file mentions Jasypt or `ENC(`.
- **What to add:**
  - **OSGi Configuration Mapper for custom application parameters** (topic, `P01-04`). Application-level configuration for JUDO additions is defined through the OSGi Configuration Mapper: a configset declares templatePath (classpath folder with *.template FreeMarker files), envPrefix (e.g. MY_APP_), and variableScopePreference (osgi,environment,system).
  - **Jasypt-encrypted configuration values (ENC(...)) and PAX-JDBC database passwords** (topic, `P27-01`). JUDO runtime ships jasypt-based encryption services (karaf-jasypt-support and osgi-encryption). A developer embeds secrets in configuration as `password=ENC(encrypted_password)`;
  - **Multiple encryptor aliases and ENC(value, alias) selection** (how-to, `P27-02`). osgi-encryption supports several independent Encryptor services, each carrying an `encryptor.alias` service property. Config values `ENC(value)` use the default encryptor; `ENC(value, alias)` select one by alias via the OSGi filter `(encryptor.alias=<alias>)` in OsgiConfigDecryptor.

### Customizing the Keycloak login theme

- **Priority:** Medium · **Area:** security · **Evidence:** judo-ng: `judo-esm-fullstack-project-template`, `judo-keycloak`, `judo-jsl-fullstack-karaf-project-template`
- **Put it in:** agent-docs/deployment/keycloak-theme.md (new)
- **Catalog today:** No file mentions the login theme or `.ftl`.
- **What to add:**
  - **Custom Keycloak login theme development** (topic, `P28-01`). The fullstack template ships a generated keycloak-theme Maven module (src/main/resources/themes/keycloak-theme/) containing FreeMarker login pages (login.ftl, register.ftl, error.ftl, template.ftl with the registrationLayout macro), a theme.properties (parent=base, import=common/keycloak, …
  - **Customizing the JUDO Keycloak auth theme (login/account/email)** (how-to, `P34-01`). JUDO ships a custom Keycloak theme (judo-keycloak) that overrides the stock `keycloak` theme via `parent=base` + `import=common/keycloak` and defines the branded login/account/admin/welcome/email templates as FreeMarker files (login.ftl, template.ftl, welcome/index.ftl).
  - **Customizing the generated Keycloak login theme (FreeMarker FTL)** (mention-only, `P30-07`). The generated project ships a Keycloak theme module (`<model>-theme`, packaged as a zip of `src/main/resources/themes`) whose login pages are FreeMarker templates: `login.ftl` (username/password, remember-me gated on `realm.rememberMe`, forgot-password on `realm.resetPasswordAllowed`, …

### Generated operation behaviours (GET_RANGE, GET_TEMPLATE, create validation)

- **Priority:** Medium · **Area:** model · **Evidence:** judo-ng: `judo-meta-psm`
- **Put it in:** agent-docs/model/esm_metamodel/operation.md (behaviour types)
- **What to add:**
  - **GET_RANGE operation behaviour (reference-range sourcing)** (how-to, `P08-05`). GET_RANGE is an operation behaviour that sources the options of a reference dropdown/autocomplete. It is implemented as an unbound operation (e.g.
  - **GET_TEMPLATE operation behaviour (default/prefill templates)** (topic, `P08-06`). GET_TEMPLATE is a modelled operation behaviour for producing a prepopulated/form template: it must be owned by an UnboundOperation, its owner must be a transfer object type, and it must not reference a relation.
  - **Creatable transfer objects: abstract targets and required-feature binding** (how-to, `P08-09`). A transfer object type used as a CREATE_INSTANCE or VALIDATE_CREATE target must not map to an abstract entity type, and every required feature of the mapped entity (required relations with lower > 0 and required attributes) must be bound by the transfer object, otherwise validation fails with AllRequiredFeaturesHaveBindingIfCreatable.

### Long-running operations: frontend/proxy timeout (503)

- **Priority:** Medium · **Area:** frontend · **Evidence:** 1 session(s)
- **Put it in:** agent-docs/deployment/production.md
- **What to add:**
  - **Frontend service-operation timeout drops long operations with 503** (topic, `S13-04`). Operations that run longer than roughly 30 s get dropped by the frontend service layer with HTTP 503 even though the backend returns the response correctly for big/long operations. The request timeout is configured in the React frontend service layer, not the backend;

### Creating and upgrading a JUDO project (archetypes, version updater)

- **Priority:** Medium · **Area:** deployment · **Evidence:** judo-ng: `documentation`, `judo-version-updater-maven-plugin`, `judo-jsl-springboot-parent`, `judo-jsl-springboot-archetype`
- **Put it in:** agent-docs/deployment/new-project.md (new)
- **What to add:**
  - **Bootstrapping a new JUDO JSL Spring Boot project (archetype + parent-POM constraints)** (how-to, `P29-01`). A new JUDO app is generated from the maven-archetype-plugin (3.1.1:generate) with `modelName` as the only required parameter (regex ^[a-zA-Z0-9]+$); groupId defaults to com.example, artifactId to lowercased modelName, package to groupId.artifactId, and the main class to <ModelName>Application.
  - **Bootstrapping an application project from Maven archetypes** (how-to, `P01-08`). Beyond the JUDO Designer 'New project' flow, applications can be bootstrapped from Maven archetypes: judo-jsl-springboot-archetype (Spring Boot app with generated application.yml, HSQLDB + Liquibase changelog classpath:model/@judo-model-name@-liquibase_hsqldb.changelog.xml, judo.modelName …
  - **Scaffolding and versioning a new JUDO project (judo-version-updater goals)** (how-to, `P34-04`). The judo-version-updater-maven-plugin provides the goals that bootstrap and pin JUDO projects: `update-judo-versions` (resolves the latest hu.blackbelt.judo:judo-versions version against version-ruleset-{channel}.xml from nexus.judo.technology, applies major/minor/incremental update constraints, …

### Static navigations and static data

- **Priority:** Low · **Area:** model · **Evidence:** judo-ng: `judo-meta-psm`
- **Put it in:** agent-docs/model/esm_metamodel/ (static navigation / static data rows) + model-development.md
- **What to add:**
  - **Static navigations (reference-data lists)** (topic, `P08-01`). A static navigation is a model element that exposes a fixed, query-free collection of entities via a getter expression (e.g.
  - **Static data (model-level constants and counters)** (topic, `P08-02`). StaticData is a model element holding a single constant value, e.g. TotalNumberOfOrders (required Integer) whose getter expression is the literal '0 // COUNT(northwind::entities::Order)'. The COUNT is only a comment, so the value is always 0.

### Request tracing (exchange id) and validation-message localization

- **Priority:** Low · **Area:** backend · **Evidence:** judo-ng: `cxf-jaxrs-application-manager`, `judo-runtime-core`
- **Put it in:** agent-docs/backend/debugging-and-monitoring-guide.md
- **What to add:**
  - **Exchange-id request/response correlation for log tracing** (how-to, `P11-06`). Two built-in CXF interceptors provide per-request correlation: ExchangeIdDecorator (IN, Phase.RECEIVE) assigns a UUID to each Exchange under the 'exchangeId' key and puts it into the SLF4J MDC under key 'RequestExchangeId';
  - **Request exchange-ID tracing (X-Exchange-Id header, MDC correlation)** (mention-only, `P18-06`). A CXF interceptor pipeline decorates each HTTP request with a UUID exchange id: ExchangeIdDecorator stores it on the CXF Exchange under key 'exchangeId' and publishes it into the SLF4J MDC under key 'RequestExchangeId';

### Low-level persistence hooks worth one paragraph each

- **Priority:** Low · **Area:** backend · **Evidence:** judo-ng: `osgi-liquibase`, `judo-dao-api`
- **Put it in:** agent-docs/backend/data-access-guide.md
- **What to add:**
  - **Running Liquibase changelogs from OSGi bundles (LiquibaseExecutor)** (mention-only, `P27-06`). osgi-liquibase exposes a LiquibaseExecutor service with executeLiquibaseScript(Connection, scriptPathInBundle, Bundle) and an overload taking a Map<String,Object> of changelog parameters.
  - **QueryCustomizer builder fields for low-level DAO calls** (how-to, `P11-08`). QueryCustomizer is a Lombok @Builder with fields: filter (String, a JQL expression), orderByList (@Singular 'orderBy'), seek, withoutFeatures, mask, parameters and instanceIds, and exposes an orderBy(OrderBy) adder.

### API-level tests against generated REST (ApiClient, Postman)

- **Priority:** Low · **Area:** testing · **Evidence:** judo-ng: `judo-tatami-tests`, `judo-psm-generator-restassured`
- **Put it in:** agent-docs/integration-testing/api-level-tests.md (new)
- **What to add:**
  - **REST Assured generated test client (ApiClient) for API-level tests** (topic, `P30-02`). The REST Assured generator (judo-psm-generator-restassured) emits a static `ApiClient.api(Config)` entry point per model with `BASE_URL_<ACTOR>` constants, `authTo<Actor>(grantType, userName, password)` OIDC password-grant helpers (posting `client_id=<model>-<actor>`, password, `grant_type`), and …
  - **Automated API-level testing of generated services (Postman / OpenAPI)** (topic, `P25-02`). The generated application ships Postman collections (v2.1.0) that exercise the REST API against a running instance (local Karaf on http://localhost:8181), asserting status codes, error codes and response shapes.

### Backend CORS filter configuration

- **Priority:** Low · **Area:** deployment · **Evidence:** judo-ng: `judo-platform`
- **Put it in:** agent-docs/deployment/application-config.md
- **What to add:**
  - **Per-model backend CORS filter configuration keys** (how-to, `P14-04`). CxfSecurityActivator registers a per-model CrossOriginResourceSharingFilter with service filter application.filter=(judo.model.name=<model name>) and derives it from OSGi config keys: cors_allowOrigin (default "*", comma-split when set), cors_allowCredentials (true), cors_allowHeaders (default …

### Flutter frontend build

- **Priority:** Low · **Area:** deployment · **Evidence:** judo-ng: `judo-maven-plugin`, `flutter-maven-plugin`
- **Put it in:** agent-docs/deployment/build-process.md (only if Flutter is in scope)
- **What to add:**
  - **Building Flutter frontends via the JUDO Maven plugin (flutter / install-flutter goals)** (topic, `P34-02`). JUDO generates Flutter frontends alongside React, and drives their build with Maven plugin goals: `install-flutter` (installs the Flutter SDK from a pinned version archive or a Git channel, default channel `stable`, verified via `flutter doctor`/`flutter --version`) and `flutter` (runs arbitrary flutter CLI commands, default `pub get`).

## 3. best-practices: missing patterns

### Model changes that break generated/custom frontend code

- **Priority:** High · **Area:** frontend · **Evidence:** 14 session(s)
- **Put it in:** best-practices/frontend/model-change-propagation.md (new)
- **What to add:**
  - **Deleting a model attribute breaks custom code that references it (TS2339) — sync custom frontend/backend** (pattern, `S06-04`). Removing a model member (e.g. the `shouldBeFilled` requiredBy attribute/DataField) regenerates the type surface, so any custom frontend hook/component that still references the property fails to compile (TS2339).
  - **Frontend generated TS breaks when model transfer objects are retargeted/added: stale custom-hook import paths and type drift** (pattern, `S03-08`). Adding or retargeting transfer objects in the model regenerates the frontend TypeScript surface, and custom hooks that import from generated dialog/page customization modules break with TS2307 'Cannot find module' when the path is removed or renamed (e.g.
  - **Renaming a model operation propagates to generated frontend (duplicate updateAction, missing custom hook path)** (how-to, `S06-03`). Renaming an operation in the model regenerates frontend action/container files and custom hook scaffolds;
  - **Frontend hook files are generated only when the hook is set in the model; the src/custom folder is gitignored so .generator-ignore entries are not needed for hooks** (mention-only, `S02-03`). The frontend generator emits a hook file only when the corresponding frontend hook/action flag is set in the model (e.g. generateActionsHook); without the model flag there is no scaffold to customize.
  - **Adding an attribute touches a whole surface: entity, service TO mapping, backend mask, frontend hook mask, i18n, Excel import, tests** (pattern, `S08-02`). Adding one model attribute is not a single edit: it must be added to the entity, mapped onto the service-level transfer objects (create/update/view/input forms), exposed in the backend query mask, and additionally added to the frontend custom hook mask so it is actually queried and rendered;
  - **Deleting model elements requires cleaning transfer views/tables/forms and resolving createability** (how-to, `S26-04`). When an attribute/relation/entity is removed from the model you must also delete it from the transfer views, tables and forms (and any related derived members/bindings), otherwise model validation fails at build.
  - **Consolidating a duplicate entity/TO across service packages cascades into generated frontend hook names and Java interceptor imports** (mention-only, `S09-06`). When the same entity/transfer object exists in several service packages (e.g.
  - **Frontend features must be modeled as ESM UI elements, not implemented as whole custom components** (pattern, `S11-07`). To add a new field/column/operation to the UI, the proper approach is to model the UI parts in the ESM model (add the element to the View/Form/Table transfer objects, with the canonical <TO>View/Form/Table naming) and then customize behavior via Pandino hooks/overrides — not to implement the whole feature as a custom frontend component replacing generated code.

### DAO read/write performance: seek, batching, eager owned relations

- **Priority:** High · **Area:** backend · **Evidence:** 9 session(s)
- **Put it in:** best-practices/backend/dao-read-write-performance.md (new)
- **What to add:**
  - **JUDO generated-DAO performance: read-bounding against H+1 and per-instance vs batched creates** (how-to, `S14-02`). When optimizing generated JUDO report/collection generation, the dominant cost is usually the shared per-header report-projection read (loading each header's faults x errorCategories x errorCodes graph), not the writes; profile first before optimizing.
  - **Optimizing bulk initial-data import: createAll batching, cached lookups, and create-with-mask** (pattern, `S20-01`). To speed up a JUDO initial-data import (Init/ExcelDataImporter), do not create entities one-by-one with per-row DAO lookups.
  - **Owned-relation (aggregation/composition) eager materialization returns empty {} payloads that fail update validation** (how-to, `S14-01`). In JUDO, an owned relation (aggregation/composition) on an editable view is eagerly embedded into the read mask regardless of the displayed columns, and the server force-materializes an aggregation's mandatory members even when unmasked, returning empty objects (e.g.
  - **Derived fields do not render unless explicitly added to the Mask / interceptor projection** (how-to, `S06-02`). A derived attribute (e.g.

### Enforce rules server-side, not only in the UI

- **Priority:** High · **Area:** security · **Evidence:** 9 session(s)
- **Put it in:** best-practices/backend/server-side-guards.md (new)
- **What to add:**
  - **Model min/max range bounds are UI-only and do not reject server-side updates** (how-to, `S06-05`). A range/min-max bound configured on a model field only drives the generated frontend display (red inline message) — it does NOT stop the backend update from persisting an out-of-range value.
  - **Delegation authorization belongs in the operation, not only in a hidden UI button; ownership propagates silently** (domain, `S17-02`). A workflow operation like delegateFaultRegistry must enforce its own state and role guards; if the only restriction lives in a frontend button expression (hiddenBy = isNotDraft), then once a record leaves that state the operation is still callable and the record strands with the original recorder.
  - **Server-side write-guard interceptors: enumerate target operations' FQNs directly and group by role instead of extracting accesses from the model at runtime** (pattern, `S18-02`). Hiding UI menus / filtering the list for a role does NOT protect the entity: the create/update/delete operations are still callable through the generated REST layer, so writes must be guarded server-side.
  - **Field-level role-based edit guard on a shared entity, with the field hidden from the view for unauthorized roles** (domain, `S04-04`). Domain rule for an inspection app: a shared entity (Partner) has fields that only elevated roles may modify — the confidence attribute may be updated only by ehsmanager, prses, operator manager and service admin — while a fault recorder may not write any partner field at all.

### E2E methodology: baseline dump, real-UI first, time budget

- **Priority:** High · **Area:** testing · **Evidence:** 9 session(s)
- **Put it in:** best-practices/ e2e entry (new) + agent-docs/e2e-testing/testing-patterns.md
- **What to add:**
  - **E2E baseline orchestration: prepared DB dump (incl. Keycloak users) built once, parallel stacks on distinct ports** (pattern, `S18-04`). For E2E suites the team wanted a reusable prepared dump produced by judo.sh containing all test data and base roles together with Keycloak users (Keycloak shares the backend DB), rebuilt once, and a flow that recreates it when it goes stale.
  - **E2E should drive real UI, API only for access/hidden-menu cases** (how-to, `S24-06`). The team convention is that e2e tests must navigate through the actual pages and assert visible elements via the browser rather than calling REST endpoints directly; only access-related assertions that verify hidden menu items/authorization shape may remain REST-only.
  - **E2E suite methodology: seed from one base dump, test groups derived from it, ~2-minute budget, UI-over-REST with mermaid-model guidance** (how-to, `S25-04`). For JUDO E2E suites, create the DB once from a single base dump and derive all test groups from that dump (no new dumps per test), keeping each test run within ~2 minutes; use a cloneable PostgreSQL for quick test purposes.
  - **Integration tests should create only the entities they need, not load full init/master data** (how-to, `S10-04`). JUDO integration tests should be class-scoped and self-contained: create exactly the entities a test needs via DAO builders/fixtures instead of invoking the application-wide `initializeMasterData`/Init seeding. Reusing a runtime version that caches the model loader makes this style faster;

### Model workflow gates as derived predicates over status

- **Priority:** High · **Area:** model · **Evidence:** 8 session(s)
- **Put it in:** best-practices/model/ (new entry)
- **What to add:**
  - **Represent transient workflow conditions as derived predicates over status, stored flags only for permission carriers** (pattern, `S17-03`). In a stateful workflow model, a condition like 'is channelled' should be derived from status plus timestamps, not stored as a boolean attribute; a stored attribute and its update logic silently drift out of sync with the state machine. Keep stored only what is a genuine permission/flag carrier (e.g.
  - **Multi-role JQL actor-filter exclusion edge case** (pattern, `S07-06`). Derived getterExpression role-guards of the form `User!filter(u | u.email == ...getVariable("ACTOR","email") and (u.roleX or u.roleY ...))!empty()` and especially their negation `not ...!empty()` can wrongly exclude a user who holds two roles, one granted and one denied (e.g.
  - **Menu/gate visibility attributes live on the principal/transfer projection** (mention-only, `S19-10`). Hidden-menu/visibility gate attributes (hiddenBy, menuHidden*, canCloseFaultRegistry* and the access gate) belong on the service-user transfer / principal projection rather than the plain entity;
  - **Role-gate polarity does NOT scope an access to the actor's own data** (pattern, `S17-01`). Adding an actor role to an access's role-gate only gates /who may open that access/; it does not restrict the rows that access reads or edits.

### Document template authoring (FreeMarker/DOCX, Handlebars) and repair

- **Priority:** High · **Area:** backend · **Evidence:** 8 session(s)
- **Put it in:** best-practices/backend/document-template-authoring.md (new)
- **What to add:**
  - **DOCX template authoring syntax and corrupted-template repair** (how-to, `S13-01`). XDocReport/Freemarker DOCX templates embed whole template directives inside Word MERGEFIELD field codes: `#list x as y` / `/#list` loops, `#if cond??` / `/#if` conditionals, `@before-row[#list ...]` / `@after-row[/#list]` row/table markers, and `${field!}` default vs `${field??}` null-guard access;
  - **FreeMarker/DOCX template null-safety and filter idioms; parse errors from mismatched #if/#list** (how-to, `S09-02`). DOCX report templates are FreeMarker (xdocreport). Every merge-field that can be null/missing must carry a default (`!false`, `!''`, `??`, or `?filter(...)`) or render fails with 'evaluated to null or missing';
  - **Handlebars in document templates: counting (@index_1) and frontmatter escaping** (how-to, `S15-04`). For Handlebars document templates (used to render markdown reports), the standard loop context exposes @index (0-based), @index_1 (1-based), @key, @first, @last, @odd, @even — so numbering like 1.1 / 2.1 can be done in the template without custom helpers.

### Report/export SPIs: JasperReports, Excel export, Markdown reports

- **Priority:** High · **Area:** integration · **Evidence:** 4 session(s); judo-ng: `judo-runtime-core`, `judo-psm-generator-report`
- **Put it in:** best-practices/backend/ (one entry per SPI)
- **What to add:**
  - **JasperReports report generation from the model** (topic, `P30-01`). The report generator (judo-psm-generator-report) produces a full JasperReports layer for every qualifying TransferObjectType: a `{Type}Report` facade with `generate{Type}Report(OutputType, dto, File|OutputStream[, Map<String,Object> additionalParameters])` overloads, …
  - **Platform EXPORT operation and Excel Export SPI (JxlsExport)** (how-to, `P16-03`). Modeled EXPORT operations run through an Export SPI whose reference implementation is JxlsExport, producing XLSX via JXLS/POI.
  - **Markdown + Handlebars report generation pipeline (replacing XDocReport DOCX leg)** (pattern, `S16-01`). The report families were migrated from the legacy XDocReport/Freemarker DOCX leg to a new pipeline: .md.hbs templates rendered with Handlebars (4.1.2), then converted docx->pdf.

### Registry numbering: no burn on regenerate, real locking (update existing blueprint)

- **Priority:** High · **Area:** backend · **Evidence:** 4 session(s)
- **Put it in:** model-blueprints/document-registry-sequence (update)
- **Catalog today:** document-registry-sequence exists but misses both rules.
- **What to add:**
  - **Registry-number stability & document versioning: don't burn currentIndex on regenerate; split view display from render version** (domain, `S09-03`). A DocumentRegistry currentIndex must only be consumed on the create path, not on regeneration of an existing AssessmentSheet/ReviewReport/Offer (allocate inside the create-only orElseGet).
  - **DocumentRegistry numbering: `synchronized` is not enough — the DAO update lands outside the atomic section (concurrency/sequence correctness)** (how-to, `S25-06`). Generating consecutive unique human-readable registry numbers (e.g. FR-00042) from a stored `DocumentRegistry.currentIndex` is a read-modify-write sequence;

### Adding a non-Java sidecar service (Node/AI) to a JUDO app

- **Priority:** Medium · **Area:** integration · **Evidence:** 2 session(s)
- **Put it in:** best-practices/backend/sidecar-service.md (new)
- **What to add:**
  - **Adding a non-Java sidecar (Node/AI service) to a JUDO Karaf app: artifact publish, env-var naming and compose wiring** (pattern, `S25-03`). To integrate an external plugin (e.g.
  - **Asynchronous fire-and-forget external-service operation bound to an instance, result observed by client-side polling** (pattern, `S04-03`). A reusable JUDO pattern for integrating an asynchronous external service (e.g. an AI/photo-processing service): declare a custom operation with NO input parameter (the bound instance IS the entity, e.g.

### Report validation problems as optional transient output, lazily loaded

- **Priority:** Medium · **Area:** model · **Evidence:** 2 session(s)
- **Put it in:** best-practices/model/ (new entry)
- **What to add:**
  - **Report validation problems as an optional output transient transfer instead of throwing** (pattern, `S19-09`). When an operation can fail validation on several items, prefer returning an optional output transient transfer that lists the errors (each with elementFaultId, position, code, message) over throwing a single business error — return no error row when everything passes.
  - **Lazy-loaded validation-error collection for registry inspection workflows** (pattern, `S19-05`). For an inspection/fault-registry workflow, report validation problems as a persistent error collection on the registry: persist errors at entity level as a composition child today but expose them at transfer level as an association that is only queried when the user expands the error list.

### Native SQL / DataSource access from custom code

- **Priority:** Medium · **Area:** backend · **Evidence:** 2 session(s)
- **Put it in:** best-practices/backend/native-sql-datasource.md (new)
- **What to add:**
  - **Native SQL / JDBC / DataSource query from a JUDO custom service** (topic, `S08-01`). To look up rows that JQL and the generated QueryCustomizer cannot express (e.g. finding the owning JobSheetItem of a picture via the join table j_entities_job_sheet_item_pictures), a service needs to run a native SQL query.

### Type-ahead with a self-learning reference dictionary

- **Priority:** Medium · **Area:** model · **Evidence:** 2 session(s)
- **Put it in:** best-practices/model/ (new entry)
- **What to add:**
  - **typeAHead designer flag + self-learning reference dictionary (learn() on parent create, bulk CSV import)** (pattern, `S14-03`). Setting a typeAHead (TypeAhead) boolean designer flag on a string attribute (e.g. form_postalcode / form_city) makes the generated frontend use the TextWithTypeAHead component with getForm_*Options getters, and the range/options come from reference-data lookups.

### Detailed bilingual history/audit messages

- **Priority:** Medium · **Area:** domain · **Evidence:** 2 session(s)
- **Put it in:** model-blueprints/history-audit-trail-entity (extend)
- **What to add:**
  - **Detailed history/audit messages with bilingual i18n and date/enum interpolation** (mention-only, `S21-03`). To enrich audit history (e.g.

### Operation input prefill (initializer) and range selectors

- **Priority:** Medium · **Area:** model · **Evidence:** 1 session(s)
- **Put it in:** best-practices/model/ (new entry)
- **What to add:**
  - **Operation input TO prefill and range-selector relation** (pattern, `S13-02`). Generate-style operations (generateDocument, generateWorkReport) take a separate `*Input` transfer object rather than reading from the entity directly.

### Serving stored binaries without exposing filestore ids

- **Priority:** Medium · **Area:** security · **Evidence:** 1 session(s)
- **Put it in:** best-practices/backend/ (new entry)
- **What to add:**
  - **Secure serving of stored binary content (images) without exposing the filestore id** (pattern, `S18-01`). Binary entities (e.g. Picture) are stored via the JUDO FileStore and returned as FileType references whose id is the filestore key; putting that id directly in a public URL lets callers retrieve any stored file by guessing/enumerating ids.

## 4. model-blueprints: missing domain knowledge

### Inspection fault-registry / ticketing lifecycle

- **Priority:** High · **Area:** domain · **Evidence:** 24 session(s)
- **Put it in:** model-blueprints/inspection-fault-registry-ticketing (new)
- **Catalog today:** No blueprint for inspection / fault-registry ticketing.
- **What to add:**
  - **Domain: fault-registry ticketing lifecycle — state machines with derived gate flags, discard/convert flows, and role+state gating reused across PreliminaryElementFault and DefectTicket** (domain, `S02-04`). The PreliminaryElementFault / DefectTicket capacity share a lifecycle pattern: an enumeration state (e.g. RECEIVED/SUPPLEMENTED/FINALIZED/DISCARDED;
  - **Domain: role-gated fault-registry close & offer readiness workflow** (domain, `S24-07`). Inspection/offer workflows: the ability to close a fault registry is a role-gated permission (e.g. canCloseFaultReport only for the ESO actor, surfaced as a checkbox on user create). Close-for-offer and close-without-offer are two mutually exclusive operations;
  - **Fault-registry modification guard: assignee/partner-territory visibility (inner roles act only on their own registries; others read-only; cannot undo DONE by re-submitting)** (pattern, `S25-05`). Recurring rackinspect role-visibility rule: a partner-related role (e.g. prses) sees only its own partner as its landing page and can modify a fault registry only while the registry is assigned to it; other (non-assignee) partner roles and ESO see registries read-only.
  - **Fault-registry workflow: delegation chain, ownership propagation, and status-gated UI vs operation guards** (domain, `S23-04`). In an inspection/repair domain the delegated owner is the load-bearing fact: `delegateFaultRegistry` sets the assigned user and that user silently becomes owner of the Offer → JobSheet → WorkReport chain (OfferServiceImpl.generateOffer copies assignedTo from the registry).
  - **Ticketing domain: role/state gates, PRSES recipients, and fault-registry flow** (domain, `S06-09`). The ticketing flow is a role/state-gated workflow: roles drive state machines and gates (e.g.
  - **Unscheduled (eseti) inspection/fault-registry document workflow** (domain, `S07-05`). An 'unscheduled' (eseti) fault registry is a distinct inspection type: it is created only via `createFaultRegistryFromPef`, has its own review-report and assessment-sheet templates (copies of the standard ones with 'eseti' instead of 'éves'), does NOT generate a registry number (like an internal …
  - **Fault registry created from an offer (clone flow + versioning constraint)** (domain, `S22-01`). In the rackinspect inspection/repair domain, a new fault registry is derived from an accepted offer by cloning only the fault elements that are not fully covered by the offer (quantity-checked);
  - **Insider roles self-delegate; non-insider roles require an assigned advisor (per-user canClose flag)** (domain, `S17-04`). In a role-partitioned inspection workflow: internal (insider) roles perform delegation freely between themselves and have no advisor; external/partner roles (PRSES, ESO, advisor-linked users) cannot self-serve and must have an assigned advisor who receives their submits.

### Job sheet → work report → completion certificate pipeline

- **Priority:** High · **Area:** domain · **Evidence:** 11 session(s)
- **Put it in:** model-blueprints/jobsheet-workreport-certificate (new); link work-status-lifecycle-enum
- **What to add:**
  - **JobSheet → WorkReport → Completion Certificate pipeline** (domain, `S11-06`). After an offer is done and quantity validation passes, generate a JobSheet and its JobSheetItems split by fault element and quantity, numbered incrementally per fault (no global sequence).
  - **JobSheet/WorkReport end-to-end domain cluster: gated generation, seeded fields, versioned document pipeline** (domain, `S12-07`). The rackinspect field-service workflow is a reusable cluster: from an Offer, `generateJobSheet` seeds externalId/subcontractor/contact and is only valid before the status is done and no completion certification exists — the generation button should be hidden unless the condition holds, but the …
  - **Work report / completion-certificate kind-gated completion workflow** (domain, `S13-03`). A reusable kind-based completion workflow: a WorkReport has a `kind` (WORK_REPORT vs COMPLETION_CERTIFICATE) and a `workStatus` enum; a `toDone` operation's prerequisite depends on the kind (WORK_REPORT requires generated documents;
  - **Work-item status-change guards: photo required for done, reason required for won't-fix** (mention-only, `S22-05`). For inspection/repair work items with a NOT_STARTED/IN_PROGRESS/DONE/WONT_FIX status, setting an item to DONE should require at least one (after) photo, and setting it to WONT_FIX should require a populated reason attribute passed into the operation input (the current bulk operation only fails the items that lack the reason).

### Offline-first mobile ingest: localId idempotency, two-stage upload, change stamps

- **Priority:** High · **Area:** domain · **Evidence:** 10 session(s)
- **Put it in:** model-blueprints/offline-mobile-ingest (new)
- **Catalog today:** No blueprint for offline mobile sync.
- **What to add:**
  - **Offline mobile sync conflict/coordination pattern (field-service owner-split)** (domain, `S01-02`). For a field-service mobile app that syncs JUDO data offline, the reusable pattern is owner-split (the technician owns workStatus + photos, the office owns assignment/composition) layered on replay-based operations rather than full record copies;
  - **Offline-first mobile ingest: embed media attachments in the input TO and track per-media upload state via localId** (domain, `S04-05`). For a mobile client that uploads a ticket with media over a flaky connection, prefer embedding `MediaAttachment` entries inside the ticket's input TO (`DefectTicketInput`) rather than a separate upload step, and give each media (and the ticket) a `localId` so the client can tell which attachments have actually uploaded.
  - **Sync change-stamps pattern (catalogue/revised timestamps for mobile pull-sync)** (pattern, `S07-03`). For mobile pull-sync, add change-stamp timestamp attributes (e.g. `catalogueChangedAt`, `supplementRequestsChangedAt`) on the partner/root TO.
  - **Client correlation-key (localId) for idempotent push** (pattern, `S01-05`). To make a client push idempotent, give the pushed object a client-generated stable key (localId) that is sent with the create and later filterable (`filterByLocalId` on the generated query customizers), so a re-submission after a lost reply can be detected and promoted from a transient record to the stored one instead of creating a duplicate.
  - **Two-stage mobile upload with short-lived file permits + localId idempotent resend** (pattern, `S05-07`). A phone report upload is two stages: each file is uploaded on its own with (1) a call for a short-lived permit and (2) a call sending the bytes that returns a file reference; then one final call submits the ticket/report with all file references.
  - **Retry-safe status-transition semantics: same-reason resend = 204 no-op, different reason = real update with 422 lock codes** (domain, `S08-03`). For mobile-originated status changes (WONT_FIX upload), a resend carrying the same reason is a retry-safe 204 no-op performed before the guards (unchanged state).

### Offer pricing: cost vs price, markup, minimum floor, quantity reconciliation

- **Priority:** High · **Area:** domain · **Evidence:** 7 session(s)
- **Put it in:** model-blueprints/offer-cost-price-minimum (new); link price-margin-calculation-utilities
- **What to add:**
  - **Offer pricing model: cost vs price side, minimum floor and dummy visual offer item** (domain, `S11-05`). Offer pricing is split into a COST side (costPrice/price, allCostPrice) and a PRICE side (sellingPrice/unitPrice, minimumPrice per-line floor), plus offer-level profitAmount and overallMarkup derived from a MinimumOfferPrice threshold per currency.
  - **Offer minimum-price domain: dummy item covers only the included-service gap; materials/non-included stack on top; red vs yellow separation** (domain, `S09-04`). For an offer's minimum-price floor, the dummy offer item covers only the gap in the included-service portion; materials and non-included items are added on top of the minimum (they are never absorbed into it).
  - **OfferItem expected-quantity reconciliation against fault elements and quantity** (domain, `S11-04`). For offer items decomposed into fault elements, an expectedQuantity is recalculated on every save from the related faults: expectedQuantity = SUM(fault.quantity × multiplier) over the faults that require this service/item (multiplier fallback 1).

### Partner-scoped multi-role users and visibility matrix

- **Priority:** High · **Area:** domain · **Evidence:** 7 session(s)
- **Put it in:** model-blueprints/partner-scoped-multi-role-users (new)
- **What to add:**
  - **Domain role matrix for multi-role partner views (PRSES / EHS / External Safety Officer, access names, advisor relation)** (domain, `S16-06`). The rackinspect S1/S2 planning defines role-specific page/access sets: PRSES and EHS share a single partner access named 'prsesPartner' (with a PartnerView), External Safety Officer is a distinct role, and a user may have a two-way advisor relation when they are an external safety officer.
  - **Partner-scoped user creation and multi-role user invariants (partner vs inner roles, ESO advisor/partner rules)** (domain, `S18-05`). For an app with operator-side and service-side partner roles, user creation must be scoped and validated server-side by invariants: a partner-related role and an inner role cannot coexist on one user (e.g.
  - **Role-visibility and user-management rules across role families** (domain, `S26-05`). A multi-role partner app needs explicit role-visibility rules: SERVICE_ADMIN sees all users; IA and SLA see only their partner's users; PRSES/EHS-MANAGER reach users only through their own partner access (not a global users access);

### Typed media-attachment entity with polymorphic owners

- **Priority:** High · **Area:** domain · **Evidence:** 3 session(s)
- **Put it in:** model-blueprints/typed-media-attachment (new)
- **What to add:**
  - **Typed media-attachment entity: polymorphic owners, MediaType filtering, and photo-only flags** (pattern, `S23-05`). Model a binary media attachment as its own entity carrying a `FileType` binary field plus a `MediaType` enumeration (PHOTO/VIDEO/AUDIO), owned polymorphically by several entities (rack, job-sheet-item, element-fault, defect-ticket) via back-references so an attachment's owner can be found (e.g.
  - **Media attachments for an external/system client must go through the MediaAttachment API, not the PhotoServlet** (domain, `S03-10`). Media attachments (photos/videos/audio) of a defect ticket must be exposed to an external AI/pass client through the same MediaAttachment API surface the frontend uses, not through the PhotoServlet (a separate, HTTP-specific handler the AI cannot know about).

### Discard with retention and age-based cleanup

- **Priority:** Medium · **Area:** domain · **Evidence:** 2 session(s)
- **Put it in:** best-practices/model/soft-delete-active-flag.md (extend: retention + cleanup)
- **Catalog today:** soft-delete-active-flag exists; retention and cleanup are missing.
- **What to add:**
  - **Instant physical delete vs soft-delete/discard with retention and age-based cleanup (fault registry ticketing)** (domain, `S05-06`). For defect-ticket / preliminary-fault workflows the client chose instant physical delete over soft delete/discard/restore: a confirmation dialog covers accidental deletes, GDPR (voice recording) removal is valued, and no second 'discarded' list/permission surface is needed.

## 5. CLI knowledge (owned by the judo-model-cli skill)

### judo-model-cli usage the catalog must teach or link

- **Priority:** High · **Area:** cli · **Evidence:** 26 session(s); judo-ng: `judo-model-cli`, `judo-tatami-jsl`, `judo-esm-fullstack-project-template`, `judo-tatami-client` …
- **Put it in:** judo-model-cli skill docs (source of truth); catalog links + agent-docs/model/model-development.md
- **Catalog today:** The catalog still teaches the old GraphQL CLI syntax (see catalog-update-report.md §5).
- **What to add:**
  - **CLI GraphQL query language and schema inspection** (how-to, `P13-06`). `query <model> <Type>` builds GraphQL queries with --select/--where/--limit/--offset where where operators eq, contains, startsWith, endsWith, regex, icontains, istartsWith, iendsWith, iregex, gt, gte, lt, lte;
  - **CLI Mermaid diagram generation from models** (how-to, `P13-07`). `mermaid model` renders the in-memory ESM as a Mermaid classDiagram with --scope/--depth/--split/--kinds/--members/--md options, and `mermaid from <file|->` converts saved query/graphql JSON to a diagram without the daemon.
  - **CLI server session and unsaved-changes persistence** (how-to, `P13-08`). The CLI runs a persistent per-model daemon with sessions under ~/.judo/sessions/<hash>/ (session.json + daemon.log), a .<model>.dirty XMI overlay written every 500 ms, and .base/.intent sidecars.
  - **JUDO Model CLI command set and syntax** (how-to, `P13-01`). The judo-model-cli (judo-cli) offers a full command surface for editing and querying ESM models programmatically: create/update/delete/move/relocate/fill/split/merge, save, discard, status, validate, transform, query, graphql, mermaid, icons and server.
  - **JUDO Model CLI query/mutation syntax gotchas (where vs filter, -w dot-operator, containment+target, dirty-state)** (how-to, `S12-02`). The `judo_cli` GraphQL surface has non-obvious syntax: filtering uses `where` not `filter` (`transferobjecttypes(filter:{...})` returns "Unknown field argument 'filter'"), the `query` command uses `--where`/`-w` with dot-operator terms like `-w "name.contains=WorkReport"`, operation parameters are …
  - **Model-change workflow: manual ESM XML edits, EVL validation only on build, judo-cli discard reverts ALL in-memory changes** (how-to, `S03-05`). Model changes in JUDO are edited by hand in the ESM model XML (model/rackinspect.model); there is no declarative diff. EVL validation (including checking a MAPPED member's `required` against its binding) runs ONLY when the project is built — it is not a standalone step.
  - **Never hand-parse .model XMI files; query the model through judo-model-cli** (how-to, `S17-06`). The .model files are large XMI documents (20MB+); reading/grepping them by hand (python regex over the ASM/PSM XML) produces wrong or incomplete answers and is slow.
  - **judo-model-cli / ESM version pins, jar redeploy, and reading upstream docs at the pinned commit** (how-to, `S22-02`). The JUDO model CLI version is pinned by two root pom.xml properties (<judo-model-cli-version> and <judo-meta-esm-version>).
  - **judo_cli cannot create reference-derived UI elements or disambiguate duplicate FQNs** (how-to, `S11-02`). The JUDO model CLI (judo_cli) cannot create reference-derived UI elements: <Kind>CreateInput schema omits name while the runtime validator requires it, so DataColumn, DataField, OperationForm, DataFilter and RowOperation (which has no create type at all) cannot be created via the CLI — the workaround is to edit the XML/XMI directly and verify with judo_cli validate.
  - **judo_cli invocation pitfalls (non-interactive alias, stale jar, wrong model in skill)** (how-to, `S01-08`). The `judo_cli` alias does not resolve in non-interactive shells, the bundled jar can be outdated (the subagent had to replace it), and a skill's SKILL.md can reference another project's model file.
  - **judo_cli location, invocation and stale --version reporting** (how-to, `S11-03`). judo_cli is not a real binary on PATH; it is a ~98 MB jar at target/judo-cli.jar built by ./judo.sh build (Maven coordinate hu.blackbelt.judo.runtime:judo-model-cli:${judo-model-cli-version}), invoked as "java -jar target/judo-cli.jar -m model/rackinspect.model <command>".
  - **judo-cli UI mutation gotchas: TabularReferenceFieldCreateInput has no name field** (how-to, `S13-05`). When adding UI elements via the judo CLI, a `TabularReferenceFieldCreateInput` has no `name` field — the name is derived from `relationFeature`, and the reported error message ('No name field') is misleading; the real cause is an ambiguous FQN.
  - **Derived-model generation and reload via CLI transform/discard** (how-to, `P13-03`). `transform` runs the ESM->PSM->ASM->RDBMS pipeline (plus esm2ui) writing derived models to cli-generated/ (or -o <dir>) and, with --load, reloads them into the running daemon.
  - **Adding a UI field/form member via judo-model-cli mutation** (how-to, `S10-01`). To expose a new model attribute on an existing view/form, you edit the UI element tree (add a DataField under a Group/TransferObjectView container) through the judo-model-cli mutation layer - there is no `ui-mutations.md` doc. The CLI's mutation command (e.g. `judo-cli -m <model>.model update ...
  - **Reference-derived UI elements have no writable name on CreateInput** (how-to, `S11-01`). UI elements DataField, DataColumn, ReferenceField, every <Feature>Filter (e.g. DataFilter), OperationForm, and Inherited* references are reference-derived: their name and fqn are computed by the metamodel from the binding (dataFeature.member.name, dataFeature.member.name + "Filter", operation.name).
  - **Renaming a JUDO model attribute via judo-cli preserves xmiId and yields an incremental renameColumn (not delete+create)** (how-to, `S25-01`). To rename a model data member you mutate it in-memory with the judo-model-cli GraphQL `update -f 'fqn' { input: { dataMember: {name: ...} } }` mutation, then discard any spike with `discard --force` before committing.
  - **Model CLI cannot add a column to a card table (switch to table, edit, switch back)** (how-to, `S22-03`). The judo model CLI refuses to add a column to a `card` table/relation and its error does not say why. The working workaround is to temporarily switch the table representation to `table`, add the column via the CLI, then switch it back to `card`;
  - **Three-way ESM model merge and conflict resolution** (topic, `P13-02`). The `merge <theirs> --base <base>` command performs a three-way merge of a parallel model copy into the loaded (mine) ESM, matched by xmi:id, as one unsaved editing step.
  - **Tatami Maven workflow plugin configuration (default-model-workflow goal and parameters)** (how-to, `P22-04`). Code generation is driven by the `judo-tatami-jsl-workflow-maven-plugin` (groupId `hu.blackbelt.judo.tatami`) with goal `default-model-workflow`, bound to `generate-sources` (or COMPILE via `default-model-workflow` Mojo) and run in parallel by default with per-step `ignore*` toggles.
  - **Eclipse m2e launcher configurations and IDE run workflow** (topic, `P28-07`). The template ships Eclipse m2e launch configurations: BuildApplication.launch (clean install of <project>/application with JudoBuildApplicationLauncher), BuildApplicationWithoutFrontend.launch (adds -DskipDocker=true -DskipFrontend=true), CompileCustomApp.launch (clean install of application/app), …
  - **JSL editor / IDE tooling (VS Code extension and TextMate bundle)** (how-to, `P34-03`). JUDO models are authored in JSL (.jsl files).
  - **Model validation gate (validateModels and ESM/UI validation rules)** (how-to, `P23-04`). Workflow validation is controlled by the `validateModels` parameter (default false). ESM validation runs before the ESM2UI step and, when enabled, stops transformation on CRITICAL/HIGH errors;

## 6. Excluded candidates

These were mined but rejected in validation. **Covered** items are findability problems, not missing knowledge: the catalog has them and search should find them.

### Already covered (findability, not missing)

| Gap | Title | Covered by |
|---|---|---|
| `P33-06` | useNavigationConfirmation generated hook | `frontend/hooks/navigation-and-access.md (Unsaved Changes Warning)` |
| `P12-09` | Time/Timestamp attribute default expressions (time!now(), timestamp!now()) | `best-practices/model/default-value-patterns.md (!now())` |
| `S01-03` | JUDO update() full-row overwrite wipes omitted fields | `best-practices/backend/mutable-entity-update-pattern.md (mask for partial update)` |
| `S26-02` | Reading principal/actor inside interceptors via dispatcher exchange keys | `agent-docs/backend/patterns-and-best-practices.md (Accessing the logged-in user)` |
| `S05-04` | Backend error code -> i18n key mapping with English fallback; every business error needs H | `best-practices/frontend/error-code-mapping-pattern.md` |
| `S13-07` | Business error TO: both message and location should be i18n-localized | `agent-docs/frontend/i18n.md + error-code-mapping-pattern.md` |
| `P24-06` | Generated input widget mapping (boolean -> TrinaryLogicCombo, never Checkbox; RadioWidget  | `agent-docs/frontend/esm-to-ui-mappings/widgets.md` |
| `P31-05` | Generated table state persistence keys and uniqueId uniqueness | `best-practices/frontend/session-storage-table-state.md` |
| `P14-01` | Custom business logic as `java.util.function.Function` OSGi services (simple dispatcher) | `best-practices/backend/custom-operation-osgi-component.md` |
| `P16-06` | DispatcherFunctionProvider SPI for registering SDK and script operation implementations | `best-practices/backend/custom-operation-osgi-component.md` |
| `P01-05` | Custom Sequence SPI | `best-practices/backend/sequence-code-generation.md` |
| `P14-06` | Automatic boot-time initializer operations (initializer-annotated EOperations run on model | `model-blueprints/initializer-entity-with-init-operation` |
| `P05-07` | JQL ternary conditional operator and switch-expression typing | `best-practices/model/conditional-visibility-getter.md (ternary in use)` |
| `P21-03` | Health-check HTTP endpoint usage and configuration (/system/health) | `agent-docs/deployment/README.md (/system/health URL)` |
| `S02-01` | Frontend build recovery: delete source dirs and rerun ./judo.sh build -i | `agent-docs/deployment/build-process.md (judo.sh build)` |
| `S09-05` | Make a mapped transfer member read-only via DERIVED attribute with getterExpression instea | `agent-docs/model/model-development.md (derived getter)` |

### Not needed by application developers

Platform-maintainer internals (generator plumbing, transformation engines, EMF/ESM Java APIs, Maven plugin parameters) and one project's own business data or infrastructure (seed rules, GCP VMs, AI-sidecar credentials).

`P02-01`, `P02-02`, `P03-01`, `P03-02`, `P03-03`, `P03-04`, `P03-05`, `P04-01`, `P04-02`, `P04-03`, `P04-04`, `P04-05`, `P04-06`, `P07-01`, `P07-03`, `P10-01`, `P10-03`, `P10-04`, `P10-05`, `P10-06`, `P10-07`, `P10-08`, `P11-04`, `P11-05`, `P11-09`, `P11-10`, `P13-04`, `P13-05`, `P14-02`, `P14-07`, `P14-08`, `P15-03`, `P15-04`, `P17-08`, `P18-01`, `P18-04`, `P19-02`, `P19-06`, `P19-07`, `P20-01`, `P20-02`, `P20-03`, `P20-06`, `P20-07`, `P20-08`, `P20-09`, `P21-01`, `P21-02`, `P21-04`, `P23-01`, `P23-02`, `P23-03`, `P24-05`, `P26-01`, `P26-02`, `P26-03`, `P26-05`, `P26-06`, `P27-05`, `P32-01`, `P32-03`, `P32-06`, `P34-05`, `S06-06`, `S06-08`, `S10-02`, `S11-08`, `S13-06`, `S13-08`, `S15-01`, `S15-02`, `S15-03`, `S16-04`, `S20-03`, `S21-01`, `S21-02`, `S24-02`, `S24-03`, `S26-07`

### Not verifiable

- `P24-01` Link columns/actions on a row table are never generated: cited path is truncated/unresolvable; claim not verifiable
