---
title: OSGi Runtime Services
description: Model bundles, datasource provisioning, model version checks, startup readiness, health checks and Karaf administration.
aliases: [deploy model as OSGi bundle, karaf startup problems, model version check failed, health check endpoint, keycloak realm sync config, CORS settings per model]
keywords: [Judo-Models, targetDatasourceModelName, ignoreVersionCheck, JUDO_MODEL_VERSIONS, retryMaxAttempts, pax-jdbc, cors_allowOrigin, realm_loginByEmail, /system/health, JUDO_STARTUP_FEATURE]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# OSGi Runtime Services and Deployment Behaviour

This guide describes how the JUDO platform behaves when a model is deployed in a Karaf/OSGi container: model bundles, datasource provisioning, startup readiness, health checks and Karaf administration. It is background for operators and for developers who debug a deployment. Examples use the model name `<app>`.

## Deploying a Model as an OSGi Bundle

Models can be deployed as raw model files in the Karaf deploy folder, or as OSGi bundles that declare a `Judo-Models` manifest header, for example `Judo-Models: name=<app>;version=1.0.0`. The generated model module does this (`<Judo-Models>name=${model-name};version=${model-version}</Judo-Models>`).

The model bundle tracker loads each model from the bundle resources with a strict naming convention:

- `model/<name>-esm.model`, `-psm.model`, `-asm.model`, `-measure.model`, `-expression.model`, `-openapi.model`, `-keycloak.model`
- per dialect: `model/<name>-rdbms_<dialect>.model`, `-asm2rdbms_<dialect>.model` and `-liquibase_<dialect>.changelog.xml`

A `dialects` (comma-separated) configuration decides which dialect resources are loaded. The default is empty: it yields one blank dialect, so the dialect resources are looked up as `model/<name>-rdbms_.model` (and the matching `asm2rdbms_`/`liquibase_` names), which do not exist, so no dialect-specific model or changelog is loaded. Set `dialects` explicitly (for example `postgresql` or `hsqldb`). A missing version uses the bundle version, a blank version becomes `1.0.0.<timestamp>_SNAPSHOT`, and `.SNAPSHOT` suffixes get a timestamp substitution.


### Libraries already in the runtime

The generated `<app>-judo-platform-prototype` Karaf feature already contains Tika (`tika-core`, `tika-parsers` 1.28.5) and PDFBox 2.0.13, and the OSGi e-mail feature brings Handlebars 4.2.0. Reuse them for document or template rendering instead of adding new bundles; add a bundle only for a library that is not listed here. Verify that the e-mail feature is installed in the target runtime before relying on Handlebars.

The generated feature descriptor is `feature.xml` (from `feature.xml.hbs`), not `features.xml`.

### Unit-testing components

Declarative Services components can be unit-tested without a container with `MockOsgi` from `osgi-utils` (`osgi-test`): `MockOsgi.activate`/`deactivate` call the `@Activate`/`@Deactivate` methods (parameters: none, `BundleContext`, `ComponentContext`, `Map`/`Dictionary`) and `MockOsgi.setReferences` injects services into `@Reference` fields or bind methods (Felix SCR and standard OSGi DS annotations).

### JAX-RS Application Address

The JAX-RS address of an application comes from the `applicationPath` entry of `Application.getProperties()`, not from an OSGi service property. If that entry is missing and the application class has no `@ApplicationPath`, the server logs a warning. If one application in a multi-application container fails to start (no classes and no singletons), the remaining applications are not started either; check the Karaf log for the first failure.

## Target Datasource Model

In a multi-model deployment one model owns the shared datasource and every other model is configured against it. Every per-model activator reads a `targetDatasourceModelName` key; for the model whose name equals that value it suppresses its own per-model components (dialect/mapper/sequence, Keycloak connector and login interceptor, dispatcher configurations, health checks, realm extractor, access manager). The managed datasource carries `dao.datasource.name`, `managed.datasource.name` and `judo.model.name`, and components bind per model through filters like `(dao.datasource.name=<name>)`. The target model also gets no `InitScriptExecutor`, so init scripts do not run for it; put startup seeding on another model in a multi-model deployment.

