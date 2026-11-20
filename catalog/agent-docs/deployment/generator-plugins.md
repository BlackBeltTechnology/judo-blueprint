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
- **Known issue:** the `ModelGenerator` overloads `resetChecksums(GeneratorParameter)`, `cleanGeneratedFromChecksum(GeneratorParameter)` and `synchronizeGitignore(GeneratorParameter)` (without `InDirectory`) build their checksum removers (`Runnable`s) but never run them. `synchronizeGitignore` builds the checksum remover instead of the `.gitignore` synchronizer. The Maven goals call the `InDirectory` variants, which are not affected.
- **Known issue:** a `START` marker without an `END` marker makes the `.gitignore` synchronizer drop every following line of the file.

### Supplying the model artifact

The `ui` parameter accepts a file path or `mvn:<groupId>:<artifactId>[:<extension>[:<classifier>]]:<version>[!path/in/archive]`. The `!` suffix selects an entry inside the artifact, extracted to a temp file. Supported archives: `.tgz`, `.tar.gz`, `.zip`, `.jar`, `.bz2`, `.tar.bzip2` (a plain `.tar` is rejected). Extraction matches entry names by string prefix, so the path `templates` also matches `templates-old/...`.

## Surviving Regeneration: checksum ignore and normalisation

Generated files whose content was changed by hand are protected from being overwritten. Two mechanisms tolerate differences:

