---
id: "karaf-customization-via-fragments"
title: "Karaf Customization via Generator Fragment Overrides"
domain: "backend"
category: "config"
score: 0
usage_count: 2
alternative_count: 0
first_seen: "2026-05-12"
last_updated: "2026-05-12"
projects:
  - compsych-letter-demo
  - rackinspect
alternatives: []
---
## Description

Customize the JUDO `karaf-features` module (extra bundles, extra repositories,
extra Maven plugins / dependencies, OSGi config PIDs) **without editing the
generated `feature.xml` or `pom.xml` files**. The generator emits these files
with named override slots — each slot is a Handlebars fragment file the
developer creates. On the next generator run the generated XML is rewritten,
but the fragment files are preserved and spliced back in at the corresponding
marker, so customizations survive regeneration.

This is the backend / deployment analog of the frontend patterns
`generator-override-extra-dependencies`,
`handlebars-generator-template-override`, and
`i18n-generator-override-extra-fragment`.

**Anti-pattern**: editing `application/karaf-features/src/main/feature/feature.xml`,
`application/karaf-features/pom.xml`, or any module's `pom.xml` directly. These
files are overwritten on every `./judo.sh build` (or `judo generate`) run. The
only ways to survive regeneration are (a) the fragment-override hook
(preferred) or (b) listing the file in `.generator-ignore` (escape hatch — see
`generator-ignore-config-protection`). Always try the fragment hook first
because it keeps the generated artifact authoritative.

## Structure

### 1. Fragment-file layout

All fragment overrides live under `application/generator-overrides/` at the
same relative path as the upstream template's `*.fragment.hbs` file. The
root `pom.xml` registers
`${maven.multiModuleProjectDirectory}/application/generator-overrides` as a
template-search URI on the `judo-esm-generator-maven-plugin` invocation,
so any file placed there shadows the upstream template default at the
matching path.

| Target | Override path |
|---|---|
| `application/karaf-features/src/main/feature/feature.xml` | `application/generator-overrides/karaf-features/src/main/feature/feature.xml.<slot>.fragment.hbs` |
| `application/<module>/pom.xml` | `application/generator-overrides/<module>/pom.xml.<slot>.fragment.hbs` |
| application-root `pom.xml` | `application/generator-overrides/pom.xml.<slot>.fragment.hbs` |

Layout matches the established `generator-overrides/ui-react/...` frontend
convention, so backend and frontend customizations sit side-by-side in the
same directory tree.

The slot name in `<slot>` matches the path quoted inside the `<!-- To define
create '<path>' file -->` marker comment in the generated artifact. Spelling
is load-bearing; typos are silently ignored.

**Verification recipe** after creating or moving a fragment file:

1. Run `./judo.sh generate` (no `-i`).
2. `git diff` the regenerated artifact — the fragment content should appear
   between the placeholder marker comments. If the markers are still empty,
   the path or slot name does not match the template; check the marker
   comment text in the generated artifact for the exact path the generator
   expects.

### 2. Override hooks in generated `feature.xml`

Generated path: `application/karaf-features/src/main/feature/feature.xml`. The
generator emits three named slots inside the `<features>` / `<feature>` blocks:

| Slot | Fragment file name | Use for |
|---|---|---|
| `extra-repositories` | `feature.xml.extra-repositories.fragment.hbs` | additional `<repository>mvn:.../xml/features</repository>` URIs |
| `extra-bundles` | `feature.xml.extra-bundles.fragment.hbs` | extra `<bundle>` lines, `<feature>` dependencies, **and inline `<config>` blocks** (see §4 — the recommended way to ship OSGi PID configuration) |
| `model-bundles` | `feature.xml.model-bundles.fragment.hbs` | replace / extend the generated model + sdk + internal + app + rest + frontend bundle block (rare; only when reordering or excluding a model bundle) |

### 3. Override hooks in generated `pom.xml`

Every generated module pom (`karaf-features`, `app`, `interceptors`, `schema`,
`web-root`, `frontend-react`, `integration-test`) carries the same five slots:

| Slot | Fragment file name | Use for |
|---|---|---|
| `project-definition` | `pom.xml.project-definition.fragment.hbs` | override `groupId` / `artifactId` / `name` / `description` / parent coordinates |
| `properties-definition` | `pom.xml.properties-definition.fragment.hbs` | extra `<properties>` (version pins, build flags) |
| `extra-plugin-management` | `pom.xml.extra-plugin-management.fragment.hbs` | `<pluginManagement>` entries |
| `extra-plugins` | `pom.xml.extra-plugins.fragment.hbs` | extra `<build><plugins>` entries |
| `extra-dependencies` | `pom.xml.extra-dependencies.fragment.hbs` | extra `<dependencies>` entries |

