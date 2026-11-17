# build-process.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/build-process.md.

## Table of Contents

- Section list of the source: judo.sh Script, Maven Commands, Build Profiles, Build Workflows, Maven Configuration, Troubleshooting, Best Practices.

## Key Concepts

- Model Transformation: ESM → PSM → ASM models, then code generation.
- SDK Generation: Java interfaces and DTOs forming the API.
- Reckless Mode: fast dev build; skips non-essential checks, enables caching.
- Hot Deployment: apply backend changes without server restart.

## Project Template and Generation

- Generated from `judo-esm-fullstack-project-template` (Handlebars templates); config in `generator-parameter.properties` at project root.
- Key params: `sqlDialects=postgresql,hsqldb`, `validateModels=true`, `useCache=false`, `rdbmsCreateSimpleName=true`, `frontendType=react`, `defaultLanguage=en-US`, `tablePageLimit=10`, `generate*Module=true` flags (Interceptor, Application, Sdk, Rest, Frontend, Docker, Karaf).
- Before hand-editing a generated file (e.g. `pom.xml`), check the template for a parameter (`#if rdbmsCreateSimpleName` blocks). Set the parameter in `generator-parameter.properties` instead. Hand edits may be overwritten on regeneration.
- Fragment overrides: generated files carry marker comments `<!-- To define create 'app/pom.xml.extra-dependencies.fragment.hbs' file -->`. Put a file with the same relative name in `application/generator-overrides/` (wired in root `pom.xml` via `${maven.multiModuleProjectDirectory}/application/generator-overrides`; a second root `generator-overrides/` exists for the project-root step).
- Fragments are snippets (no wrapping element); they are inlined. Handlebars and generator params work inside.
- Example: add a runtime dep to `application/app/pom.xml` via `application/generator-overrides/app/pom.xml.extra-dependencies.fragment.hbs`, then `./judo.sh generate` or `build`.
- Platform libraries are available at runtime, but compile-time deps still need the pom fragment.
- Fragment points (stubs, survive regeneration without `.generator-ignore`): root `pom.xml.{project-definition,properties-definition,model-properties-definition,judo-properties-definition,extra-dependency-management,extra-plugin-management,extra-plugins,extra-modules,extra-profiles,release-profiles,distribution-management,repository-definition}.fragment.hbs`; `app/pom.xml.{project-definition,properties-definition,extra-plugin-management,extra-plugins,extra-dependencies}.fragment.hbs`; same set for `karaf-features/`, `e2e/`, `frontend-react/` poms; `karaf-features/src/main/feature/feature.xml.{extra-repositories,extra-bundles,model-bundles}.fragment.hbs`.
- Frontend fragments under `actor/`: `package.json.{dependencies,dev-dependencies,scripts}.extra.fragment.hbs`; `public/i18n/application_default_extra.fragment.hbs` (stub `"__extra": "..."`, write `key: value,` lines); `src/fragments/operations/operation-primary-output-handler.fragment.hbs` (context: `operation`, `action`).
- Theme fragments: see [Theming](../frontend/theming.md).
- Template helpers: `elementHasAnnotation(element, "<name>")`; `operation.output.target`. Escape a literal expression with `\{{name}}`.
- Prefer fragments over `.generator-ignore`: `.generator-ignore` freezes output and drifts from templates.
- Common params: `rdbmsCreateSimpleName` (false), `validateModels` (true), `useCache` (false), `sqlDialects`, `frontendType` (react), `generateDockerModule` (true).

## judo.sh Script

- Orchestrates env setup (SDKMAN, tools), model transformation, build, service lifecycle (start/stop/status), Docker compose.
- Location: `/judo.sh`.

### `judo.sh build` flag reference

- Several flags mean "skip": `-M` skips the ESM→PSM→ASM→RDBMS→keycloak transformation (NOT "model only"). `-B` skip backend, `-F` skip frontend, `-KA` skip Karaf, `-S` skip schema image.
- `-a` builds `app/` module only (fast Java iteration). `-f` frontend module only. `-sc` schema CLI JAR. `-d` / `--docker` Docker images. `-p` parallel. `-q` quick (cache, skip validations). `-i` ignore checksum errors and refresh checksums.
- Model-only changes need full `./judo.sh build` (no flags), not `-M`. `asm2keycloak` emits the Keycloak realm only when model build runs. With `-M` a stale realm sticks; app shows blank and `/system/health` lacks `JaxRsApplicationsReady`.

