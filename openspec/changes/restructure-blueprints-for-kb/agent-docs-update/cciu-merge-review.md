# cciu merge: agent-docs conflicts kept as ours, theirs for review

`origin/feature/cciu-model-patterns` (2a27d6a) was merged locally. For agent-docs, each file was merged three-way into `catalog/agent-docs/`. Where both sides changed the same lines, the **catalog version was kept** (it was verified against judo-ng in the sweep). The cciu text is listed below so it can be checked and applied where it adds verified knowledge.


## Result

- rejected: 42
- already-covered: 41
- applied in spirit: cciu was right that src/custom is NOT gitignored: 11
- applied: 5
- unverified: 1

The real fixes came from **checking**, not copying: cciu was right that `src/custom/` is not gitignored, which corrected 8 agent-docs and 17 entries. The Keycloak managed-realm sync and the principal back-link exclusivity were verified in judo-runtime-core and esm.ecore and restored. The two-way relation rules are real EVL constraints. cciu was wrong about `claimPrincipal` (does not exist), `getOperations()` returning strings, CLI lists being append-only, and `subThemes` on the customizer.

Status values: `open` (not reviewed), `applied`, `rejected` (with reason), `already-covered`.

## catalog/agent-docs/backend/architectural-patterns.md

### CM-001 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
2. **`self` is not in scope.** The actor has no `self`; always iterate from the entity with a lambda variable. This applies to actor **access getters** only. A derived member on a transfer object or entity (including the principal's transfer object) does have `self`, which is the instance it is evaluated on; see [advanced-modeling-patterns.md](../model/advanced-modeling-patterns.md).
````

</details>

cciu:

````markdown
2. **`self` is not in scope.** The actor has no `self`; always iterate from the entity with a lambda variable.
````

## catalog/agent-docs/backend/authentication-guide.md

### CM-002 (both changed) — applied (Keycloak managed-realm sync section restored; verified against judo-runtime-core-security UserManagedWrappedDao + KeycloakUserManager.getManagedActorOfPrincipal; skill links → kb links)

<details><summary>catalog (kept)</summary>

````markdown
> See [ACTOR vs PRINCIPAL vs USER](../model/advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables) for the full decision matrix and the silent-failure pitfall.
````

</details>

cciu:

````markdown
> See ACTOR vs PRINCIPAL vs USER (see `judo-model-docs` skill) for the full decision matrix and the silent-failure pitfall.

---

## Keycloak managed-realm sync — trigger surface

With `ActorType.managed=true`, the JUDO framework delegates CUD on the principal TO to Keycloak's managed realm (create / update / delete the realm user matching the row). The dispatcher injects this sync **only** when the DAO layer is invoked with the **principal TO's metadata**. Sync follows TO metadata, not the underlying entity.

Consequences:

-  Other TOs mapping the same principal entity (e.g., an admin user-management `UserTO`, a list `UserListTO`) do **NOT** auto-sync when their endpoints mutate the row. The entity row updates; the Keycloak realm user does not.
-  Multiple TOs CAN map the same principal entity. The metamodel allows it; only the `actorType` back-link is exclusive — at most ONE principal TO per actor. See *Principal back-link exclusivity* in accesspoint.md (see `judo-model-docs` skill) for why.
-  To get Keycloak sync from an admin user-management surface, write a custom operation on the admin TO that delegates through the **principal TO's DAO** (re-dispatch with principal-TO metadata). Direct CUD on admin TOs skips Keycloak.
-  Design rule: keep ONE lean principal TO that owns `actorType` AND framework-managed Keycloak sync. Use other mapped TOs for admin / list projections. Route admin mutations through a custom op calling the principal TO's DAO when realm sync is required; otherwise accept that admin TO mutations are DB-only.

See Managed-realm sync trigger and Principal back-link exclusivity in accesspoint.md (see `judo-model-docs` skill) for the authoritative metamodel-level treatment and the 2026-05-11 empirical validation on `compsych-letter-demo`.

For the canonical admin-surface shape and the custom-op delegation pattern that routes admin mutations through the principal TO's DAO, see `judo-blueprint/best-practices/backend/managed-actor-admin-pattern.md`.
````

### CM-003 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
> If the `ActorType` in your ESM is **mapped + `managed="true"` + has `<claims>`** (see [Mapped Managed Principal with Claim Mapping](../model/advanced-modeling-patterns.md#pattern-mapped-managed-principal-with-claim-mapping)), the JUDO runtime is *intended* to insert the principal row on first login and update it on every subsequent `#_principal` call, directly from the JWT claims declared in `<claims>`. In that intended case you do not need an `AuthenticationInterceptor` for the baseline insert.
````

</details>

cciu:

````markdown
> If the `ActorType` in your ESM is **mapped + `managed="true"` + has `<claims>`** (see Mapped Managed Principal with Claim Mapping (see `judo-model-docs` skill)), the JUDO runtime is *intended* to insert the principal row on first login and update it on every subsequent `#_principal` call, directly from the JWT claims declared in `<claims>`. In that intended case you do not need an `AuthenticationInterceptor` for the baseline insert.
````

### CM-004 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown

### Provisioning Interceptor Code
````

</details>

cciu:

````markdown
(removed)
````

## catalog/agent-docs/backend/custom-operations.md

### CM-005 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
<generated-root-package>.<app>.custom
````

</details>

cciu:

````markdown
<generated-root-package>.webshop.custom
````

### CM-006 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
application/app/src/main/java/<generated-root-package>/<app>/custom/
````

</details>

cciu:

````markdown
application/app/src/main/java/<generated-root-package>/webshop/custom/
````

### CM-007 (both changed) — rejected (example package name only; catalog example kept)

<details><summary>catalog (kept)</summary>

````markdown
**Concrete example (real project):** `hu.blackbelt.compsych.letter.compsychletter.custom/` — derived from the root package `hu.blackbelt.compsych.letter` plus the lower-cased model name `compsychletter` plus the fixed `.custom` suffix.
````

</details>

cciu:

````markdown
**Concrete example (real project):** `hu.blackbelt.webshop.webshop.custom/` — derived from the root package `hu.blackbelt.webshop` plus the lower-cased model name `webshop` plus the fixed `.custom` suffix.
````

### CM-008 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
> The build's `resetChecksum` goal periodically clears `application/app/src/main/java/.generated-files/`. After that the `.default` blueprints and the checksum registry are gone until the next full generator run — which can break incremental builds and make your `.generator-ignore` entries look orphaned.
````

</details>

cciu:

````markdown
> The build's `resetChecksum` goal periodically clears `application/app/src/main/java/.generated-files/`. After that the `.default` blueprints and the checksum registry are gone until the next full generator run — which can break incremental builds.
````

### CM-009 (both changed) — applied (catalog contradicted itself: line 39 already said no entry and linked a missing One Rule section; cciu One Rule restored, the "add .default to .generator-ignore" bullet removed)

<details><summary>catalog (kept)</summary>

````markdown
- ✅ Add the `.default` path (at its real generator-emitted location) to the root `.generator-ignore`.
````

</details>

cciu:

````markdown
- (No `.generator-ignore` entry — see One Rule section below.)

### `.generator-ignore` — One Rule

`.generator-ignore` uses `.gitignore`-style matching, scoped to generator output. Single purpose: stop the generator from re-emitting a file at path X because you have hand-edited that exact generated file in place. It is **not** a "this file is custom" marker, and it is **not** needed for files the generator never produces.

Three cases:

1. **Generator emits file at path X, and you hand-edit X in place.** → Add `X` to `.generator-ignore`. This is the only legitimate case. Example: `application/pom.xml`, `integration-test/pom.xml`.
2. **`.default` rename pattern** (custom operations, interceptors, validators). Generator emits `X.java.default`. Rename to `X.java` once, fill in the body. The generator re-emits `X.java.default` next round as a reference and never touches `X.java`. → `X.java` is OUTSIDE generator scope. **No entry needed.** Do NOT add `X.java.default` either — you want it to keep regenerating as a read-only reference.
3. **Brand-new hand-written file the generator never emits at that path** (new helper classes in fresh packages, new factories like `ExceptionUtils.java`). → OUTSIDE generator scope. **No entry needed.**

Adding purely-custom files or `.default` paths to `.generator-ignore` is noise; remove such entries.
````

## catalog/agent-docs/backend/error-handling-guide.md

### CM-010 (both changed) — rejected (catalog error-handling-guide already lists the runtime-core exceptions with constructors and per-project generated faults; cciu table presents GenericOperationErrorException/BusinessErrorException as fixed platform classes, which they are not)

<details><summary>catalog (kept)</summary>

````markdown
When you read an example that calls such a helper, translate it to the platform mechanism above (`new ValidationException(List<ValidationResult>)`, or a modeled fault).
````

</details>

cciu:

````markdown
### Exception Types

| Exception Type | When to Use | HTTP Status | Client-Side Effect |
| :--- | :--- | :--- | :--- |
| `ValidationException` | For input validation failures on specific fields, **and** for business-semantic failures carried via machine-code prefixes (see note below). | 400 | Field-level error messages are displayed. |
| `BusinessErrorException` | For modeled, type-safe business rule violations. | 422 | Can be caught by type for specific error handling. |
| `GenericOperationErrorException` | For general business rule violations not tied to a specific field. | 500 | A general error notification is shown to the user. |
| `NotFoundException` | When a required entity cannot be found in the database. | 404 | Standard "Not Found" handling. |
| `AccessDeniedException` | For permission or authorization failures. | 403 | Standard "Forbidden" handling. |
````

## catalog/agent-docs/backend/interceptors.md

### CM-011 (both changed) — rejected (judo-runtime-core-dispatcher OperationCallInterceptor: `Collection<EOperation> getOperations(AsmModel)`, `preCall(EOperation, Object)`; cciu `List<String> getOperations()` is wrong)

<details><summary>catalog (kept)</summary>

````markdown
    private AsmUtils asmUtils;                     // built from asmModel.getResourceSet()
    private List<EOperation> operations;

    @Override public String getName() { return getClass().getSimpleName(); }

    @Override public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (operations == null) {
            asmUtils = new AsmUtils(asmModel.getResourceSet());
            operations = Stream.of("<model>.services.MyTO#_getById",     // illustrative FQNs, see
                                   "<model>.services.MyTO#_query")        // "Operation FQN Format Reference"
                    .map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return operations;
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
            throws InterceptorCallBusinessException {
        Payload result = (Payload) returnPayload;      // list operations return a Collection<Payload>
````

</details>

cciu:

````markdown
    @Override public List<String> getOperations() {
        return List.of("<model>.services.MyTO._getById",
                       "<model>.services.MyTO._query");
    }
    @Override public Payload postCall(Payload result, ...) {
````

## catalog/agent-docs/deployment/build-process.md

### CM-012 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
#### Worked Example: Adding a Dependency
````

</details>

cciu:

````markdown
(removed)
````

### CM-013 (both changed) — rejected (escaped Handlebars wording; catalog form is the rendered-docs convention)

<details><summary>catalog (kept)</summary>

````markdown
Fragments are Handlebars templates, so you can use expression syntax and generator parameters (for example `\<app>`) inside them.

#### Available Fragment Extension Points

Every generated module (application root, app, interceptors, karaf-features, schema, e2e, web-root) has these empty stubs; a file with exactly that name in the override directory survives regeneration and needs no `.generator-ignore` entry.
````

</details>

cciu:

````markdown
Fragments are Handlebars templates, so you can use `{{ }}` expressions and generator parameters (for example `{{ lowerCase model.name }}`) inside them.
````

### CM-014 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
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

**`build` options:** `-v <version>` (model and application version), `-p` (parallel), `-a` (app module only), `-f` (frontend module only), `-sc` (build the schema CLI standalone JAR), `-d` / `--docker` (build Docker images), `-M` (skip model), `-B` (skip backend), `-F` (skip frontend), `-KA` (skip Karaf), `-S` (skip schema migration image), `-ma <arg>` (extra Maven argument), `-q` (quick: cache, no validation), `-i` (ignore checksum errors, regenerate and update checksums).

**`start` options:** `-W` (do not watch bundle changes), `-K` (skip Keycloak), `-o "<name>=<value>,..."` with:

| Option | Values |
|--------|--------|
| `runtime` | `karaf` \| `compose` |
| `dbtype` | `hsqldb` \| `postgresql` |
| `compose_env` | `compose-develop` \| `compose-postgresql-https` \| any directory under the model's `doc` directory |
| `model_dir` | model project directory (default: the application's parent) |
| `karaf_port`, `postgres_port`, `keycloak_port` | port overrides (Karaf HTTP default **8181**) |
| `compose_access_ip` | alternate IP used to access the app |
| `karaf_enable_admin_user` | `1` enables the Karaf admin user |
| `java_compiler` | `ejc` (default) \| `javac` |

Defaults for the options can be placed in `judo.properties` (or the properties file chosen with `env`).

> **`judo.sh` has no `-D` pass-through.** Use `-d` / `--docker` to build Docker images and `-ma "<arg>"` for extra Maven arguments. Docker profiles activate on `!skipDocker`, so defining `-DskipDocker` in any form (even `=false`) **disables** Docker.  Without `-d`, `judo.sh build` itself passes `-DskipDocker -DskipSchemaDocker`, and `reckless` skips Docker builds.
````

</details>

cciu:

````markdown
(removed)
````

### CM-015 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
## Frontend Build Recovery

When `./judo.sh build -i` fails in the frontend reactor (typically after model or OpenSpec-driven changes, for example `TS2307 Cannot find module ~/services/data-axios/...`), delete the generated folders of the `frontend-react` module - `src/pages/`, `src/dialog/`, `src/containers/` and `src/services/` - and run `./judo.sh build -i` again; the generator recreates them. Re-running the build alone is not enough in this case.

## Stale Artifacts and Multi-Module Build Order

- A JUDO application is a Maven reactor (model, schema, sdk, internal, app, common). The SDK POM is regenerated at `generate-sources` **from the installed model jar in `~/.m2`**, not from the edited model source, so a stale installed jar poisons the whole chain. Building `sdk` standalone fails with `Could not collect dependencies` until model and schema are installed; then use `-pl` with `-o` and `validateModels=false`.
- Tests can pass while the installed SNAPSHOT jars are stale (and `mvnd` can print `BUILD SUCCESS` while installing stale jars). Always rebuild with `./judo.sh build -i` (forces regeneration, ignoring checksums - hand edits not covered by `.generator-ignore` are lost) and verify the installed jar content with `unzip -l` / `javap` rather than jar timestamps. Working in two parallel copies of a repository is a common cause of such confusion.
- Additive model changes (a new stored attribute) need **no** manual migration step: the generated Liquibase changelog (`<app>-liquibase_postgresql.changelog.xml` under `application/model/target/generated-resources/model/`) already contains the new column. See [Schema Evolution](./schema-evolution.md#when-no-manual-step-is-needed).
- Do **not** run the `initdatatests` as part of the baseline build; they are very long and only needed when the init data changes.

## Multi-Repository Development (platform changes)

A runtime change can span several repositories (`judo-runtime-core`, `judo-platform`, `osgi-filestore`) plus the application. Create matching feature branches, build bottom-up (runtime-core, install the snapshot into `~/.m2`, then platform pins the new runtime-core, then the application pins the platform) and update the versions in **both** `application/pom.xml` and `judo-version.properties`. The `judo-versions` repository holds the real versions in its `pom.xml` `<properties>`; `src/main/resources/versions.properties` only contains `${}` placeholders. Before merging verify that the feature commit is an ancestor of the develop build and that the new artifact is really in the assembled `karaf-offline` zip or Docker image. `./judo.sh update` refreshes the pinned versions.

## Creating a New Project from the ESM Fullstack Template

The template (`judo-esm-fullstack-project-template`) has the modules `-root`, `-application`, `-common` and `-test`. The root module's resources contain `pom.xml.hbs`, `judo.sh.hbs`, `generator-parameter.properties.hbs`, `AGENTS.md.hbs`, `README.adoc.hbs` and the `pom.xml.*.fragment.hbs` files. To start a project:

1. Place the model at `model/<app>.model` and generate the project with the `create-judo-project` goal of `judo-version-updater-maven-plugin` (parameters `-DmodelName`, `-DprojectGroupId`, `-DprojectArtifactId`, `-DprojectVersion`, `-Dversion`).
2. The root POM has a `generate-root` execution with `synchronizeGitignore` (`esm=${basedir}/model/<app>.model`, ignored files `pom.xml`, `**/pom.xml`, `judo.sh`, `.mvn/jvm.config`).
3. Add a `<server>` with the id `<app>-distribution` to `~/.m2/settings.xml` if you deploy artifacts.
4. Run `./judo.sh build`; Docker must be installed (the local database and Keycloak run in containers).

## Toolchain Bootstrap and Versions

Node and pnpm versions are template parameters (defaults `node-version` 24.13.1, `pnpm-version` 10.15.0, `frontend-maven-plugin` 1.12.1; Maven properties `nodeVersion` / `pnpmVersion` override them). The `prepare-nodejs` profile runs `install-node-and-pnpm` into `${maven.multiModuleProjectDirectory}/.nodejs`, so the frontend and e2e modules need no pre-installed Node.

## Docker Image Build

The `docker` module builds one image tar per architecture with `jib-maven-plugin` 3.3.2 (profiles `x86_64`, `amd64`, `arm64`), writing `target/<artifactId>-<version>_docker_image_<arch>.tar` on the base image `azul/zulu-openjdk-debian:21-latest`. Tags come from the property `DOCKER_IMAGE_TAGS` (default `dev`). JMX exporter, Elastic APM and New Relic agents are added only when the template variables `dockerPrometheusJmxExporterAgentVersion`, `dockerElasticApmAgentVersion` and `dockerNewrelicAgentVersion` are set. The entrypoint runs `/<name>/bin/karaf run clean`, the exposed ports are 8181, 8081, 1099, 44444, 5000, 9090 and 5005, `/<name>/deploy` and `/<name>/data` are volumes, and files in `${project.basedir}/overrided` are copied into the image.

## Eclipse Launch Configurations

The template ships Eclipse m2e launchers: `BuildApplication.launch` (clean install of `application`), `BuildApplicationWithoutFrontend.launch` (adds `-DskipDocker=true -DskipFrontend=true`), `CompileCustomApp.launch` (clean install of `application/app`), `RunApplication.launch` (starts the backend from `application/karaf-offline` with `-DrunKaraf=true`) and `RunFrontend.launch` (profile `react-build`, `-DskipDist=true -DrunServer=true`, from `application/frontend`).

## Template Agent-Docs Placeholders

The generated agent-docs are Handlebars templates in the project template. They use only `docLink`/`localHubLink` helpers (defined in `EsmProjectHelper`, `judo-esm-fullstack-project-template-common`), a lower-case model-name expression and a model-name expression; literal double braces are escaped with a backslash. `docLink` becomes `[text](path)` and `localHubLink` becomes `[text](./README.md)`. Code constructs like `#if`/`#each` inside docs are examples only.
````

</details>

cciu:

````markdown
(removed)
````

## catalog/agent-docs/frontend/README.md

### CM-016 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
1. **Edit the generated file** with your changes (e.g., `src/containers/...`)
2. **Add to `.generator-ignore`** to protect it from regeneration
````

</details>

cciu:

````markdown
1. **Edit the generated file** with your changes (e.g., in `src/generated/`)
2. **Add to `.generator-ignore`** to protect it from regeneration. Only this case (case 1 below) belongs in `.generator-ignore`:
````

### CM-017 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
**Authoring vs customizing.** This skill covers **customizing the generated React frontend** (hooks, theming, i18n, overrides). The UI layout itself — Form / Table / View scaffolds on each `TransferObjectType`, the menu on each `ActorType` — is **authored in the ESM model**. For that, see the model skill's [UI Authoring Guide](../model/ui-authoring-guide.md).
````

</details>

cciu:

````markdown
**Authoring vs customizing.** This skill covers **customizing the generated React frontend** (hooks, theming, i18n, overrides). The UI layout itself — Form / Table / View scaffolds on each `TransferObjectType`, the menu on each `ActorType` — is **authored in the ESM model**. For that, see the model skill's UI Authoring Guide (see `judo-model-docs` skill).
````

### CM-018 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
# Option 1: Add the file to .generator-ignore (keep your changes)
echo "src/pages/MyPage.tsx" >> .generator-ignore
````

</details>

cciu:

````markdown
# Option 1: Add the file to .generator-ignore (keep your changes) — case 1 only
echo "src/generated/pages/MyPage.tsx" >> .generator-ignore
````

## catalog/agent-docs/frontend/advanced-patterns.md

### CM-019 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
**Rule of thumb**: each subsystem-specific dialog must be triggered ONLY by an explicit backend `code` value. HTTP status alone is not enough — a 500 can come from anywhere in the stack. If you want to show a generic "server error" dialog for unknown 5xx, add an `isGenericServerError` predicate and a separate `compsych.error.server.title` / `.message` i18n pair; do not reuse the converter dialog.
````

</details>

cciu:

````markdown
### Anti-pattern — do not blanket-classify generic 5xx as a specific subsystem fault

A **common bug** in custom interceptors: catching every HTTP 5xx and showing a domain-specific dialog (e.g. "Document converter is unavailable", "AI service is down"). This **masks unrelated server errors** and blames the wrong subsystem to the user.

**Wrong** — 5xx fall-through to a specific dialog:

```typescript
const isConverterUnavailable = (err: any, errors: ServerError[]): boolean => {
  const status = err?.response?.status;
  return (
    !!errors.find((e) => e.code === 'ConverterUnavailable') ||
    (typeof status === 'number' && status >= 500 && status < 600) // ← catch-all
  );
};

// Result: a NullPointerException in any unrelated operation → user sees
// "Document converter is unavailable".
```

**Right** — only attribute a subsystem dialog when the explicit backend code is present; let generic 5xx fall through to the framework default:

```typescript
const isExplicitConverterUnavailable = (errors: ServerError[]): boolean =>
  !!errors.find((e) => e.code === 'ConverterUnavailable');

shouldInterceptError: (error, opts) => {
  const errors = extractServerErrors(error);
  if (isKnownBusinessCode(errors)) return true;
  if (isHttpStatus(error, 403)) return true;
  if (isExplicitConverterUnavailable(errors)) return true;
  return false; // unrecognized 5xx → framework default handles it
},

interceptError: (error, opts) => {
  const errors = extractServerErrors(error);
  if (isExplicitConverterUnavailable(errors)) {
    openFaultDialog('converter', { title: '…', message: '…' });
    return;
  }
  // …other known codes…
},
```

**Rule of thumb**: each subsystem-specific dialog must be triggered ONLY by an explicit backend `code` value. HTTP status alone is not enough — a 500 can come from anywhere in the stack. If you want to show a generic "server error" dialog for unknown 5xx, add an `isGenericServerError` predicate and a separate `webshop.error.server.title` / `.message` i18n pair; do not reuse the converter dialog.
````

## catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md

### CM-020 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
Reserve `RelationColumn` for embedded relation tables inside detail screens where relation-navigation semantics are explicitly expected. See also [UI Authoring Guide — Pitfalls](../../model/ui-authoring-guide.md#14-pitfalls-and-validation-rules).
````

</details>

cciu:

````markdown
Reserve `RelationColumn` for embedded relation tables inside detail screens where relation-navigation semantics are explicitly expected. See also UI Authoring Guide — Pitfalls (see `judo-model-docs` skill).
````

### CM-021 (both changed) — rejected (skill-link wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
- [UI Element Behaviour Rules](../../model/esm_metamodel/ui-behaviour.md) - Conditional attribute rules and validation
- [ESM UI Package Reference](../../model/esm_metamodel/ui.md) - Complete UI element definitions
- [UI Authoring Guide](../../model/ui-authoring-guide.md) - Authoring playbook for ESM UI scaffolds
````

</details>

cciu:

````markdown
- UI Element Behaviour Rules (see `judo-model-docs` skill) - Conditional attribute rules and validation
- ESM UI Package Reference (see `judo-model-docs` skill) - Complete UI element definitions
- UI Authoring Guide (see `judo-model-docs` skill) - Authoring playbook for ESM UI scaffolds
````

## catalog/agent-docs/frontend/hooks/README.md

### CM-022 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
`src/custom/` is gitignored in the frontend module, so the copy is not touched by regeneration and needs no `.generator-ignore` entry. Do not edit the `.default` file itself; it is regenerated on every build.
````

</details>

cciu:

````markdown
**Advantages:**
- ✅ No file copying needed
- ✅ Generator updates blueprint without overwriting your changes
- ✅ Clear that file originated from template

#### Option 2: Remove .default Extension

```bash
# Copy/rename to remove .default
cp src/custom/application-customizer.tsx.default src/custom/application-customizer.tsx

# Case 1: now hand-editing the generator-emitted path in place — protect it.
# See "Understanding .generator-ignore" below for the rule.
echo "src/custom/application-customizer.tsx" >> .generator-ignore
````

### CM-023 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# Step 5: Test (src/custom/ is gitignored and not regenerated, no .generator-ignore entry needed)
cd application/frontend-react/<app>__[actor_fqn]
````

</details>

cciu:

````markdown
# Step 5: Protect custom hook
# No .generator-ignore entry — tableRowHighlighting.tsx is a brand-new hand-written
# file (case 3); the generator never emits this path.

# Step 6: Test
cd application/frontend-react/webshop__[actor_fqn]
````

### CM-024 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
**Add to .generator-ignore:**
- ✅ Generated files outside `src/custom/` that you **edited directly** (not preferred): theme files such as `src/theme/palette.ts`, generated containers
- ✅ Custom files you add outside `src/custom/` that collide with generated paths

**Don't add to .generator-ignore:**
- ❌ Anything under `src/custom/` (gitignored, never regenerated)
- ❌ `.default` scaffolds and generated files you have not modified
````

</details>

cciu:

````markdown
**Add to .generator-ignore (case 1 only):**
- ✅ Generator-emitted stubs that you hand-edit in place (e.g. `src/custom/application-customizer.tsx`)
- ✅ Generated files you must edit directly because no hook exists (e.g. files under `src/generated/`)

**Don't add to .generator-ignore:**
- ❌ `*.default` template files — keep them regenerating as references
- ❌ Brand-new hand-written files the generator never emits
- ❌ Files renamed away from `.default` — outside generator scope
````

### CM-025 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# Theme customizations edited by hand
src/theme/palette.ts
src/theme/typography.ts

# Directly edited generated files (not recommended)
# src/containers/Service/Users/Users_View_Edit/ServiceUsersView.tsx
````

</details>

cciu:

````markdown
# Case 1 only: paths the generator emits AND you hand-edit in place.

# Generator-emitted stub, hand-edited in place
src/custom/application-customizer.tsx

# Generator-emitted theme files, hand-edited in place
src/theme/palette.ts
src/theme/typography.ts

# Directly edited generated file (not recommended)
# src/generated/pages/CustomPage.tsx

# Do NOT list brand-new hand-written files — the generator never emits them.
# Do NOT list *.default — keep them regenerating as a reference.
````

### CM-026 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# ❌ Do not edit the .default file in place
````

</details>

cciu:

````markdown
# ⚠️ Acceptable. Per directive, the generator-emitted `application-customizer.tsx`
# (without .default) is a case-1 path: hand-edit it in place → add to .generator-ignore.
cp src/custom/application-customizer.tsx.default src/custom/application-customizer.tsx
echo "src/custom/application-customizer.tsx" >> .generator-ignore
````

## catalog/agent-docs/frontend/hooks/action-hooks.md

### CM-027 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# Nothing to do for files under src/custom/: the folder is gitignored and never regenerated.
````

</details>

cciu:

````markdown
# Apply the One Rule (see hooks/README.md → Understanding .generator-ignore).
# Brand-new hand-written files → NO .generator-ignore entry (case 3).
# Only add an entry if the generator emits a stub at that exact path AND you
# hand-edited it in place (case 1).
# Flag for human review: whether containerActions.tsx / pageActions.tsx /
# operationFlowManager.tsx are generator-emitted stubs in this template is
# unclear. Verify with:
#   find src/custom -name 'containerActions*' -o -name 'pageActions*' -o -name 'operationFlowManager*'
# after a clean generate; treat any .default match as case 2 (no entry, no .default in ignore).
````

## catalog/agent-docs/frontend/hooks/data-hooks.md

### CM-028 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
Files in `src/custom/` are gitignored in the frontend module and never regenerated, so no `.generator-ignore` entry is needed.
````

</details>

cciu:

````markdown
```bash
# Do NOT blindly add custom-hook paths to .generator-ignore. Apply the One Rule
# (see hooks/README.md → "Understanding .generator-ignore"):
#   - Brand-new hand-written file generator never emits at path → case 3, NO entry.
#   - Generator-emitted stub hand-edited in place                → case 1, add entry.
#   - .tsx.default rename pattern                                → case 2, NO entry
#     (and do NOT add the .default either).
# Flag for human review: unclear whether usePrincipal.tsx / useViewData.tsx are
# generator-emitted stubs in this template. Verify with:
#   find src/custom -name 'usePrincipal*' -o -name 'useViewData*'
# after a clean generate. Treat any .default as case 2; any non-.default emission as case 1.
```
````

## catalog/agent-docs/frontend/hooks/navigation-and-access.md

### CM-029 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# Nothing to do: src/custom/ is gitignored and never regenerated, no .generator-ignore entry is needed
````

</details>

cciu:

````markdown
# Apply the One Rule (see hooks/README.md → Understanding .generator-ignore).
# Brand-new hand-written files → NO .generator-ignore entry (case 3).
# Only add an entry if the generator emits a stub at that exact path AND it
# was hand-edited in place (case 1).
# Flag for human review: redirectService.tsx and AccessFilter.tsx generator-emit
# status unclear; AccessFilter.tsx under src/custom/components/ looks like a
# brand-new hand-written component (case 3, no entry).
````

## catalog/agent-docs/frontend/hooks/table-hooks.md

### CM-030 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
Files in `src/custom/` are gitignored and never regenerated, so no `.generator-ignore` entry is needed.
````

</details>

cciu:

````markdown
```bash
# Apply the One Rule (see hooks/README.md → Understanding .generator-ignore).
# tableRowHighlighting.tsx and EntityChartSidekick.tsx are brand-new hand-written
# files (case 3); the generator never emits these paths. NO .generator-ignore
# entry needed. Adding them is noise.
```
````

## catalog/agent-docs/frontend/hooks/validation-hooks.md

### CM-031 (both changed) — applied in spirit: cciu was right that src/custom is NOT gitignored (judo-ui-react-template ad0848bc actor/gitignore ignores only *.ts.default/*.tsx.default; ui-react.yaml generates application-customizer.tsx, index.tsx, custom-element-types.ts, interfaces.ts in src/custom). Catalog wording fixed in 8 agent-docs + 17 entries; claim-check pattern added. cciu text not copied (its project names and option lists are superseded)

<details><summary>catalog (kept)</summary>

````markdown
# Nothing to do: src/custom/ is gitignored and never regenerated, so no .generator-ignore entry is needed
````

</details>

cciu:

````markdown
# Apply the One Rule (see hooks/README.md → Understanding .generator-ignore).
# Brand-new hand-written file → NO .generator-ignore entry (case 3).
# Only add an entry if the generator emits a stub at this exact path AND it
# was hand-edited in place (case 1).
# Flag for human review: containerActions.tsx generator-emit status unclear.
````

## catalog/agent-docs/frontend/theming.md

### CM-032 (both changed) — rejected (catalog matches judo-ui-react-template SubThemeWrapper.tsx.hbs: a `SubThemeHook` service selected by the widget `subTheme` name; cciu `applicationCustomizer.subThemes` map does not exist in the template)

<details><summary>catalog (kept)</summary>

````markdown
2. **Component sub-themes (frontend)** — a `subTheme` name set on a widget in the UI model selects a registered `SubThemeHook` service that returns partial MUI overrides, applied via a nested `ThemeProvider`. Use this for per-card, per-view, per-table color variations.
````

</details>

cciu:

````markdown
2. **Component sub-themes (frontend)** — `applicationCustomizer.subThemes` maps generated component names to partial MUI themes, applied via a nested `ThemeProvider`. Use this for per-card, per-view, per-table color variations.
````

## catalog/agent-docs/integration-testing/access-and-derived-testing.md

### CM-033 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
title: Testing Access Rules and DERIVED Attributes
description: Integration-test patterns for Access.getterExpression and DERIVED attribute getters in JUDO models. Covers DAO-level derived projection, dispatcher-driven per-actor access scoping, and ACTOR-context-dependent derived getters.
name: judo-integration-testing-access-and-derived
````

</details>

cciu:

````markdown
name: judo-integration-testing-access-and-derived
description: Integration-test patterns for Access.getterExpression and DERIVED attribute getters in JUDO models. Covers DAO-level derived projection, dispatcher-driven per-actor access scoping, and ACTOR-context-dependent derived getters.
````

### CM-034 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
# Testing Access Rules and DERIVED Attributes

**[◄ Back to Integration Testing index](./README.md)**
````

</details>

cciu:

````markdown

# Testing Access Rules and DERIVED Attributes

**[◄ Back to Integration Testing index](./SKILL.md)**
````

### CM-035 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
*   **`managed=true` first-login auto-insert is not implemented in the current runtime** (see [Authentication Guide](../backend/authentication-guide.md)). For Pattern B and Pattern C the test must `dao.create(...)` the principal row itself before calling the dispatcher with a matching `JudoPrincipal`.
````

</details>

cciu:

````markdown
*   **`managed=true` first-login auto-insert is not implemented in the current runtime** (see Authentication Guide (see `judo-backend-docs` skill)). For Pattern B and Pattern C the test must `dao.create(...)` the principal row itself before calling the dispatcher with a matching `JudoPrincipal`.
````

### CM-036 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
        modelName = "<app>",
````

</details>

cciu:

````markdown
        modelName = "webshop",
````

### CM-037 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
That the JQL `getterExpression` of the `DERIVED` attribute parses, transforms, and evaluates against the entity row — catching the common authoring mistakes (wrong member name, missing `not`, wrong type, missing `!any()` at the tail of a singleton-typed expression).

### What this does NOT prove

That the value is correct under an authenticated actor context. If the getter expression contains `!getVariable("ACTOR", …)` switch to **Pattern C** — the variable resolver returns empty in the bare-DAO context, masking real bugs.

---

## Pattern B — Testing `Access.getterExpression` per actor via the Dispatcher
````

</details>

cciu:

````markdown
That the JQL `getterExpression` of the `DERIVED` attribute parses, transforms, and evaluates against the entity row \u2014 catching the common authoring mistakes (wrong member name, missing `not`, wrong type, missing `!any()` at the tail of a singleton-typed expression).

### What this does NOT prove

That the value is correct under an authenticated actor context. If the getter expression contains `!getVariable("ACTOR", …)` switch to **Pattern C** \u2014 the variable resolver returns empty in the bare-DAO context, masking real bugs.

---

## Pattern B \u2014 Testing `Access.getterExpression` per actor via the Dispatcher
````

### CM-038 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
1.  Seed the principal entity row via the entity DAO (since `managed=true` auto-insert is not implemented — see Limitations above).
````

</details>

cciu:

````markdown
1.  Seed the principal entity row via the entity DAO (since `managed=true` auto-insert is not implemented \u2014 see Limitations above).
````

### CM-039 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
        modelName = "<app>",
````

</details>

cciu:

````markdown
        modelName = "webshop",
````

### CM-040 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
            "<app>::accesspoint::GenericUser::orders::__get";
````

</details>

cciu:

````markdown
            "webshop::accesspoint::GenericUser::orders::__get";
````

### CM-041 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
*   Wrong attribute name in `getVariable("ACTOR", "...")` — returns empty results for everyone.
*   Wrong type in the typed prefix (`String!getVariable` vs `Boolean!getVariable`) — expression rejects at evaluation.
*   Forgetting `!any()` where the expression must terminate at a single instance.
*   Off-by-one membership bugs from a `!filter` predicate that doesn't match the intent.
*   `Access.upper`, `createable`, `updateable`, `deleteable` flag mismatches — the dispatcher rejects the operation with the access-point's permission semantics.

### What this does NOT prove

That the menu actually surfaces this access in the UI — that requires the paired `MenuItemAccess` and is an E2E concern. See [E2E Testing Guide](../e2e-testing/README.md).

---

## Pattern C — Testing DERIVED getters that depend on `ACTOR.*`

When a `DERIVED` attribute's getter references `!getVariable("ACTOR", "...")`, its value is per-request — it can only be evaluated when a principal is in scope. The plain DAO path used in Pattern A returns empty because the variable resolver has nothing to resolve.

The mechanics are the same as Pattern B: build a `JudoPrincipal`, put it in the exchange under `Dispatcher.PRINCIPAL_KEY`, and call the access-point query through the dispatcher. The difference is the assertion target — you read a `DERIVED` field off the *projected TO returned by the dispatcher response*, not a row count.
````

</details>

cciu:

````markdown
*   Wrong attribute name in `getVariable("ACTOR", "...")` \u2014 returns empty results for everyone.
*   Wrong type in the typed prefix (`String!getVariable` vs `Boolean!getVariable`) \u2014 expression rejects at evaluation.
*   Forgetting `!any()` where the expression must terminate at a single instance.
*   Off-by-one membership bugs from a `!filter` predicate that doesn't match the intent.
*   `Access.upper`, `createable`, `updateable`, `deleteable` flag mismatches \u2014 the dispatcher rejects the operation with the access-point's permission semantics.

### What this does NOT prove

That the menu actually surfaces this access in the UI \u2014 that requires the paired `MenuItemAccess` and is an E2E concern. See E2E Testing Guide (see `judo-e2e-testing-docs` skill).

---

## Pattern C \u2014 Testing DERIVED getters that depend on `ACTOR.*`

When a `DERIVED` attribute's getter references `!getVariable("ACTOR", "...")`, its value is per-request \u2014 it can only be evaluated when a principal is in scope. The plain DAO path used in Pattern A returns empty because the variable resolver has nothing to resolve.

The mechanics are the same as Pattern B: build a `JudoPrincipal`, put it in the exchange under `Dispatcher.PRINCIPAL_KEY`, and call the access-point query through the dispatcher. The difference is the assertion target \u2014 you read a `DERIVED` field off the *projected TO returned by the dispatcher response*, not a row count.
````

### CM-042 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
        modelName = "<app>",
````

</details>

cciu:

````markdown
        modelName = "webshop",
````

### CM-043 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
            "<app>::accesspoint::GenericUser::orders::__get",
````

</details>

cciu:

````markdown
            "webshop::accesspoint::GenericUser::orders::__get",
````

### CM-044 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
If you tried to assert `ownedByMe` via `orderDao.query().selectList()`, every row would come back with `ownedByMe = empty Optional` (or `false`, depending on coercion) regardless of the data, because there is no `__principal` in scope to populate `getVariable("ACTOR", "userName")`. The DAO test would either always fail or always trivially "pass" — neither catches the real bug. **Always route ACTOR-dependent derived getters through the dispatcher.**
````

</details>

cciu:

````markdown
If you tried to assert `ownedByMe` via `orderDao.query().selectList()`, every row would come back with `ownedByMe = empty Optional` (or `false`, depending on coercion) regardless of the data, because there is no `__principal` in scope to populate `getVariable("ACTOR", "userName")`. The DAO test would either always fail or always trivially "pass" \u2014 neither catches the real bug. **Always route ACTOR-dependent derived getters through the dispatcher.**
````

### CM-045 (both changed) — already-covered (same link; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
*   [Mocking VariableResolver for custom operations](./advanced-patterns.md#pattern-mocking-variableresolver-for-authentication) — the analogous pattern for *custom Java code* that calls `VariableResolver.resolve("ACTOR", …)` directly. Use that helper when the SUT is a custom operation implementation; use Patterns B and C here when the SUT is the JQL evaluation pipeline itself.
*   [Role Flags on the Principal Entity](../model/advanced-modeling-patterns.md#pattern-role-flags-on-the-principal-entity) — every model authored from that pattern should ship with the corresponding Pattern A (for the `isNotAdmin` mirror) and Pattern B (for the role-scoped access getter) tests.
*   [Three actor shapes](../model/esm_metamodel/accesspoint.md#three-actor-shapes-authoring-reference) — determines which of `USER` / `PRINCIPAL` / `ACTOR` is populated, and therefore which test patterns apply.
````

</details>

cciu:

````markdown
*   [Mocking VariableResolver for custom operations](./advanced-patterns.md#pattern-mocking-variableresolver-for-authentication) \u2014 the analogous pattern for *custom Java code* that calls `VariableResolver.resolve("ACTOR", …)` directly. Use that helper when the SUT is a custom operation implementation; use Patterns B and C here when the SUT is the JQL evaluation pipeline itself.
*   Role Flags on the Principal Entity (see `judo-model-docs` skill) \u2014 every model authored from that pattern should ship with the corresponding Pattern A (for the `isNotAdmin` mirror) and Pattern B (for the role-scoped access getter) tests.
*   Three actor shapes (see `judo-model-docs` skill) \u2014 determines which of `USER` / `PRINCIPAL` / `ACTOR` is populated, and therefore which test patterns apply.
````

## catalog/agent-docs/integration-testing/osgi-ds-descriptor-tests.md

### CM-046 (both changed) — rejected (cciu drops the kb frontmatter and links ./SKILL.md)

<details><summary>catalog (kept)</summary>

````markdown
---
title: Integration Testing - OSGi DS Descriptor Contract Tests
description: "Part of: Integration Testing Documentation(./README.md)"
---
# Integration Testing - OSGi DS Descriptor Contract Tests

**Part of**: [Integration Testing Documentation](./README.md)
````

</details>

cciu:

````markdown
# Integration Testing - OSGi DS Descriptor Contract Tests

**Part of**: [Integration Testing Documentation](./SKILL.md)
````

### CM-047 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
- [Back to Main Hub](./README.md)
````

</details>

cciu:

````markdown
- [Back to Main Hub](./SKILL.md)
````

### CM-048 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
application/app/target/<app><postfix>-app-<version>.jar
````

</details>

cciu:

````markdown
application/app/target/webshop-application-app-<version>.jar
````

### CM-049 (both changed) — already-covered (same paragraph; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
> **Orphaned-from-reactor build.** The `application/integration-test` module is intentionally not listed in `application/pom.xml`'s module tree; it is built standalone via `mvn -pl application/integration-test …` (or from the module directory). This is the established JUDO pattern (see <app>'s `application/test/` for a richer example) and is what lets the tests consume the already-packaged upstream app jar without creating a reactor cycle with the `package`-phase bundle plugin.

## Complete Example

Below is a self-contained descriptor contract test that asserts the `@Reference` field `myService` in two custom-operation classes (`OP_A`, `OP_B`), which both declare `target="(profile=${app.profile})"`. Adapt the resource paths, reference names, and expected filter to your project's invariants.

### Example Test Class

```java
package com.example.<app>.integration.dscomponent;
````

</details>

cciu:

````markdown
> **Orphaned-from-reactor build.** The `application/integration-test` module is intentionally not listed in `application/pom.xml`'s module tree; it is built standalone via `mvn -pl application/integration-test …` (or from the module directory). This is the established JUDO pattern (see rackinspect's `application/test/` for a richer example) and is what lets the tests consume the already-packaged upstream app jar without creating a reactor cycle with the `package`-phase bundle plugin.

## Complete Example

Below is a self-contained descriptor contract test that asserts four `@Reference` fields across four custom-operation classes all declare `target="(profile=${app.profile})"`. Adapt the resource paths, reference names, and expected filter to your project's invariants.

```java
package com.example.webshop.integration.dscomponent;
````

### CM-050 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
            "OSGI-INF/com.example.<app>.custom.….OperationACustomImplementation.xml";
    private static final String OP_B =
            "OSGI-INF/com.example.<app>.custom.….OperationBCustomImplementation.xml";
````

</details>

cciu:

````markdown
            "OSGI-INF/com.example.webshop.custom.….OperationACustomImplementation.xml";
    private static final String OP_B =
            "OSGI-INF/com.example.webshop.custom.….OperationBCustomImplementation.xml";
````

### CM-051 (both changed) — rejected (judo-runtime-core-guice-testkit JudoTest is meta-annotated @ExtendWith(JudoTestExtension.class); catalog wording is right, no extra @RegisterExtension needed)

<details><summary>catalog (kept)</summary>

````markdown
| Test annotation | `@JudoTest` (the annotation registers `JudoTestExtension` itself) | Plain `@Test` |
````

</details>

cciu:

````markdown
| Test annotation | `@JudoTest` (+ `@RegisterExtension JudoRuntimeExtension`) | Plain `@Test` |
````

## catalog/agent-docs/model/README.md

### CM-052 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
- **[JUDO Model CLI](judo-cli.md)**: The `judo-cli.jar` platform tool — the only sanctioned way to read or change the ESM. **Read this first if you have not used the CLI before.**
- **[Transformation Pipeline](transformation-pipeline.md)**: ESM → PSM → ASM → RDBMS → Liquibase, server-side vs client-side regeneration, and the in-memory state model.
````

</details>

cciu:

````markdown
(removed)
````

### CM-053 (both changed) — rejected (cciu links ./esm_metamodel/SKILL.md; catalog links README files)

<details><summary>catalog (kept)</summary>

````markdown
- **[Operation Script Language (JCL)](jcl-operation-scripts.md)**: Syntax and restrictions of operation bodies.
- **[JSL Language Rules](jsl-language-notes.md)**: Identifiers, built-in libraries, actor grammar and the rules that fail a build.
- **[Validation and Transformation Options](model-validation-and-transformation.md)**: EVL validation, ETL vs ZETA engines, Maven workflow, measures, known issues.
- **[ESM Metamodel](./esm_metamodel/README.md)**: Detailed breakdown of every component in `esm.ecore`.
````

</details>

cciu:

````markdown
- **[ESM Metamodel](./esm_metamodel/SKILL.md)**: Detailed breakdown of every component in `esm.ecore`.
````

### CM-054 (cciu adds) — rejected (cciu adds a YAML entity template; catalog entries never carry generator YAML, and the YAML format is project tooling)

<details><summary>catalog (kept)</summary>

````markdown

````

</details>

cciu:

````markdown

### Entity YAML Template

```yaml
name: Customer
namespace: webshop::entities
extends: AbstractEntity
crud:
  createable: true
  updateable: true
  deleteable: true
attributes:
  - name: email
    type: String
    cardinality: 0..1
relations:
  - name: orders
    target: Order
    cardinality: 0..*
    bidirectional: true
    opposite: customer
```
````

## catalog/agent-docs/model/advanced-modeling-patterns.md

### CM-055 (both changed) — unverified, not applied (realm = schema_name and the keycloak-disable-ssl-required.sh timeout: the script is not in the judo-ng clones; esm.ecore confirms only realm defaultValueLiteral="DEFAULT"). Candidate for passb2-doc-gaps B list

<details><summary>catalog (kept)</summary>

````markdown
#### Reading the persisted row in access getters

*   **Access getters then read the persisted row.** The JQL key is the `DataMember.name` on the principal TO, not the JWT claim name — the `<claims>` element is what links them. The example below uses `EMAIL`; swap in `USERNAME` — with an `<claims claimType="USERNAME">` pointing at a `userName` / `preferredUsername` member — if that is the identifier your IdP guarantees stable.
    ```jql
    // Root access: the User row for this actor (EMAIL-keyed variant)
    <app>::entities::User
      !filter(u | u.email == <app>::types::String!getVariable("ACTOR", "email"))
      !any()

    // USERNAME-keyed variant, same pattern
    <app>::entities::User
      !filter(u | u.userName == <app>::types::String!getVariable("ACTOR", "userName"))
      !any()
    ```
    This pairs naturally with the *Fully User-Scoped Data Access* pattern above: every other access is a navigation from this root.
#### Principal conventions and limits

*   **Principal TO conventions.** The TO used as `ActorType.principal` typically carries `createable="false" updateable="false" deleteable="false"` at the outer level (no public CRUD service — the framework owns the row) and `actorType="<ActorType.id>"` as the back-link. Individual `accesses[*]` inside the actor can still grant CRUD on other TOs, including a separate `users` access targeting the same entity for administrators.
*   **Extending beyond the automatic sync.** The model-driven sync only covers the declared `<claims>` attributes. When you need more — copying a custom claim to a plain entity attribute, initialising roles from a group claim, writing an audit row — add an `AuthenticationInterceptor` on `#_principal`; it runs **before** the framework's actor lookup. See [Authentication Guide](../backend/authentication-guide.md).
*   **Verified runtime gap (judo-runtime-core-dispatcher 1.0.6.20241030 / 1.0.6.20251205).** `DefaultActorResolver.getActorByClaims` is lookup-only — it calls `dao.search(actorType, …)` and throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. No insertion code path exists for `managed=true` actors in these versions. The `INFO` log `"Operation failed, authenticated entity not found in database"` on every first login is the symptom. **Mitigation:** add the *Just-in-Time User Provisioning* `AuthenticationInterceptor` from [the Authentication Guide](../backend/authentication-guide.md#example-just-in-time-user-provisioning), even for the textbook mapped + managed + `<claims>` shape. The interceptor's `authenticate()` hook runs **before** `getActorByClaims`, so inserting there satisfies the upcoming lookup.
````

</details>

cciu:

````markdown
    4.  **`ActorType.realm`** must be set to your `judo.properties` `schema_name`. In `esm.ecore` the attribute carries `defaultValueLiteral="DEFAULT"`, and `asm2keycloak` emits this value verbatim as the Keycloak `Realm.id` / `Realm.realm`. Leaving the default (or writing `realm="DEFAULT"` literally) produces a Keycloak realm named `DEFAULT`, which does NOT match `schema_name` and breaks the local-dev `bin/keycloak-disable-ssl-required.sh` wait (180s timeout, then the script gives up and the app realm keeps `sslRequired=external`). Pattern: `realm=<schema_name>` (every analyzed project that ships a working local stack uses this).
*   **Access getters then read the persisted row.** The JQL key is the `DataMember.name` on the principal TO, not the JWT claim name — the `<claims>` element is what links them. The example below uses `EMAIL`; swap in `USERNAME` — with an `<claims claimType="USERNAME">` pointing at a `userName` / `preferredUsername` member — if that is the identifier your IdP guarantees stable.
    ```jql
    // Root access: the User row for this actor (EMAIL-keyed variant)
    MyApp::entities::User
      !filter(u | u.email == MyApp::types::String!getVariable("ACTOR", "email"))
      !any()

    // USERNAME-keyed variant, same pattern
    MyApp::entities::User
      !filter(u | u.userName == MyApp::types::String!getVariable("ACTOR", "userName"))
      !any()
    ```
    This pairs naturally with the *Fully User-Scoped Data Access* pattern above: every other access is a navigation from this root.
*   **Principal TO conventions.** The TO used as `ActorType.principal` typically carries `createable="false" updateable="false" deleteable="false"` at the outer level (no public CRUD service — the framework owns the row) and `actorType="<ActorType.id>"` as the back-link. Individual `accesses[*]` inside the actor can still grant CRUD on other TOs, including a separate `users` access targeting the same entity for administrators.
*   **Principal TO is exclusive — one principal TO + N admin TOs on same entity.** `TransferObjectType.actorType` is the eOpposite of `ActorType.principal`. Single-valued on both sides. Only ONE TO per actor holds `actorType=<Actor>`. Setting `actorType` on a second TO mapping the same entity transparently reassigns `ActorType.principal` to it and clears the back-link on the previous TO. Cannot keep both a lean principal TO and a separate admin TO marked as principal. Other TOs mapping the same entity exist as plain mapped TOs without `actorType`. Empirical validation 2026-05-11 on `compsych-letter-demo` (`compsychletter::services::UserPrincipal` vs `compsychletter::services::UserTO`, actor `compsychletter::actors::LetterUser`) — see [Principal back-link exclusivity](./esm_metamodel/accesspoint.md#principal-back-link-exclusivity).
*   **Keycloak managed-realm sync follows principal TO metadata, not the entity.** With `managed=true`, the framework delegates CUD on the principal TO to Keycloak's managed realm. The dispatcher injects sync ONLY when the DAO layer is invoked with **principal TO metadata**. Other TOs mapping the same principal entity (admin user-management `UserTO`, list `UserListTO`, etc.) do NOT auto-sync — entity row updates; Keycloak realm user does not. To get Keycloak sync from an admin user-management surface, write a custom operation on the admin TO that re-dispatches through the **principal TO's DAO**. Direct CUD on admin TOs is DB-only. Design rule: ONE lean principal TO owns `actorType` AND framework-managed Keycloak sync; admin / list projections are separate mapped TOs on the same entity; route admin mutations through a custom op calling the principal TO's DAO when realm sync is required. See [Managed-realm sync trigger](./esm_metamodel/accesspoint.md#managed-realm-sync-trigger).
*   **Extending beyond the automatic sync.** The model-driven sync only covers the declared `<claims>` attributes. When you need more — copying a custom claim to a plain entity attribute, initialising roles from a group claim, writing an audit row — add an `AuthenticationInterceptor` on `#_principal`; it runs **before** the framework's actor lookup. See Authentication Guide (see `judo-backend-docs` skill).
*   **Canonical admin-surface specialization.** For an admin user-management surface on top of this pattern (read-only access + custom ops + principal-DAO routing for Keycloak realm sync), the canonical recipe combining Findings on `actorType` back-link exclusivity, managed-realm sync trigger, path-agnostic outer CRUD, and the capability ladder is documented in `judo-blueprint/best-practices/backend/managed-actor-admin-pattern.md`.
*   **Verified runtime gap (judo-runtime-core-dispatcher 1.0.6.20241030 / 1.0.6.20251205 / 1.0.6.20260313).** `DefaultActorResolver.getActorByClaims` is lookup-only — it calls `dao.search(actorType, …)` and throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. No insertion code path exists for `managed=true` actors in these versions. The `INFO` log `"Operation failed, authenticated entity not found in database"` on every first login is the symptom. Reproduced 2026-05-11 on `compsych-letter-demo` against `compsych-letter-framework`'s actor shape: `GET /api/<schema>/actors/<Actor>/actors/<Actor>/~principal` returns HTTP 403 with body `{"code":"AUTHENTICATED_ENTITY_NOT_FOUND","level":"ERROR","details":{"ACTOR":"<fqn>"}}` on the first call; after `INSERT INTO t_entities_user (…)` by hand the next call returns 200 with the principal projection. **Mitigation:** add the *Just-in-Time User Provisioning* `AuthenticationInterceptor` from the Authentication Guide (see `judo-backend-docs` skill), even for the textbook mapped + managed + `<claims>` shape. The interceptor's `authenticate()` hook runs **before** `getActorByClaims`, so inserting there satisfies the upcoming lookup. Reference implementation: `com.compsych.letterframework.auth.CompsychAuthInterceptor` in compsych-letter-framework, paralleling `LogAuthenticationInterceptor` in alba / mlszksz-platform / ubives / park-here / indamedia-adtrack (see `best-practices/backend/keycloak-jit-user-provisioning.md`).
````

### CM-056 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
#### Reading the role flag in JQL
````

</details>

cciu:

````markdown
(removed)
````

### CM-057 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
    <app>::types::Boolean!getVariable("ACTOR", "isAdmin")
````

</details>

cciu:

````markdown
    MyApp::types::Boolean!getVariable("ACTOR", "isAdmin")
````

### CM-058 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
*   **Fallback form** when the `ACTOR` category is **not** available (e.g., an actor without a mapped principal / `managed=true`, where only `USER` is populated). Re-derive the user row from a JWT claim, then test the flag:
````

</details>

cciu:

````markdown
*   **Fallback form** when the `ACTOR` category is **not** available (e.g., a `claimPrincipal: true` actor without `<claims>` / `managed=true`, where only `USER` is populated). Re-derive the user row from a JWT claim, then test the flag:
````

### CM-059 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
    <app>::entities::User
      !filter(u | u.userName == <app>::types::String!getVariable("USER", "userName")
````

</details>

cciu:

````markdown
    MyApp::entities::User
      !filter(u | u.userName == MyApp::types::String!getVariable("USER", "userName")
````

### CM-060 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
#### Role-scoped access getters

*   **Wiring the flag into an `Access.getterExpression`** (admin sees all rows; non-admin sees only their own). JQL has no `if/then/else` operator — use a single `!filter` whose lambda disjuncts the role flag with the per-user clause. The `!getVariable("ACTOR", "isAdmin")` call is constant per request, so when it returns `true` the predicate admits every row:

    ```jql
    <app>::entities::Order!filter(o |
      <app>::types::Boolean!getVariable("ACTOR", "isAdmin")
      or o.owner.userName == <app>::types::String!getVariable("ACTOR", "userName"))
    ```

#### Hiding menu items by role

*   **Wiring the flag into a `hiddenBy` on a `MenuItemAccess`.** `hiddenBy` must reference a **boolean `DataMember` on the principal TO** (see [UI Authoring Guide, section 5 (data-binding cheat sheet)](./ui-authoring-guide.md#5-data-binding-cheat-sheet)). Since `hiddenBy` hides when *true*, model the negation as a derived attribute on the principal TO itself — inside that getter `self` already **is** the actor's row, so no `!getVariable` call is needed:
````

</details>

cciu:

````markdown
*   **Wiring the flag into an `Access.getterExpression`** (admin sees all rows; non-admin sees only their own). JQL has no `if/then/else` operator — use a single `!filter` whose lambda disjuncts the role flag with the per-user clause. The `!getVariable("ACTOR", "isAdmin")` call is constant per request, so when it returns `true` the predicate admits every row:

    ```jql
    MyApp::entities::Order!filter(o |
      MyApp::types::Boolean!getVariable("ACTOR", "isAdmin")
      or o.owner.userName == MyApp::types::String!getVariable("ACTOR", "userName"))
    ```

*   **Wiring the flag into a `hiddenBy` on a `MenuItemAccess`.** `hiddenBy` must reference a **boolean `DataMember` on the principal TO** (see [UI Authoring Guide §6](./ui-authoring-guide.md)). Since `hiddenBy` hides when *true*, model the negation as a derived attribute on the principal TO itself — inside that getter `self` already **is** the actor's row, so no `!getVariable` call is needed:
````

### CM-061 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
*   **Testing**. Every site this pattern produces has a corresponding integration-test recipe: the `isNotAdmin` derived mirror is covered by Pattern A (DAO projection), the role-scoped `Access.getterExpression` by Pattern B (dispatcher with a `JudoPrincipal`), and any `ownedByMe`-style derived flag by Pattern C. See [Testing Access Rules and DERIVED Attributes](../integration-testing/access-and-derived-testing.md).
````

</details>

cciu:

````markdown
*   **Testing**. Every site this pattern produces has a corresponding integration-test recipe: the `isNotAdmin` derived mirror is covered by Pattern A (DAO projection), the role-scoped `Access.getterExpression` by Pattern B (dispatcher with a `JudoPrincipal`), and any `ownedByMe`-style derived flag by Pattern C. See Testing Access Rules and DERIVED Attributes (see `judo-integration-testing-docs` skill).
````

### CM-062 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
    *   The `Actor` is token-only (it has no `principal` TO and no persisted principal record).
    *   You want the **raw JWT claim** regardless of actor shape (e.g. `sub`, `email`, a custom scope claim).
    *   This category reads the raw token claims for every actor shape, and it is the only one that works for token-only actors — `PRINCIPAL.*` against such an actor silently returns empty.

*   **Use `!getVariable('PRINCIPAL', 'claim_name')` when:**
    *   Your user representation is **stateless and transient** via a framework-populated principal TO.
    *   The `Actor`'s `principal` is an **unmapped `TransferObjectType`**.
````

</details>

cciu:

````markdown
    *   The `Actor` is declared with **`claimPrincipal: true`** (token-only actor; no persisted principal record).
    *   You want the **raw JWT claim** regardless of actor shape (e.g. `sub`, `email`, a custom scope claim).
    *   This is the **only** category that surfaces JWT claims for `claimPrincipal: true` actors — `PRINCIPAL.*` against such an actor silently returns empty.

*   **Use `!getVariable('PRINCIPAL', 'claim_name')` when:**
    *   Your user representation is **stateless and transient** via a framework-populated principal TO.
    *   The `Actor`'s `principal` is an **unmapped `TransferObjectType`** and the actor is **not** `claimPrincipal: true`.
````

### CM-063 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
> Access `Derived` filters and custom-op helpers that reference `PRINCIPAL.*` on a token-only actor (no `principal` TO) compile and deploy, but evaluate to empty at runtime. Symptoms: empty result sets, `null` audit-user fields, or "access denied" despite valid tokens. Fix by switching those call sites to `USER.*`. Audit every access-filter and interceptor whenever an actor gains or loses its `principal` TO.
````

</details>

cciu:

````markdown
> Access `Derived` filters and custom-op helpers that reference `PRINCIPAL.*` on a `claimPrincipal: true` actor compile and deploy, but evaluate to empty at runtime. Symptoms: empty result sets, `null` audit-user fields, or "access denied" despite valid tokens. Fix by switching those call sites to `USER.*`. Audit every access-filter and interceptor whenever an actor is migrated to or from `claimPrincipal: true`.
````

### CM-064 (both changed) — applied, merged with corrections (judo-meta-esm b78cc703 structure/twoWayRelationMember.evl + relationFeature.evl: the two bidirectional rules ARE real EVL constraints, so cciu "unverified" is wrong; the self-mapping diagnostic and the both-ASSOCIATION usual shape are kept; the corpus counts are labelled project data)

<details><summary>catalog (kept)</summary>

````markdown
### Pattern: Asymmetric bidirectional relations (AGGREGATION × ASSOCIATION)

*   **Use Case**: A parent-child relationship between two entities that must be navigable from both sides (e.g. `Partner` has many `PartnerSupportedLanguage`, and each `PartnerSupportedLanguage` points back at its `Partner`).
*   **Problem**: The UML-intuitive answer — declare both ends as `COMPOSITION`, or both as `AGGREGATION` — fails EVL (`twoWayRelationMember.evl`): *"Bidirectional association: X cannot be composition"* (`TwoWayRelationIsNotComposition`) and *"Partner of bidirectional association: X cannot be aggregation"* (the partner of an `AGGREGATION` end must be an `ASSOCIATION`).
*   **Pattern**: Make the two ends asymmetric:
    *   Owner end (the `upper ≠ 1` end, i.e. the collection side) = `AGGREGATION`
    *   Child end (the `upper = 1` end, i.e. the back-pointer) = `ASSOCIATION`
*   **Authoring with `judo-cli`**: the CLI rejects `relationKind=AGGREGATION` on `create` and `update` (`'AGGREGATION' is not valid`, valid: `ASSOCIATION · COMPOSITION`) for both one-way and two-way relation members. Set the owner end's kind in the modeling tool or in the XMI; with the CLI alone, model both ends as `ASSOCIATION`.
*   **Cardinality companion rule**: EVL additionally emits *"At least one reference of a bidirectional association should have lower bound with zero"*. Relax the owner-collection end (`1..*` → `0..*`); relaxing the child end breaks referential integrity.
*   **Scope**: These rules apply to bidirectional (`TwoWayRelationMember`) relations. `ASSOCIATION` is **not** forbidden on entities: an `ASSOCIATION` end is valid, and unidirectional entity relations are not required to be `AGGREGATION` or `COMPOSITION`. Which relation kinds an application uses is a design choice; check the project's own models before generalising.
````

</details>

cciu:

````markdown
### Pattern: Relation kind is layer-dependent

> **Corrected 2027-02-16.** An earlier revision of this section claimed entity `ASSOCIATION` was
> forbidden, that every unidirectional entity relation had to be `AGGREGATION` or `COMPOSITION`, and
> that bidirectional entity relations required an asymmetric `AGGREGATION` × `ASSOCIATION` split.
> **All three are wrong.** They were generalised from a single project and the root cause was
> misread — see the diagnostic note below, which is the reusable part.

*   **Rule**, measured across **nine** models in `PROJECTS.md`:

    | Owner | Allowed | Never observed |
    |---|---|---|
    | `EntityType` | `ASSOCIATION` or `COMPOSITION` | — |
    | `TransferObjectType` | `AGGREGATION` or `ASSOCIATION` | `COMPOSITION` (0 of 632) |

*   **Counts** (AdTrack, alba, compsych-letter-demo, e-demokracia, mlszksz-platform, park-here, rackinspect, trivia, ubives):

    ```
    EntityType         one-way  ASSOCIATION 182 | COMPOSITION 85 | AGGREGATION 10*
    EntityType         two-way  ASSOCIATION 130 | AGGREGATION  0 | COMPOSITION  0
    TransferObjectType one-way  AGGREGATION 418 | ASSOCIATION 214 | COMPOSITION 0
    TransferObjectType two-way  none in the corpus
    ```

    `*` **All ten entity `AGGREGATION` relations are in one model, `compsych-letter-demo`** — and in
    that model **no entity carries a self-mapping**. That is not a coincidence; it is the bug.

*   **Both ends of a bidirectional entity relation are `ASSOCIATION`.** 130 of 130 across the corpus,
    with zero counter-examples. There is no asymmetric split at the entity layer.

*   **Diagnostic — the misreading worth keeping.** An entity missing its self-mapping is treated by
    EVL as an *unmapped transfer object*, and the error it emits is
    *"Unmapped transfer object type: X can only have aggregation kind relations. Y is not aggregation."*
    That message names `aggregation`, so the obvious response is to change the relation kind — which
    silences it. **The relation kind was never the problem.** The fix is the self-mapping (see the
    pattern below); changing kinds is a workaround that leaves a model whose entity relations disagree
    with every other project in the corpus. This section previously quoted that very error under the
    self-mapping pattern while also recommending the workaround above it, and the contradiction went
    unnoticed.

    > **If you see "can only have aggregation kind relations", add the self-mapping. Do not change
    > the relation kind.**

*   **Unverified, retained for provenance**: the EVL messages *"Bidirectional association: X cannot be
    composition"* and *"Partner of bidirectional association: X cannot be aggregation"*, and the
    companion *"At least one reference of a bidirectional association should have lower bound with
    zero"*. These are plausible — the corpus has no bidirectional entity `COMPOSITION` or
    `AGGREGATION` to contradict them, which is consistent with EVL rejecting both. They were not
    reproduced during this correction. Treat them as constraints on what bidirectional ends may be,
    not as a mandate for `AGGREGATION`.
````

### CM-065 (both changed) — applied, merged with corrections (dataMember.evl: "must bind itself" exists as a critique (warning), so neither "error" nor "no check" is right; MAPPED required-flag constraint MappedAttributeRequiredMatchesBindingRequired confirmed and added as its own pattern; the self-mapping section was already in structure.md)

<details><summary>catalog (kept)</summary>

````markdown
*   **Convention**: Every derived `DataMember` sets `binding="<self-id>"` pointing at its own `xmi:id`. This is a modelling convention: the EVL validator does **not** emit a "must bind itself" error when it is missing (verified with a create → `validate --strict` → `discard` probe), so no validator will tell you if you omit it.
*   **Authoring**: This is distinct from — and complements — the mandatory self-mapping on every `EntityType` (see [structure.md](./esm_metamodel/structure.md), *Mandatory self-mapping on `EntityType`*). Code generators that emit YAML→XMI must set both.
````

</details>

cciu:

````markdown
*   **Convention**: Set `binding="<self-id>"` pointing at the member's own `xmi:id`.
*   **⚠️ EVL does NOT enforce this — corrected 2027-02-16.** An earlier revision stated EVL emits
    *"Derived data member X must bind itself"*. Reproduced against `judo-cli` with a create →
    `validate --strict` → `discard` probe: an unbound `DERIVED` member passes EVL cleanly. A control
    in the same session (an entity created without its self-mapping) **did** fail, confirming
    `validate` reads the in-memory model and that the probe was meaningful. `mlszksz-platform` also
    ships **5 unbound derived entity members** against 6 bound.
*   **Follow it anyway.** Entity data members are self-bound 138 of 145 in that model, the cost is one
    `update` mutation per derived member, and the full `./judo.sh build` runs validators EVL does not
    — the MAPPED-member rule below is a documented case of a constraint that fires only there. Cheap
    insurance against a late failure; not a rule you can rely on EVL to catch for you.
*   **The CLI does half of it silently.** `create(dataMember, memberType: STORED)` sets `binding` to
    self automatically; `memberType: DERIVED` leaves it **null**. Measured on a fresh model: 26 of 26
    STORED bound, 0 of 1 DERIVED. A generator that assumes the CLI is consistent will emit correct
    stored members and unbound derived ones.
*   **Authoring**: Distinct from — and complementary to — the mandatory self-mapping on every
    `EntityType` (see [structure.md](./esm_metamodel/structure.md), *Mandatory self-mapping on
    `EntityType`*), which **is** EVL-enforced. Code generators emitting YAML→XMI should set both.

### Pattern: MAPPED member `required` must match its binding

*   **Use Case**: Any `DataMember` on a mapped `TransferObjectType` whose `memberType` is `MAPPED` (i.e., `binding` is set to a stored `EntityType` attribute).
*   **Rule**: The MAPPED member's `required` flag MUST equal the bound entity attribute's `required` flag. EVL emits *"Required flag of data member: X (in: TO) must match the required flag of its binding"* otherwise. The build fails at the `Verify ESM model is presented` workflow step — the failure does NOT appear during in-memory CLI mutation or `transform --load`, only under full `./judo.sh build`.
*   **Companion rule**: A MAPPED member must also set `dataType` to the same primitive as the bound entity attribute (the EReference `dataType` on `DataMember` has `lowerBound:1` in `esm.ecore`). Saving without `dataType` is accepted by the CLI mutation but rejected at maven validation with `Diagnostic ERROR ... The required feature 'dataType' of 'DataMemberImpl@...' must be set`.
*   **Authoring**: When projecting an entity attribute through a principal TO (or any mapped TO), copy both `required` and `dataType` straight from the entity attribute. Default `required=false` on the TO is a common slip when the entity attribute is `required=true`.

### Pattern: EntityType self-mapping is a universal requirement

*   **Use Case**: Every `EntityType` — whether or not it is referenced by a `TransferObjectType` as `mapping.target`, and whether or not it currently carries any relations.
*   **Rule**: Every `EntityType` must carry a `<mapping target="<own-FQN>"/>` child (self-mapping). EVL constraint: `EntityTypeHasSelfMapping`. Without it the validator treats the entity as an *unmapped transfer object*, which produces two distinct error messages depending on the failure mode:
    *   *"Entity type: X must have mapping with a target pointing to the entity type"* — fires when another TO references `X` as its `mapping.target`.
    *   *"Unmapped transfer object type: X can only have aggregation kind relations. Y is not aggregation."* — fires when `X` itself carries an `ASSOCIATION` or `COMPOSITION` relation but has no self-mapping, **even if no TO references `X` at all**. Observed 2026-05-12 on `compsych-letter-demo` `RuleViolation` (ASSOCIATION → `Rule`) and `DataObject` (COMPOSITION → `RuleViolation`): neither was yet referenced by any TO, yet both EVL messages appeared together after the self-mapping was omitted.
*   **Authoring**: Add the self-mapping immediately after every `create.entityType` call, before adding any relations. See [structure.md](./esm_metamodel/structure.md) *"Mandatory self-mapping on EntityType"* for the canonical statement of this rule. Previously noted under CLI authoring of `compsych-letter-demo`'s `User`+`UserPrincipal` shape 2026-05-11 (TO-target trigger); broadened to cover the relation-kind trigger 2026-05-12.
*   **⚠️ Do not "fix" the second error by changing the relation kind.** *"can only have aggregation kind relations"* names `aggregation`, so switching the relation to `AGGREGATION` silences it — and leaves the missing self-mapping in place. That workaround is visible in the corpus: `compsych-letter-demo` holds **all ten** entity-level `AGGREGATION` relations found across nine models, and **none** of its entities carries a self-mapping. See *Relation kind is layer-dependent* above; entity relations are `ASSOCIATION` or `COMPOSITION` everywhere else.
````

### CM-066 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
    <app>::types::PartnerCodeType
````

</details>

cciu:

````markdown
    webshop::types::PartnerCodeType
````

## catalog/agent-docs/model/esm_metamodel/accesspoint.md

### CM-067 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
| `managed` | Boolean | `[1]` | If `true`, the framework is *intended* to synchronise the `principal` row in the DB from the IdP token during the `#_principal` operation. Requires `principal` to be a **mapped** `TransferObjectType` (projecting an `EntityType`) and at least one `<claims>` element that marks which `DataMember` is the identity key. **Empirical caveat:** in `judo-runtime-core-dispatcher` 1.0.6.20241030 / 1.0.6.20251205 only the *lookup* side is implemented — the first-login *insert* is not, and `DefaultActorResolver.getActorByClaims` throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. Pair `managed=true` with an `AuthenticationInterceptor` that performs the insert (see [Just-in-Time User Provisioning](../../backend/authentication-guide.md#example-just-in-time-user-provisioning)). See *Three actor shapes* below and [Mapped Managed Principal with Claim Mapping](../advanced-modeling-patterns.md#pattern-mapped-managed-principal-with-claim-mapping). |
````

</details>

cciu:

````markdown
| `managed` | Boolean | `[1]` | If `true`, the framework is *intended* to synchronise the `principal` row in the DB from the IdP token during the `#_principal` operation. Requires `principal` to be a **mapped** `TransferObjectType` (projecting an `EntityType`) and at least one `<claims>` element that marks which `DataMember` is the identity key. **Empirical caveat:** in `judo-runtime-core-dispatcher` 1.0.6.20241030 / 1.0.6.20251205 only the *lookup* side is implemented — the first-login *insert* is not, and `DefaultActorResolver.getActorByClaims` throws `AccessDeniedException("AUTHENTICATED_ENTITY_NOT_FOUND")` when the row is missing. Pair `managed=true` with an `AuthenticationInterceptor` that performs the insert (see Just-in-Time User Provisioning (see `judo-backend-docs` skill)). See *Three actor shapes* below and Mapped Managed Principal with Claim Mapping (see `judo-advanced-modeling-patterns.md#pattern-mapped-managed-principal-with-claim-mapping-docs` skill). |
````

### CM-068 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
**Pairing rule (`Access` ↔ `MenuItemAccess`).** An `Access` is a *data-permission* grant only; it does **not** create any navigation entry. Every `Access` on an `ActorType` that should be reachable from the UI **must** be paired with a `MenuItemAccess` placed under that same `ActorType.<menuItems>` (directly or inside a `MenuItemGroup`), with its `access` reference pointing back to this `Access`. Without the paired `MenuItemAccess` the target is exposed through the access point API but never appears in the actor's menu. See [ui.md — MenuItemAccess](./ui.md) and [UI Authoring Guide](../ui-authoring-guide.md).
````

</details>

cciu:

````markdown
**Pairing rule (`Access` ↔ `MenuItemAccess`).** An `Access` is a *data-permission* grant only; it does **not** create any navigation entry. Every `Access` on an `ActorType` that should be reachable from the UI **must** be paired with a `MenuItemAccess` placed under that same `ActorType.<menuItems>` (directly or inside a `MenuItemGroup`), with its `access` reference pointing back to this `Access`. Without the paired `MenuItemAccess` the target is exposed through the access point API but never appears in the actor's menu. See [ui.md — MenuItemAccess](./ui.md) and UI Authoring Guide (see `judo-ui-authoring-guide.md-docs` skill).
````

### CM-069 (both changed) — applied (Principal back-link exclusivity + Managed-realm sync trigger; verified: esm.ecore actorType/principal eOpposite, UserManagedWrappedDao; project names neutralised)

<details><summary>catalog (kept)</summary>

````markdown
### Three actor shapes (authoring reference)

Three shapes for `ActorType.principal` are supported (there is no `claimPrincipal` flag: the shape follows from `principal`, `managed` and `claims`). The shape dictates which JQL category surfaces the identity data and what the framework persists:

| Shape | `principal` | `managed` | `<claims>` | Framework persists | JQL for JWT claims | JQL for persisted attrs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Token-only** | absent (no `principal`) | `false` | none | nothing | `USER.*` | — |
| **Transient principal** | unmapped `TransferObjectType` | `false` | optional | nothing | `PRINCIPAL.*` | — |
| **Managed mapped principal** | mapped `TransferObjectType` projecting an `EntityType` | `true` | ≥ 1, each pointing at a `MAPPED` `DataMember` | the principal entity row (auto-insert / auto-update from JWT) | `USER.*` (raw claim) | `ACTOR.*` (from the row) |

See [ACTOR vs PRINCIPAL vs USER](../advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables) for the matching JQL decision matrix and the silent-failure pitfall when the chosen category doesn't match the chosen shape.
````

</details>

cciu:

````markdown
### Principal back-link exclusivity

`TransferObjectType.actorType` = eOpposite of `ActorType.principal`. Single-valued on both sides. Only ONE TO per actor holds `actorType=<Actor>`.

Setting `TO.actorType` transparently reassigns `ActorType.principal` to that TO. Previously-linked TO loses back-link (cleared to null).

Consequence: cannot keep lean principal TO AND separate full admin TO both carrying `actorType=<Actor>`. Pick one. Other TOs mapping same entity exist as plain mapped TOs without the back-link.

**Empirical validation (2026-05-11, `compsych-letter-demo`).** `compsychletter::services::UserPrincipal` and `compsychletter::services::UserTO` both map `User`; actor = `compsychletter::actors::LetterUser`. Reassigning `UserTO.actorType=LetterUser` swapped `LetterUser.principal` from `UserPrincipal` to `UserTO`. Build broke at `esm2ui/claim.etl`: *"Could not find attribute: userName"*. Restoring `LetterUser.principal=UserPrincipal` cleared `UserTO.actorType` to null. Build succeeded.

### Managed-realm sync trigger

When `ActorType.managed=true`, framework delegates CUD on principal TO to Keycloak managed realm (create / update / delete realm user matching the row).

Sync trigger bound to **principal TO's DAO metadata**. Dispatcher injects Keycloak sync ONLY when DAO layer invoked with principal-TO metadata (operation bound to principal TO). Sync follows TO metadata, not entity.

Other TOs mapping same principal entity (e.g. admin user-management `UserTO`, list `UserListTO`) do NOT auto-sync to Keycloak. Entity row updates; Keycloak realm user does not.

Multiple TOs CAN map same principal entity — admin user-management coexists with lean principal TO. Metamodel allows it; only `actorType` back-link is exclusive (see *Principal back-link exclusivity* above).

**Pattern.** For Keycloak sync from admin user-management surface: custom operation on admin TO that delegates through **principal TO's DAO** (re-dispatch with principal-TO metadata). Direct CUD on admin TOs skips Keycloak.

**Design rule.** Keep ONE lean principal TO owning `actorType` AND framework-managed Keycloak sync. Use other mapped TOs for admin / list projections. Route admin mutations through a custom op calling principal TO's DAO when realm sync required; otherwise accept admin TO mutations are DB-only.

### Three actor shapes (authoring reference)

Three mutually exclusive shapes for `ActorType.principal` are supported. The shape dictates which JQL category surfaces the identity data and what the framework persists:

| Shape | `principal` | `managed` | `<claims>` | Framework persists | JQL for JWT claims | JQL for persisted attrs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Token-only** (`claimPrincipal: true`) | absent / unmapped | `false` | ignored | nothing | `USER.*` | — |
| **Transient principal** | unmapped `TransferObjectType` | `false` | optional | nothing | `PRINCIPAL.*` | — |
| **Managed mapped principal** | mapped `TransferObjectType` projecting an `EntityType` | `true` | ≥ 1, each pointing at a `MAPPED` `DataMember` | the principal entity row (auto-insert / auto-update from JWT) | `USER.*` (raw claim) | `ACTOR.*` (from the row) |

See ACTOR vs PRINCIPAL vs USER (see `judo-advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables-docs` skill) for the matching JQL decision matrix and the silent-failure pitfall when the chosen category doesn't match the chosen shape.
````

## catalog/agent-docs/model/esm_metamodel/generator-reserved-names.md

### CM-070 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
---
title: Generator Reserved Names
description: Member names that collide with generator-emitted methods and how to avoid them.
---

# Generator Reserved Names

**[◄ Back to Index](./README.md)**

Create and operation-input usage of a `TransferObjectType` (relations with the `createable` flag that target it, operations that take it as input) causes the generators to emit methods with fixed names. A relation or attribute whose `name` collides with one of these methods surfaces only at `tsgo` / `vite build` time as `error TS2393: Duplicate function implementation`, several transformation steps away from the root cause.
````

</details>

cciu:

````markdown
# Generator Reserved Names

**[◄ Back to Index](./SKILL.md)**

Structural flags on a `TransferObjectType` (`createable`, …) cause the generators to emit methods with fixed names. A relation or attribute whose `name` collides with one of these methods surfaces only at `tsgo` / `vite build` time as `error TS2393: Duplicate function implementation`, several transformation steps away from the root cause.
````

### CM-071 (both changed) — rejected (catalog wording is more precise: template is generated when a createable relation targets the TO or it is an operation input)

<details><summary>catalog (kept)</summary>

````markdown
| the TO can be created through a relation (a `createable` relation targets it) or is the input of an operation | `getTemplate()` — returns a blank prototype for Create forms and operation forms (endpoint `<TO>/~template`; the REST client generator emits it when the TO `isTemplateable`). | **`template`** |
````

</details>

cciu:

````markdown
| `createable="true"` | `getTemplate()` — returns a blank prototype for Create forms (endpoint `/services/<TO>/~template`). | **`template`** |
````

## catalog/agent-docs/model/esm_metamodel/structure.md

### CM-072 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
**Mandatory self-mapping on `EntityType`.** Every `EntityType` must carry a `<mapping target="<own xmi:id>"/>` child (`target` = the entity's own id). EVL rejects an entity without it (`EntityTypeHasMapping`); removing these because they look redundant produces a cascade of validation errors. This is distinct from a `TransferObjectType`'s `mapping`, which projects the TO from an entity and carries the optional `filter`.
````

</details>

cciu:

````markdown
**Mandatory self-mapping on `EntityType`.** Every `EntityType` must carry a `<mapping target="<own xmi:id>"/>` child (`target` = the entity's own id). EVL rejects an entity without it (`EntityTypeHasSelfMapping`); removing these because they look redundant produces a cascade of validation errors. This is distinct from a `TransferObjectType`'s `mapping`, which projects the TO from an entity and carries the optional `filter`.
````

## catalog/agent-docs/model/esm_metamodel/ui-behaviour.md

### CM-073 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
- [Frontend ESM-to-UI Mapping](../../frontend/esm-to-ui-mappings/README.md) - ESM to React mapping
````

</details>

cciu:

````markdown
- Frontend ESM-to-UI Mapping (see `judo-frontend-docs` skill) - ESM to React mapping
````

## catalog/agent-docs/model/esm_metamodel/ui.md

### CM-074 (cciu removes) — rejected (cciu deletes catalog text that was verified against judo-ng in the sweep)

<details><summary>catalog (kept)</summary>

````markdown
> **Generated `name`.** `name` is inherited from `NamedElement`, but `RelationColumn` declares a generated `getName()` EOperation that **overrides the stored value at runtime**, derived from `relationFeature`. On the `judo_cli` GraphQL surface `name` is queryable but **omitted from `RelationColumnCreateInput`** and **silently dropped on `update`**. The required identity field at create time is `dataFeatureOfRelationFeature` (see also the top-level-table pitfall below).
````

</details>

cciu:

````markdown
(removed)
````

### CM-075 (both changed) — rejected (cciu skill/SKILL.md harness wording; catalog uses kb links)

<details><summary>catalog (kept)</summary>

````markdown
- [Frontend ESM-to-UI Mapping](../../frontend/esm-to-ui-mappings/README.md) - ESM to React mapping
````

</details>

cciu:

````markdown
- Frontend ESM-to-UI Mapping (see `judo-frontend-docs` skill) - ESM to React mapping
````

## catalog/agent-docs/model/model-development.md

### CM-076 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
4.  **Prefer JUDO Model CLI mutations (see [judo-cli.md](./judo-cli.md)) over hand-editing the XMI**, so the set of changes is reproducible from transcripts even if the working copy is lost.
````

</details>

cciu:

````markdown
4.  **Prefer `judo-model-designer` CLI mutations over hand-editing the XMI**, so the set of changes is reproducible from transcripts even if the working copy is lost.
````

### CM-077 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
    *   **Purpose**: To read an attribute of the current **principal `TransferObjectType`**. The runtime calls the actor's generated `_principal` operation and returns the named attribute of its result (`PrincipalVariableProvider`).
    *   **Use Case**: Actors whose `principal` is an `unmapped` `TransferObjectType` populated by the framework from the IdP token. The values come from the principal TO's attributes, not directly from the raw JWT. An actor with **no** `principal` has no `_principal` operation, so `PRINCIPAL.*` yields nothing.
````

</details>

cciu:

````markdown
    *   **Purpose**: To access claims on the current **principal `TransferObjectType`** of a non-`claimPrincipal` actor.
    *   **Use Case**: Actors whose `principal` is an `unmapped` `TransferObjectType` populated by the framework from the IdP token and **without** `claimPrincipal: true`. The values come from the principal TO's attributes, not directly from the raw JWT.
````

### CM-078 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
    *   **Use Case**: **Required** for token-only actors (no `principal` TO). For such actors the JWT claims surface under the `USER` category — `PRINCIPAL.*` returns empty and silently breaks access filters, custom ops, and audit logic. This is the single most common source of "mysterious empty claim" bugs. The `USER` category reads the attributes of the authenticated `JudoPrincipal` (the token claims) and works for every actor shape.
````

</details>

cciu:

````markdown
    *   **Use Case**: **Required** for actors declared with `claimPrincipal: true`. For such actors the JWT claims surface under the `USER` category — `PRINCIPAL.*` returns empty and silently breaks access filters, custom ops, and audit logic. This is the single most common source of "mysterious empty claim" bugs.
````

### CM-079 (both changed) — rejected (no `claimPrincipal` attribute exists in judo-meta-esm esm.ecore or anywhere in the judo-ng clones; catalog wording "token-only actor, no principal TO" kept)

<details><summary>catalog (kept)</summary>

````markdown
> | Token-only: no `principal` TO (no persisted record) | `USER.*` | n/a |
> | Unmapped principal TO | `PRINCIPAL.*` (principal TO attributes) or `USER.*` (raw claims) | n/a |
> | Mapped principal TO (persisted Actor entity) | `USER.*` for raw claims | `ACTOR.*` |
>
> Using `PRINCIPAL.*` against an actor with no `principal` TO is valid JQL but returns empty at runtime. See [ACTOR vs PRINCIPAL vs USER](./advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables).

### Other environment-variable categories

Besides `PRINCIPAL`, `USER` and `ACTOR`, the engine knows more categories, mostly used implicitly:

- **`SYSTEM`**: `current_date`, `current_timestamp`, `current_time`, reached through `<Type>!now()` (see *Temporal functions*).
- **`PARAMETER`**: the attributes of an input parameter transfer object of a parameterized query become `PARAMETER`-category variables while the expression is resolved.
- **`ENVIRONMENT`, `SEQUENCE`, `REQUEST`**: runtime providers registered by the default variable resolver (environment configuration values, database sequences, per-request parameters). An undefined variable resolves to `null` with a warning.

`!getVariable` is typed by the primitive it is called on (`Integer`, `Decimal`, `Boolean`, `String`, an enumeration, a custom type, `Date`, `Timestamp`, `Time`); for measured numerics the variable carries the unit. It always returns a scalar, never a collection.

### JQL grammar quirks

- The ternary `cond ? then : else` is right-associative and compiles to a typed switch expression. The condition must be a logical expression; `then` and `else` must be of the same kind (a decimal result is chosen when either side is decimal; entity branches resolve to a common supertype, and an ambiguous or missing common supertype fails the build).
- Equality is `==` and `!=` only (no `=` and no `<>`). Keywords are case-insensitive.
- There is a `^` power operator between multiplication and the `as` (spawn) operator.
- Enumeration literals are `EnumType#LITERAL`; a function call is `expr!name(args)` and its result can be navigated further.
- Collection iterator functions take a lambda over **one** iterator variable and may select only an immediate field of it; multi-step navigation inside the lambda body is out of scope (see *Lambda scopes do not nest*).
````

</details>

cciu:

````markdown
> | `claimPrincipal: true` (token-only, no persisted record) | `USER.*` | n/a |
> | Unmapped principal TO, no `claimPrincipal` | `PRINCIPAL.*` | n/a |
> | Mapped principal TO (persisted Actor entity) | `USER.*` for raw claims | `ACTOR.*` |
>
> Using `PRINCIPAL.*` against a `claimPrincipal: true` actor is valid JQL but returns empty at runtime. See [ACTOR vs PRINCIPAL vs USER](./advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables).
````

### CM-080 (both changed) — already-covered (catalog states the same, more precisely: parsed, but the query engine converter throws Not supported yet)

<details><summary>catalog (kept)</summary>

````markdown
| `!join(i \| selector, separator)` | String | ⚠️ **Recognised by the JQL grammar and expression builder, but not implemented by the query engine** (the converter throws `Not supported yet`). The function name is registered in the parser (so expressions using it pass `transform` without an `Unknown function` error), but evaluation fails downstream — there is currently no built-in string-aggregation function. For concatenating a string attribute across a collection, use a **backend-computed `TRANSIENT` TO attribute** populated from an `OperationCallInterceptor` (see Pitfall 5.1 below and the backend Interceptors guide). Do **not** use `!collectAsString` or `!mkString` either — they do not exist at all. |
````

</details>

cciu:

````markdown
| `!join(i \| selector, separator)` | String | ⚠️ **Recognised by the JQL grammar but not implemented at runtime.** The function name is registered in the parser (so expressions using it pass `transform` without an `Unknown function` error), but evaluation fails downstream — there is currently no built-in string-aggregation function. For concatenating a string attribute across a collection, use a **backend-computed `TRANSIENT` TO attribute** populated from an `OperationCallInterceptor` (see Pitfall 5.1 below and the backend Interceptors guide). Do **not** use `!collectAsString` or `!mkString` either — they do not exist at all. |
````

### CM-081 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
  .accessibleTemplates

-- Same result, redundant !any()
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
````

</details>

cciu:

````markdown
webshop::entities::User
  !filter(u | u.userName == webshop::types::String!getVariable('ACTOR', 'userName'))
  .accessibleTemplates

-- Same result, redundant !any()
webshop::entities::User
  !filter(u | u.userName == webshop::types::String!getVariable('ACTOR', 'userName'))
````

### CM-082 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
````

</details>

cciu:

````markdown
webshop::entities::User
  !filter(u | u.userName == webshop::types::String!getVariable('ACTOR', 'userName'))
````

### CM-083 (both changed) — already-covered (catalog line 387 already says !collectAsString and !mkString do not exist)

<details><summary>catalog (kept)</summary>

````markdown
Any `!<name>(...)` call whose `<name>` is not in this list fails the builder with `Unknown function: <name>`. In particular `!collectAsString` and `!mkString` **do not exist** — there is no working string-aggregation function: `!join(lambda, separator)` is parsed but not supported by the query engine (see the `!join` row above), so compute the string in a backend `TRANSIENT` TO attribute.
````

</details>

cciu:

````markdown
Any `!<name>(...)` call whose `<name>` is not in this list fails the builder with `Unknown function: <name>`. In particular `!collectAsString` and `!mkString` **do not exist** — use `!join(lambda, separator)` (with the runtime caveat noted on the `!join` row above).
````

### CM-084 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
When the inner predicate must reach the outer collection, navigate via a relation (e.g. `y.parent.xs`). Bipartite / cross-product predicates of the form "∀ a ∈ A, ∀ b ∈ B, ∃ c ∈ C(a,b)" are **not expressible** as a single JQL expression — compute them in Java via an `OperationCallInterceptor` writing to a `TRANSIENT` TO attribute. See [Interceptors Guide](../backend/interceptors.md), *Backend-Computed TO Attribute (JQL Escape Hatch)*.
````

</details>

cciu:

````markdown
When the inner predicate must reach the outer collection, navigate via a relation (e.g. `y.parent.xs`). Bipartite / cross-product predicates of the form "∀ a ∈ A, ∀ b ∈ B, ∃ c ∈ C(a,b)" are **not expressible** as a single JQL expression — compute them in Java via an `OperationCallInterceptor` writing to a `TRANSIENT` TO attribute. See Interceptors Guide (see `judo-backend-docs` skill), *Backend-Computed TO Attribute (JQL Escape Hatch)*.
````

### CM-085 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
<app>::types::String!getVariable('PRINCIPAL', 'claim_name')
````

</details>

cciu:

````markdown
webshop::types::String!getVariable('PRINCIPAL', 'claim_name')
````

### CM-086 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
Multi-value claims (e.g. an array `partner_scope` claim) are therefore **not consumable in JQL**. Options: (a) flatten at the IdP and compare with `==`; or (b) compute the scope in Java from `SecurityContext` and narrow via an `OperationCallInterceptor`. See [Architectural Patterns](../backend/architectural-patterns.md), §1 *Model-Driven Multi-Tenancy*.
````

</details>

cciu:

````markdown
Multi-value claims (e.g. an array `partner_scope` claim) are therefore **not consumable in JQL**. Options: (a) flatten at the IdP and compare with `==`; or (b) compute the scope in Java from `SecurityContext` and narrow via an `OperationCallInterceptor`. See Architectural Patterns (see `judo-backend-docs` skill), §1 *Model-Driven Multi-Tenancy*.
````

### CM-087 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
<app>::entities::Partner!filter(p |
  p.code == <app>::types::String!getVariable('PRINCIPAL', 'partner_code'))

// ❌ fails ASM ReferenceExpressionMatchesBinding
<app>::services::PartnerTO!filter(…)
````

</details>

cciu:

````markdown
webshop::entities::Partner!filter(p |
  p.code == webshop::types::String!getVariable('PRINCIPAL', 'partner_code'))

// ❌ fails ASM ReferenceExpressionMatchesBinding
webshop::services::PartnerTO!filter(…)
````

### CM-088 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
See [Architectural Patterns](../backend/architectural-patterns.md), *Rules for `accesses[*].getterExpression`*, for the complete set of four rules.
````

</details>

cciu:

````markdown
See Architectural Patterns (see `judo-backend-docs` skill), *Rules for `accesses[*].getterExpression`*, for the complete set of four rules.
````

### CM-089 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
The ESM model file (`/model/<app>.model`) is complex XML (XMI). **The primary authoring tool is `judo-model-cli`** (or the Judo Designer GUI). Direct edits should be avoided because they are easy to get wrong and bypass schema validation.
````

</details>

cciu:

````markdown
The ESM model file (`/model/webshop.model`) is complex XML (XMI). **The primary authoring tool is `judo-model-cli`** (or the Judo Designer GUI). Direct edits should be avoided because they are easy to get wrong and bypass schema validation.
````

### CM-090 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
- **Filter base = entity FQN**, not TO FQN: `<app>::entities::<Entity>!filter(x | …)`.
- **No `self`** (unbound at actor scope; see §5.4).
- **No boolean literals** — `getterExpression="true"` on a `DERIVED` access fails ASM `ReferenceBindingExpressionIsValid`. For an unfiltered access, use `accessType="ALL"` with no getter.
- **Fully-qualified primitives** in any `!getVariable(…)` call (see §5.2).

### Do not edit the model file by hand
The ESM model file (`model/<app>.model`) is XMI. Never edit it as text: change it only through the JUDO Model CLI (see [judo-cli.md](./judo-cli.md)) or the JUDO Designer. Hand edits break cross-references (`xmi:id`) and can corrupt the model.
````

</details>

cciu:

````markdown
- **Filter base = entity FQN**, not TO FQN: `webshop::entities::<Entity>!filter(x | …)`.
- **No `self`** (unbound at actor scope; see §5.4).
- **No boolean literals** — `getterExpression="true"` on a `DERIVED` access fails ASM `ReferenceBindingExpressionIsValid`. For an unfiltered access, use `accessType="ALL"` with no getter.
- **Fully-qualified primitives** in any `!getVariable(…)` call (see §5.2).
````

## catalog/agent-docs/model/ui-authoring-guide.md

### CM-091 (both changed) — rejected (cciu drops the kb frontmatter and links ./SKILL.md)

<details><summary>catalog (kept)</summary>

````markdown
---
title: UI Authoring Guide
description: How to compose form, table and view scaffolds on transfer objects and wire them onto an actor menu in the ESM, with bindings, layout rules, pitfalls and audits.
---

# UI Authoring Guide

**[◄ Back to Index](./README.md)**

This guide is the **authoring playbook** for composing ESM UI presentations (Form, Table, View) on `TransferObjectType`s, and for wiring them onto an `ActorType` menu. It is the companion to the per-element reference in [ui.md](./esm_metamodel/ui.md).

**Scope boundary.** This file explains **what to put in the model**. For how to actually mutate the model, see [judo-cli.md](./judo-cli.md). For per-element attribute definitions, enums, and conditional rules, see [ui.md](./esm_metamodel/ui.md) and [ui-behaviour.md](./esm_metamodel/ui-behaviour.md). For customizing the **generated React** once the UI model is in place, see the [frontend documentation](../frontend/README.md).
````

</details>

cciu:

````markdown
# UI Authoring Guide

**[◄ Back to Index](./SKILL.md)**

This guide is the **authoring playbook** for composing ESM UI presentations (Form, Table, View) on `TransferObjectType`s, and for wiring them onto an `ActorType` menu. It is the companion to the per-element reference in [ui.md](./esm_metamodel/ui.md).

**Scope boundary.** This file explains **what to put in the model**. For how to actually mutate the model, see the `judo-model-cli` skill. For per-element attribute definitions, enums, and conditional rules, see [ui.md](./esm_metamodel/ui.md) and [ui-behaviour.md](./esm_metamodel/ui-behaviour.md). For customizing the **generated React** once the UI model is in place, see the frontend skill.
````

### CM-092 (cciu adds) — rejected (judo-cli in target/ has `move` and create --index/--before/--after; "append-only, no reorder" is wrong for this CLI)

<details><summary>catalog (kept)</summary>

````markdown

````

</details>

cciu:

````markdown
9.  **EList children created via `judo-cli` are append-only.** Every multi-valued containment in the UI/structure metamodel — `components`, `columns`, `filters`, `rowOperations`, `tableOperations`, `tabs`, `steps`, `actions`, `menuItems` on the UI side; `attributes`, `relations`, `operations`, `members` on the structure / accesspoint side — is treated by the CLI's `create` mutation as **append to the end**. There is **no insert-at-position and no reorder operation**. The final order of any list therefore equals the order in which `create` calls are issued. Plan the complete ordered list **before** running the first mutation; treat "insert one in the middle later" as a delete-and-rebuild (which invalidates xmi:ids and forces re-pointing every `dataFeature` / `relationFeature` / `hiddenBy` / `access` reference into the affected tail). See [Repairing layout debt at scale §16](#16-repairing-layout-debt-at-scale) and `judo-model-cli/mutations.md` §*EList Append-Only*.
````

### CM-093 (cciu adds) — rejected (link into .claude/skills, which is not part of the catalog)

<details><summary>catalog (kept)</summary>

````markdown

````

</details>

cciu:

````markdown
*See also [ui-mutations.md §Pitfalls and workarounds](../../../.claude/skills/judo-model-cli/ui-mutations.md) for CLI-specific gotchas (ambiguous FQN containers, `git restore` caveat, stale UI queries after `transform --load`).*
````

### CM-094 (both changed) — rejected (link into .claude/skills; catalog sentence kept)

<details><summary>catalog (kept)</summary>

````markdown
If `menuItems.totalCount == 0` but `accesses.totalCount > 0`, every access in that actor is API-only (invisible in the menu). Add a `MenuItemAccess` per access (directly on `<menuItems>` or nested in a `MenuItemGroup`).
````

</details>

cciu:

````markdown
If `menuItems.totalCount == 0` but `accesses.totalCount > 0`, every access in that actor is API-only (invisible in the menu). Add `MenuItemAccess` per access — see [ui-mutations.md Recipe 16](../../../.claude/skills/judo-model-cli/ui-mutations.md).
````

### CM-095 (both changed) — rejected (append-only ordering claim is wrong, see CM-092; project name)

<details><summary>catalog (kept)</summary>

````markdown
2. **Cheap rollback** — `git restore model/<app>.model` reverts cleanly when the stage was small.

A stage of ~80 mutations against 4 TOs is workable; a stage of 200+ mutations across 15 TOs is not.

### Pre-stage prep — rename ambiguous containers FIRST

If the audit shows multiple TOs sharing `TransferObjectView::View`, `TransferObjectTable::Table`, or `TransferObjectForm::Form` FQNs, rename them all to `<TO>View` / `<TO>Table` / `<TO>Form` **before adding any children**. Given an ambiguous container FQN, a `create` mutation picks one parent non-deterministically — children land under the wrong scaffold and the only safe recovery is renaming the containers and re-creating the children.
````

</details>

cciu:

````markdown
2. **Cheap rollback** — `git restore model/webshop.model` reverts cleanly when the stage was small.

A stage of ~80 mutations against 4 TOs is workable; a stage of 200+ mutations across 15 TOs is not.

### Ordering within a stage (EList append-only)

The CLI's `create` mutation appends to every multi-valued EList. **Within a stage, sequence the mutations so each EList ends up in the desired final order on the first pass.**

| List | Desired sequence |
|---|---|
| `TransferObjectTable.columns` | left-to-right column order |
| `TransferObjectTable.filters` | filter bar order |
| `TransferObjectTable.rowOperations` / `tableOperations` | action button order |
| `Container.components` (View / Form / Group) | top-to-bottom layout order |
| `TabBar.tabs` / `Stepper.steps` | tab / step order |
| `ActionGroup.actions` | button order; first `featuredActions` get promoted |
| `ActorType.menuItems` / `MenuItemGroup.menuItems` | top-to-bottom navigation order |
| `EnumType.members` | ordinal-ascending |
| `EntityType.attributes` / `relations` / `operations` | structural order (matters for downstream consumers that iterate) |

If the order is wrong after a stage, the only CLI remedy is **delete every element from the misplaced position to the end of the list, then recreate the corrected tail**. Each delete invalidates the element's `xmi:id`, so every other element that referenced it (`dataFeature`, `relationFeature`, `hiddenBy`, `enabledBy`, `requiredBy`, `access`, `target`, `targetOperation`) must be re-pointed at the newly created replacement — typically by re-running the mutations that depended on them. Plan the list order at design time.

This is the rule that makes OpenSpec task ordering load-bearing for any change that emits CLI mutations: **task order = final EList order**. See `openspec-apply-change` guardrails.

### Pre-stage prep — rename ambiguous containers FIRST

If the audit shows multiple TOs sharing `TransferObjectView::View`, `TransferObjectTable::Table`, or `TransferObjectForm::Form` FQNs, rename them all to `<TO>View` / `<TO>Table` / `<TO>Form` **before adding any children**. The CLI's `create` mutation, given an ambiguous container FQN, picks one parent non-deterministically — see [ui-mutations.md Pitfall A](../../../.claude/skills/judo-model-cli/ui-mutations.md).
````

### CM-096 (both changed) — already-covered (every cciu sentence is already in the catalog file)

<details><summary>catalog (kept)</summary>

````markdown
- Either `git add && git commit` after each `save` (a "checkpoint commit" per stage), or copy `model/<app>.model` to a `.bak` before any git operation.
````

</details>

cciu:

````markdown
- Either `git add && git commit` after each `save` (a "checkpoint commit" per stage), or copy `model/webshop.model` to a `.bak` before any git operation.
````

### CM-097 (both changed) — rejected (cciu uses a concrete project name; catalog keeps the <app> placeholder)

<details><summary>catalog (kept)</summary>

````markdown
git add model/<app>.model
````

</details>

cciu:

````markdown
git add model/webshop.model
````

### CM-098 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
#    git restore model/<app>.model
````

</details>

cciu:

````markdown
#    git restore model/webshop.model
````

### CM-099 (both changed) — rejected (link into .claude/skills)

<details><summary>catalog (kept)</summary>

````markdown
Pair every `Access` that should appear in the navigation with a `MenuItemAccess` on the actor's `<menuItems>` — directly, or nested inside a `MenuItemGroup` to organise related items. Order, grouping, and `hiddenBy` claims on the menu items follow the same conditional model as the rest of the UI (see [ui-behaviour.md](./esm_metamodel/ui-behaviour.md)).

---

## 17. Reference-derived elements, custom components and capability rules

### Reference-derived elements have no writable name

`DataField`, `DataColumn`, `ReferenceField`, the `<Feature>Filter` elements (for example `DataFilter`), `OperationForm` and the `Inherited*` references are **reference-derived**: the metamodel computes their `name` and FQN from the binding (`dataFeature.member.name`, `...name + "Filter"`, `operation.name`). Their CLI `CreateInput` therefore has no `name`; the identity is the binding (`dataFeature`, `relationFeature` or `operation`) and the writable fields are `container`, `containment`, `label`, `documentation` and the binding. Unmapped `User` elements should not set a name, and bare View/Form/Table sibling names are forbidden. Place bound widgets with `update <container> --add feature ...` (see [judo-cli.md](./judo-cli.md)); there is no separate `ui-mutations` document. To add a model attribute to an existing view or form, add a `DataField` under a `Group` or the view container, bound to a `dataFeature` that already exists as a `MAPPED` or `TRANSIENT` member of the transfer object.

### Embedded tables bind the member or its inherited reference

Columns and filters of an embedded table may bind either the member or its inherited reference; `EsmUtils.purifyAttribute` rebinds them to the `InheritedDataFeatureReference`, and both forms are equivalent for UI generation.

### A button representation still needs columns

A `TabularReferenceField` with `representationComponent="button"` still raises the validator warning `Columns are not defined for viewable table` unless its `<columns>` are populated.

### Conditional confirmation

For a `CONDITIONAL` operation-form confirmation, `confirmationCondition` must be a boolean attribute of the operation's **root type**; otherwise validation fails with `Confirmation condition must be an attribute of the root type`. The candidates listed by a selector can include fields of another entity, so the EVL root-type rule, not the list, is authoritative.

### What enables sorting and filtering in the generated UI

Sort and filter controls appear only for references whose target is mapped and has at least one non-`TRANSIENT` attribute of a supported type (orderable: string, numeric, date, timestamp, time, boolean; filterable: those plus enumeration). See [model-validation-and-transformation.md](./model-validation-and-transformation.md).

### Selecting a custom React component from the model

A model annotation whose name starts with the prefix `use` (configurable with the `customComponentAnnotationPrefix` generator parameter, default `use`) makes the generator register and use a custom component. An annotation such as `useFancyText` on a visual element selects the custom widget that the developer implements; see the [frontend documentation](../frontend/README.md).

---

## 18. Related documentation
````

</details>

cciu:

````markdown
See [ui-mutations.md Recipe 16](../../../.claude/skills/judo-model-cli/ui-mutations.md) for the full menu authoring playbook (groups, hidden-by-claim, ordering).

---

## 17. Related documentation
````

### CM-100 (both changed) — already-covered (wording-only difference, ratio ≥ 0.85; catalog wording kept)

<details><summary>catalog (kept)</summary>

````markdown
- [JUDO Model CLI](./judo-cli.md) — how to actually create/mutate these elements from the CLI
- [Frontend documentation](../frontend/README.md) — customizing the **generated** React once this UI model is in place
````

</details>

cciu:

````markdown
- `judo-model-cli` skill — how to actually create/mutate these elements from the CLI
- Frontend skill — customizing the **generated** React once this UI model is in place
````

