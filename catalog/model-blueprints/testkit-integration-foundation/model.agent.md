# model.md — index

Pull-only condensed map. Source: catalog/model-blueprints/testkit-integration-foundation/model.md.

## Model shape
- Blueprint has no model shape: it is a test module. The page describes module layout, Maven tiers and tooling.
- Structural side only: test module organisation, the tiers (DS / Layer-0 / Layer-1 / Layer-2 / pure-infra), `pom.xml` wiring of surefire, failsafe and `-Pdocker`, tooling (`logback-test.xml`, `.sdkmanrc`, dependency pinning).
- Java code (support classes, IT shapes, gotchas, verbatim source) lives in backend.md.

## Module layout
- Root: `application/integration-test/` with `pom.xml`, `README.md`, `resources/logback-test.xml`, `src/test/`.
- `src/test/java/<pkg>/integration/`: `dscomponent/` (Tier 1, `*Test.java`), `testkit/` (Tier 2, `*IT.java`), `filestore/`, `keycloak/`, `stack/` (Tier 3).
- `testkit/support/`: the 8 reusable scaffolding classes (`TestContext`, `Roles`, `Seed`, `Calls`, `AuditAssertions`, `FieldInjector`, `FoundationModule`, `SdkFunctionRegistry`).
- `testkit/`: `BootIT.java` (smoke, must go green first), `access/` (12 matrix ITs, Phase 2), `operations/` (9 custom-op ITs, Phase 4), `derived/` (3 derived-attribute ITs, Phase 5), `docker/` (Layer-1 and Layer-2 overlays, Phase 6).
- `src/test/resources/realm.json`: Keycloak realm import for Layer-2 and Tier-3.
- Why a separate `testkit/` package: each tier has different runtime and lifecycle needs; keeps surefire/failsafe config simple and lets profiles include or exclude it without `@Tag` indirection.

## Tier model in detail
- Tier 1, DS component: asserts OSGi DS descriptor XML (`@Reference target=` filters, service properties); classpath only; runs on every `mvn test`.
- Tier 2a, Layer-0 testkit: dispatcher path (access manager, actor resolver, JQL filters, custom ops, interceptors), DAO surface; in-process JUDO + HSQLDB; excluded only under `-Pdocker`.
- Tier 2b, Layer-1 docker: external service (e.g. document-converter) swapped from stub to testcontainer; opt-in via `-Pdocker`.
- Tier 2c, Layer-2 docker: JWT to `JudoPrincipal` to dispatcher round-trip; production `AuthenticationInterceptor`; Keycloak testcontainer; opt-in via `-Pdocker`.
- Tier 3, pure infra: contract on one external service (e.g. MinIO sha256 round-trip) or full-stack compose smoke; testcontainers only; opt-in via `-Pdocker`.

### Why two docker overlay sub-tiers (2b / 2c)?
- Same Guice pattern (extend `FoundationModule`, swap one `@Provides` via static flag); different concerns.
- Layer-1 isolates `DocumentConverterClient` (or another backend HTTP client) for PDF-bytes and page-count asserts.
- Layer-2 isolates `AuthenticationInterceptor` wiring to prove claim decoding.
- Gotcha: do not subclass-override `@Provides` (`DUPLICATE_BINDING`); use the static-flag pattern in backend.md.

## `pom.xml` shape
- Parent: `<app>-application`; artifact `<app>-application-integration-test`, packaging jar.
- `dependencyManagement`: pin `logback-core` and `logback-classic` to 1.5.12 (older transitive versions throw `NoSuchMethodError` on `<encoder>`).
- Surefire: `dialect=hsqldb`, `container=none` system properties; `excludedGroups docker`; `excludes **/testkit/docker/**`.
- Failsafe: must declare both `integration-test` and `verify` goals in the child `<plugins>` block; parent `pluginManagement` registers only `integration-test`, so without `verify` failures are invisible to `mvn verify`. Same `dialect`/`container` properties and belt-and-braces exclusions.
- `maven-bundle-plugin` listed in build plugins.
- Dependencies: `<app>-application-sdk`, `-app`, `-internal` at `${project.version}`; `-interceptors` test-scoped so `derived/` ITs can register production interceptors.
- Testkit deps (test scope): `judo-runtime-core-guice-testkit`, `judo-runtime-core-guice`, `judo-runtime-core-guice-hsqldb` (`${judo-runtime-core-version}`), `hsqldb` 2.6.1.
- Test deps: `junit-jupiter`; `mockito-core` and `mockito-junit-jupiter` 3.12.4.
- Testcontainers: `testcontainers`, `junit-jupiter` (`${testcontainers-version}`), `testcontainers-keycloak`, `keycloak-admin-client`.

### Docker profile
- `-Pdocker` requires a running Docker daemon and locally built or pulled images.
- `REQUIRE_DOCKER_IMAGES=1` switches missing-image behaviour from skip to fail (CI); see backend.md, `BaseDockerIT`.

### Docker profile body
- Surefire and failsafe use `combine.self="override"` to clear `excludedGroups` and `excludes`, then set positive `<groups>docker</groups>`.
- Positive scoping stops the profile from re-running the whole Layer-0 suite.

### Key `pom.xml` decisions
- Failsafe `:verify` must sit in the child plugins block; verify with a deliberately broken IT that `mvn -pl <module> verify` fails.
- Keep both tag and path exclusion; either alone has leaked.
- `combine.self="override"` plus positive groups is what lets docker tests run.
- `dialect=hsqldb` and `container=none` must be set on both surefire and failsafe; surefire-only ITs fail with a different default dialect.
- Force one Logback 1.5.x in `dependencyManagement`.

## Tooling
- `src/test/resources/logback-test.xml`: STDOUT console appender, root INFO, project package DEBUG, WARN for hibernate, hsqldb and liquibase loggers.
- `.sdkmanrc`: `java=21.0.7-zulu`, `maven=3.9.10`, `mvnd=1.0.2`. Java 17 fails on pattern-matching switch; Maven 3.6 fails on `combine.self`.
- Run commands: `mvn -pl application/integration-test verify` (default, no Docker); `-Pdocker verify` (Layer-1, Layer-2, pure-infra); `REQUIRE_DOCKER_IMAGES=1 ... -Pdocker verify` (CI fail-fast).
- Local prerequisite for Layer-1: build `document-converter:dev` from `services/document-converter` (CI does this as a pre-step).
