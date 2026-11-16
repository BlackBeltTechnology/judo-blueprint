---
id: osgi-karaf-bundle-architecture
title: OSGi Bundle Architecture with Karaf Deployment
description: How a JUDO application is split into OSGi bundles deployed to Apache Karaf (generated model, sdk, internal, rest bundles plus custom app and interceptor bundles) and the extra modules projects add on top.
aliases: [Karaf modules, bundle layout, application module structure]
keywords: [osgi, bundle, architecture, karaf, deployment, module, feature, declarative services, hot deployment]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:mlszksz-platform", "project:viterra_demo", "project:bhs-global-operation", "project:mjsz", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:InterfaceRegister", "project:judo-partner", "project:workflow-poc", "project:reserve-app", "status:established"]
category: config
status: established
projects: [trivia, rackinspect, itracker, alba, mlszksz-platform, viterra_demo, bhs-global-operation, mjsz, judo-demo-miniworkflow, ubives, park-here, indamedia-adtrack, InterfaceRegister, judo-partner, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:application/karaf-features/src/main/feature/feature.xml", "itracker:unrecorded", "alba:unrecorded", "mlszksz-platform:application/karaf-features/src/main/feature/feature.xml", "viterra_demo:unrecorded", "bhs-global-operation:unrecorded", "mjsz:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "InterfaceRegister:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A JUDO application is a set of OSGi bundles running in Apache Karaf: platform-generated bundles plus a small number of custom bundles. Know which bundles are generated, which are yours, and where applications add their own modules, so custom code lands in the right place and survives regeneration.

## Practice

### Platform: generated and custom modules

- Generated, not to be edited: SDK interfaces and DAOs (`application/sdk`), internal SDK wrappers (`application/internal`), REST endpoints (`application/rest`) and the compiled model. Custom code lives in `application/app` (operation implementations) and `application/interceptors` ([backend overview](../../agent-docs/backend/README.md#architecture)).
- Checksums guard the generated files: editing one makes the build fail unless the file is listed in `.generator-ignore`. Prefer generator parameters or the fragment-override hooks for pom and feature files ([build process](../../agent-docs/deployment/build-process.md)); see [[generator-ignore-config-protection]].
- Custom implementations register as OSGi Declarative Services components with `@Component(immediate = true, service = <OperationInterface>.class)` ([OSGi component registration](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)); see [[custom-operation-osgi-component]]. An interceptor component must carry the property `judo.model.name=<app>` to bind to its model ([key patterns](../../agent-docs/backend/authentication-guide.md#key-patterns-in-the-example)).
- A model is deployed either as raw files or as an OSGi bundle with a `Judo-Models` manifest header; the model bundle tracker then loads the `model/<name>-*.model` resources ([deploying a model as an OSGi bundle](../../agent-docs/deployment/osgi-runtime-services.md#deploying-a-model-as-an-osgi-bundle)).
- `application/karaf-features` aggregates the bundles into a Karaf feature (extra bundles are added through the feature fragment hooks) and `application/karaf-offline` assembles the distribution; the Karaf `etc/*.cfg` files are overwritten on rebuild, so configure through environment variables ([application config](../../agent-docs/deployment/application-config.md)).
- Hot deployment lets backend changes reach a running Karaf without a restart; `JUDO_PLATFORM_BUNDLE_WATCHER=false` turns bundle watching off, and reckless mode is the fast development build ([build process](../../agent-docs/deployment/build-process.md#reckless-mode)). If a change does not show up, the [debugging guide](../../agent-docs/backend/debugging-and-monitoring-guide.md) covers the stale-bundle case.

### Practice notes: extra modules next to the generated ones

The baseline layout (model, sdk, internal, app, interceptors, rest, schema, docker, karaf-features, karaf-offline, plus frontend bundles) is the same across applications. Larger ones add their own bundles:

- `common` for shared services used by `app` and `interceptors` (several applications).
- `scheduler` for scheduled jobs and their activators ([[quartz-scheduled-job]]).
- Integration-client bundles that isolate third-party libraries: SOAP, XSD-generated JAXB clients, Google Ads, email provider wrappers ([[external-api-adapter-pattern]]).
- Keycloak bundles: admin client, magic-link authenticator, login theme ([[multi-tenant-keycloak-realm]], [[magic-link-authentication]]).
- An `integration-test` module, and `generator-overrides` for pom and feature fragments.
- Extra third-party bundles (Tika, PDFBox, CXF, Handlebars, JODConverter) are added to the Karaf feature.
- When a bundle injects services from another custom bundle (for example interceptors using an app-level service), start order and package exports must allow it.

## Rationale

- Each concern is its own bundle with its own dependencies, so a heavy library stays out of the app bundle and the generated bundles remain untouched.
- Declarative Services wires components at runtime, and hot deployment shortens the edit loop.
- Cost: OSGi class-loading and bundle-lifecycle problems, and the runtime is harder to debug than a plain application. Applications reported both (for example the composite class loader needed for the Keycloak admin client).

## Example

The smallest observed applications (a blank skeleton, a demo, a simple register) use only the generated layout with empty custom directories. A mid-size application adds `common`, `scheduler` and one integration client. The largest adds Keycloak client and magic-link bundles, a mail wrapper, an integration-test module and generator overrides. One older application used Pax CDI with Weld instead of Declarative Services and had no interceptors or internal module; new applications use the Declarative Services layout above. Java 17 or 21 with the Eclipse compiler and Karaf 4.4.x were the versions in use.

## When to avoid

- Do not split into more custom bundles than the code needs; an application that only has a few operations should stay with `app` and `interceptors`.
- Do not hand-edit generated bundle sources to add behaviour; use a custom implementation, an interceptor, or a generator fragment.
- If the target runtime is the Spring Boot variant instead of Karaf, the bundle layout does not apply ([Spring Boot runtime](../../agent-docs/deployment/spring-boot-runtime.md)).

## Related

- [[custom-operation-osgi-component]] — how a custom operation registers as a component
- [[generator-ignore-config-protection]] — keeping hand-edited generated files from being overwritten
- [[quartz-scheduled-job]] — scheduler bundle
- [[external-api-adapter-pattern]] — client bundles for external APIs