A sixth slot, `extra-modules` (`pom.xml.extra-modules.fragment.hbs`), exists on
the application-root pom for adding extra Maven sub-modules.

### 4. Configuring OSGi components — three approaches, ranked

OSGi components consume configuration by `@Component(configurationPid = "<pid>")`.
There are three ways to land that PID at runtime. Use them in this order:

#### 4a. Preferred — inline `<config>` block in `extra-bundles.fragment.hbs`

Place the PID configuration **inside the `<feature>`** via the `extra-bundles`
fragment file:

```xml
<config name="hu.example.MyComponent">
    endpoint=${env:MY_ENDPOINT:-https://localhost:8443}
    username=${env:MY_USER:-admin}
    password=${env:MY_PASSWORD:-changeme}
    timeoutMs=${env:MY_TIMEOUT_MS:-5000}
</config>
```

Why this is the default choice:

- **Env-var substitution at install time.** `${env:VAR:-default}` is resolved
  by Karaf's feature installer from the JVM process environment when the
  feature is installed. `judo.sh` populates that environment from
  `judo-karaf.env`, so the same `feature.xml` works in dev / staging / prod by
  changing the env file alone — no rebuild required.
- **Self-contained defaults.** Missing env-vars degrade to the inline
  fallback, so a fresh checkout boots cleanly with no env-file edits.
- **PID is guaranteed to be registered.** Consuming components can use
  `configurationPolicy = ConfigurationPolicy.REQUIRE` and rely on the config
  being present at activation time.
- **No assembly-time packaging.** Travels with the feature; the Karaf feature
  installer registers it into OSGi Config Admin directly.
- **Self-documenting wiring.** The PID name sits next to the bundle that
  consumes it, so reviewers see the full picture in one place.

#### 4b. Fallback — `karaf-features/etc/<pid>.cfg`

Plain `.cfg` files in `application/karaf-features/etc/` are picked up by the
karaf-maven-plugin during feature/distribution assembly. Use this only when:

- the value cannot be expressed as env-var substitution (e.g. a multi-line
  PEM cert), and
- the project's `karaf-offline` assembly is configured to package
  `karaf-features/etc/` into the runtime Karaf `etc/` (verify by checking
  `karaf-offline/pom.xml` for a resource copy targeting `etc/`).

> **Caveat — silent miswiring**: if the assembly does **not** package
> `karaf-features/etc/`, the `.cfg` never reaches Config Admin and
> `configurationPolicy = REQUIRE` components silently stay inactive. Either
> wire the assembly step, switch to `configurationPolicy = OPTIONAL` with
> `@Component property` defaults, or — preferably — migrate to approach 4a.

#### 4c. Last resort — `.generator-ignore` + direct edit

Add `feature.xml` (or the relevant pom) to `.generator-ignore` and hand-edit.
Only when no fragment slot exposes the location you need. Accept that future
generator changes must be merged by hand; see
`generator-ignore-config-protection`.

### Decision matrix

| You want to… | Use |
|---|---|
| Add a third-party OSGi bundle to the runtime | `feature.xml.extra-bundles.fragment.hbs` (one `<bundle>mvn:…</bundle>` per line) |
| Pull in an existing Karaf feature (e.g. `epsilon-runtime`, `judo-platform-export-jxls`) | `feature.xml.extra-bundles.fragment.hbs` with `<feature>name</feature>` — if the feature repo is outside `judo-platform-karaf-features`, also add it via `feature.xml.extra-repositories.fragment.hbs` |
| Configure an OSGi component with env-var-overridable values (DB URL, API keys, endpoints, timeouts, feature flags) | inline `<config>` block in `feature.xml.extra-bundles.fragment.hbs` using `${env:VAR:-default}` — **preferred** (see §4a) |
| Configure an OSGi component with values that env-vars can't express (multi-line cert, large blob) | `karaf-features/etc/<pid>.cfg` — only if the assembly packages `etc/` (see §4b) |
| Pin a Maven property (e.g. `cxf-version`) across the karaf-features build | `karaf-features/pom.xml.properties-definition.fragment.hbs` |
| Add a Maven plugin execution (license check, formatter) | `<module>/pom.xml.extra-plugins.fragment.hbs` |
| Add a Java compile-time dependency to a generated module | `<module>/pom.xml.extra-dependencies.fragment.hbs` |
| Add an extra Maven sub-module under `application/` (e.g. `common/`, `scheduler/`, `keycloak-client/`) | application-root `pom.xml.extra-modules.fragment.hbs` |
| Customize the `karaf-offline` assembly (startup features, boot features, javase) | `karaf-offline/pom.xml` is typically **not** regenerated after first scaffold. Verify by checking whether it carries `fragment.hbs` markers — if not, edit directly. Otherwise treat as a fragment-driven module. |

