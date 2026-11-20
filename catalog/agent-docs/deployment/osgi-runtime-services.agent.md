# osgi-runtime-services.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/osgi-runtime-services.md.

## Deploying a Model as an OSGi Bundle
- Manifest header `Judo-Models: name=<app>;version=1.0.0`; generated model module sets `<Judo-Models>name=${model-name};version=${model-version}</Judo-Models>`.
- Resources: `model/<name>-esm.model` (also `-psm`, `-asm`, `-measure`, `-expression`, `-openapi`, `-keycloak`); per dialect `-rdbms_<dialect>.model`, `-asm2rdbms_<dialect>.model`, `-liquibase_<dialect>.changelog.xml`.
- `dialects` (comma-separated) selects dialect resources; default empty loads none. Missing version uses bundle version; blank version becomes `1.0.0.<timestamp>_SNAPSHOT`.

### Libraries already in the runtime
- Feature `<app>-judo-platform-prototype` includes `tika-core` and `tika-parsers` 1.28.5, PDFBox 2.0.13; e-mail feature brings Handlebars 4.2.0 (verify it is installed).
- Feature descriptor is `feature.xml` (from `feature.xml.hbs`), not `features.xml`.

### Unit-testing components
- `MockOsgi` (`osgi-utils`, `osgi-test`): `activate`/`deactivate` call `@Activate`/`@Deactivate`; `setReferences` injects `@Reference` fields or bind methods.

### JAX-RS Application Address
- Address comes from the `applicationPath` entry of `Application.getProperties()`, not an OSGi service property; missing entry with no `@ApplicationPath` logs a warning.
- If one application fails (no classes and no singletons), the others in the container are not started; check the Karaf log for the first failure.

## Target Datasource Model
- Activators read `targetDatasourceModelName`; the matching model suppresses its per-model components (dialect/mapper/sequence, Keycloak connector, dispatcher, health checks, access manager, etc.).
- Managed datasource carries `dao.datasource.name`, `managed.datasource.name`, `judo.model.name`; components bind via filters like `(dao.datasource.name=<name>)`.
- Target model gets no `InitScriptExecutor`; put startup seeding on another model.

## Runtime Model Version Check
- Liquibase pre-hook either runs the migration or checks/records the version in `JUDO_MODEL_VERSIONS`.
- Mismatch fails with `There are RDBMS model changes which have not been applied to database`; migrate per [Schema Evolution](./schema-evolution.md). `ignoreVersionCheck=true` skips the store check and only runs the Liquibase update.
- **Known issue:** `LiquibaseException` during prepare is only logged; the datasource can still be handed out. Check logs for Liquibase errors after start.

## Embedded HSQLDB Server
- Per Liquibase model; required `dataSourceName`, `databaseName`, `databasePath` (no defaults); optional `port` (default 9001).
- Ports auto-assigned from 30000 (+1 per model); URL `jdbc:hsqldb:hsql://localhost:<port>/<databaseName>`; `pax-jdbc.` keys forwarded to the datasource config with prefix stripped.
- **Known issue:** `Asm2RdbmsTransformationAsmModelTracker` and `Rdbms2LiquibaseTranformationSerivce` hard-code `hsqldb`; deploy pre-built `-rdbms_postgresql.model` and `-liquibase_postgresql.changelog.xml`.

## PostgreSQL Bootstrap Retry and Datasource Keys
- Defaults: `retryMaxAttempts` `1000`, `retryExponentialBackoff` `true`, `retryWaitDuration` `1000` ms, `ignoreVersionCheck` `false`.
- `pax-jdbc.*` keys are copied to the datasource config with the prefix stripped (the HSQLDB tracker keeps the prefix).
- If retries fail, the error is only logged and no datasource config is created for that model.

