---
id: "osgi-karaf-bundle-architecture"
title: "OSGi Bundle Architecture with Karaf Deployment"
domain: "backend"
category: "config"
score: 83.2
usage_count: 16
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - mlszksz-platform
  - viterra_demo
  - bhs-global-operation
  - mjsz
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

The application is structured as multiple OSGi bundles deployed to Apache Karaf. Each module (app, interceptors, SDK, internal, REST, frontend) is a separate bundle. Services are discovered and wired at runtime via OSGi Declarative Services. Karaf features aggregate bundles for deployment. Development supports hot-reload via bundle watching.

## Structure

Bundle modules:
- `application/model` -- Compiled model + script2operation mapping
- `application/sdk` -- Generated SDK (API interfaces, DAOs, DTOs)
- `application/internal` -- Generated internal wiring
- `application/app` -- Custom operation implementations
- `application/interceptors` -- Custom interceptors
- `application/rest` -- Generated REST endpoints
- `application/frontend-react` -- Frontend bundles
- `application/karaf-features` -- Feature descriptors aggregating bundles
- `application/karaf-offline` -- Offline Karaf distribution

Karaf feature XML declares bundle dependencies and deployment order.

## Examples

### Trivia
11 modules built as OSGi bundles. Karaf feature `trivia-application-judo-platform-prototype` based on `judo-platform-default-sdk`. Includes additional bundles: Apache Tika, PDFBox, JSON.org, Apache Sling. 8 application bundles deployed. Development uses `judo.sh reckless` for fast hot-reload.

### RackInspect
17+ modules including dedicated `common/` (shared services), `mnb-soap-client/` (SOAP integration), `report/` (XDocReport), `scheduler/` (Quartz), and `test/` (integration tests). Additional third-party bundles for CXF, Handlebars, JODConverter. Significantly more modular than Trivia.

### itracker
Standard 9-module architecture (model, sdk, internal, app, interceptors, rest, docker, karaf-features, karaf-offline) plus 2 frontend bundles. Feature `itracker-application-judo-platform-prototype` includes Apache Tika and PDFBox. Interceptors module scaffolded but empty. Demonstrates the minimal baseline JUDO OSGi/Karaf deployment.

### ALBA
Full OSGi/Karaf stack with modules for model, sdk, internal, app, interceptors, rest, schema, docker, karaf-features, plus dedicated keycloak-theme and generator-overrides modules. Runtime on Karaf 4.4.6 with PostgreSQL 16.2 and Keycloak 23.0. Docker Compose deployment with health-check dependency chain.

### mlszksz-platform
15+ modules: app (65+ custom ops), common (15+ services), interceptors (5), scheduler (4 jobs), keycloak-client, keycloak-extensions (magic link authenticator), integration-test (20+ test classes), sdk, model, rest, resteasy, web-root, schema, karaf-features, karaf-offline, docker. Dedicated modules for Keycloak integration and scheduled jobs. Java 21 with ECJ compiler.

### viterra_demo
Standard 10-module layout: model, sdk, internal, app, interceptors, rest, schema, karaf-features, karaf-offline, docker, plus 2 React frontend bundles (admin + partner portals). Karaf feature includes Apache Tika, PDFBox, JSON.org, Apache Sling bundles. Java 17 with ECJ compiler. Karaf 4.4.5, PostgreSQL 16.2, Keycloak 23.0. Template/demo project demonstrating the baseline JUDO architecture.

### bhs-global-operation
Minimal blank-slate project with standard 10-module layout (model, sdk, internal, app, interceptors, rest, schema, docker, karaf-features, karaf-offline). All custom code directories empty. Java 17 with ECJ compiler, Karaf 4.4.5, PostgreSQL 16.2, Keycloak 23.0. Includes Apache Tika, PDFBox, JSON.org, and Apache Sling bundles in Karaf feature. Demonstrates the generated project skeleton before any business logic is added.

### mjsz
Older JUDO stack variant (2022) using Pax CDI 1.1.3 with Weld instead of OSGi DS for dependency injection. Simplified module layout: model, sdk, app, schema, karaf-features, karaf-offline, docker, plus Flutter frontend bundle. No dedicated interceptors or internal modules. Karaf 4.3.4, Java 11, Hsqldb default. Feature includes Apache Tika, PDFBox, JSON.org, Apache Sling. App bundle empty (gitkeep only). Demonstrates the earlier-generation JUDO project skeleton with CDI-based DI.

