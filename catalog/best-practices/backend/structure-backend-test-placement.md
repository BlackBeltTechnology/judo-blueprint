---
id: structure-backend-test-placement
title: Where Backend Tests Live in the Application Modules
description: Practice for placing backend tests by tier: mock-based unit tests inside the module they test, runtime-backed tests in one separate test module outside the reactor, and end-to-end tests in the profile-gated e2e module.
aliases: [test module layout, test placement, where tests go]
keywords: [test, unit test, integration test, testkit, e2e, src/test, test module, surefire, tag, structure, module]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/test/pom.xml", "rackinspect:application/test/README.md", "rackinspect:application/integration-test/pom.xml", "rackinspect:application/report/AGENTS.md", "rackinspect:application/pom.xml"]
alternatives: []
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Backend tests come in tiers with very different costs: a mock-based unit test runs in milliseconds, a runtime-backed test boots the model runtime and a database, an end-to-end test needs the whole stack. Put each tier in a fixed place, so a plain build stays fast and a reader knows where to look for the test of a class.

## Practice

### Platform base

- Unit tests for interceptors and custom operations that mock DAOs run in the module they belong to with `mvn test` ([running integration tests](../../agent-docs/backend/testing-guide.md#running-integration-tests)).
- Integration tests with the runtime testkit live in a separate test module, not in the generated build profiles, and run after the application artifacts are installed ([running integration tests](../../agent-docs/backend/testing-guide.md#running-integration-tests), [integration testing guide](../../agent-docs/integration-testing/README.md)).
- The generated `e2e` module is built by the `build-e2e` profile and skipped with `-DskipE2E` ([build profiles](../../agent-docs/deployment/build-process.md#build-profiles), [E2E testing](../../agent-docs/e2e-testing/README.md)).

### Practice notes: three tiers, three places

```
application/
├── app/src/test/java/<root>/<feature>/...          tier 1: unit tests of app logic
├── common/src/test/java/<root>/common/<pkg>/...     tier 1: unit tests of shared services
├── report/src/test/{java,resources/data/fixtures}   tier 1: library tests with fixtures
├── test/                                            tier 2: runtime-backed tests, NOT a reactor module
│   ├── pom.xml          parent = <app>-application; depends on sdk, internal, app, interceptors, other bundles
│   ├── README.md        tags, slow suites, how to run a subset
│   └── src/test/java/<root>/
│       ├── <feature>/          one package per business area
│       ├── testdata/           builders and seeders
│       └── testsupport/        test wiring module, capturing stubs, fixtures
└── e2e/                                             tier 3: generated, profile build-e2e
```

- **Tier 1 stays in the module.** A test sits in `src/test/java` under the same package as the class it tests. Fixtures sit in `src/test/resources` of that module.
- **Tier 2 is one module for the whole application**, kept out of the root `<modules>` list and run with `mvn test -f application/test/pom.xml` after `mvn install`. It depends on every bundle it exercises, so it is the only place where `app`, `interceptors`, `scheduler` and client modules meet in one classpath.
- **Packages in tier 2 follow business areas** (`order`, `account`, `user`, `access`), not production modules; shared wiring goes into a `testsupport` package and data builders into `testdata` ([[test-data-builder-factory]], [[integration-test-reflection-injection]]).
- **Tag slow suites** (a full master-data load) and document `-DincludeTags` / `-DexcludeTags` in the test module README, so the fast path is one flag away.
- **Tune surefire in the test module only**: a few reused forks and no in-fork class parallelism when tests share a cached datasource per class.
- **No test resource reaches into a sibling module.** A symlink or relative path from `report/src/test` into `app/src/main/resources` breaks as soon as a module moves; copy the fixture or move the shared resource into the module that owns it.

## Rationale

- The root build, the launcher script build and hot deployment never wait for runtime-backed tests.
- One runtime-test module means one Guice wiring and one datasource configuration instead of one per bundle.
- Cost: tier 2 runs against installed artifacts, so a stale jar in the local repository can hide a change; install before testing ([multi-module build order](../../agent-docs/deployment/build-process.md#stale-artifacts-and-multi-module-build-order)).

## Example

One application has unit tests in `app` (pricing logic), `common` (utility services) and `report` (renderer with fixture data). Its `test` module holds many runtime-backed test classes, plus helper and builder classes, grouped by business area, a `testsupport/wiring` package with the services test module and capturing stubs for e-mail and history, and a README that lists the tagged slow init-data suites. A second, older `integration-test` module (DAO integration tests) is also outside the reactor and holds only a pom; keeping two such modules invites confusion, so new tests go into one. The generated `e2e` module stays in the reactor behind `build-e2e`.

A test-data seeder component lives in `app/src/main` (package `testdata`) so it can run in a deployed environment. Production code that only serves tests should be switched off by configuration or moved into its own bundle that production does not install.

## When to avoid

- An application with a few operations and no runtime-backed tests needs no separate test module.
- Tests that need a browser belong in `e2e`, not in the runtime test module.

## Related

- [[testkit-integration-foundation]] — pom and fixtures of a runtime-backed test module
- [[test-data-builder-factory]] — builders that live in `testdata`
- [[integration-test-reflection-injection]] — wiring custom components into runtime tests
- [[structure-custom-module-dependency-direction]] — which modules the test module depends on