- **`.generator-checksum-ignore`** (glob patterns, searched from the file's directory up to the root) makes matching files be overwritten even when manually modified.
- **Whitespace-tolerant comparison.** A checksum-mismatched file is compared in normalised form against the saved checksum. The `fileNormalizers` presets are `auto`, `none`, `java`, `ts`, `js`, `rust`, `go`, `python`, `xml`, `html`, `css`, `json`; `auto` expands to all, `none` disables, a missing or empty list falls back to `auto`. When the normalised content matches, the file is kept and its checksum is updated (INFO log). `normalizeContent=false` disables the normalised comparison.

The normalisers can hide real changes. The tab handling deletes tab characters instead of replacing them with a space, so `public<TAB>class` normalises to `publicclass` and a hand edit that joins two words is not detected. The `json` preset also collapses runs of spaces and removes whitespace around `{ } [ ] : ,` even inside JSON string values, so an edit that changes only such whitespace inside a string is not detected.

`.generator-ignore` has no negation. Each line is a plain glob on the file path relative to the folder of that `.generator-ignore`, so a `!` prefix does not re-include a file. A file is excluded when any `.generator-ignore` from its folder up to the project root matches; a deeper file cannot override a parent rule. Narrow the broader pattern instead of negating it.

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

- `overrides` is read but never used: the override URIs are resolved and then dropped, so they have no effect. Use the frontend hook scaffolds for custom frontend code.
- `additionalFiles` is declared but never read: `dest`/`source` entries are not copied and no error is raised. Copy the files with a separate Maven step, for example `maven-resources-plugin`.
- If a model given as `mvn:<coordinates>!<path>` cannot be extracted from its archive, the plugin fails with a `NullPointerException` instead of the read error. Check the coordinates and that the artifact resolves, for example with `mvn dependency:get`.
- The save wrapper used by the mojo defaults to `catchError=true`, so an EMF save failure for `<modelName>-esm.model` or `<modelName>-ui.model` is swallowed and the build can still succeed. Check that both files exist in `destination` and read the build log.

### JSL model workflow (`judo-tatami-jsl-workflow-maven-plugin`, goal `default-model-workflow`)

Bound to `compile` (or `generate-sources` in archetype projects). Key parameters: `dialects` (default `postgresql,hsqldb`), `destination` (default `${project.basedir}/target/model`; archetype projects read `${basedir}/src/main/resources/model` and write `target/generated-sources/model`), `transformationMode` (default `ETL` in this plugin; set `ZETA` to use the Zeta engine, which is the default of the ESM client workflow, see [transformation mode](../model/model-validation-and-transformation.md#transformation-mode-and-generation-switches)), `runInParallel`, `useCache` (default `true`), `saveModels` (default `true`), `ignore*` flags (`ignorePsm2AsmTrace`, `ignoreAsm2Keycloak`, `ignoreAsm2KeycloakTrace` (default `true`), `ignoreJsl2PsmTrace`). The RDBMS maximum column name length parameter is `rdbmsColumnMaxNameSize` (`rdbmsColumnNameMaxSize` is not a valid key). The plugin has no `useDependencies` parameter; `.jsl` discovery uses the `sources` list and `scanSources`. Artifacts are named `<modelName with ':' replaced by '_'>-<suffix>.model`, per dialect `-rdbms_<dialect>.model` and `-liquibase_<dialect>.changelog.xml`.

With several dialects in one build, the Liquibase step takes any `LiquibaseModel` in the transformation context (`getByClass`) instead of the model keyed for the current dialect, so one dialect may be built on another dialect's model. Check each dialect changelog after a multi-dialect build.

### Tatami workflow plugin (`judo-tatami-workflow-maven-plugin`)

- The `operation` parameter is written `<operation>...</operation>` (the closing tag must match).
- The `keycloak` parameter loads the Keycloak model, not the Measure model.
- The per-dialect trace element is `<asm2rdbmsTrace>...</asm2rdbmsTrace>`.
- RDBMS trace skipping is governed by `ignoreAsm2RdbmsTrace` (default `false`) and the per-dialect `asm2rdbmsTrace`; there is no Keycloak trace check for it.
- A dialect's RDBMS model path is loaded only when that dialect's `asm2rdbmsTrace` is set.
- The column length parameter is `rdbmsColumnMaxNameSize`.
- `esm`, `psm` and `asm` are `String` parameters (an `mvn:` URL or a path), not `File` parameters.
- `useCache` is effectively `false` unless the POM sets it: the `@Parameter` default `false` overrides the field initialiser `true`. Set `<useCache>true</useCache>` to enable caching.
- `destination` has no default, but the mojo calls `mkdirs()` whenever `saveModels` (default `true`) or an error occurs. Set it explicitly, for example `${project.basedir}/target/model`, or the build fails with a `NullPointerException`.
- With `<asm>` set and `ignorePsm2AsmTrace` at its default `true`, the mojo calls `getArtifact(null)` and fails with a `NullPointerException` unless `<psm2AsmTrace>` is also set. The same applies to `<measure>` and `<psm2MeasureTrace>`.
- Without a generator class and method, the ESM mojo needs `<esmModelFile>` and the PSM mojo needs `<psmModelFile>`; otherwise the build fails with a `NullPointerException`.
- In the ESM mojo, a failed save after an `IllegalStateException` is silent: the save sits in a try block with an empty catch. Check `destination` after a failed build.
- If an archive model cannot be read, the build reports a `NullPointerException` instead of the read error. Check the archive path and the `mvn:` coordinates first.

### JSL generator plugin (`generator-maven-plugin`)

With `modelNames` empty, only root model declarations are candidates; the build fails with `Multiple root model` when more than one root exists. The mojo deletes nothing in its target directory: it writes `<modelName>-jsl.model` there and excludes that directory.

If an input archive cannot be read, the generator fails with a `NullPointerException` that hides the real I/O error. If an input directory is not readable, it fails the same way because `listFiles()` returns `null`. Check that the input directories are readable, and read the stack trace in the build log for the cause.

### Template URI priority and naming helpers

`ChainedURLTemplateLoader` is last-wins: later template URIs override the first (base) URI. `camelCaseToSnakeCase` returns upper-case `SNAKE_CASE` names.

Known issue: non-actor templates get only the default Handlebars context. Values bound to the per-element template context are not passed to them. `JslDslGenerator` evaluates non-actor templates with the model-level evaluation context (`JslDslGenerator.java:226`), while actor templates receive the per-element context (`:197`). `EsmGenerator` and `PsmGenerator` follow the same pattern. Workaround: check the generated output of such templates and do not rely on a template-context variable inside a non-actor template.

### RDBMS naming prefixes

Generated tables, columns, foreign keys, inverse foreign keys and junction tables use configurable prefixes `T_`, `C_`, `FK_`, `FK_INV_`, `J_`; each can be overridden. An empty value removes the prefix; any other value, including `-`, is used as written. They are set in the workflow plugin configuration. Entity tables are therefore named like `T_ENTITIES_<NAME>` (for example `T_ENTITIES_ADDRESS`) and columns `C_<NAME>`. With an empty column prefix, user attributes named `id`, `type` or `version` are written as `DOMAIN_ID`, `DOMAIN_TYPE` and `DOMAIN_VERSION` to avoid clashes with system columns.

Known issue: if both ends of a bidirectional many-to-many relation have the same name, the generator emits two junction tables, each with one `C_<NAME>` foreign-key column and no `ID` primary key, so the relation is not stored as one junction table. The ETL picks the main side with `<= 0` (`reference.etl:96`), while the EOL helper `isFirst()` uses `< 0` (`operations/asm/reference.eol:69`). Workaround: give the two relation ends different names. With different names the generator emits one junction table with two foreign-key columns and an `ID` primary key.

### Indexes

A non-derived attribute with `identifier=true` on an entity gets one non-unique index (`IDX_<hash>`) on its column. The generator creates no index for foreign-key columns, and the model has no syntax to declare other indexes; add them with a hand-written schema changeset (see [schema evolution](schema-evolution.md)).

Without an index on a foreign-key column, a derived member or query that joins or filters on that column scans the table that holds the column, which gets slow with many rows. Add the index by hand in a schema changeset.

## Derived Models via the Model CLI

`transform` of the model CLI runs the ESM -> PSM -> ASM -> RDBMS pipeline (plus esm2ui) and writes derived models to `cli-generated/` (or `-o <dir>`); with `--load` it reloads them into the running daemon. Derived models are recognised by the suffixes `-psm.model`, `-asm.model`, `-rdbms_<db>.model`, `-ui.model`, searched in the first directory holding a match (custom path, then `generated-resources/model`, then `cli-generated`). `discard --derived --from <dir>` resets them.

## Project Generation Toggles

Generation is controlled by per-module flags (`shouldGenerate*`, from `generator-parameter.properties`): model, sdk, application, rest, internal, frontend, docker, interceptor, schema, karaf, keycloak-theme, web-root, e2e and launcher. Everything defaults to `true` except `e2e` and `launcher`.

A single-actor application (`generateSingleActorApplication`) has no separate web-root module and serves the frontend from `/` (multi-actor: `/<model>_react/<actor>`). Combining `generateSingleActorApplication` with `generateWebrootModule` + `generateWebrootContent` throws `IllegalArgumentException: Do not use "generateSingleActorApplication" with "generateWebrootModule"`.

## OpenAPI / Swagger Documentation

With `generateOpenApiAnnotations=true` the rest module runs `swagger-maven-plugin` (resolve), writes OpenAPI JSON/YAML to `target/api-documentation-swagger` and embeds it into the bundle; services and DTOs carry `@Schema` annotations. The generated `ApplicationConfig` declares one server per actor (`<baseUrl>/api/<restPath>/<actor>`) and an OpenID Connect security scheme for actors with a realm. The Swagger UI is switched on at runtime with `JUDO_PLATFORM_SWAGGER_UI` (path `JUDO_PLATFORM_SWAGGER_UI_PATH`, default `/swagger-ui`).

Annotations are off unless `generateOpenApiAnnotations` is set: an unset flag is read as `false`, so set it to `true` to get the `@Schema` annotations and the OpenAPI output. In generated relation DTOs the `@Schema` name is rendered from `attribute.name` in a block where `attribute` is not in scope, so the Swagger property name can differ from the Java getter. Take the property name from the generated getter, not from Swagger UI.

## SDK Generator Template Parameters

`judo-psm-generator-sdk-core` reads five template variables, set as plugin parameters or in `generator-parameter.properties`: `apiPrefix` (package prefix for generated API packages), `generateOptionalTypes` (wrap non-required attributes and relations in `java.util.Optional`), `generatePayloadValidator` (gate `validatePayload` in the generated DAO implementations), `debugPrint` (debug banner comments) and `identifierType` (Java type of identifiers in generated DAO and DTO code). They change the shape of the SDK your code compiles against.

`apiPrefix` has two defects in the path and package helpers. An empty value makes the default API package start with a dot (`.<model>`), which is not valid Java (`judo-psm-generator-jaxrs`). A non-empty value is mangled in the jaxrs, restassured and sdk-core generators: the path is built with `replaceAll(".", "/")`, where the dot is a regex wildcard, so every character of the prefix becomes `/`. Generated API files then go to a wrong path.

## Report Generator (JasperReports)

`judo-psm-generator-report` (generator type `psm-report`, parameters `reportPrefix`, `reportFqNameFilter`, `locales`) generates for each qualifying transfer object type a `{Type}Report` facade with `generate{Type}Report(OutputType, dto, File|OutputStream[, Map additionalParameters])`, data-source classes, a per-model `ReportUtil` (`OutputType`: PDF, XLSX, CSV, HTML; compiles `.jrxml` at runtime when no `.jasper` exists) and master and sub-report `.jrxml` files (sub-reports for embedded collections). Call the facade from custom operations to export reports.

## REST Assured Test Client

`judo-psm-generator-restassured` emits `ApiClient.api(Config)` per model with `BASE_URL_<ACTOR>` constants, `authTo<Actor>(grantType, userName, password)` password-grant helpers (client id `<model>-<actor>`) and one wrapper per exposed transfer object whose operations pin `REQ_METHOD` (GET only for stateless operations without input, else POST) and `REQ_URI`, with `body(...)`, `xJudoCountRecordsHeader`, `xJudoMaskHeader`, `xJudoSignedIdentifierHeader` and `execute()`. Postman collections are not part of generated projects; they exist only in the platform's integration-test project. The OpenAPI toggle is `ignoreOpenAPI=false`.

Each `authTo<Actor>(...)` call reads the client config's request-spec supplier and replaces it with one that adds the `Authorization` header, so headers from earlier calls on the same client, including an earlier `Authorization` header, stay in the chain. Create one client per actor in tests.

## OpenAPI Client for OSGi (`jaxrs-cxf-client-osgi-ds`)

The generator `jaxrs-cxf-client-osgi-ds` (`openapi-generator-cxf-jaxrs-client-osgi-ds`) produces a CXF JAX-RS client bundle with a Declarative Services `ClientApiServiceActivator`. Configuration: `endPoint`, `log_payload`, `log_payload_limit` (1000), `connection_timeout` (10000 ms), `receive_timeout` (15000 ms). Options: `activatorPackage` (default `org.openapitools.activator`), `activatorDsConfigurationRequired` (`false`; `true` emits `configurationPolicy=REQUIRE`), `useGzipFeature`, `useLoggingFeature`.

With `useGzipFeature` the generated service activator uses `GZIPOutInterceptor` and `GZIPInInterceptor` without importing them, so the bundle may not compile. Disable `useGzipFeature` or add the missing imports in a custom template.

## Generator Fragment Slots

Fragments are files named `<target>.<slot>.fragment.hbs`: `feature.xml` slots `extra-repositories`, `extra-bundles`, `model-bundles`; each module `pom.xml` slots `project-definition`, `properties-definition`, `extra-plugin-management`, `extra-plugins`, `extra-dependencies`; the application `pom.xml` `extra-modules`. Slot names come from the `<!-- To define create ... -->` markers in the generated file. Tools that scan for overrides should glob `*.fragment.hbs`. See also the [Backend README](../backend/README.md).

## Custom Keycloak Login Theme

The generated `keycloak-theme` module (`src/main/resources/themes/keycloak-theme/`) holds FreeMarker login pages (`login.ftl`, `register.ftl`, `error.ftl`, `template.ftl` with the `registrationLayout` macro and an empty `footer.ftl` override point), `theme.properties` (`parent=base`, `import=common/keycloak`, `kc*` class keys) and `login.css`. `test-users-realm.json` (realm `TEST_USERS`) and `test-theme-with-compose.sh` start a dev Keycloak on port 8080 with the built theme unzipped into `./keycloak-themes`. The realm's `loginTheme` must equal the theme name exactly. the keycloak-theme module is one of the project generation toggles. The theme zip contains the theme folders under `src/main/resources/themes` at its root.

## Flutter Frontends

Flutter frontends are built with the goals `install-flutter` (installs the SDK from a pinned version or a Git channel, default `stable`) and `flutter` (runs flutter CLI commands, default `pub get`). Parameters: `flutter.arguments`, `flutter-version`, `flutter-channel`, `flutter-skip`, `flutter-install-skip`, `workingDirectory` / `installDirectory` / `tempDirectory` (defaults `${basedir}`, `${basedir}/.flutter`, `${basedir}/target/temp`) and `flutterInheritsProxyConfigFromMaven=true`. The `parallel` parameter of `flutter-maven-plugin` is set by the system property `flutter.parallel` (default `false`).

The `flutter-download-root` default is `https://storage.googleapis.com/flutter_infra_release/releases/`, and the install always passes it on. If that host is not reachable, set `flutter-download-root` to a reachable mirror.

## Frontend Environment Variables

The generated React frontend reads: `VITE_API_DEFAULT_BASE_URL` (fallback `window.location.origin`), `VITE_API_RELATIVE_PATH` (fallback `/api`), `VITE_FILE_DEFAULT_BASE_URL` (fallback the API base URL) and optionally `VITE_MUI_LICENSE_KEY`. The API base is `VITE_API_DEFAULT_BASE_URL` + `VITE_API_RELATIVE_PATH`; the file base is the file base URL + `/<modelName>`.

## Related Documentation

- [Build Process](./build-process.md)
- [Schema Evolution](./schema-evolution.md)
- [Deployment Overview](./README.md)
