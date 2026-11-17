---
title: Code Generation Maven Plugins
description: ESM and UI generator goals, checksums, Tatami workflow plugins, generation toggles, OpenAPI, Flutter and frontend environment variables.
aliases: [maven generator goals, regenerate frontend code, checksum ignore, generation toggles, tatami workflow plugin, openapi generation, flutter frontend]
keywords: [judo-esm-generator-maven-plugin, judo-ui-generator-maven-plugin, judo-tatami-client-workflow-maven-plugin, default-workflow, checksum, OpenAPI, JasperReports]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Code Generation Maven Plugins and Workflow Goals

This guide describes the Maven plugins that drive code generation in the JUDO build. Most developers use them indirectly through `./judo.sh generate` and `./judo.sh build`; read this when you need to call a goal directly or debug generation.

## Raw Generation Flags

`./judo.sh generate` runs Maven `compile` with the VM flags `-DgenerateRoot=true -DgenerateApplication=true -DskipApplicationBuild=true`; updating versions adds `-DupdateJudoVersions=true`. New-project scaffolding runs the `create-judo-project` goal of `judo-version-updater-maven-plugin` with `-DmodelName`, `-DprojectGroupId`, `-DprojectArtifactId`, `-DprojectVersion` and `-Dversion`. The backend is started with `clean install` in `application/karaf-offline` plus `-DrunKaraf=true`.

## ESM Generator Plugin (`judo-esm-generator-maven-plugin`)

| Goal | Default phase | Purpose |
|------|---------------|---------|
| `generate` | `generate-resources` | Generate the project from the ESM model |
| `create` | none (`requiresProject=false`) | Standalone creation of a project |
| `checksum` | `generate-resources` | Compute checksums |
| `clean` | `clean` | Delete tracked generated files |
| `resetChecksum` | `clean` | Rewrite stored checksums |
| `synchronizeGitignore` | `process-resources` | Maintain the managed `.gitignore` block |

`generate` parameters: `esm` (required; a file path or `mvn:` URL), `destination` (required; commonly `${project.basedir}/target/fullstack-project`), `uris` (required; template locations), `type` (default `fullstack-project`), `actors`, `helpers`, `scanDependencies` (default `true`), `validateChecksum` (default `true`). Template parameters come from `templateParameters` (inline map), `parameterFiles` (properties files) and `variablePrecedence` (conflict order).

- Template URIs accept `mvn:groupId:artifactId:version` or `mvn:groupId:artifactId:version!path/in/jar` over `tgz`/`tar.gz`/`zip`/`jar`/`bz2`.
- An empty `actors` list generates code for all actor types; a non-empty list restricts generation to the listed actor FQ names.

## UI Generator Plugin (`judo-ui-generator-maven-plugin`)

Five goals: `generate` (`generate-resources`, needs the YAML descriptor type), `checksum` (`generate-resources`), `clean` (`clean`), `resetChecksum` (`clean`) and `synchronizeGitignore` (`process-resources`).

- Checksums live in a CSV file `.generated-files` (`path,md5`), per application `.generated-files-<appName>`.
- `clean` deletes only tracked files whose MD5 on disk still matches the stored checksum, so hand-edited files survive a clean.
- `synchronizeGitignore` maintains a block delimited by `# JUDO GENERATOR BLOCK START/END` and takes an `ignoredFiles` glob list.

### Supplying the model artifact

The `ui` parameter accepts a file path or `mvn:<groupId>:<artifactId>[:<extension>[:<classifier>]]:<version>[!path/in/archive]`. The `!` suffix selects an entry inside the artifact, extracted to a temp file. Supported archives: `.tgz`, `.tar.gz`, `.zip`, `.jar`, `.bz2`, `.tar.bzip2` (a plain `.tar` is rejected). Extraction matches entry names by string prefix, so the path `templates` also matches `templates-old/...`.

## Surviving Regeneration: checksum ignore and normalisation

Generated files whose content was changed by hand are protected from being overwritten. Two mechanisms tolerate differences:

