# generator-plugins.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/generator-plugins.md.

## Raw Generation Flags
- `./judo.sh generate` = Maven `compile` with `-DgenerateRoot=true -DgenerateApplication=true -DskipApplicationBuild=true`; version update adds `-DupdateJudoVersions=true`.
- New project: `create-judo-project` goal of `judo-version-updater-maven-plugin`. Backend start: `clean install` in `application/karaf-offline` with `-DrunKaraf=true`.

## ESM Generator Plugin (`judo-esm-generator-maven-plugin`)
- Goals: `generate`, `create`, `checksum`, `clean`, `resetChecksum`, `synchronizeGitignore`.
- `generate` needs `esm`, `destination`, `uris`; `type` defaults to `fullstack-project`; an empty `actors` list generates all actors.

## UI Generator Plugin (`judo-ui-generator-maven-plugin`)
- Checksums in `.generated-files` (`path,md5`); `clean` deletes only files whose MD5 still matches, so hand edits survive.
- `.gitignore` block `# JUDO GENERATOR BLOCK START/END`; a START without END drops the rest of the file (known issue).

## Surviving Regeneration: checksum ignore and normalisation
- `.generator-checksum-ignore` forces overwrite of matching files; `.generator-ignore` keeps a file under manual control.
- Whitespace-tolerant comparison via `fileNormalizers` (default `auto`); `normalizeContent=false` disables it.

## Tatami Workflow Plugins
- Client `default-workflow`: `saveModels` and `validateModels` default `false`; models are saved only with `saveModels=true` or on failure.
- JSL `default-model-workflow`: `dialects` default `postgresql,hsqldb`, `transformationMode` `ETL` (set `ZETA` for Zeta; the ESM client workflow already defaults to `ZETA`), `saveModels` `true`; column length key is `rdbmsColumnMaxNameSize`.
- JSL `generator-maven-plugin`: more than one root model with empty `modelNames` fails with `Multiple root model`.
- RDBMS prefixes `T_`, `C_`, `FK_`, `FK_INV_`, `J_` (configurable; `-` suppresses).

## Derived Models via the Model CLI
- `transform` writes PSM/ASM/RDBMS/UI models to `cli-generated/` (or `-o`); `--load` reloads them; `discard --derived` resets.

## Project Generation Toggles
- `shouldGenerate*` flags all default `true` except `e2e` and `launcher`.
- `generateSingleActorApplication` serves the frontend from `/` and cannot be combined with `generateWebrootModule`.

## OpenAPI / Swagger Documentation
- `generateOpenApiAnnotations=true` writes OpenAPI to `target/api-documentation-swagger`; Swagger UI at runtime via `JUDO_PLATFORM_SWAGGER_UI` (path default `/swagger-ui`).

## SDK Generator Template Parameters
- `apiPrefix`, `generateOptionalTypes`, `generatePayloadValidator`, `debugPrint`, `identifierType` change the SDK shape.

## Report Generator (JasperReports)
- `psm-report` generates `{Type}Report` facades and `ReportUtil` (PDF, XLSX, CSV, HTML); call them from custom operations.

## REST Assured Test Client
- `ApiClient.api(Config)`, `BASE_URL_<ACTOR>`, `authTo<Actor>(...)`; no Postman collections in generated projects.

## OpenAPI Client for OSGi (`jaxrs-cxf-client-osgi-ds`)
- CXF JAX-RS client bundle with a DS activator; config `endPoint`, timeouts 10000/15000 ms.

## Generator Fragment Slots
- `<target>.<slot>.fragment.hbs`; slots for `feature.xml`, module `pom.xml` and root pom `extra-modules`.

## Custom Keycloak Login Theme
- FreeMarker pages under `themes/keycloak-theme/`; the realm's `loginTheme` must equal the theme name.

## Flutter Frontends
- Goals `install-flutter` and `flutter` (default `pub get`); `flutter.parallel` default `false`.

## Frontend Environment Variables
- `VITE_API_DEFAULT_BASE_URL` (fallback origin) + `VITE_API_RELATIVE_PATH` (fallback `/api`); `VITE_FILE_DEFAULT_BASE_URL`; optional `VITE_MUI_LICENSE_KEY`.

## Related Documentation
- [Build Process](./build-process.md)
