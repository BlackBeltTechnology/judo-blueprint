---
title: Backend Platform Behavior Reference
description: Signed identifiers, optimistic locking, reserved payload keys, REST wire contract, time zones, variables and sequences.
aliases: [optimistic locking, signed id, reserved payload keys, time zone handling, sequence generator, variable provider, upload token]
keywords: [__version, Keycloak, CXF, sequence, variable provider, upload token]
tags: [domain:backend, layer:backend, status:platform]
---

# Backend Platform Behavior Reference

## Overview

Platform behaviours that surprise backend developers and are not visible in the generated code: signed identifiers, optimistic locking, reserved payload keys, the REST wire contract, time zones, variable providers, sequences, custom REST resources and tuning properties. Each section states what the runtime really does (verified against `judo-runtime-core` and related modules).

## Signed Identifiers

- Every instance the REST layer returns carries `__identifier` and a `__signedIdentifier`. Bound operations and instance updates take the signed identifier (request header `X-Judo-SignedIdentifier`), not the plain id.
- The signature covers the id, the entity type, the entity **`__version`** and an **immutable** flag (`DefaultIdentifierSigner`). Because the version is part of the token, **the signed identifier changes after every update** of the entity. A signed identifier you stored earlier can therefore differ from the current one.
- Signing uses a key: a configured HMAC `secret` or, if none is configured, a key generated at start. With a generated key all previously issued signed identifiers become invalid after a restart, and nodes of a cluster cannot validate each other's tokens. Configure a stable secret in production.
- Server or client code **cannot mint** a signed identifier; the runtime signs identifiers only while serving a response. Code that needs the signed id of an instance must obtain it from a response of the API.
- `immutable`: instances produced from an `immutable` copy carry the flag inside the signed identifier. The dispatcher refuses exposed operations on such instances with `AccessDeniedException` (`BOUND_OPERATION_INSTANCE_IS_IMMUTABLE`).
- `immutable` is not an attribute of entities or transfer objects in the ESM and cannot be set in the model. It is a flag of the generated transfer operations: the ESM→PSM transformation sets it to `true` on the `_getRangeReference<Relation>` operations (relation and input-parameter ranges) and on the get-template operation, and PSM→ASM writes it as an `immutable` annotation. Instances returned by those operations are signed as immutable.
- Instance ids come from the `IdentifierProvider` SPI (`get()`, `getType()`, `getName()`). The default `UUIDIdentifierProvider` returns random `UUID`s of type `UUID` and names the payload key `__identifier`. The Guice module binds it unless the module configuration supplies another `IdentifierProvider`.
- A signed instance of a bound operation must come from a transfer object exposed to the calling actor, else `ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION` (403).

## Optimistic Locking and `__version`

- Optimistic locking is **on by default** in the RDBMS runtime (`rdbmsDaoOptimisticLockEnabled = true`). Inserts set the version to 1; each write increments it.
- The check happens in `UpdatePayloadDaoProcessor` and **only when the update payload contains `__version`**: it must equal the stored version, otherwise `IllegalArgumentException("Outdated instance to update")`. If `__version` is absent, no check is performed, so omitting it silently disables the guard.
- At SQL level the `VERSION` predicate is added only to the meta `UPDATE` (`WHERE ID = :id AND VERSION = :__version`), not to the attribute `UPDATE`. A stale version makes the statement update no rows, and the executor fails with "There is illegal state, no records updated".
- Clients must echo `__version` back and handle the stale-update error. Custom update operations that rebuild payloads must carry the current version.

## Reserved Payload Keys

Do not use these names for model features. DAO payload processors and the dispatcher reserve them:

| Key | Meaning |
| :--- | :--- |
| `__identifier` | Plain instance id. |
| `__signedIdentifier` | Signed id, see above. |
| `__version` | Optimistic-lock version. |
| `__entityType` | Entity type marker (`Dispatcher.ENTITY_TYPE_MAP_KEY`). |
| `__referenceId` | Client reference id used to correlate validation results. |
| `__selected` | Selected-item marker in the range/selection path. |
| `__deleteable`, `__updateable`, `__immutable` | Instance metadata flags added when signing. |
| `__principal`, `__actor`, `__this` | Exchange keys with the caller and the bound instance (`Dispatcher.PRINCIPAL_KEY`, `ACTOR_KEY`, `INSTANCE_KEY_OF_BOUND_OPERATION`). |