### judo-demo-miniworkflow
Standard 10-module layout: model, sdk, internal, app, interceptors, rest, schema, karaf-features, docker, plus React frontend bundle. Karaf feature `miniworkflow-application-judo-platform-prototype` based on `judo-platform-default-sdk`. Includes Apache Tika, PDFBox, and script2operation bundle. Java 17 with ECJ compiler, Karaf 4.4.5, PostgreSQL 16.2, Keycloak 23.0. Deployment via `judo.sh build start` with Docker Compose (dev and production with Traefik SSL).

### Ubives
12+ modules: app (42 custom ops + 7 services), interceptors (2 auth interceptors), keycloak-client (Keycloak admin API), keycloak-magic-link (magic link SPI), keycloak-theme, sendgrid (email wrapper), sdk, model, rest, resteasy, schema, karaf-features, karaf-offline, docker, web-root. Java 17, Karaf 4.4.7, PostgreSQL+HSQLDB. Dedicated modules for Keycloak integration (client + magic link) and SendGrid email. Separate `face-recognitation/` directory with Python Flask face recognition backend.

### ParkHere
12+ modules: app (20 custom ops), common (7 services), interceptors (7 interceptors), scheduler (3 jobs + RDBMS activator), sdk, model, internal, rest, schema, karaf-features, karaf-offline, docker, frontend-react. Java 17 with ECJ compiler and Lombok. Generator overrides for app, interceptors, and karaf-features POM/feature fragments. Karaf feature includes i18n bundles, scheduler bundles, and common service bundle. PostgreSQL/HSQLDB dual dialect support.

### Indamedia-AdTrack
14+ modules: app (17 custom ops), common (6 services + utils + i18n), interceptors (1 auth interceptor), scheduler (4 jobs + 2 activators), adapters/ads-business-api (API abstraction), adapters/google-ads (Google Ads v20 integration), sdk, model, internal, rest, schema, karaf-features, karaf-offline, docker, frontend-react. Java 21 with ECJ compiler. Karaf 4.4.7, PostgreSQL/HSQLDB. Dedicated adapter modules for external API integration with Google Ads SDK 38.0.0. Includes Guava 33, google-api-ads, and Apache Tika features.

### InterfaceRegister
Standard module layout: model, sdk, internal, app, schema, karaf-features, karaf-offline, docker, plus React frontend bundle. Karaf feature `interfaceregister-application-judo-platform-prototype` based on `judo-platform-default-sdk`. Includes Apache Tika, PDFBox, JSON.org, Apache Sling bundles. Java 17, Karaf 4.4.3, PostgreSQL/HSQLDB dual dialect. No dedicated interceptors or common module. Bundle start order: model -> sdk -> internal -> app. Deployment via Docker Compose with Traefik reverse proxy and Keycloak.

### judo-partner
12+ modules: app (15 custom ops + 7 services + 7 utils), interceptors (3 interceptors in separate bundle), navonline-client (JAXB-generated NAV Online API v3.0 client), sdk, internal, model, schema, rest, web-root, karaf-features, karaf-offline, docker, frontend-react. Java 17 with ECJ compiler. Karaf 4.4.7. Dedicated `navonline-client` bundle with XSD-generated JAXB classes. Interceptors bundle depends on app bundle for `PartnerServices` injection.

### workflow-poc
Standard module layout: model, sdk, internal, app, interceptors, rest, schema, web-root, docker, karaf-features, karaf-offline, plus React frontend bundle. App module contains 4 custom operations and 2 utility services. Interceptors module contains default templates only (`.java.default`). Java 17 with ECJ compiler (`plexus-compiler-eclipse`). HSQLDB default with PostgreSQL support. Uses `mvnd` for builds.

### ReserveApp
Standard 10+ module layout: model, sdk, internal, app (empty -- no custom operations), interceptors (2 hand-written interceptors), rest, schema, web-root, karaf-features, karaf-offline, docker, plus 5 React frontend bundles (one per actor). Java 17 with ECJ compiler. Karaf 4.4.7, PostgreSQL/HSQLDB dual dialect. Interceptors-only customization approach with zero custom Java operations. 5 actor-specific frontends (Admin, Partner, Logistician, Doorman, Readonly).

## Trade-offs

- Pros: Hot deployment, modular architecture, service isolation, runtime wiring flexibility
- Cons: OSGi complexity (classloader issues, bundle lifecycle), harder to debug than monolithic apps
- Alternative: Spring Boot monolith, Docker container per service (microservices)

