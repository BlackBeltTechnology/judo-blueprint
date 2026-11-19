# platform-behavior-reference.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/platform-behavior-reference.md.

## Overview
- Runtime behaviour not visible in generated code (verified against `judo-runtime-core`): signed ids, optimistic locking, reserved keys, REST wire, time zones, variables, sequences, custom REST/CXF, config, Keycloak, initializers, scheduling, email.

## Signed Identifiers
- Responses carry `__identifier` and `__signedIdentifier`. Bound ops and instance updates send signed id in header `X-Judo-SignedIdentifier`.
- Signature covers id, type, `__version`, immutable flag (`DefaultIdentifierSigner`). Signed id changes after every update; stored ones go stale.
- Key: configured HMAC `secret`, else generated at start. Generated key → all signed ids invalid after restart; cluster nodes cannot validate each other. Set stable secret in production.
- Code cannot mint signed ids; only responses are signed. Get them from API responses.
- `immutable`: not an ESM attribute. ESM→PSM sets it `true` on `_getRangeReference<Relation>` ops and the get-template op; PSM→ASM writes `immutable` annotation. Exposed ops on immutable instances → `AccessDeniedException` (`BOUND_OPERATION_INSTANCE_IS_IMMUTABLE`).
- Bound op instance must come from a TO exposed to the caller, else `ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION` (403).
- Ids from `IdentifierProvider` SPI (`get()`, `getType()`, `getName()`). Default `UUIDIdentifierProvider`: random UUID, payload key `__identifier`. Guice binds it unless module config supplies another.

## Optimistic Locking and `__version`
- On by default in RDBMS (`rdbmsDaoOptimisticLockEnabled = true`). Insert sets version 1; each write increments.
- Check in `UpdatePayloadDaoProcessor` ONLY when payload has `__version`; mismatch → `IllegalArgumentException("Outdated instance to update")`. Over REST: HTTP 500, `code: INTERNAL_SERVER_ERROR` (not a BusinessException). Omitting `__version` silently disables the guard.
- SQL: `VERSION` predicate only on meta UPDATE (`WHERE ID = :id AND VERSION = :__version`). Stale → no rows → "There is illegal state, no records updated".
- Clients echo `__version`; custom update ops rebuilding payloads must carry current version.

## Reserved Payload Keys
- Do not use for model features: `__identifier` (plain id), `__signedIdentifier`, `__version`, `__entityType` (`Dispatcher.ENTITY_TYPE_MAP_KEY`), `__referenceId` (correlates validation results), `__selected` (range/selection marker), `__deleteable`/`__updateable`/`__immutable` (metadata added on signing), `__principal`/`__actor`/`__this` (`Dispatcher.PRINCIPAL_KEY`, `ACTOR_KEY`, `INSTANCE_KEY_OF_BOUND_OPERATION`).

## REST Wire Contract
- Root `/api/<Model>/...`. Each op `@JudoOperation(fqn)` → `Dispatcher.callOperation(fqn, params)`; params always include `__exposed=TRUE` plus header-derived `__countRecords`, `__mask`, `__locale`, `__requestParameters`, `__principal`.
- Verb suffixes: `~create`, `~list`, `~get`, `~update`, `~delete`, `~set`, `~unset`, `~add`, `~remove`, `~range`, `~template`, `~validate`, `~export`, `~meta`, `~principal`, `~upload-token`. `~update` is partial (absent fields unchanged).
- List: `_orderBy`, `_seek` keyset (`lastItem` with signed id + sort key, `limit`, `offset`, `reverse`), per-attribute filter operators. Unparseable mask → `INVALID_QUERY_MASK`.
- Wire: enums as ordinals; binaries as file-store tokens; dates ISO strings.
- Status: no bound dispatcher → 503; malformed params → 400; op without output → 204; export streams file with `Content-Disposition`.
- `java.util.Date` params: `yyyy-MM-dd` by default (`ISO8601DateParamHandler`); else `IllegalArgumentException("Invalid date parameter")`. OSGi bundle reads key `ISO8601DateParamHandler.DATE_FORMAT`; Guice/CXF server does not.
- Error shapes: error-handling-guide.md.
- Class names: `<Name>Response`, `<Name>Request`, `<Name>CreateRequest`, `<Name>RangeRequest` (no `For`).
- Response DTOs of mapped TOs carry `__deleteable`, `__updateable`, `__entityType`, `__identifier`, `__signedIdentifier`, `__version`, `__referenceId`. Request DTOs: only `__identifier`, `__signedIdentifier`, `__referenceId`. Use `__updateable`/`__deleteable` for row actions.
- Unknown request keys are dropped.
- Access through a non-updatable path rejects updates (signed id records navigation). Identifiers are type-specific.