- **`.generator-checksum-ignore`** (glob patterns, searched from the file's directory up to the root) makes matching files be overwritten even when manually modified.
- **Whitespace-tolerant comparison.** A checksum-mismatched file is compared in normalised form against the saved checksum. The `fileNormalizers` presets are `auto`, `none`, `java`, `ts`, `js`, `rust`, `go`, `python`, `xml`, `html`, `css`, `json`; `auto` expands to all, `none` disables, a missing or empty list falls back to `auto`. When the normalised content matches, the file is kept and its checksum is updated (INFO log). `normalizeContent=false` disables the normalised comparison.

To keep a file under manual control use `.generator-ignore`; to extend generated POMs use the extension fragments described in [Build Process](./build-process.md#extending-generated-files-via-fragment-overrides).

## Tatami Workflow Plugins

### Client workflow (`judo-tatami-client-workflow-maven-plugin`, goal `default-workflow`)

Bound to the `compile` phase; runs the ESM -> UI pipeline during a build.

| Parameter | Default |
|-----------|---------|
| `destination` | `${project.basedir}/target/classes/model` |
| `runInParallel` | `true` |
| `enableMetrics` | `true` |
| `ignoreEsm2Ui` | `false` |
| `validateModels` | `false` |
| `saveModels` | `false` |
| `esm` / `ui` | optional model inputs |

Model inputs use the `mvn:` URI syntax or plain file paths; a `file:` scheme is **not** stripped. Saved artifacts per model: `<modelName>-esm.model`, `<modelName>-ui.model` (XMI) and `<modelName>-ui.json`. Models are saved with validation **disabled**; validation is a separate step that only runs with `validateModels=true`. The Mojo writes models only when `saveModels=true` or when the workflow failed, so generated models are not auto-validated.

### JSL model workflow (`judo-tatami-jsl-workflow-maven-plugin`, goal `default-model-workflow`)

Bound to `compile` (or `generate-sources` in archetype projects). Key parameters: `dialects` (default `postgresql,hsqldb`), `destination` (default `${project.basedir}/target/model`; archetype projects read `${basedir}/src/main/resources/model` and write `target/generated-sources/model`), `transformationMode` (default `ETL`; Zeta is opt-in), `runInParallel`, `useCache` (default `true`), `saveModels` (default `true`), `ignore*` flags (`ignorePsm2AsmTrace`, `ignoreAsm2Keycloak`, `ignoreAsm2KeycloakTrace` (default `true`), `ignoreJsl2PsmTrace`). The RDBMS maximum column name length parameter is `rdbmsColumnMaxNameSize` (`rdbmsColumnNameMaxSize` is not a valid key). The plugin has no `useDependencies` parameter; `.jsl` discovery uses the `sources` list and `scanSources`. Artifacts are named `<modelName with ':' replaced by '_'>-<suffix>.model`, per dialect `-rdbms_<dialect>.model` and `-liquibase_<dialect>.changelog.xml`.

### Tatami workflow plugin (`judo-tatami-workflow-maven-plugin`)

- The `operation` parameter is written `<operation>...</operation>` (the closing tag must match).
- The `keycloak` parameter loads the Keycloak model, not the Measure model.
- The per-dialect trace element is `<asm2rdbmsTrace>...</asm2rdbmsTrace>`.
- RDBMS trace skipping is governed by `ignoreAsm2RdbmsTrace` (default `false`) and the per-dialect `asm2rdbmsTrace`; there is no Keycloak trace check for it.
- The column length parameter is `rdbmsColumnMaxNameSize`.

### JSL generator plugin (`generator-maven-plugin`)

With `modelNames` empty, only root model declarations are candidates; the build fails with `Multiple root model` when more than one root exists. The mojo deletes nothing in its target directory: it writes `<modelName>-jsl.model` there and excludes that directory.

### Template URI priority and naming helpers

`ChainedURLTemplateLoader` is last-wins: later template URIs override the first (base) URI. `camelCaseToSnakeCase` returns upper-case `SNAKE_CASE` names.

### RDBMS naming prefixes

Generated tables, columns, foreign keys, inverse foreign keys and junction tables use configurable prefixes `T_`, `C_`, `FK_`, `FK_INV_`, `J_`; each can be overridden, and `-` suppresses the prefix. They are set in the workflow plugin configuration. Entity tables are therefore named like `T_ENTITIES_<NAME>` (for example `T_ENTITIES_ADDRESS`) and columns `C_<NAME>`.

## Derived Models via the Model CLI

`transform` of the model CLI runs the ESM -> PSM -> ASM -> RDBMS pipeline (plus esm2ui) and writes derived models to `cli-generated/` (or `-o <dir>`); with `--load` it reloads them into the running daemon. Derived models are recognised by the suffixes `-psm.model`, `-asm.model`, `-rdbms_<db>.model`, `-ui.model`, searched in the first directory holding a match (custom path, then `generated-resources/model`, then `cli-generated`). `discard --derived --from <dir>` resets them.

## Project Generation Toggles

Generation is controlled by per-module flags (`shouldGenerate*`, from `generator-parameter.properties`): model, sdk, application, rest, internal, frontend, docker, interceptor, schema, karaf, keycloak-theme, web-root, e2e and launcher. Everything defaults to `true` except `e2e` and `launcher`.

A single-actor application (`generateSingleActorApplication`) has no separate web-root module and serves the frontend from `/` (multi-actor: `/<model>_react/<actor>`). Combining `generateSingleActorApplication` with `generateWebrootModule` + `generateWebrootContent` throws `IllegalArgumentException: Do not use "generateSingleActorApplication" with "generateWebrootModule"`.

## OpenAPI / Swagger Documentation

With `generateOpenApiAnnotations=true` the rest module runs `swagger-maven-plugin` (resolve), writes OpenAPI JSON/YAML to `target/api-documentation-swagger` and embeds it into the bundle; services and DTOs carry `@Schema` annotations. The generated `ApplicationConfig` declares one server per actor (`<baseUrl>/api/<restPath>/<actor>`) and an OpenID Connect security scheme for actors with a realm. The Swagger UI is switched on at runtime with `JUDO_PLATFORM_SWAGGER_UI` (path `JUDO_PLATFORM_SWAGGER_UI_PATH`, default `/swagger-ui`).

## SDK Generator Template Parameters

`judo-psm-generator-sdk-core` reads five template variables, set as plugin parameters or in `generator-parameter.properties`: `apiPrefix` (package prefix for generated API packages), `generateOptionalTypes` (wrap non-required attributes and relations in `java.util.Optional`), `generatePayloadValidator` (gate `validatePayload` in the generated DAO implementations), `debugPrint` (debug banner comments) and `identifierType` (Java type of identifiers in generated DAO and DTO code). They change the shape of the SDK your code compiles against.

## Report Generator (JasperReports)

`judo-psm-generator-report` (generator type `psm-report`, parameters `reportPrefix`, `reportFqNameFilter`, `locales`) generates for each qualifying transfer object type a `{Type}Report` facade with `generate{Type}Report(OutputType, dto, File|OutputStream[, Map additionalParameters])`, data-source classes, a per-model `ReportUtil` (`OutputType`: PDF, XLSX, CSV, HTML; compiles `.jrxml` at runtime when no `.jasper` exists) and master and sub-report `.jrxml` files (sub-reports for embedded collections). Call the facade from custom operations to export reports.

## REST Assured Test Client

`judo-psm-generator-restassured` emits `ApiClient.api(Config)` per model with `BASE_URL_<ACTOR>` constants, `authTo<Actor>(grantType, userName, password)` password-grant helpers (client id `<model>-<actor>`) and one wrapper per exposed transfer object whose operations pin `REQ_METHOD` (GET only for stateless operations without input, else POST) and `REQ_URI`, with `body(...)`, `xJudoCountRecordsHeader`, `xJudoMaskHeader`, `xJudoSignedIdentifierHeader` and `execute()`. Postman collections are not part of generated projects; they exist only in the platform's integration-test project. The OpenAPI toggle is `ignoreOpenAPI=false`.

## OpenAPI Client for OSGi (`jaxrs-cxf-client-osgi-ds`)

The generator `jaxrs-cxf-client-osgi-ds` (`openapi-generator-cxf-jaxrs-client-osgi-ds`) produces a CXF JAX-RS client bundle with a Declarative Services `ClientApiServiceActivator`. Configuration: `endPoint`, `log_payload`, `log_payload_limit` (1000), `connection_timeout` (10000 ms), `receive_timeout` (15000 ms). Options: `activatorPackage` (default `org.openapitools.activator`), `activatorDsConfigurationRequired` (`false`; `true` emits `configurationPolicy=REQUIRE`), `useGzipFeature`, `useLoggingFeature`.

## Generator Fragment Slots

Fragments are files named `<target>.<slot>.fragment.hbs`: `feature.xml` slots `extra-repositories`, `extra-bundles`, `model-bundles`; each module `pom.xml` slots `project-definition`, `properties-definition`, `extra-plugin-management`, `extra-plugins`, `extra-dependencies`; the root pom `extra-modules`. Slot names come from the `<!-- To define create ... -->` markers in the generated file. Tools that scan for overrides should glob `*.fragment.hbs`. See also the [Backend README](../backend/README.md).

## Custom Keycloak Login Theme

The generated `keycloak-theme` module (`src/main/resources/themes/keycloak-theme/`) holds FreeMarker login pages (`login.ftl`, `register.ftl`, `error.ftl`, `template.ftl` with the `registrationLayout` macro and an empty `footer.ftl` override point), `theme.properties` (`parent=base`, `import=common/keycloak`, `kc*` class keys) and `login.css`. `test-users-realm.json` (realm `TEST_USERS`) and `test-theme-with-compose.sh` start a dev Keycloak on port 8080 with the built theme unzipped into `./keycloak-themes`. The realm's `loginTheme` must equal the theme name exactly. the keycloak-theme module is one of the project generation toggles.

## Flutter Frontends

Flutter frontends are built with the goals `install-flutter` (installs the SDK from a pinned version or a Git channel, default `stable`) and `flutter` (runs flutter CLI commands, default `pub get`). Parameters: `flutter.arguments`, `flutter-version`, `flutter-channel`, `flutter-skip`, `flutter-install-skip`, `workingDirectory` / `installDirectory` / `tempDirectory` (defaults `${basedir}`, `${basedir}/.flutter`, `${basedir}/target/temp`) and `flutterInheritsProxyConfigFromMaven=true`.

## Frontend Environment Variables

The generated React frontend reads: `VITE_API_DEFAULT_BASE_URL` (fallback `window.location.origin`), `VITE_API_RELATIVE_PATH` (fallback `/api`), `VITE_FILE_DEFAULT_BASE_URL` (fallback the API base URL) and optionally `VITE_MUI_LICENSE_KEY`. The API base is `VITE_API_DEFAULT_BASE_URL` + `VITE_API_RELATIVE_PATH`; the file base is the file base URL + `/<modelName>`.

## Related Documentation

- [Build Process](./build-process.md)
- [Schema Evolution](./schema-evolution.md)
- [Deployment Overview](./README.md)
