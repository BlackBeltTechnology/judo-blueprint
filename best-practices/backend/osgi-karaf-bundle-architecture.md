---
id: "osgi-karaf-bundle-architecture"
title: "OSGi Bundle Architecture with Karaf Deployment"
domain: "backend"
category: "config"
score: 60.7
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

## Related Patterns

- custom-operation-osgi-component
- generator-ignore-config-protection