## REST Wire Contract

- Generated JAX-RS services are rooted at `/api/<Model>/...`. Each operation is annotated `@JudoOperation(operationAsmFqName)` and forwards to `Dispatcher.callOperation(fqName, parameters)`; the parameters always include `__exposed=TRUE` plus values derived from headers (`__countRecords`, `__mask`, `__locale`, `__requestParameters`, `__principal`).
- Resource verbs are suffixes such as `~create`, `~list`, `~get`, `~update`, `~delete`, `~set`, `~unset`, `~add`, `~remove`, `~range`, `~template`, `~validate`, `~export`, `~meta`, `~principal` and `~upload-token`. `~update` is a partial update: fields absent from the body stay unchanged.
- List queries combine `_orderBy`, a `_seek` keyset cursor (`lastItem` with the signed identifier and sort key, `limit`, `offset`, `reverse`) and per-attribute filter operators. A query mask that cannot be parsed fails with `INVALID_QUERY_MASK`.
- Wire conversions: enumerations travel as ordinals, binaries as file-store tokens (see below), dates as ISO strings.
- JSON response payloads are written with the platform default charset, not UTF-8: `PayloadMessageBodyWriter` wraps the entity stream in an `OutputStreamWriter` without a charset.
- Behaviours: no bound dispatcher gives 503, malformed request parameters give 400, an operation without output gives 204, export operations stream a file with `Content-Disposition`.
- `java.util.Date` query/path parameters are parsed as `yyyy-MM-dd` by default (`ISO8601DateParamHandler`); anything else fails with `IllegalArgumentException("Invalid date parameter")`. The OSGi bundle reads the key `ISO8601DateParamHandler.DATE_FORMAT` to change the format; the Guice/CXF server does not read it.
- Error shapes are described in the [Error Handling Guide](error-handling-guide.md).

### Binary Upload Tokens

A transfer field that maps a binary on a create-capable transfer gets a generated `getUploadTokenFor<Field>` operation. It returns an `UploadToken` object with one required `token` string. Upload is two-phase: request the token, upload the content to the file store with it, then send the token as the attribute value in `~create`/`~update`. Invalid tokens fail with `INVALID_FILE_TOKEN`.

### FileStore Java API

Custom Java code reads and writes binary content through the OSGi service `hu.blackbelt.osgi.filestore.api.FileStoreService`:

- `String put(InputStream data, String fileName, String mimeType)` stores the content and returns the file id.
- `InputStream get(String fileId)`, `boolean exists(String fileId)`.
- `getMimeType(fileId)`, `getFileName(fileId)`, `long getSize(fileId)`, `Date getCreateTime(fileId)`, `URL getAccessUrl(fileId)`, `getProtocol()`.

A binary attribute value in generated Java is `hu.blackbelt.judo.dispatcher.api.FileType` (Lombok `@Builder`, getters): `id`, `fileName`, `size` (`Long`), `mimeType`. It is persisted as a JSON string `{"id":..,"fileName":..,"size":..,"mimeType":..}`. To attach a file from Java, `put` the content and set a `FileType` built with the returned id, name, size and MIME type.

File names longer than 128 characters are cut to their first 127 characters by `FilenameUtils.makeValidFilename`, which the filesystem, RDBMS and S3 backends call on the name they store.

A `null` file name stores the file as `<fileId>.<mimeType>` (for example `uuid.image/png`). The stored `size` comes from `InputStream.available()`, which is not guaranteed to equal the content length.

The backend is chosen with `JUDO_PLATFORM_FILESTORE`: `filesystem` (directory `filestoreDirectory`, default `$HOME/file-store`), `rdbms` (table `FILESTORE`) or `s3`. Any other value, including a typo, disables the file store and the upload/download endpoints. `JUDO_PLATFORM_FILESTORE_TOKEN_EXPIRY` sets the upload token lifetime in minutes (`0` = no expiry).

### Actor Access List Operations