### Binary Upload Tokens
- Create-capable transfer with binary field → `getUploadTokenFor<Field>` returns `UploadToken` (`token`). Two-phase: get token → upload to file store → send token as attribute in `~create`/`~update`. Invalid → `INVALID_FILE_TOKEN`.

### FileStore Java API
- OSGi `hu.blackbelt.osgi.filestore.api.FileStoreService`: `String put(InputStream, fileName, mimeType)` → id; `get(id)`, `exists(id)`, `getMimeType`, `getFileName`, `getSize`, `getCreateTime`, `getAccessUrl`, `getProtocol`.
- Binary value type `hu.blackbelt.judo.dispatcher.api.FileType` (Lombok builder): `id`, `fileName`, `size` (Long), `mimeType`. Persisted as JSON `{"id","fileName","size","mimeType"}`. To attach: `put`, then build `FileType` from returned id/name/size/mime.
- Backend via `JUDO_PLATFORM_FILESTORE`: `filesystem` (dir `filestoreDirectory`, default `$HOME/file-store`), `rdbms` (table `FILESTORE`), `s3`. Any other value (typo too) disables file store and upload/download endpoints.
- `JUDO_PLATFORM_FILESTORE_TOKEN_EXPIRY`: upload token lifetime in minutes (`0` = no expiry).

### Range and Choice Operations
- `getRangeFor<Name>` ops take synthesized `_GetRangeInput...` (`owner` relation; `queryCustomizer` for mapped refs). Out-of-range → `NOT_ACCEPTED_BY_RANGE`.

### Protocol Headers
- `X-Judo-CountRecords` → `__countRecords` (response `X-Judo-Count`).
- `X-Judo-Mask` → `__mask` (projection).
- `X-Judo-RequestParameters` → `__requestParameters` (map; malformed → 400).
- `X-Judo-SignedIdentifier` → bound instance (bound op / instance command).
- `X-Judo-MarkSelectedRangeItems` → range ops (marks already attached items).
- `__principal` from security context; `__locale` from first `Accept-Language`.
- CORS filter allows `X-Judo-SignedIdentifier`, `X-Judo-CountRecords`; exposes `X-Judo-Count`, `X-Exchange-Id`, `X-Fault`. See deployment/osgi-runtime-services.md#cors-filter-per-model.

### Response Metadata and Wire Conversion
- Enum ordinal not a member → response conversion throws `Invalid enumeration value '<n>' of type <FQN>`; request throws for unknown literal; filter with unknown ordinal → `Invalid enumeration member`.
- JQL: same-enum comparisons `==`, `!=`, `<`, `>`, `<=`, `>=`; different enums rejected (`Operands are not of the same enumeration`).
- SDK enum: `getOrdinal()`, `getName()`, static `getByOrdinal(Integer)` (throws `Invalid ordinal: <n>` for null/unknown).
- Query customizer filter operator codes: strings `0 <`, `1 >`, `2 <=`, `3 >=`, `4 ==`, `5 !=`, `6 ~` (matches), `7 like`; numbers/dates/times `0`–`5`; booleans only `0` (equal); enums `0` (equal), `1` (not equal).

### Client Side of the Upload Token Flow
- Axios `accessServiceImpl.ts`: token in header `X-Token`. `uploadFile` requests `<attributePath>/~upload-token` then posts multipart with `X-Token`.
- `downloadFile`: `?disposition=inline|attachment` + `X-Token`. Inline renders in dialog frame in generated frontend; replaced handlers may open new tab, so check generated caller.
- Wire: `GET /download?id=<fileId>` with `X-Token`; param is `id`, not `fileId`. Uploaded file JSON keys: `id`, `token` (plus `field`, `name`, `url`, `ctype`, `size`); not `fileId`/`downloadToken`.
- File-store servlets: `*` CORS origin answered with literal `*`, never with `Access-Control-Allow-Credentials`.

