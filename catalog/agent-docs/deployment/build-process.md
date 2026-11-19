---
title: Build Process
description: judo.sh command reference, Maven profiles, build workflows, project template generation, Docker image build and build troubleshooting.
aliases: [build the project, judo.sh build flags, maven build profiles, skip docker build, build failure, prune untracked files]
keywords: [judo.sh, generator-parameter.properties, generator-overrides, DOCKER_IMAGE_TAGS, skipDocker, skipFrontendReact, rdbmsCreateSimpleName, reckless, prune, MAVEN_OPTS, jib-maven-plugin]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Build Process

This guide covers the build system, Maven configuration, and build workflows for the <app> project.

## Table of Contents

- [judo.sh Script](#judosh-script)
- [Maven Commands](#maven-commands)
- [Build Profiles](#build-profiles)
- [Build Workflows](#build-workflows)
- [Maven Configuration](#maven-configuration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Key Concepts

- **Model Transformation**: The process of converting the high-level ESM model into more detailed PSM and ASM models, which are then used to generate code.
- **SDK Generation**: The process of creating the Java interfaces and DTOs that make up the application's API.
- **Reckless Mode**: A fast build mode for development that skips non-essential checks and enables caching.
- **Hot Deployment**: A development feature that allows you to apply backend code changes without restarting the server.

## Project Template and Generation

### How the Project is Generated

This project was initially generated using the **JUDO ESM Fullstack Project Template**:
- **Template Repository**: [judo-esm-fullstack-project-template](https://github.com/BlackBeltTechnology/judo-esm-fullstack-project-template)
- **Generator**: Uses Handlebars templates to create project skeleton
- **Configuration**: `generator-parameter.properties` file in project root

### generator-parameter.properties

This file controls how the project structure is generated from templates.

**Location:** `/generator-parameter.properties`

**Key Parameters:**

```properties
# Model Generation
sqlDialects=postgresql,hsqldb
validateModels=true
useCache=false
rdbmsCreateSimpleName=true              # Use simple table names in RDBMS

# Frontend
frontendType=react
defaultLanguage=en-US
tablePageLimit=10

# Modules to Generate
generateInterceptorModule=true
generateApplicationModule=true
generateSdkModule=true
generateRestModule=true
generateFrontendModule=true
generateDockerModule=true
generateKarafModule=true
```

### When to Check Templates Instead of Patching

**⚠️ IMPORTANT**: Before manually editing generated files (like `pom.xml`), check if the template supports a parameter.

**Why?**
- Manual edits may be overwritten on regeneration
- Template parameters are the proper way to configure generation
- Ensures consistency across regenerations

**Process:**

1. **Identify the generated file** you want to modify (e.g., `application/model/pom.xml`)

2. **Find the template** in [judo-esm-fullstack-project-template](https://github.com/BlackBeltTechnology/judo-esm-fullstack-project-template)
   - Example: `judo-esm-fullstack-project-template-application/src/main/resources/model/pom.xml.hbs`

3. **Check for conditional blocks** in the template:
   ```text
   #if rdbmsCreateSimpleName
   <rdbmsCreateSimpleName>(value of rdbmsCreateSimpleName)</rdbmsCreateSimpleName>
   /if
   ```

4. **Add parameter** to `generator-parameter.properties` instead of manually editing
   ```properties
   rdbmsCreateSimpleName=true
   ```

5. **Regenerate** if needed, or apply manually for existing projects

**Example: Adding rdbmsCreateSimpleName**

Instead of manually editing `application/model/pom.xml`:
```xml
<!-- ❌ DON'T: Manual edit -->
<rdbmsCreateSimpleName>true</rdbmsCreateSimpleName>
```

Add to `generator-parameter.properties`:
```properties
# ✅ DO: Configure via parameter
rdbmsCreateSimpleName=true
```

### Extending Generated Files via Fragment Overrides

Some generated files (mostly `pom.xml` and `feature.xml`) cannot be fully controlled by template parameters because they need to carry project-specific content (extra dependencies, plugins, bundles, …). For these, the templates expose **named fragment extension points** that you can fill in without touching the generated output.

**How to spot one:** generated files contain paired marker comments like

```xml
<!-- To define create 'app/pom.xml.extra-dependencies.fragment.hbs' file -->
<!-- End of 'app/pom.xml.extra-dependencies.fragment.hbs' -->
```

By default the fragment resolves to an empty stub from the template jar. You override it by dropping a file with the **same relative path and name** into the override directory.

**Override directory:** `application/generator-overrides/` (wired into the generator invocation in the root `pom.xml` via `<uri>${maven.multiModuleProjectDirectory}/application/generator-overrides</uri>`; a second override root `generator-overrides/` exists for the project-root generator step).

#### Worked Example: Adding a Dependency

**Worked example — add a runtime dependency to `application/app/pom.xml`:**

1. Locate the marker in `application/app/pom.xml`:
   ```xml
   <!-- To define create 'app/pom.xml.extra-dependencies.fragment.hbs' file -->
   <!-- End of 'app/pom.xml.extra-dependencies.fragment.hbs' -->
   ```
2. Create `application/generator-overrides/app/pom.xml.extra-dependencies.fragment.hbs` containing just the snippet to be inlined (no wrapping `<dependencies>` element — it is injected inside the existing `<dependencies>` block):
   ```xml
   <dependency>
       <groupId>hu.blackbelt.judo.runtime</groupId>
       <artifactId>judo-runtime-core-dispatcher</artifactId>
       <version>${judo-runtime-core-version}</version>
   </dependency>
   ```
3. Run `./judo.sh generate` (or `./judo.sh build`). The dependency now appears in the regenerated `application/app/pom.xml`, and its checksum in `.generated-files` stays stable because the content is produced by the template, not by a manual edit.

Platform-provided libraries (for example PDF, template-engine or file-store service APIs) are available at runtime, but the app module still needs a compile-time dependency in its pom (via this fragment) before their imports resolve.

Fragments are Handlebars templates, so you can use expression syntax and generator parameters (for example `\<app>`) inside them.

#### Available Fragment Extension Points

Every generated module (application root, app, interceptors, karaf-features, schema, e2e, web-root) has these empty stubs; a file with exactly that name in the override directory survives regeneration and needs no `.generator-ignore` entry.

**Available fragment extension points (from `judo-esm-fullstack-project-template`):**

| Scope | Fragment | Typical use |
|-------|----------|-------------|
| Root `pom.xml` | `pom.xml.project-definition.fragment.hbs` | Override parent/artifact coordinates |
| Root `pom.xml` | `pom.xml.properties-definition.fragment.hbs` | Extra `<properties>` entries |
| Root `pom.xml` | `pom.xml.model-properties-definition.fragment.hbs` | Override model-related properties |
| Root `pom.xml` | `pom.xml.judo-properties-definition.fragment.hbs` | Override JUDO version properties |
| Root `pom.xml` | `pom.xml.extra-dependency-management.fragment.hbs` | Extra `<dependencyManagement>` entries |
| Root `pom.xml` | `pom.xml.extra-plugin-management.fragment.hbs` | Extra `<pluginManagement>` entries |
| Root `pom.xml` | `pom.xml.extra-plugins.fragment.hbs` | Extra `<plugins>` in `<build>` |
| Root `pom.xml` | `pom.xml.extra-modules.fragment.hbs` | Extra `<modules>` |
| Root `pom.xml` | `pom.xml.extra-profiles.fragment.hbs` / `pom.xml.release-profiles.fragment.hbs` | Extra / release `<profiles>` |
| Root `pom.xml` | `pom.xml.distribution-management.fragment.hbs` / `pom.xml.repository-definition.fragment.hbs` | Custom deploy & repository config |
| `app/pom.xml` | `app/pom.xml.project-definition.fragment.hbs` | Override coordinates of the `app` module |
| `app/pom.xml` | `app/pom.xml.properties-definition.fragment.hbs` | Extra properties for `app` |
| `app/pom.xml` | `app/pom.xml.extra-plugin-management.fragment.hbs` | Extra `<pluginManagement>` for `app` |
| `app/pom.xml` | `app/pom.xml.extra-plugins.fragment.hbs` | Extra `<plugins>` for `app` |
| `app/pom.xml` | `app/pom.xml.extra-dependencies.fragment.hbs` | Extra `<dependencies>` for `app` (e.g. custom interceptor SPIs) |
| `karaf-features/pom.xml` | `karaf-features/pom.xml.{project-definition,properties-definition,extra-plugin-management,extra-plugins,extra-dependencies}.fragment.hbs` | Same pattern for the Karaf features module |
| `karaf-features/.../feature.xml` | `karaf-features/src/main/feature/feature.xml.{extra-repositories,extra-bundles,model-bundles}.fragment.hbs` | Extra Karaf bundles / repositories in the generated feature descriptor |
| `e2e/pom.xml`, `e2e/actor/pom.xml`, `e2e/model/pom.xml` | `e2e/**/pom.xml.{project-definition,properties-definition,extra-plugin-management,extra-plugins,extra-dependencies}.fragment.hbs` | Same pattern for the E2E test modules |
| `frontend-react/pom.xml`, `frontend-react/actor/pom.xml`, `frontend-react/model/pom.xml` | `frontend-react/**/pom.xml.{project-definition,properties-definition}.fragment.hbs` | Override coordinates / properties for React frontend modules |

##### Frontend (React) fragment extension points

Frontend (React) fragments, all placed in the override directory under `actor/`:

- `actor/package.json.dependencies.extra.fragment.hbs`, `actor/package.json.dev-dependencies.extra.fragment.hbs` and `actor/package.json.scripts.extra.fragment.hbs` add entries to the matching `package.json` section.
- `actor/public/i18n/application_default_extra.fragment.hbs` adds translation keys to the default language file. The stub is `"__extra": "Placeholder for additional translations",`, so write JSON key-value lines with a trailing comma.
- `actor/src/fragments/operations/operation-primary-output-handler.fragment.hbs` is included after each operation call, with `operation` and `action` in context. The stub is an empty comment. Use it to handle the operation result.
- Theme fragments are covered in [Theming](../frontend/theming.md).

In templates, `elementHasAnnotation(element, "<name>")` is true when the model element has an annotation with exactly that name, and `operation.output.target` is the output's target class type. To keep a literal Handlebars expression in the generated file, escape it with a backslash: `\{{name}}` renders as `{{name}}` (the generated i18n files use this for i18next placeholders).

> **Prefer fragment overrides over `.generator-ignore`.** A fragment keeps the file under the generator's control so future template improvements still flow in; adding the file to `.generator-ignore` freezes the generated output and will drift from the template over time.

### Common Generator Parameters

| Parameter | Purpose | Values | Default |
|-----------|---------|--------|---------|
| `rdbmsCreateSimpleName` | Simple RDBMS table names | `true`/`false` | `false` |
| `validateModels` | Enable model validation | `true`/`false` | `true` |
| `useCache` | Cache model transformations | `true`/`false` | `false` |
| `sqlDialects` | Target database dialects | `postgresql,hsqldb` | - |
| `frontendType` | Frontend framework | `react` | `react` |
| `generateDockerModule` | Generate Docker configs | `true`/`false` | `true` |

See `generator-parameter.properties` for complete list.

---

## judo.sh Script

Main orchestration script that simplifies common operations.

**Location:** `/judo.sh`

**Capabilities:**
- Environment setup (SDKMAN, tools)
- Model transformation
- Build orchestration
- Service lifecycle management (start/stop/status)
- Docker compose management

### `judo.sh build` flag reference

`./judo.sh build` accepts a set of single-letter flags whose semantics are non-obvious — several look like "only X" but actually mean "skip X". Inverting them is a common source of "my model change isn't taking effect" reports.

| Flag | Long form | Meaning |
|------|-----------|---------|
| `-M` | `--skip-model` | **Skip** the ESM→PSM→ASM→RDBMS→keycloak transformation. NOT "model only". Use when iterating on Java backend only. |
| `-B` | `--skip-backend` | Skip backend (custom ops + interceptors + REST). |
| `-F` | `--skip-frontend` | Skip frontend React generation/build. |
| `-KA` | `--skip-karaf` | Skip Karaf assembly. |
| `-S` | `--skip-schema` | Skip schema-migration image. |
| `-a` | `--build-app-module` | Build the `app/` (custom ops) module only — fast iteration on Java code. The running application does not load it: `start` unpacks the `karaf-offline` package again, so after Java changes run `./judo.sh build -M -F` (backend and Karaf package, skipping model and frontend) before `./judo.sh start`. |
| `-f` | `--build-frontend-module` | Build the frontend React module only. The Karaf package is not rebuilt, so a running application keeps serving the old frontend: after a frontend change that a running application must show, run `./judo.sh build` (no flags, rebuilds Karaf) and restart with `./judo.sh start`. |
| `-sc` | `--build-schema-cli` | Build the standalone schema CLI JAR. |
| `-d` | `--docker` | Build Docker images. |
| `-p` | `--build-parallel` | Maven parallel build (noisier logs). |
| `-q` | `--quick` | Quick mode — use cache, skip validations. |
| `-i` | `--ignore-checksum` | Ignore generator checksum errors and refresh checksums. |

`-KA` (skip Karaf) does not rebuild the `karaf-offline` package. `./judo.sh start` re-extracts that package on every start, so `build -F -KA` after Java changes leaves the running backend on the old custom operations. Drop `-KA` before `start`.

**Model-only changes need a full `./judo.sh build` (no flags) — not `-M`.** The `asm2keycloak` transformation (which emits the Keycloak realm from your `ActorType`s) only runs when model build is enabled. With `-M` the previous build's Keycloak realm artifact sticks and a new actor / claim / realm-name change never reaches Keycloak; the local stack starts but the React app shows blank and `/system/health` reports `JaxRsApplicationsReady` missing because the Keycloak adapter cannot find a realm matching `schema_name`.

### Local-dev Keycloak realm dependency

Projects generated from the JUDO platform ship a helper script `bin/keycloak-disable-ssl-required.sh` (invoked in the background by `./judo.sh start_local_env` right after `start_keycloak`). It:

1. logs into the Keycloak `master` realm as `admin`/`judo`,
2. flips `sslRequired=NONE` on `master` (so further admin calls work over plain HTTP from Karaf),
3. waits up to 180s for a realm named **exactly** `<schema_name>` (from `judo.properties`) to appear,
4. when it does, flips `sslRequired=NONE` on that realm too,
5. logs `WARNING: app realm '<schema_name>' did not appear within 180s; skipping` if it never shows.

The app realm's name is `ActorType.realm` emitted verbatim by `asm2keycloak` as `<keycloak:Realm id="<realm>" realm="<realm>">`. `ActorType.realm` has `defaultValueLiteral="DEFAULT"` in `esm.ecore`, so an actor without an explicit `realm` (or with `realm="DEFAULT"` literally) produces a Keycloak realm named `DEFAULT` — which will never match `schema_name` and triggers the 180s wait + give-up. The realm stays at `sslRequired=external`, and the React app silently fails because `/.well-known/openid-configuration` returns 403 over plain HTTP.

**Authoring rule:** always set `ActorType.realm = <schema_name>` (the value in `judo.properties`). Every analyzed project that ships a working local stack does this.

### Quick Reference Commands

```bash
# Build from scratch
./judo.sh build

# Build and start
./judo.sh build start

# Stop services
./judo.sh stop

# Check status
./judo.sh status

# Fast iteration mode
./judo.sh reckless

# Clean everything
./judo.sh clean

# Prune untracked files (DESTRUCTIVE - see warning below)
./judo.sh prune          # prunes the whole repo working tree
./judo.sh prune -f       # prunes frontend-react/ only
./judo.sh prune -y       # skip confirmation prompt (DANGEROUS)

# View help
./judo.sh --help
```

### Command Reference

`./judo.sh COMMANDS... [OPTIONS...]` - several commands can be chained (`./judo.sh build clean start`).

| Command | Purpose |
|---------|---------|
| `env <env>` | Use an alternate custom properties file (default `judo.properties`), e.g. `./judo.sh env compose-dev build start` |
| `clean` | Stop the PostgreSQL container and clear its data |
| `prune` (`-f`, `-y`) | Delete untracked files (see warning below) |
| `update` (`-i`) | Update dependency versions in the JUDO project |
| `generate` (`-i`) | Regenerate the application from the model (`-DgenerateApplication -DskipApplicationBuild`) |
| `generate-root` (`-i`) | Regenerate the application root structure (`-DgenerateRoot`) |
| `dump` | Dump PostgreSQL data before clearing and starting |
| `import` (`-dn <name>`) | Import a dump; without a name the last one is loaded |
| `schema-upgrade` | Persistent PostgreSQL only: generates the difference against the running database and applies it |
| `build` | Build the project (options below) |
| `reckless` | Build and run as fast as possible (skips validation and Docker) |
| `start` | Run the application with PostgreSQL and Keycloak |
| `stop` | Stop application, PostgreSQL and Keycloak |
| `status` | Print the status of the containers |

> **`schema-upgrade` is one step.** It generates the difference and applies it immediately, so a hand-written backfill changeset cannot be inserted between generation and execution. Do not use `schema-upgrade` when a backfill is needed.

**`build` options:** `-v <version>` (model and application version), `-p` (parallel), `-a` (app module only), `-f` (frontend module only), `-sc` (build the schema CLI standalone JAR), `-d` / `--docker` (build Docker images), `-M` (skip model), `-B` (skip backend), `-F` (skip frontend), `-KA` (skip Karaf), `-S` (skip schema migration image), `-ma <arg>` (extra Maven argument), `-q` (quick: cache, no validation), `-i` (ignore checksum errors, regenerate and update checksums).

**`start` options:** `-w` (do not watch bundle changes; long form `--skip-watch-bundles`; `-W` is not parsed), `-K` (skip Keycloak), `-o "<name>=<value>,..."` with:

| Option | Values |
|--------|--------|
| `runtime` | `karaf` \| `compose` |
| `dbtype` | `hsqldb` \| `postgresql` |
| `compose_env` | `compose-develop` \| `compose-postgresql-https` \| any directory under the model's `doc` directory |
| `model_dir` | model project directory (default: the application's parent) |
| `karaf_port`, `postgres_port`, `keycloak_port` | port overrides (Karaf HTTP default **8181**) |
| `compose_access_ip` | alternate IP used to access the app |
| `karaf_enable_admin_user` | `1` enables the Karaf admin user |
| `java_compiler` | `ejc` \| `javac`; not read by `judo.sh` (the help text lists it), so it has no effect |

Defaults for the options can be placed in `judo.properties` (or the properties file chosen with `env`).

> **`judo.sh` has no `-D` pass-through.** Use `-d` / `--docker` to build Docker images and `-ma "<arg>"` for extra Maven arguments. Docker profiles activate on `!skipDocker`, so defining `-DskipDocker` in any form (even `=false`) **disables** Docker.  Without `-d`, `judo.sh build` itself passes `-DskipDocker -DskipSchemaDocker`, and `reckless` skips Docker builds.

### ⚠️ Prune (Destructive) — Read Before Running

`./judo.sh prune` runs `git clean` against the working tree and **permanently deletes every file that is not tracked by git**. There is no undo.

| Variant | What it deletes |
|---------|-----------------|
| `./judo.sh prune` | All untracked files in the whole repository |
| `./judo.sh prune -f` | All untracked files inside `application/frontend-react/` |
| `./judo.sh prune -y` | Same as above but skips the `[Y/n]` confirmation |

Without `-y`, the `[Y/n]` prompt continues only for an exact `Y`; Enter, `y` and any other input abort (`Aborting prune.`, exit 13).

**What gets wiped that you likely care about:**

- Custom frontend code that has not yet been committed (Pandino hooks, theme overrides, custom components, i18n overrides under `frontend-react/<app>/src/custom/**`, `.../theme/**`, `.../i18n/**`).
- Any scratch files, notes, screenshots, or locally generated artifacts in the working tree (for the bare `prune` variant).
- `node_modules/`, generator caches, and other untracked build output — this is the *intended* use case.

**Mandatory safety checklist before running `prune` / `prune -f`:**

1. `git status` — confirm every custom file you want to keep is either tracked or intentionally disposable.
2. `git stash -u` (or `git add` + commit) any untracked customizations you want to preserve.
3. Prefer `./judo.sh prune` (interactive) over `./judo.sh prune -y`. Never chain `-y` in an automated agent workflow unless the working tree is verified clean first.
4. For agents: treat `prune -y` as equivalent to `rm -rf` on customer code. Require explicit human confirmation.

**When `prune -f` is actually the right tool:**

- The JUDO designer freezes on opening the model project (stale generated frontend state).
- After major model refactors where generator output layout changed (e.g. actor renamed) and stale per-actor dirs need to disappear.
- As the first step of a fully clean rebuild: `./judo.sh prune -f && ./judo.sh build -i`.

`./judo.sh clean` does not delete untracked files, but it is not a generator-cache clear either: it stops the PostgreSQL container and clears its data (see the command table).

## Frontend Build Recovery

When `./judo.sh build -i` fails in the frontend reactor (typically after model or OpenSpec-driven changes, for example `TS2307 Cannot find module ~/services/data-axios/...`), delete the generated folders of the `frontend-react` module - `src/pages/`, `src/dialog/`, `src/containers/` and `src/services/` - and run `./judo.sh build -i` again; the generator recreates them. Re-running the build alone is not enough in this case.

After renaming a transfer object, container or page, the generated names derived from it change: customization component names and interface keys (`<ContainerComponentName>...Component`, upper-snake `..._INTERFACE_KEY`), page and dialog folders. Rename the matching custom files and constants by hand, delete the stale generated `src/pages/`, `src/dialog/`, `src/containers/` and `src/services/` folders, then run `./judo.sh build -i`.

**Known issue: UI validation errors print as `{}: {}`.** The UI validation step logs through `StringBuilderLogger`, which formats messages with `String.format`. Slf4j-style `{}` placeholders are not replaced, so each failing UI constraint is logged as the bare line `{}: {}` with no constraint name or message. The Java validator path (`UiJavaValidator`) logs this way; the build reaches it when the Epsilon UI executor cannot be loaded, and then logs `Validator class ... not found. Using fallback.` Workaround: run `judo-cli -m <model-path> validate`, which prints each UI finding as `error ui <constraint> <element>: <message>`, and fix the reported constraints. Platform fix: format the placeholders in `StringBuilderLogger` the way slf4j does.

## Stale Artifacts and Multi-Module Build Order

- A JUDO application is a Maven reactor (model, schema, sdk, internal, app, common). The SDK POM is regenerated at `generate-sources` **from the installed model jar in `~/.m2`**, not from the edited model source, so a stale installed jar poisons the whole chain. Building `sdk` standalone fails with `Could not collect dependencies` until model and schema are installed; then use `-pl` with `-o` and `validateModels=false`.
- Tests can pass while the installed SNAPSHOT jars are stale (and `mvnd` can print `BUILD SUCCESS` while installing stale jars). Always rebuild with `./judo.sh build -i` (forces regeneration, ignoring checksums - hand edits not covered by `.generator-ignore` are lost) and verify the installed jar content with `unzip -l` / `javap` rather than jar timestamps. Working in two parallel copies of a repository is a common cause of such confusion.
- Additive model changes (a new stored attribute) need **no** manual migration step: the generated Liquibase changelog (`<app>-liquibase_postgresql.changelog.xml` under `application/model/target/generated-resources/model/`) already contains the new column. See [Schema Evolution](./schema-evolution.md#when-no-manual-step-is-needed).
- Do **not** run the `initdatatests` as part of the baseline build; they are very long and only needed when the init data changes.

## Multi-Repository Development (platform changes)

A runtime change can span several repositories (`judo-runtime-core`, `judo-platform`, `osgi-filestore`) plus the application. Create matching feature branches, build bottom-up (runtime-core, install the snapshot into `~/.m2`, then platform pins the new runtime-core, then the application pins the platform) and update the versions in **both** `application/pom.xml` and `judo-version.properties`. The `judo-versions` repository holds the real versions in its `pom.xml` `<properties>`; `src/main/resources/versions.properties` only contains `${}` placeholders. Before merging verify that the feature commit is an ancestor of the develop build and that the new artifact is really in the assembled `karaf-offline` zip or Docker image. `./judo.sh update` refreshes the pinned versions.

## Creating a New Project from the ESM Fullstack Template

The template (`judo-esm-fullstack-project-template`) has the modules `-root`, `-application`, `-common` and `-test`. The root module's resources contain `pom.xml.hbs`, `judo.sh.hbs`, `generator-parameter.properties.hbs`, `AGENTS.md.hbs`, `README.adoc.hbs` and the `pom.xml.*.fragment.hbs` files. To start a project:

1. Place the model at `model/<app>.model` and generate the project with the `create-judo-project` goal of `judo-version-updater-maven-plugin` (parameters `-DmodelName`, `-DprojectGroupId`, `-DprojectArtifactId`, `-DprojectVersion`, `-Dversion`). The plugin's groupId is `hu.blackbelt.judo`; its version selects the template version, so take the plugin version and `-Dversion` from the target JUDO versions rather than from whatever is cached in `~/.m2`.
2. The root POM has a `generate-root` execution with `synchronizeGitignore` (`esm=${basedir}/model/<app>.model`, ignored files `pom.xml`, `**/pom.xml`, `judo.sh`, `.mvn/jvm.config`). When adopting generated output into a repository that already has its own `.gitignore`, copy only the generated files and keep the managed `# JUDO GENERATOR BLOCK` in `.gitignore`; overwriting the tracked file wholesale makes `generate-root` stop with a manual-changes error.
3. Add a `<server>` with the id `<app>-distribution` to `~/.m2/settings.xml` if you deploy artifacts.
4. Run `./judo.sh build`; Docker must be installed (the local database and Keycloak run in containers).

The version updater goals read the update channel from `-Djudo-version-update-channel=<channel>` (default `develop`); `-DupdateChannel` does not bind. The repository server id comes from `-Djudo-version-rules-serverId=<id>` (default `serverId`); `-DserverId` does not bind.

## Toolchain Bootstrap and Versions

Node and pnpm versions are template parameters (defaults `node-version` 24.13.1, `pnpm-version` 10.15.0, `frontend-maven-plugin` 1.12.1; Maven properties `nodeVersion` / `pnpmVersion` override them). The `prepare-nodejs` profile runs `install-node-and-pnpm` into `${maven.multiModuleProjectDirectory}/.nodejs`, so the frontend and e2e modules need no pre-installed Node.

## Docker Image Build

The `docker` module builds one image tar per architecture with `jib-maven-plugin` 3.3.2 (profiles `x86_64`, `amd64`, `arm64`), writing `target/<artifactId>-<version>_docker_image_<arch>.tar` on the base image `azul/zulu-openjdk-debian:21-latest`. Tags come from the property `DOCKER_IMAGE_TAGS` (default `dev`). JMX exporter, Elastic APM and New Relic agents are added only when the template variables `dockerPrometheusJmxExporterAgentVersion`, `dockerElasticApmAgentVersion` and `dockerNewrelicAgentVersion` are set. The entrypoint runs `/<name>/bin/karaf run clean`, the exposed ports are 8181, 8081, 1099, 44444, 5000, 9090 and 5005, `/<name>/deploy` and `/<name>/data` are volumes, and files in `${project.basedir}/overrided` are copied into the image.

## Eclipse Launch Configurations

The template ships Eclipse m2e launchers: `BuildApplication.launch` (clean install of `application`), `BuildApplicationWithoutFrontend.launch` (adds `-DskipDocker=true -DskipFrontend=true`), `CompileCustomApp.launch` (clean install of `application/app`), `RunApplication.launch` (starts the backend from `application/karaf-offline` with `-DrunKaraf=true`) and `RunFrontend.launch` (profile `react-build`, `-DskipDist=true -DrunServer=true`, from `application/frontend`).

## Template Agent-Docs Placeholders

The generated agent-docs are Handlebars templates in the project template. They use only `docLink`/`localHubLink` helpers (defined in `EsmProjectHelper`, `judo-esm-fullstack-project-template-common`), a lower-case model-name expression and a model-name expression; literal double braces are escaped with a backslash. `docLink` becomes `[text](path)` and `localHubLink` becomes `[text](./README.md)`. Code constructs like `#if`/`#each` inside docs are examples only.

## Maven Commands

### Essential Maven Commands

```bash
# Full build
mvn clean install

# Build specific profiles
mvn clean install -DskipFrontendReact  # Skip frontend
mvn clean install -DskipDocker         # Skip Docker
mvn clean install -DskipSchema         # Skip schema

# Build single module
cd application/app
mvn clean install

# Parallel build
mvn clean install -T 4                 # 4 threads
```

## Build Profiles

Control what gets built using Maven profiles:

### Available Profiles

| Profile | Description | Skip Flag | Default |
|---------|-------------|-----------|---------|
| `build-model` | Backend model transformation (ESM→PSM→ASM) | `-DskipBackendModels` | Enabled |
| `build-schema` | Database schema evolution scripts | `-DskipSchema` | Enabled |
| `build-sdk` | Java SDK API generation | `-DskipSDK` | Enabled |
| `build-frontend-react` | React frontend generation and build | `-DskipFrontendReact` | Enabled |
| `build-karaf` | Karaf runtime assembly | `-DskipKaraf` | Enabled |
| `build-docker` | Docker image creation | `-DskipDocker` | Enabled |

### Usage Examples

```bash
# Backend only (no frontend)
mvn clean install -DskipFrontendReact -DskipDocker

# Model changes only
mvn clean install -DskipFrontendReact -DskipKaraf -DskipDocker

# Everything except Docker
mvn clean install -DskipDocker
```

## Build Workflows

### Full Build Process

```bash
./judo.sh build
```

**Steps Executed:**
1. **Environment Check** - Verify Docker, Java, Maven
2. **Model Transformation**
   - Load `/model/<app>.model`
   - Generate ESM, PSM, ASM models
   - Create database schemas (see [Schema Evolution](./schema-evolution.md) for schema migration)
   - Generate expression models
3. **SDK Generation**
   - Create Java interfaces from ASM
   - Generate DAO and Service APIs
4. **Backend Compilation**
   - Compile SDK module
   - Compile custom operations (`app/`)
   - Compile interceptors
   - Compile REST endpoints
5. **Frontend Generation and Build**
   - Generate UI model from ESM
   - Generate React components
   - Run `pnpm install`
   - Run `pnpm build`
   - Package as JAR
6. **Karaf Assembly**
   - Collect all OSGi bundles
   - Create feature definitions
   - Assemble standalone distribution
7. **Docker Image** (optional)
   - Build container image
   - Include Karaf distribution

**Duration:**
- First build: 10-15 minutes
- Incremental: 3-5 minutes
- With cache: 1-2 minutes

### Incremental Build

Build only changed modules:

```bash
# Model changed
mvn clean install -pl application/model,application/sdk,application/rest

# Backend code changed
cd application/app
mvn install

# Frontend changed
cd application/frontend-react/<app>__[actor_fqn]
mvn install
```

### Reckless Mode

Fastest build for rapid iteration:

```bash
./judo.sh reckless
```

**What it does:**
- Enables Maven caching
- Disables validation
- Skips non-essential checks
- Uses incremental compilation

**Use for:**
- Rapid prototyping
- Frequent small changes
- Development iterations

**Don't use for:**
- Production builds
- Breaking changes
- Final testing

## Maven Configuration

### Distribution Repository

**Location:** `~/.m2/settings.xml`

```xml
<settings>
  <servers>
    <server>
      <id>[private-maven-repo]</id>
      <username>YOUR_USERNAME</username>
      <password>YOUR_PASSWORD</password>
    </server>
  </servers>
</settings>
```

### Memory Configuration

**Increase Maven memory for large builds:**

```bash
export MAVEN_OPTS="-Xmx4g"
```

## Troubleshooting

### Build Failures

#### "Model validation failed"

**Solution:**
- Check model file: `/model/<app>.model`
- Run: `mvn clean install -X` for detailed errors

#### "Could not resolve dependencies"

**Solution:**
- Check Maven settings: `~/.m2/settings.xml`
- Verify repository credentials
- Clear cache: `rm -rf ~/.m2/repository/hu/blackbelt`

#### "Frontend build failed"

**Solution:**
- Check Node.js version: `node --version` (should be 18+)
- Clear node_modules: `rm -rf node_modules && pnpm install`

#### "Out of memory"

**Solution:**
- Increase Maven memory: `export MAVEN_OPTS="-Xmx4g"`

### Duplicate type imports with a third actor (known issue)

A third actor can break the generated frontend build: `./judo.sh build` stops at `pnpm run format` (biome) with `Declarations inside of a import declaration may not have duplicates` (for example `import type { CsvFile, CsvFile, ... }`) when an operation has an input and an output of the same type. The template emits one import per entry of `getApiImportsForPage`, built from a `HashSet<ClassType>` that deduplicates by object identity, so two `ClassType` objects for one class produce duplicate lines. It appears with any third actor (human or system, anonymous or not) and disappears when the third actor is removed. A two-actor build right after a model switch (for example after leaving a branch with the third actor) can show the same error from a stale, mixed model; run `./judo.sh generate` and `./judo.sh build -i` again before blaming the actor count. Workaround: keep the frontend to two actors and route the extra operation through an existing actor.

## Best Practices

### Performance Optimization

1. **Parallel builds** - Use `-T` flag for Maven
   ```bash
   mvn clean install -T 4  # Use 4 threads
   ```

2. **Skip unnecessary profiles** - Don't build Docker in development
   ```bash
   mvn clean install -DskipDocker
   ```

3. **Cache dependencies** - Use local Maven mirror

### Development Workflow

1. **Use incremental builds** - Build only what changed
2. **Use reckless mode** - For rapid iteration
3. **Test before committing** - Full clean build

## Related Documentation

- [Local Development](./local-development.md) - Development environment and hot deployment
- [Production Deployment](./production.md) - Production build and deployment
- [Deployment Overview](./README.md) - Main deployment documentation