### Local-dev Keycloak realm dependency

- `bin/keycloak-disable-ssl-required.sh` (run by `start_local_env` after `start_keycloak`): logs into `master` as `admin`/`judo`, sets `sslRequired=NONE`, waits up to 180s for realm named exactly `<schema_name>` (from `judo.properties`), sets same on it; warns `app realm ... did not appear within 180s; skipping` otherwise.
- The realm name is `ActorType.realm` (emitted by `asm2keycloak`). `ActorType.realm` defaults to `DEFAULT` in `esm.ecore`, which never matches `schema_name`; realm stays `sslRequired=external`, and `/.well-known/openid-configuration` returns 403 over HTTP.
- Authoring rule: always set `ActorType.realm = <schema_name>`.

### Quick Reference Commands

- `./judo.sh build`, `build start`, `stop`, `status`, `reckless`, `clean`, `prune` (`-f`, `-y`), `--help`.

### Command Reference

- Chain commands: `./judo.sh build clean start`.
- `env <env>`: alternate properties file (default `judo.properties`), e.g. `env compose-dev build start`.
- `clean`: stops PostgreSQL container and clears its data. Does NOT delete untracked files.
- `prune` (`-f`, `-y`): deletes untracked files (see Prune below).
- `update` (`-i`): update dependency versions.
- `generate` (`-i`): regenerate app from model (`-DgenerateApplication -DskipApplicationBuild`). `generate-root` (`-i`): `-DgenerateRoot`.
- `dump`: dump PostgreSQL before clearing and starting. `import` (`-dn <name>`): import dump; no name loads last.
- `schema-upgrade`: persistent PostgreSQL only; generates the diff against the running DB and applies it immediately. Do NOT use when a backfill changeset is needed (no insertion point).
- `build` options: `-v <version>`, `-p`, `-a`, `-f`, `-sc`, `-d`/`--docker`, `-M`, `-B`, `-F`, `-KA`, `-S`, `-ma <arg>` (extra Maven arg), `-q`, `-i`.
- `reckless`: build and run fast; skips validation and Docker. `start`: app with PostgreSQL and Keycloak. `stop`. `status`.
- `start` options: `-W` (no bundle watch), `-K` (skip Keycloak), `-o "<name>=<value>,..."`:
  - `runtime`: `karaf` | `compose`
  - `dbtype`: `hsqldb` | `postgresql`
  - `compose_env`: `compose-develop` | `compose-postgresql-https` | a dir under the model's `doc` dir
  - `model_dir` (default: app's parent)
  - `karaf_port`, `postgres_port`, `keycloak_port` (Karaf HTTP default 8181)
  - `compose_access_ip`, `karaf_enable_admin_user` (`1`), `java_compiler` (`ejc` default | `javac`)
- Option defaults can go in `judo.properties`.
- No `-D` pass-through in `judo.sh`. Use `-d` for Docker and `-ma` for Maven args. Docker profiles activate on `!skipDocker`, so ANY `-DskipDocker` (even `=false`) disables Docker. `judo.sh build` without `-d` passes `-DskipDocker -DskipSchemaDocker`; `reckless` skips Docker.

### Prune (Destructive)

- `prune` runs `git clean`: permanently deletes ALL untracked files. No undo.
- Variants: `prune` (whole repo), `prune -f` (only `application/frontend-react/`), `prune -y` (skips `[Y/n]`).
- Wipes uncommitted custom frontend code (`frontend-react/<app>/src/custom/**`, `.../theme/**`, `.../i18n/**`), scratch files, `node_modules/`.
- Safety checklist: `git status`; `git stash -u` or commit customizations; prefer interactive `prune`; never chain `-y` in an agent workflow unless tree verified clean. For agents, `prune -y` equals `rm -rf` on customer code; require human confirmation.
- Right use: designer freezes on open (stale frontend); model refactors renamed actors; clean rebuild `./judo.sh prune -f && ./judo.sh build -i`.

## Frontend Build Recovery

- If `./judo.sh build -i` fails in the frontend reactor (e.g. `TS2307 Cannot find module ~/services/data-axios/...`): delete `src/pages/`, `src/dialog/`, `src/containers/`, `src/services/` in `frontend-react`, then `./judo.sh build -i`. Re-running alone is not enough.
- After renaming a transfer object, container or page: generated names change (`<ContainerComponentName>...Component`, `..._INTERFACE_KEY`, page and dialog folders). Rename custom files and constants by hand, delete stale generated folders, then `./judo.sh build -i`.

## Stale Artifacts and Multi-Module Build Order

- Maven reactor: model, schema, sdk, internal, app, common. SDK POM regenerates from the INSTALLED model jar in `~/.m2`, not the edited source. Stale jar poisons the chain.
- Building `sdk` standalone fails `Could not collect dependencies` until model and schema are installed; then `-pl` with `-o` and `validateModels=false`.
- Tests may pass on stale SNAPSHOTs; `mvnd` can print `BUILD SUCCESS` while installing stale jars. Rebuild with `./judo.sh build -i` (ignores checksums; hand edits not in `.generator-ignore` are lost). Verify with `unzip -l` / `javap`, not timestamps. Two parallel repo copies cause confusion.
- Additive model changes (new stored attribute) need no manual migration: generated Liquibase changelog `<app>-liquibase_postgresql.changelog.xml` under `application/model/target/generated-resources/model/` has the column. See [Schema Evolution](./schema-evolution.md#when-no-manual-step-is-needed).
- Do NOT run `initdatatests` in baseline builds (very long; only when init data changes).

## Multi-Repository Development (platform changes)

- Runtime change may span `judo-runtime-core`, `judo-platform`, `osgi-filestore`, and the app.
- Create matching feature branches. Build bottom-up: runtime-core, install snapshot to `~/.m2`, platform pins new runtime-core, app pins platform.
- Update versions in BOTH `application/pom.xml` and `judo-version.properties`.
- Real versions live in `judo-versions` repo `pom.xml` `<properties>`; its `src/main/resources/versions.properties` only has `${}` placeholders.
- Before merging: feature commit is ancestor of develop build; new artifact is in assembled `karaf-offline` zip or Docker image.
- `./judo.sh update` refreshes pinned versions.

## Creating a New Project from the ESM Fullstack Template

- Template modules: `-root`, `-application`, `-common`, `-test`. Root resources: `pom.xml.hbs`, `judo.sh.hbs`, `generator-parameter.properties.hbs`, `AGENTS.md.hbs`, `README.adoc.hbs`, `pom.xml.*.fragment.hbs`.
- 1. Place model at `model/<app>.model`; run goal `create-judo-project` of `judo-version-updater-maven-plugin` (groupId `hu.blackbelt.judo`) with `-DmodelName`, `-DprojectGroupId`, `-DprojectArtifactId`, `-DprojectVersion`, `-Dversion`. Plugin version and `-Dversion` come from target JUDO versions, not `~/.m2` cache.
- 2. Root POM `generate-root` execution with `synchronizeGitignore` (`esm=${basedir}/model/<app>.model`; ignored `pom.xml`, `**/pom.xml`, `judo.sh`, `.mvn/jvm.config`). When adopting into a repo with its own `.gitignore`, copy only generated files and keep the managed `# JUDO GENERATOR BLOCK`; overwriting wholesale makes `generate-root` fail with manual-changes error.
- 3. Add `<server>` id `<app>-distribution` to `~/.m2/settings.xml` for deploys.
- 4. Run `./judo.sh build`. Docker required (DB and Keycloak run in containers).

## Toolchain Bootstrap and Versions

- Template defaults: `node-version` 24.13.1, `pnpm-version` 10.15.0, `frontend-maven-plugin` 1.12.1. Maven properties `nodeVersion` / `pnpmVersion` override.
- `prepare-nodejs` profile runs `install-node-and-pnpm` into `${maven.multiModuleProjectDirectory}/.nodejs`; frontend and e2e need no pre-installed Node.

## Docker Image Build

- `docker` module: one image tar per arch via `jib-maven-plugin` 3.3.2; profiles `x86_64`, `amd64`, `arm64`; output `target/<artifactId>-<version>_docker_image_<arch>.tar`; base `azul/zulu-openjdk-debian:21-latest`.
- Tags from `DOCKER_IMAGE_TAGS` (default `dev`).
- JMX exporter, Elastic APM, New Relic agents added only when `dockerPrometheusJmxExporterAgentVersion`, `dockerElasticApmAgentVersion`, `dockerNewrelicAgentVersion` are set.
- Entrypoint `/<name>/bin/karaf run clean`. Ports 8181, 8081, 1099, 44444, 5000, 9090, 5005. Volumes `/<name>/deploy`, `/<name>/data`. Files in `${project.basedir}/overrided` copied in.

## Eclipse Launch Configurations

- `BuildApplication.launch`: clean install of `application`.
- `BuildApplicationWithoutFrontend.launch`: adds `-DskipDocker=true -DskipFrontend=true`.
- `CompileCustomApp.launch`: clean install of `application/app`.
- `RunApplication.launch`: backend from `application/karaf-offline`, `-DrunKaraf=true`.
- `RunFrontend.launch`: profile `react-build`, `-DskipDist=true -DrunServer=true`, from `application/frontend`.

## Template Agent-Docs Placeholders

- Agent-docs are Handlebars templates. Only helpers: `docLink` (→ `[text](path)`), `localHubLink` (→ `[text](./README.md)`), both defined in `EsmProjectHelper` (`judo-esm-fullstack-project-template-common`), plus a lower-case model-name expression and a model-name expression.
- Literal double braces escaped with backslash. `#if`/`#each` in docs are examples only.

## Maven Commands

- Full: `mvn clean install`. Skip flags: `-DskipFrontendReact`, `-DskipDocker`, `-DskipSchema`. Single module: `cd application/app && mvn clean install`. Parallel: `-T 4`.

## Build Profiles

| Profile | Skip flag | Default |
|---|---|---|
| `build-model` (ESM→PSM→ASM) | `-DskipBackendModels` | Enabled |
| `build-schema` (schema evolution scripts) | `-DskipSchema` | Enabled |
| `build-sdk` (Java SDK) | `-DskipSDK` | Enabled |
| `build-frontend-react` | `-DskipFrontendReact` | Enabled |
| `build-karaf` | `-DskipKaraf` | Enabled |
| `build-docker` | `-DskipDocker` | Enabled |

- Examples: backend only `-DskipFrontendReact -DskipDocker`; model only `-DskipFrontendReact -DskipKaraf -DskipDocker`.

## Build Workflows

### Full Build Process

- `./judo.sh build` steps: 1 env check (Docker, Java, Maven); 2 model transformation (load `/model/<app>.model`, generate ESM/PSM/ASM, schemas — see [Schema Evolution](./schema-evolution.md), expression models); 3 SDK generation; 4 backend compile (SDK, `app/`, interceptors, REST); 5 frontend (UI model, React, `pnpm install`, `pnpm build`, JAR); 6 Karaf assembly; 7 Docker image (optional).
- Duration: first 10-15 min; incremental 3-5 min; cached 1-2 min.

### Incremental Build

- Model changed: `mvn clean install -pl application/model,application/sdk,application/rest`.
- Backend changed: `cd application/app && mvn install`.
- Frontend changed: `cd application/frontend-react/<app>__[actor_fqn] && mvn install`.

### Reckless Mode

- `./judo.sh reckless`: Maven caching, validation disabled, non-essential checks skipped, incremental compile.
- Use for prototyping and small iterations. Not for production builds, breaking changes, or final testing.

## Maven Configuration

### Distribution Repository

- `~/.m2/settings.xml` `<servers>` with `<id>` of the private repo and credentials.

### Memory Configuration

- Large builds: `export MAVEN_OPTS="-Xmx4g"`.

## Troubleshooting

### Build Failures

- "Model validation failed": check `/model/<app>.model`; run `mvn clean install -X`.
- "Could not resolve dependencies": check `~/.m2/settings.xml` credentials; clear `rm -rf ~/.m2/repository/hu/blackbelt`.
- "Frontend build failed": Node version (source says 18+); `rm -rf node_modules && pnpm install`.
- "Out of memory": `export MAVEN_OPTS="-Xmx4g"`.

## Best Practices

### Performance Optimization

- `-T` for parallel Maven; skip Docker in dev (`-DskipDocker`); use a local Maven mirror for cache.

### Development Workflow

- Incremental builds for changed modules; reckless mode for iteration; full clean build before committing.

## Related Documentation

- [Local Development](./local-development.md) — dev environment and hot deployment.
- [Production Deployment](./production.md) — production build and deployment.
- [Deployment Overview](./README.md) — main deployment docs.