## Examples

### rackinspect

Centralized `application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs`
demonstrates the full set of techniques in one file:

- **Extra features** pulled from the platform repo: `judo-platform-export-jxls`,
  `judo-platform-report-xdocreport`, `epsilon-runtime`.
- **Scheduler stack**: `rackinspect-scheduler` bundle plus
  `org.apache.karaf.scheduler.core` from the Karaf distribution.
- **Inline `<config>` with env-var substitution — Keycloak admin client**:
  ```xml
  <config name="hu.blackbelt.rackinspect.keycloak.osgi.KeycloakFactoryComponent">
      serverUrl=${env:JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL:-http://localhost:8080/auth}
      username=${env:JUDO_PLATFORM_KEYCLOAK_USER:-admin}
      password=${env:JUDO_PLATFORM_KEYCLOAK_PASSWORD:-judo}
      realm=${env:JUDO_PLATFORM_KEYCLOAK_REALM:-master}
      clientId=${env:JUDO_PLATFORM_KEYCLOAK_CLIENT_ID:-admin-cli}
  </config>
  ```
  Five values come from `judo-karaf.env` at runtime; defaults are sane for
  local dev. `KeycloakFactoryComponent` uses `configurationPolicy = REQUIRE`
  and activates as soon as the feature is installed.
- **Inline `<config>` — bootstrap admin users** (env-only, empty default):
  ```xml
  <config name="hu.blackbelt.rackinspect.admin.bootstrap">
      admins = ${env:RACKINSPECT_ADMIN_USERS:-}
      adminPassword = ${env:RACKINSPECT_ADMIN_PASSWORD:-}
  </config>
  ```
- **Inline `<config>` — Quartz job schedules** (literal cron, no env-vars):
  ```xml
  <config name="updateExchangeRatesConfig">
      scheduler.expression=0 0 13 ? * MON,TUE,WED,THU,FRI *
      scheduler.concurrent=false
  </config>
  ```
- **Inline `<config>` — servlet path + base URL** (compose env-var into multiple PIDs):
  ```xml
  <config name="hu.blackbelt.rackinspect.common.photo.PhotoServlet">
      servletPath=${env:RACKINSPECT_PHOTO_SERVLET_PATH:-/photos}
  </config>
  <config name="hu.blackbelt.rackinspect.common.photo.PhotoUrlServiceImpl">
      baseUrl=${env:RACKINSPECT_PHOTO_BASE_URL:-http://localhost:8181}
      servletPath=${env:RACKINSPECT_PHOTO_SERVLET_PATH:-/photos}
  </config>
  ```

rackinspect also exercises `pom.xml.properties-definition.fragment.hbs` and
`pom.xml.extra-dependencies.fragment.hbs` under
`application/generator-overrides/karaf-features/` and `…/app/`, `…/interceptors/`,
plus a top-level `application/generator-overrides/pom.xml.extra-modules.fragment.hbs`
that registers the extra Maven sub-modules (`common`, `mnb-soap-client`, `report`,
`scheduler`, `keycloak-client`, `resteasy`, `test`) which are not part of the
generated project skeleton.

### compsych-letter-demo

Centralized `generator-overrides/` layout — fragments live under
`application/generator-overrides/...` at the same relative path as the
upstream template's `*.fragment.hbs`. Two overrides exercised so far:

1. **Add `cxf-rt-rs-sse/3.5.6` bundle for the agent REST endpoint's
   Server-Sent Events provider** (`openspec change wire-agent-rest-endpoint`).
   The platform's `judo-platform-cxf-jaxrs` feature ships
   `cxf-rt-frontend-jaxrs/3.5.6` but not `cxf-rt-rs-sse`; the SSE API types
   (`javax.ws.rs.sse.Sse`, `SseEventSink`, `OutboundSseEvent`,
   `SseBroadcaster`) are on the classpath via the platform's
   `jakarta.ws.rs-api/2.1.6`, but the runtime implementation is a separate
   bundle. File:
   `application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs`
   carrying a single `<bundle>mvn:org.apache.cxf/cxf-rt-rs-sse/3.5.6</bundle>`
   line plus a comment block. On the next `./judo.sh generate` the
   regenerated `application/karaf-features/src/main/feature/feature.xml`
   has the bundle line inlined between the
   `<!-- To define create 'karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs' file -->`
   markers; the `karaf-offline` assembly subsequently packages
   `cxf-rt-rs-sse-3.5.6.jar` into
   `target/assembly/system/org/apache/cxf/cxf-rt-rs-sse/3.5.6/`.
   Rejected alternatives captured in the design doc: editing `feature.xml`
   directly (merge pain), referencing a non-existent `cxf-rt-rs-sse` Karaf
   feature, upgrading the platform's vendored CXF version.
   See also: `custom-jaxrs-sse-endpoint`.