## Startup Banner and Readiness
- Banner prints when seven services are registered per model: Dispatcher, JaxRsApplicationsReady, PersistenceReady, ScriptsReady, SdkOperationsReady, IdentityManagerReady, InitScriptsCompleted; then `JudoApplicationReady` is published.
- Keys: `bannerEnabled`, `bannerFonts`, `bannerHslStart`/`bannerHslEnd`, `enableJMX`, system property `disableJudoAnsiColors` (see [Application Configuration](./application-config.md#8-startup-banner-and-jmx)).
- With `enableJMX=true`: MBeans `hu.blackbelt.judo:type=<model>,name=Application`; health checks `<SimpleName>_<model>`.

## Health Check Endpoint Details
- Servlet at `/system/health`; extensions `.html`, `.json`, `.jsonp`, `.txt`, `.verbose.txt`; also selected by `Accept` header. Plain text returns only the overall status.
- Status mapping: `OK`/`WARN` 200; `TEMPORARILY_UNAVAILABLE`/`CRITICAL` 503; `HEALTH_CHECK_ERROR` 500.
- Query parameters: `tags`, `names`, `format`, `httpStatus` (e.g. `CRITICAL:503`), `combineTagsWithOr`, `forceInstantExecution`, `timeout`, `hcDebug`, JSONP callback (default `processHealthCheckResults`).
- Config keys: `allowed_formats`, `cors_accessControlAllowOrigin` (default `*`), `disable_request_configuration`, `disabled`.

### Writing a custom health check
- JUDO registers `ModelsCheck`, `OperationsCheck`, `PlatformComponentsCheck`.
- Implement `org.apache.felix.hc.api.HealthCheck` as an OSGi component tagged with the model name; it appears at `http://localhost:8181/system/health?tags=<app>`.

## Karaf Administration
- Console users in `etc/users.properties` as `USER=PASSWORD,_g_:GROUP`; roles `group`, `admin`, `manager`, `viewer`, `systembundles`, `ssh`. Admin user enabled at boot with the `karaf_enable_admin_user` start option of `judo.sh`.
- SSH port 8101 and `karaf`/`karaf` are Apache Karaf defaults; change or disable them for non-local deployments.
- Startup feature of the offline assembly can be overridden with `JUDO_STARTUP_FEATURE`.

## Model Artifact Names Produced by the Workflow
- Names: `<modelName>-rdbms_<dialect>.model`, `<modelName>-<realm>-keycloak.json`, `<modelName>-liquibase_<dialect>.changelog.xml`, and operation bundle `Bundle-SymbolicName` `<modelName>-script2operation`.
- Written only when `saveModels` is true (default) or the workflow failed; the destination directory must already exist.

## Keycloak Connector and Realm Synchronizer Configuration
- Connector keys: `serverUrl`, `publicUrl`, `adminUser`, `adminPassword`, optional `clientSecret`. `managementEnabled` defaults `false` (`true` also registers admin client, realm synchronizer, user manager, password policies `NO_PASSWORD`, `SAME_EMAIL`, `SAME_USERNAME`).
- Realm synchronizer: `realm_loginByEmail` (`true`), `client_accessType_human` (`CONFIDENTIAL`), `client_accessType_system` (`BEARER_ONLY`). Must be exact `AccessType` enum names or activation fails with `IllegalArgumentException`. Retry defaults: `asyncServiceCall=true`, `retryMaxAttempts=1000`, `retryExponentialBackoff=true`, `retryWaitDuration=1000` ms.
- User manager: `updateExistingUsers`, `enabled`, `requiredActions` (comma-separated, no default). Login interceptor: `acceptableClients` (`ActorFQN=client1,client2;OtherActor=client3`).
- Guice runtime (`JudoKeycloakModuleConfiguration`) defaults `keycloakServerUrl` to `http://localhost:8080/auth` and `keycloakAdminPassword` to `judo`.

### Realm and client generation from the model
- ASM-to-Keycloak transformation makes one realm per distinct actor `realm` annotation (value kept untrimmed) and one client per annotated actor type, named by actor FQN with `.` replaced by `-`.
- Client generation trims the realm name before lookup, so a padded realm name does not match its realm; write names without surrounding spaces.

## CORS Filter per Model
- `CxfSecurityActivator` registers one `CrossOriginResourceSharingFilter` per model, filter `application.filter=(judo.model.name=<model>)`.
- Defaults: `cors_allowOrigin` `*`, `cors_allowCredentials` `true`, `cors_maxAge` `-1`, `cors_prefligthErrorStatus` `400` (real key spelling), `cors_blockIfUnauthorized` `false`, `cors_defaultOptionsMethodsHandlePreflight` `false`.
- `cors_allowHeaders` defaults to `Content-Type,Origin,Accept,Authorization,X-Judo-SignedIdentifier,X-Judo-CountRecords`; `cors_exposeHeaders` to `X-Exchange-Id,X-Fault,X-Judo-Count`.
- A frontend sending `X-Judo-Mask` or `X-Judo-RequestParameters` from another origin needs them added to `cors_allowHeaders`.

## Swagger UI Serving Location
- Swagger UI servlet per OpenAPI model at `/api-spec/<model name>`.
- `apiRoot` (default `/api`) prefixes the `basePath` of the generated `swagger.json`; host and scheme come from the request.

## Filestore S3 Backend Details
- Required: `protocol`, `bucketName`, `accessKey`, `secretKey`; `endpoint` defaults to empty (AWS), `region` to `us-east-1`.
- Access URL is internal `<protocol>:<fileId>-<filename>`, not signed; downloads go through the Karaf servlet. No metadata cache: each name, size, type or time lookup is a HEAD request.
- Only HTTP 404 means not found; other statuses (e.g. 403, 500) are returned as file content, so check HTTP status and file size.
- URL resolution cuts the file id at the first dash, so UUID-style ids fail from a URL (pass the file id); a URL without a dash fails with an index error, so build `<fileId>-<filename>` with a dash-free file id.

## Running Liquibase Changelogs from a Bundle
- `LiquibaseExecutor.executeLiquibaseScript(Connection, scriptPathInBundle, Bundle)`, plus an overload taking a `Map` of changelog parameters.
- **Known issue:** the default executor rethrows only `LiquibaseException`; other exceptions are swallowed and not logged, so a caller can see success after failure. Check database state.
- **Known issue:** an unreadable changelog (`URISyntaxException`) is reported as an empty list and silently not applied; verify the model's tables exist after deployment. `StreamResourceAccessor.list()` ignores the requested path and returns every registered stream name.

## Related Documentation
- [Application Configuration](./application-config.md), [Schema Evolution](./schema-evolution.md), [Spring Boot Runtime](./spring-boot-runtime.md), [Deployment Overview](./README.md).