## Hot-Reload Caveats (Observed)

These are operational gotchas that have surfaced on live JUDO-Karaf deployments. Worth knowing before relying on hot reload.

### 1. `judo.sh start` extracts the karaf-offline tarball; m2-only installs are NOT picked up

`./judo.sh start` (and `judo.sh build start`) extract
`application/karaf-offline/target/<app>-application-karaf-offline-<version>.tar.gz`
into `application/.karaf/`. The system bundles served at startup come from
that tarball's `system/` tree, NOT from `~/.m2/repository/`.

Consequence: `mvn -o install -DskipTests -pl application/internal` updates
the m2 cache but the next `./judo.sh start` boots with the **previous**
bundle from the karaf-offline assembly. Symptoms: code change appears to
have no effect; `unzip -p .karaf/data/cache/bundle<N>/version*/bundle.jar`
shows the old class file even though the source compiles correctly.

**Fix**: rebuild the assembly after the module change:

```bash
mvn -o install -DskipTests -pl application/internal,application/karaf-features,application/karaf-offline
```

or run a full `./judo.sh build -F -M` (skip frontend + model regen) when
the code change is in a backend module. `mvnd`-based incremental builds
are fine — just make sure `karaf-offline` is part of the build reactor.

### 2. `bundle:watch` hot-reload of a bundle with split-package stubs breaks all components in that bundle

Karaf's `bundle:watch` re-installs a bundle in place when its file
changes. This **shifts OSGi package wires** that were resolved at the
original cold-boot time.

If a hand-written class lives in a package that another bundle exports
("split package"), the cold-boot wiring usually resolves the package to
the bundle that defines that class. After a `bundle:watch` reload, the
resolver may shift the wire to the *other* bundle, which doesn't carry
the hand-written class — SCR reflection over the reloaded bundle's
components fails with `ClassNotFoundException` for the missing class,
cascading to `Field [...] not found; Component will fail` errors for
every `@Reference` in that bundle.

**Concrete example (compsych-letter-demo)**: the temporary stub
`BusinessErrorException.java` lives in
`application/internal/src/main/java/.../services/businesserror/` while
the SDK bundle exports the same package without that class. Cold boot:
resolver picks `internal` as the package provider, all components
activate fine. `bundle:watch` after `mvn install`: resolver picks `sdk`,
ALL components in `internal` fail (`SpelEvaluatorImpl`,
`YamlParserImpl`, `HttpDocumentConverterClient`,
`InMemoryDocumentConverterClient`, `LangChain4jLlmProvider`,
`MockLlmProvider`, `ChatSessionStore`, `AgentRestResource`).

**Workarounds**:

1. **Cold restart instead of hot reload** when the bundle contains
   split-package stubs: `pkill -f karaf.main.Main && ./judo.sh start -K`
   (assumes postgres + keycloak already running).
2. **Eliminate the split package** by either embedding the missing
   classes into the bundle (`<Conditional-Package>` or
   `<Embed-Dependency>` in maven-bundle-plugin instructions) or by
   moving the hand-written class into a package that no other bundle
   exports.
3. **Replace the hand-written stub** with the generator-emitted class
   as soon as the model declares an operation that uses it (for the
   `BusinessErrorException` example: the first Wave-3 operation that
   declares `BusinessError` as a fault).

This caveat applies to any JUDO project that carries hand-written
stand-ins for not-yet-generated SDK classes. It is invisible until the
first `bundle:watch` reload, because cold boot always works.

### 3. Cold restart requires a fresh schema check loop on schema drift

The platform refuses to complete startup if the running database is
behind the compiled RDBMS model. Symptoms in `console.out`:

```
WARN  Retry N - Waiting for compatibility schema model
WARN  Error message There are RDBMS model changes which have not been applied to database
DATABASE HAVE TO BE UPDATED!
Create table operation: <model>.entities.<Entity> - T_ENTITIES_<ENTITY>
```

The model deployer retries indefinitely; REST endpoints never register;
`/api/agent/chat` etc. return 404 even though the bundle is installed.

**Fix**: either `./judo.sh schema-upgrade` (PostgreSQL only —
generates and applies the difference) or `./judo.sh clean` (DESTRUCTIVE,
wipes the postgres docker volume; only acceptable for dev environments).

## Related Patterns

- custom-operation-osgi-component
- generator-ignore-config-protection
- karaf-customization-via-fragments
- custom-jaxrs-sse-endpoint
