---
id: structure-third-party-wrapper-bundle
title: Wrapper Module That Repackages a Non-OSGi Library as a Bundle
description: Practice for a code-free Maven module under application/ that embeds a third-party library which has no usable OSGi metadata and exports its packages, so client modules can import it in Karaf.
aliases: [wrapper bundle, embed dependency bundle, repackaged library bundle]
keywords: [osgi, bundle, Embed-Dependency, Export-Package, Import-Package, DynamicImport-Package, maven-bundle-plugin, wrapper, karaf, third-party library, structure]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/resteasy/pom.xml", "rackinspect:application/keycloak-client/pom.xml", "rackinspect:application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs"]
alternatives: []
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Some client libraries (a JAX-RS client stack with its providers, an identity-provider admin client) ship as plain jars or with OSGi metadata that does not resolve in Karaf. Put the repackaging into its own module with no source code, so the client module that uses the library stays small and the repackaging can be replaced in one place.

## Practice

### Platform base

- A bundle sees only the packages its manifest imports; a missing import shows up as `ClassNotFoundException` at runtime ([ClassNotFoundException](../../agent-docs/backend/debugging-and-monitoring-guide.md#classnotfoundexception)).
- Extra third-party bundles are installed through the `extra-bundles` slot of the generated feature ([[karaf-customization-via-fragments]]). The docs do not describe embedding or wrapper bundles; the rest is a convention.

### Practice notes: one module, only a pom

```
application/
├── <library>/              wrapper: pom.xml only, no src/
│   └── pom.xml             packaging = bundle, Embed-Dependency, Export-Package
└── <client>/               own code that uses the library
    ├── pom.xml             compiles against the library artifacts, embeds only its own SDK jars
    └── src/main/java/<root>/<client>/{,osgi/}
```

- **Name the module after the library** (`resteasy`, not `rest-client-libs`), so the bundle list in the feature reads as an inventory of third-party stacks.
- **The pom holds the whole recipe** in the `maven-bundle-plugin` instructions:
  - `Embed-Dependency`: the exact list of library artifacts to inline (core, SPI, client, the providers you need).
  - `Export-Package`: the library's packages, so the client module can import them.
  - `Import-Package: *;resolution:=optional` and `DynamicImport-Package: *`: the embedded jars reference many optional packages; making them optional lets the bundle resolve.
- **Keep the client module separate.** The client compiles against the same library artifacts in the same version as the wrapper, embeds only its own SDK jars and imports the library packages from the wrapper at runtime; keep the version in one Maven property so the two cannot drift. The client also carries the components and any class-loader workaround (a composite class loader for a service-loader lookup).
- **Install order**: put the wrapper `<bundle>` line before its consumers in `extra-bundles`, with a comment that says so.
- Prefer a ready-made OSGi bundle of the library, or a Karaf feature that provides it, when one exists in a compatible version; write a wrapper only when there is none.

## Rationale

- One place to change when the library version moves; client code does not change.
- The wrapper is the only bundle with the broad optional and dynamic imports; the client keeps a precise manifest.
- Cost: `DynamicImport-Package: *` and optional imports hide missing packages until runtime, and the embedded library can clash with another copy in the container. Keep exactly one wrapper per library and check the bundle state after install.

## Example

One application has a `resteasy` module with only a pom: it embeds the RESTEasy core, client, SPI and JSON, JAXB and multipart providers plus the JSON and mail APIs they need, and exports `org.jboss.resteasy*` with an explicit `version="0.0.0"` (the reason is not recorded; *verify* how the client's import ranges resolve against it before copying that value). The library version is a literal in both the wrapper and the client pom, a drift risk the Maven property above removes. The identity-provider client module embeds the admin-client jars, imports the RESTEasy packages from the wrapper, and holds the factory, the custom client provider and the retry helper in its `keycloak` package, and only the component and the connector activator in its `osgi` package. The feature fragment installs the wrapper first, with the comment that it must load before the client.

## When to avoid

- The library already ships valid OSGi metadata or a Karaf feature: install that instead.
- Only one module uses a small library: embed it in that module directly (`Embed-Dependency` in the client pom) instead of a separate wrapper.

## Related

- [[structure-custom-module-dependency-direction]] — where wrapper and client sit in the module graph
- [[structure-adding-a-custom-backend-module]] — registering the wrapper in the build and the feature
- [[osgi-karaf-bundle-architecture]] — class-loading cost of the bundle layout
- [[multi-tenant-keycloak-realm]] — an identity-provider admin client that needs such a library
- [[external-api-adapter-pattern]] — client modules for external APIs