Each actor access declaration gets a `LIST` behaviour and an unbound `listOf<Access>` operation when `generateBehaviours` is set. The generated list has no list-permission check of its own.

### Range and Choice Operations

Choice and range lookups are generated as `getRangeFor<Name>` operations whose input is a synthesized `_GetRangeInput...` transfer object (an `owner` relation and, for mapped references, a `queryCustomizer`). Values outside the allowed range fail with `NOT_ACCEPTED_BY_RANGE`.

### Protocol Headers

Generated REST operations read these request headers (`rest.service.operation.fragment.hbs`; the React client declares them in `headers.ts`):

| Header | Maps to | Use |
| :--- | :--- | :--- |
| `X-Judo-CountRecords` | `__countRecords` | Ask for a total count of a collection. The response carries `X-Judo-Count`. |
| `X-Judo-Mask` | `__mask` | Projection of the response. |
| `X-Judo-RequestParameters` | `__requestParameters` | Query parameters as a map; a malformed value gives HTTP 400. |
| `X-Judo-SignedIdentifier` | bound instance | Target of a bound operation or an instance command. |
| `X-Judo-MarkSelectedRangeItems` | range operations | Marks the items that are already attached. |

`__principal` comes from the security context and `__locale` from the first `Accept-Language` value. The generated CORS filter allows `X-Judo-SignedIdentifier` and `X-Judo-CountRecords` by default and exposes `X-Judo-Count`, `X-Exchange-Id` and `X-Fault`; see [OSGi Runtime Services](../deployment/osgi-runtime-services.md#cors-filter-per-model).

### Response Metadata and Wire Conversion

- Response DTOs of mapped transfer objects carry `__deleteable`, `__updateable`, `__entityType`, `__identifier`, `__signedIdentifier`, `__version` and `__referenceId`. Request DTOs carry only `__identifier`, `__signedIdentifier` and `__referenceId`. Use `__updateable` and `__deleteable` to enable or disable row actions. The generated JAX-RS DTO classes are named `<Name>Response`, `<Name>Request`, `<Name>CreateRequest` and `<Name>RangeRequest` (no `For` infix).
- Enum attributes travel as integer ordinals; `ResponseConverter` turns the ordinal back into a literal. Binary attributes travel as file-store tokens, and the token's context must name an attribute of the same binary type. Unknown keys in a request are dropped.
- Query customizer filter operators are numeric codes: strings `0 <`, `1 >`, `2 <=`, `3 >=`, `4 ==`, `5 !=`, `6 ~` (matches), `7 like`; numbers, dates and times use `0`-`5`; booleans only `0` (equal); enumerations `0` (equal) and `1` (not equal).
- An access reached through a path that is not updatable rejects updates, because the signed identifier records the navigation that produced the instance. Identifiers are type specific: an identifier of one transfer object type cannot be used for another type.
- Enumeration values are stored and sent as the member ordinal. An ordinal that is not a member of the enumeration is rejected: the response conversion throws `IllegalArgumentException` ("Invalid enumeration value '<n>' of type <FQN>"), the request conversion throws it for an unknown literal, and a query-customizer filter with an unknown ordinal throws "Invalid enumeration member".
- JQL compares two values of the same enumeration with `==`, `!=`, `<`, `>`, `<=` and `>=`; comparing different enumerations is rejected ("Operands are not of the same enumeration").
- The generated SDK enum has `getOrdinal()`, `getName()` and a static `getByOrdinal(Integer)`; `getByOrdinal` throws `IllegalArgumentException` ("Invalid ordinal: <n>") for null or an unknown ordinal.

### Client Side of the Upload Token Flow

The generated axios service (`accessServiceImpl.ts`) sends the token in the `X-Token` header. `uploadFile` first requests `<attributePath>/~upload-token`, then posts the multipart data with `X-Token`. `downloadFile` calls the download path with `?disposition=inline|attachment` and `X-Token`; an inline download renders in a dialog frame in the generated frontend. Projects that replace the handler may open a new tab instead, so check the generated `downloadFile` caller in your version before relying on either.

On the wire, the download request is `GET /download?id=<fileId>` with the `X-Token` header; the file id parameter is `id`, not `fileId`. Each uploaded file's JSON entry has the keys `id` and `token` (plus `field`, `name`, `url`, `ctype`, `size`), not `fileId` or `downloadToken`. In the file-store servlets, a `*` CORS origin is answered with a literal `*` and never with `Access-Control-Allow-Credentials`.

### File-Store Servlet Checks

- The file-store `maxSize` settings are in kB, but `UploadServlet.checkRequest` compares the raw `Content-Length` (bytes) with the limit, so a configured value N allows at most N bytes.
- `UploadAction` overrides `doPost` and calls `parsePostRequest` directly with a `null` max file size, so it skips the upload-token check at the top of `UploadServlet.doPost`.
- Upload tokens are parsed whenever a `TokenValidator` is bound, even when the `tokenRequired` flag is `false`.
- Generated EC keys always use the P-521 curve, whatever `ES256` or `ES384` algorithm is configured.
- `UploadAction` hands the received file items to its `executeAction` method and does not store them in `FileStoreService`; `UploadServlet.doPost` stores each item with `put`.
- `DownloadServlet` has no size limit setting; only `UploadServlet` has `maxSize`.

### Excel Export Operations

Modeled `EXPORT` operations call the `Export` SPI. The reference implementation is `JxlsExport` (JXLS/POI): row 0 holds headers, row 1 placeholders and data starts at row 2. Cell formats follow the type: timestamp `dd/mm/yyyy hh:mm:ss`, date `dd/mm/yyyy`, time `hh:mm:ss`, decimal `#,##0.00`, integer `0`. Only the overloads taking an ASM model and a fully qualified name work. When no `Export` is configured the default module binds `UnsupportedExportImpl`, and export calls fail with `Not implemented`.

`Export` is bound to `UnsupportedExportImpl` by default in the Guice module and in the Spring configuration; every method throws `UnsupportedOperationException("Not implemented")`, so an `EXPORT` operation fails until `JxlsExport` is supplied. In the Karaf platform `DefaultJxlsExportComponent` registers `JxlsExport`; in a Guice setup pass it as the `export` of the module configuration. `JxlsExport` implements only the `AsmModel`/FQN variants; the `Class`-based `exportToInputStream` throws `UnsupportedOperationException`.

### Payload Type

`Payload` (`judo-dao-api`) is a `Map<String,Object>` with static factories (`asPayload`, `map(k1, v1, ...)`, `entry`) and typed accessors (`getAs(Class, key)`, `getAsPayload`, `getAsCollectionPayload`). `PayloadImpl` keeps its values in a `TreeMap`; the constructor wraps nested maps and collections as `Payload`, but `put` and `putAll` do not. Keys starting with `__$` are transient: `equals()` ignores them but `hashCode()` includes them, so two equal payloads can have different hash codes.

## Time and Time Zones

Two clocks exist and they do not agree:

- `Timestamp!now()` / `current_timestamp` in model expressions follows the platform parameter `defaultZoneId` (`JUDO_PLATFORM_DEFAULT_ZONE_ID`; the configuration template defaults to `UTC`), not the JVM time zone.
- `LocalDateTime.now()` in custom Java follows the JVM `TZ` / `user.timezone`.
- The persistence mapper converts to UTC and the JSON layer serializes ISO offset/UTC values.

Writing with one clock and comparing against the other yields a fixed offset (for example two hours in a Budapest summer) that silently breaks age or duration limits. Use one clock for both writing and comparing.

- Generated UI columns and fields format timestamps in the **browser** time zone (the React template calls `Intl.DateTimeFormat` without a `timeZone`). A string built in a model expression uses `defaultZoneId`, so the same instant shows with the zone offset between the two (for example `18:00` in a model-built string and `20:00` in a history column). The model cannot read the browser zone: show the timestamp itself in the UI and avoid a derived string that formats it.

- The generated TypeScript REST client turns `yyyy-MM-dd` strings into dates with `new Date(string)`, which reads them as UTC midnight. With a negative UTC offset the displayed date is one day earlier.

## Variables and Sequences

### Variable Providers

JQL `!getVariable('CATEGORY', 'key')` and Java `VariableResolver.resolve(Integer.class, "SYSTEM", "random")` read variables from the categories `SYSTEM`, `ENVIRONMENT`, `REQUEST`, `ACTOR`, `PRINCIPAL` and `SEQUENCE` (plus `USER`). `SYSTEM` provides `current_date`, `current_time` and `current_timestamp`. Register your own provider as an OSGi component with the property `judo.environment-variable-provider=true` and a `category` property: a provider with a key is a `java.util.function.Supplier`, one without a key a `Function`; providers that depend on request context must set `cacheable=false`.

The built-in `EnvironmentVariableProvider` is a concrete class implementing `Function<String, Object>` (`apply(String)`), not an interface with `get()`.

### Dispatcher Function Providers

`DispatcherFunctionProvider` exposes `getSdkFunctions()` and `getScriptFunctions()`, each returning `Map<EOperation, Function<Payload, Payload>>`.

### Custom Sequences

Identifier or number sequences default to database sequences. To plug in your own, implement `hu.blackbelt.judo.dispatcher.api.Sequence` (`getNextValue(String)`, `getCurrentValue(String)`) as an OSGi component registered with the property `Sequence.TYPE_KEY` (`type`). The platform parameter `sequenceType` selects `rdbms` (default) or a custom/`transient` type; transient sequences are not supported on multi-node deployments. Sequences can have gaps because values of rolled-back transactions are not reused.

## Custom REST Endpoints and CXF

- A custom endpoint is an OSGi DS component annotated `@Path`, registered with a discriminator property and bound into a `BasicApplication` (`cxf-jaxrs-application-manager`) through the `jaxrs.resource.components` LDAP filter (matching services become singletons) or a comma-separated `jaxrs.resource.classes` list (`Class.forName`, failures are logged and skipped).
- Custom JAX-RS providers (`@Provider`) are picked up only when the bundle manifest has `X-JAXRS-Provider: true`. Without an `applications.filter` property a provider applies to all applications.
- CXF interceptors are OSGi components implementing `org.apache.cxf.interceptor.Interceptor` with properties `judo.model.name` and `interceptor.direction` (`in`, `out` or `fault`).
- The shared Jackson `ObjectMapper` is obtained with the OSGi filter `(&(source=judo-services-jackson-objectmapper)(type=extended))`. `JacksonProvider` reads `JacksonProvider.SerializationFeature.<NAME>` and `JacksonProvider.DeserializationFeature.<NAME>` configuration keys.
- Each CXF bus is a `CxfContext` component (`configurationPolicy=REQUIRE`, required `busId`). Its optional keys are `interceptors.in.components`, `interceptors.out.components` and `interceptors.fault.components` (OSGi filters selecting `org.apache.cxf.interceptor.Interceptor` services), `metrics.enabled` and `logging.enabled` (both default `false`), `wadl.service.description.available` (default `true`) and `skip.default.json.provider.registration` (default `true`). The application manager creates the default bus `DEFAULT_CXF_BUS_FOR_JAXRS_APPLICATIONS`; a `BasicApplication` can use another context through its optional `CxfContext` reference.
- Request correlation: see `X-Exchange-Id` in the [Debugging and Monitoring Guide](debugging-and-monitoring-guide.md).

## Configuration Mapper for Custom Parameters

Custom application parameters use the OSGi Configuration Mapper: a configset declares `templatePath` (classpath folder of `*.template` FreeMarker files), `envPrefix` (for example `MY_APP_`) and `variableScopePreference` (`osgi,environment,system`). Each template file name becomes a configuration PID (`ApplicationConfiguration.template` gives PID `ApplicationConfiguration`); with `envPrefix=MY_APP_` the variable `MY_APP_PROP_NAME` is referenced as `propName`. Consumers read it with `ConfigurationAdmin.getConfiguration("ApplicationConfiguration")`.

## Tuning System Properties

Read at class load time: `EsmModelCacheExpiration` (seconds, default 5), `AsmUtilsCacheExpiration` (default 60), `FqnCacheExpiration` (default 300, idle-based expiry), `JqlExpressionBuilderModelAdapterCacheExpiration` (default 86400). `templateDebug` enables template debugging in the generator context.

## Keycloak Users and the Entity Store

For managed actors the runtime bridges Keycloak and the database through `UserManager`/`UserManagedWrappedDao`. The two stores can drift, so an admin user can exist in Keycloak while its entity row is missing. Invitation and initialization flows must verify and create the database row instead of assuming Keycloak membership implies an entity. Invitation e-mails are sent by Keycloak, not by the application, and on every Karaf start the Keycloak connector rewrites the default realm's SMTP settings from the `JUDO_PLATFORM_MAIL_SMTP_*` values. To test invitations locally run a mail catcher such as mailpit (SMTP 1025, web inbox 8025) and point `JUDO_PLATFORM_MAIL_SMTP_*` at it.

## Initializer Operations

An operation with `initializer = true` (an ESM `Operation` flag, not `OperationType.INITIALIZER`) is run by the platform; nobody calls it.

- **Shape**: `STATIC`, no input (validation `InitializerOperationIsValid`).
- **When**: in the OSGi runtime, `InitScriptExecutor` runs every initializer synchronously when the model's component activates, after the SDK operations and the identity manager are ready. It runs on **every** start of the model bundle, not once per deploy, so write initializers idempotently (check before create).
- **Identity**: `dispatcher.callOperation(name, exchange)` is called with an empty exchange: no principal and no `ACTOR`. Do not read the actor or rely on role-based access inside an initializer.
- **Transaction**: a script or custom (Java) operation is wrapped in `TransactionalOperationCall`, so each initializer runs in its own transaction.
- **Failure**: an exception is logged (`Initializer script <fqn> failed`) and the next initializer still runs; the `InitScriptsCompleted` service is registered only if all initializers succeeded.
- Spring Boot runtime: no caller of the initializer flag was found in the runtime sources (*verify* before relying on it there).

The generated `<Entity>Initializer.initBuilder()` Java interface belongs to the separate transfer-object initializer (`OperationType.INITIALIZER`), not to this flag.

## Transaction Rollback

A call that joins an existing transaction is not rolled back. The rollback happens only when the call started a new transaction (`AlwaysRollbackTransactionalBehaviourCall` checks `isNewTransaction()`).

## Scheduled Work

The platform has no scheduler: `judo-services-job` only runs the initializer operations at startup, and no Quartz or scheduling component exists in the runtime. Periodic work is application code (for example an OSGi component with its own executor).

- A scheduler thread has no request context: no principal and no `ACTOR`.
- To get the platform's transaction and operation handling, call a modeled operation through the `Dispatcher` (`callOperation`) instead of using the DAO directly; script and custom operations run in their own transaction (see Initializer Operations).
- Do not rely on `ACTOR`-based access or variables in such a call: the exchange carries no actor unless you put one in.

## Email Service

Inject `hu.blackbelt.email.api.EmailService` (OSGi) and call `sendMessage(EmailMessage.emailBuilder()....build())` (or pass the builder):

- Fields: `from`, `tos`, `ccs`, `bccs` (sets), `replyTo`, `subject`, `plaintTemplate`, `htmlTemplate`, `model`.
- Attachments: `fileAttachments` / `inputStreamAttachments` (name -> `File` / `BinaryAttachment`); inline content: `fileInlinedContents` / `inputStreamInlinedContents` (content id -> ...). `BinaryAttachment` (`binaryAttachmentBuilder()`) holds `inputStream` or `bytes`, and `mimeType`.
- **Templates**: `plaintTemplate` and `htmlTemplate` are Handlebars strings compiled inline and applied to `model` (a `Map`, bean or object with fields). The `subject` is **not** a template. At least one of the two templates must be non-blank, otherwise the call throws `No HTML or Plain message defined`. With both, a multipart message is sent.
- Every address is validated; an invalid one throws `IllegalArgumentException("Email is not valid: ...")`.
- The call is synchronous and uses the SMTP settings of the platform (`JUDO_PLATFORM_MAIL_SMTP_*`, mapped to `mail.smtp.*` JavaMail properties on the `JavaMailSenderActivator` configuration). With `JUDO_PLATFORM_LOG_SMTP_SERVER=true` a local log SMTP server receives the messages and only logs them.

## See Also

- [Error Handling Guide](error-handling-guide.md)
- [Interceptors](interceptors.md)
- [Data Access Guide](data-access-guide.md)
- [Authentication Guide](authentication-guide.md)