## Runtime Model Version Check

Before a datasource is used, the Liquibase model datasource pre-hook either runs the Liquibase migration or checks and records the model version in the `JUDO_MODEL_VERSIONS` table and verifies that the RDBMS model matches the database. When the stored version differs, it fails with `There are RDBMS model changes which have not been applied to database` - run the incremental schema migration (see [Schema Evolution](./schema-evolution.md)). Setting `ignoreVersionCheck=true` skips the model-store check and only runs the Liquibase update.

**Known issue:** a `LiquibaseException` during prepare is only logged and not rethrown, so the datasource can be handed out even though the migration failed. Always check the log for Liquibase errors after a start, not only whether the application came up.

## Embedded HSQLDB Server

For local development and tests the platform starts an embedded HSQLDB TCP server per Liquibase model. The server needs `dataSourceName`, `databaseName` and `databasePath` (no defaults) and optional `port` (default 9001). The Liquibase tracker auto-assigns ports starting at 30000 (incremented per model), sets `pax-jdbc.url=jdbc:hsqldb:hsql://localhost:<port>/<databaseName>` and creates an `org.ops4j.datasource` factory configuration. Keys prefixed `pax-jdbc.` are forwarded to the datasource configuration with the prefix stripped.

**Known issue:** the OSGi transformation services that generate the RDBMS and Liquibase models inside a running container (`Asm2RdbmsTransformationAsmModelTracker`, `Rdbms2LiquibaseTranformationSerivce`) hard-code the dialect `hsqldb`. In such a deployment the generated schema model is HSQLDB-shaped regardless of the configured database. The Java API and the workflow Maven plugin honour the configured dialects, so deploy the pre-built `-rdbms_postgresql.model` / `-liquibase_postgresql.changelog.xml` from the model bundle.

## PostgreSQL Bootstrap Retry and Datasource Keys

The PostgreSQL datasource tracker waits for the database with a retry loop before it creates the `org.ops4j.datasource` factory configuration:

| Key | Default |
|-----|---------|
| `retryMaxAttempts` | `1000` |
| `retryExponentialBackoff` | `true` |
| `retryWaitDuration` | `1000` ms |
| `ignoreVersionCheck` | `false` |

`pax-jdbc.*` keys are copied into the datasource configuration with the prefix stripped (the HSQLDB tracker keeps the prefix). If the connection still fails after the retries the error is only logged and no datasource configuration is created for that model.

## Startup Banner and Readiness