### Excel Export Operations
- Modeled `EXPORT` ops call `Export` SPI. Reference `JxlsExport` (JXLS/POI): row 0 headers, row 1 placeholders, data from row 2.
- Cell formats: timestamp `dd/mm/yyyy hh:mm:ss`, date `dd/mm/yyyy`, time `hh:mm:ss`, decimal `#,##0.00`, integer `0`.
- Only overloads taking ASM model + FQN work. `Class`-based `exportToInputStream` throws `UnsupportedOperationException`.
- Default binding `UnsupportedExportImpl` (Guice and Spring): all methods throw `Not implemented`. Karaf: `DefaultJxlsExportComponent` registers `JxlsExport`. Guice: pass as `export` in module configuration.

### Payload Type
- `Payload` (`judo-dao-api`) = `Map<String,Object>`; factories `asPayload`, `map(k1,v1,...)`, `entry`; accessors `getAs(Class,key)`, `getAsPayload`, `getAsCollectionPayload`.
- `PayloadImpl` uses `TreeMap`; constructor wraps nested maps/collections as `Payload`, but `put`/`putAll` do not.
- Keys starting `__$` are transient: `equals()` ignores them, `hashCode()` includes them (equal payloads may differ in hash).

## Time and Time Zones
- Two clocks disagree:
  - `Timestamp!now()` / `current_timestamp` in model expressions → platform `defaultZoneId` (`JUDO_PLATFORM_DEFAULT_ZONE_ID`; template default `UTC`), not JVM zone.
  - `LocalDateTime.now()` in custom Java → JVM `TZ` / `user.timezone`.
  - Persistence converts to UTC; JSON serializes ISO offset/UTC.
- Mixing clocks for write vs compare gives fixed offset that breaks age/duration limits. Use one clock for both.
- UI timestamps format in browser zone (`Intl.DateTimeFormat` without `timeZone`). Model-built strings use `defaultZoneId` → mismatch (e.g. 18:00 vs 20:00). Model cannot read browser zone: show the timestamp itself, avoid derived formatted strings.

## Variables and Sequences

### Variable Providers
- JQL `!getVariable('CATEGORY', 'key')`; Java `VariableResolver.resolve(Integer.class, "SYSTEM", "random")`.
- Categories: `SYSTEM`, `ENVIRONMENT`, `REQUEST`, `ACTOR`, `PRINCIPAL`, `SEQUENCE` (plus `USER`). `SYSTEM`: `current_date`, `current_time`, `current_timestamp`.
- Custom provider: OSGi component with `judo.environment-variable-provider=true` and `category` property. With key → `Supplier`; without key → `Function`. Request-context providers set `cacheable=false`.

### Custom Sequences
- Default: DB sequences. Custom: implement `hu.blackbelt.judo.dispatcher.api.Sequence` (`getNextValue(String)`, `getCurrentValue(String)`), OSGi component with property `Sequence.TYPE_KEY` (`type`).
- Platform parameter `sequenceType`: `rdbms` (default) or custom/`transient`. Transient not supported on multi-node.
- Gaps possible: rolled-back values not reused.

## Custom REST Endpoints and CXF
- Custom endpoint: OSGi DS component with `@Path`, discriminator property, bound into `BasicApplication` (`cxf-jaxrs-application-manager`) via `jaxrs.resource.components` LDAP filter (singletons) or `jaxrs.resource.classes` comma list (`Class.forName`; failures logged and skipped).
- `@Provider` JAX-RS providers picked up only with bundle manifest `X-JAXRS-Provider: true`. No `applications.filter` → applies to all apps.
- CXF interceptors: OSGi components implementing `org.apache.cxf.interceptor.Interceptor`, properties `judo.model.name`, `interceptor.direction` (`in`/`out`/`fault`).
- Shared Jackson `ObjectMapper`: OSGi filter `(&(source=judo-services-jackson-objectmapper)(type=extended))`. `JacksonProvider` keys `JacksonProvider.SerializationFeature.<NAME>` / `DeserializationFeature.<NAME>`.
- Each bus = `CxfContext` component (`configurationPolicy=REQUIRE`, required `busId`). Optional keys: `interceptors.in|out|fault.components` (OSGi filters), `metrics.enabled` (false), `logging.enabled` (false), `wadl.service.description.available` (true), `skip.default.json.provider.registration` (true).
- Default bus `DEFAULT_CXF_BUS_FOR_JAXRS_APPLICATIONS` from application manager; `BasicApplication` may reference another `CxfContext`.
- Request correlation: `X-Exchange-Id` (debugging-and-monitoring-guide.md).