2. **Document-converter and LLM provider PID configuration**
   (`openspec changes wire-document-converter-client`, `wire-llm-provider`).
   Files: `application/karaf-features/etc/org.blackbelt.compsych.letter.converter.cfg`
   and `…llm.cfg`. **This is the §4b fallback path and is currently
   miswired** — the `karaf-offline` assembly does not package
   `karaf-features/etc/`, so these `.cfg` files never reach the runtime Karaf
   `etc/`. Consuming components compensate via `configurationPolicy=OPTIONAL`
   plus `@Component property` defaults. **Recommended remediation**: migrate
   both PIDs to inline `<config>` blocks in
   `feature.xml.extra-bundles.fragment.hbs` with `${env:…:-default}`
   substitution (the §4a pattern rackinspect uses), then drop the
   `configurationPolicy=OPTIONAL` workaround and the unused `etc/*.cfg`
   files. Tracked as a future cleanup.
3. **`internal/pom.xml` hand-edited dependencies** (LangChain4j,
   Spring SpEL, SnakeYAML, jakarta.ws.rs-api). The upstream
   `judo-esm-fullstack-project-template-application` `internal/pom.xml.hbs`
   does NOT expose an `extra-dependencies.fragment.hbs` slot — the
   `<dependencies>` block is emitted verbatim with no override hooks. The
   only way to preserve hand-edits is the §4c last-resort path: add
   `internal/pom.xml` to `application/.generator-ignore` (matches the
   existing `integration-test/pom.xml` precedent in the same file). NB:
   `./judo.sh generate -i` SILENTLY DROPS hand-edits to any
   non-ignored generated file — always add the path to
   `.generator-ignore` BEFORE running with `-i`, or commit-stash the
   edits so `git checkout HEAD -- <file>` is the recovery. See
   `generator-ignore-config-protection` for the precedent.

## Trade-offs

- **Pros**: customizations survive `./judo.sh build` regeneration; the
  generated XML remains the authoritative description, so diffs review
  cleanly; no `.generator-ignore` entry needed; inline `<config>` plus
  `${env:VAR:-default}` makes per-environment overrides a `judo-karaf.env`
  edit instead of a rebuild; PID + bundle wiring self-documents in one
  location.
- **Cons**: only the slots the generator emits are available — you cannot
  insert content at an arbitrary location in `feature.xml` / `pom.xml`; for
  that you must fall back to `.generator-ignore` and accept manual merge on
  every regen; fragment-file naming is precise (typo → silently ignored, no
  build error), the marker comment is the source of truth. **`./judo.sh
  generate -i` is destructive**: it force-overwrites every checksum-drifted
  generated file with the template's output, silently dropping hand-edits;
  use it ONLY to refresh checksums after you have already moved your
  changes into either a fragment override OR a `.generator-ignore` entry.
- **Alternative**: list the generated file in `.generator-ignore`
  (`generator-ignore-config-protection`) and hand-edit. Use only when no
  fragment slot exists — e.g. `application/internal/pom.xml` on the
  current generator version, which lacks an `extra-dependencies.fragment.hbs`
  hook.

## Related Patterns

- [osgi-karaf-bundle-architecture](osgi-karaf-bundle-architecture.md) —
  architectural context for the `karaf-features` / `karaf-offline` modules.
- [generator-ignore-config-protection](generator-ignore-config-protection.md) —
  escape hatch when no fragment hook exists.
- [generator-override-extra-dependencies](../frontend/generator-override-extra-dependencies.md) —
  frontend twin pattern for `package.json` dependencies (same mechanism,
  frontend side).
- [handlebars-generator-template-override](../frontend/handlebars-generator-template-override.md) —
  broader generator-override discussion (frontend-side).
- [i18n-generator-override-extra-fragment](../frontend/i18n-generator-override-extra-fragment.md) —
  frontend-side fragment override for translations.
- [quartz-scheduled-job](quartz-scheduled-job.md) — uses inline
  `<config>` blocks (`scheduler.expression`, `scheduler.concurrent`) authored
  via this pattern.
- [magic-link-authentication](magic-link-authentication.md), [email-service-integration](email-service-integration.md) —
  examples of `configurationPolicy = REQUIRE` components that rely on the
  PID being registered at feature-install time (§4a).