A startup banner is printed when seven platform services are registered for a model: Dispatcher, JaxRsApplicationsReady, PersistenceReady, ScriptsReady, SdkOperationsReady, IdentityManagerReady and InitScriptsCompleted. At that point a `JudoApplicationReady` service is published. Configuration keys (`bannerEnabled`, `bannerFonts`, `bannerHslStart`/`bannerHslEnd`, `enableJMX`, system property `disableJudoAnsiColors`) are listed in [Application Configuration](./application-config.md#8-startup-banner-and-jmx). With `enableJMX=true` the MBeans are named `hu.blackbelt.judo:type=<model>,name=Application` and `<SimpleName>_<model>` for the health checks.

## Health Check Endpoint Details

The Felix Health Check servlet is served at `/system/health` (default servlet path) with the format extensions `.html`, `.json`, `.jsonp`, `.txt` and `.verbose.txt`. It also selects a serializer by the `Accept` header (`application/json`, `text/html`, `text/plain`).

- **Query parameters:** `tags`, `names`, `format`, `httpStatus` (e.g. `CRITICAL:503`), `combineTagsWithOr`, `forceInstantExecution`, `timeout`, `hcDebug` and a JSONP callback (default `processHealthCheckResults`).
- **HTTP status mapping:** `OK`/`WARN` -> 200, `TEMPORARILY_UNAVAILABLE`/`CRITICAL` -> 503, `HEALTH_CHECK_ERROR` -> 500.
- **JSON body:** `{"overallResult": <STATUS>, "results": [{name, status, timeInMs, finishedAt, tags, messages: [{status, message, exception?}]}]}`. `finishedAt` has the format `yyyy-MM-dd'T'HH:mm:ss.SSS` (no time zone). Debug messages are omitted unless debug is requested; exceptions are serialized as a stack-trace string.
- **Plain text** returns only the overall status name (`OK`, `CRITICAL`, ...), which suits load balancers.
- **Configuration keys:** `allowed_formats`, `cors_accessControlAllowOrigin` (default `*`), `disable_request_configuration`, `disabled`.

### Writing a custom health check

JUDO registers the rules `ModelsCheck`, `OperationsCheck` and `PlatformComponentsCheck`. To publish an application-specific readiness signal, create an OSGi component implementing `org.apache.felix.hc.api.HealthCheck` and tag it with the model name; it then appears in `http://localhost:8181/system/health?tags=<app>`.

## Karaf Administration

- The Karaf console is secured by JAAS users in `etc/users.properties` in the format `USER=PASSWORD,_g_:GROUP`, with roles (`group`, `admin`, `manager`, `viewer`, `systembundles`, `ssh`) granted per group. An admin user can be enabled at boot with the `karaf_enable_admin_user` start option of `judo.sh`.
- The SSH port 8101 and the `karaf`/`karaf` login are Apache Karaf defaults, not settings of the project template. Change or disable them for any non-local deployment.
- The startup feature of the offline assembly can be overridden at runtime with `JUDO_STARTUP_FEATURE`.

## Model Artifact Names Produced by the Workflow

The workflow save step writes deterministic file names: `<modelName>-rdbms_<dialect>.model`, `<modelName>-<realm>-keycloak.json`, `<modelName>-liquibase_<dialect>.changelog.xml`, and the generated Java operation bundle with `Bundle-SymbolicName` `<modelName>-script2operation`. Models are written only when `saveModels` is true (default) or when the workflow failed, and the destination directory must already exist.

## Keycloak Connector and Realm Synchronizer Configuration

The OSGi Keycloak activator builds per-model components from these keys (defaults in the source):

- Connector: `serverUrl`, `publicUrl`, `adminUser`, `adminPassword`, optional `clientSecret`.
- `managementEnabled` (default `false`): `false` registers only the connector; `true` also registers the admin client, realm synchronizer, user manager and password policies (`NO_PASSWORD`, `SAME_EMAIL`, `SAME_USERNAME`).
- Realm synchronizer: `realm_loginByEmail` (`true`), `client_accessType_human` (`CONFIDENTIAL`), `client_accessType_system` (`BEARER_ONLY`). Values go through `AccessType.valueOf`, so they must be exact enum names or activation fails with `IllegalArgumentException`. Retry defaults: `asyncServiceCall=true`, `retryMaxAttempts=1000`, `retryExponentialBackoff=true`, `retryWaitDuration=1000` ms.
- User manager: `updateExistingUsers`, `enabled` and `requiredActions` (comma separated, no default).
- Login interceptor: `acceptableClients` (`ActorFQN=client1,client2;OtherActor=client3`), see the [Authentication Guide](../backend/authentication-guide.md#several-keycloak-clients-in-one-realm).

The realm synchronizer provisions realms, clients and users from the model's asm2keycloak output when the runtime starts. Existing realms and clients are updated only when a compared field differs; redirect URIs and web origins are merged as sorted unions. User provisioning waits until the synchronizer calls `setIdentityManagerReady(true)`, and runs asynchronously by default.

The Guice runtime (`JudoKeycloakModuleConfiguration`) defaults `keycloakServerUrl` to `http://localhost:8080/auth` and `keycloakAdminPassword` to `judo`. Both runtimes pass `CONFIDENTIAL` for human actors and `BEARER_ONLY` for system actors (the constructor-level defaults of `KeycloakRealmSynchronizer` are the reverse, but they are always overridden).

### Realm and client generation from the model

The ASM-to-Keycloak transformation turns every distinct `realm` annotation on actor types into a realm (used as written, untrimmed; blank values are not skipped) (`loginWithEmailAllowed`), and every actor type with a `realm` annotation into a client named after the actor FQN with `.` replaced by `-` (`directAccessGrantsEnabled`, `redirectUris=["*"]`). Adding a `realm` annotation therefore provisions Keycloak without manual client setup. Write the realm name without surrounding spaces: the realm keeps the untrimmed value, but client generation trims it before looking the realm up, so a padded name does not match its realm.

## CORS Filter per Model

`CxfSecurityActivator` registers one `CrossOriginResourceSharingFilter` per model (service filter `application.filter=(judo.model.name=<model>)`). Keys and defaults: `cors_allowOrigin` `*`, `cors_allowCredentials` `true`, `cors_allowHeaders` `Content-Type,Origin,Accept,Authorization,X-Judo-SignedIdentifier,X-Judo-CountRecords`, `cors_exposeHeaders` `X-Exchange-Id,X-Fault,X-Judo-Count`, `cors_maxAge` `-1`, `cors_prefligthErrorStatus` `400` (the spelling is the real key), `cors_blockIfUnauthorized` `false`, `cors_defaultOptionsMethodsHandlePreflight` `false`. A frontend that sends `X-Judo-Mask` or `X-Judo-RequestParameters` from another origin needs them added to `cors_allowHeaders`.

## Swagger UI Serving Location

A Swagger UI servlet is registered per OpenAPI model at `/api-spec/<model name>`. The `apiRoot` key (default `/api`) prefixes the `basePath` of the generated `swagger.json`; the host and scheme come from the request.

## Filestore S3 Backend Details

Besides the environment variables in [Application Configuration](./application-config.md), the S3 component needs `protocol`, `bucketName`, `accessKey` and `secretKey`; `endpoint` defaults to empty (AWS) and `region` to `us-east-1`. The access URL it returns is an internal `<protocol>:<fileId>-<filename>` URL, not a public or signed link, so downloads flow through the Karaf servlet. The S3 backend has no metadata cache: each name, size, type or time lookup is a HEAD request. Only HTTP 404 is treated as not found; other error statuses (for example 403 or 500) are returned as file content, so check the HTTP status and file size before trusting a downloaded file. File URLs are resolved by cutting the file id at the first dash, so RDBMS ids that contain dashes (UUIDs) fail when resolved from a URL; pass the file id instead. A URL without a dash fails with an index error, so build file URLs as `<fileId>-<filename>` with a file id that has no dash.

## Running Liquibase Changelogs from a Bundle

`osgi-liquibase` exposes `LiquibaseExecutor.executeLiquibaseScript(Connection, scriptPathInBundle, Bundle)` and an overload taking a `Map` of changelog parameters. **Known issue:** the default executor rethrows only `LiquibaseException`; any other exception is swallowed, so the caller can see success after a failure. Nothing is logged for these, so check the database state. An unreadable changelog entry (a `URISyntaxException` while the bundle URL is converted) is reported as an empty list, so the changelog is silently not applied; check that the model's tables exist after deployment. `StreamResourceAccessor.list()` ignores the requested path and returns every registered stream name, so a directory listing through it is not limited to the folder.

## Related Documentation

- [Application Configuration](./application-config.md)
- [Schema Evolution](./schema-evolution.md)
- [Spring Boot Runtime](./spring-boot-runtime.md)
- [Deployment Overview](./README.md)