## Configuration Mapper for Custom Parameters
- Configset: `templatePath` (classpath folder of `*.template` FreeMarker), `envPrefix` (e.g. `MY_APP_`), `variableScopePreference` (`osgi,environment,system`).
- Template file name = PID (`ApplicationConfiguration.template` → `ApplicationConfiguration`). `MY_APP_PROP_NAME` referenced as `propName`.
- Read: `ConfigurationAdmin.getConfiguration("ApplicationConfiguration")`.

## Tuning System Properties
- Read at class load: `EsmModelCacheExpiration` (s, default 5), `AsmUtilsCacheExpiration` (60), `FqnCacheExpiration` (300, idle-based), `JqlExpressionBuilderModelAdapterCacheExpiration` (86400). `templateDebug` enables generator template debugging.

## Keycloak Users and the Entity Store
- Managed actors: `UserManager` / `UserManagedWrappedDao` bridge Keycloak and DB; stores can drift (admin in Keycloak, entity row missing).
- Invitation/init flows must verify and create the DB row; do not assume Keycloak membership implies entity.
- Invitation e-mails sent by Keycloak. On every Karaf start the connector rewrites default realm SMTP from `JUDO_PLATFORM_MAIL_SMTP_*`.
- Local testing: mailpit (SMTP 1025, web 8025), point `JUDO_PLATFORM_MAIL_SMTP_*` at it.

## Initializer Operations
- `initializer = true` is an ESM `Operation` flag (not `OperationType.INITIALIZER`). Platform runs it; nobody calls it.
- Shape: `STATIC`, no input (validation `InitializerOperationIsValid`).
- When: OSGi runtime `InitScriptExecutor` runs all initializers synchronously on model component activation, after SDK ops and identity manager. Runs on EVERY start, not per deploy → idempotent (check before create).
- Identity: `dispatcher.callOperation(name, exchange)` with empty exchange: no principal, no `ACTOR`. No actor-based access inside.
- Transaction: script/custom op wrapped in `TransactionalOperationCall`; each initializer own transaction.
- Failure: logged (`Initializer script <fqn> failed`); next still runs; `InitScriptsCompleted` registered only if all succeeded.
- Spring Boot: no caller of the flag found (verify).
- Generated `<Entity>Initializer.initBuilder()` belongs to TO initializer (`OperationType.INITIALIZER`), not this flag.

## Transaction Rollback
- A call that joins an existing transaction is not rolled back; rollback happens only when the call started a new transaction (`isNewTransaction()`).
- Read-type calls (refresh, list, input validation) roll back the transaction they start; a write in their interceptors (e.g. postCall of `_refresh`) is discarded. Write in update or custom operations.

## Scheduled Work
- No platform scheduler. `judo-services-job` only runs initializers at startup; no Quartz/scheduling component. Periodic work = app code (e.g. OSGi component with own executor).
- Scheduler thread: no principal, no `ACTOR`.
- Use `Dispatcher.callOperation` for a modeled op (gets transaction/operation handling) instead of DAO. Script/custom ops run in own transaction.
- Don't rely on `ACTOR` access or variables unless you put an actor in the exchange.

## Email Service
- Inject `hu.blackbelt.email.api.EmailService`; `sendMessage(EmailMessage.emailBuilder()....build())`.
- Fields: `from`, `tos`, `ccs`, `bccs` (sets), `replyTo`, `subject`, `plaintTemplate`, `htmlTemplate`, `model`.
- Attachments: `fileAttachments` / `inputStreamAttachments` (name → `File` / `BinaryAttachment`); inline: `fileInlinedContents` / `inputStreamInlinedContents` (content id → …). `BinaryAttachment.binaryAttachmentBuilder()`: `inputStream` or `bytes`, `mimeType`.
- Templates: `plaintTemplate`, `htmlTemplate` = Handlebars strings applied to `model`. `subject` is NOT a template. At least one template non-blank, else `No HTML or Plain message defined`. Both → multipart.
- Invalid address → `IllegalArgumentException("Email is not valid: ...")`.
- Synchronous; uses `JUDO_PLATFORM_MAIL_SMTP_*` → `mail.smtp.*` on `JavaMailSenderActivator`. `JUDO_PLATFORM_LOG_SMTP_SERVER=true` → local log SMTP server only logs.

## See Also
- error-handling-guide.md, interceptors.md, data-access-guide.md, authentication-guide.md
