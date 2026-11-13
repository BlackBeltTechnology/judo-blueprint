---
id: structure-adding-a-custom-backend-module
title: Wiring a New Custom Backend Module into Build and Karaf Feature
description: Checklist practice for adding a hand-written Maven module under application/ so it builds in the right profile, reaches its consumers and is installed in Karaf, using only generator fragment files.
aliases: [add backend module, register custom bundle, new OSGi module wiring]
keywords: [module, maven, extra-modules, extra-bundles, extra-dependencies, profile, build-sdk, karaf feature, fragment, generator-overrides, structure]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/generator-overrides/pom.xml.extra-modules.fragment.hbs", "rackinspect:application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs", "rackinspect:application/generator-overrides/app/pom.xml.extra-dependencies.fragment.hbs"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

A new module under `application/` is only useful when three things happen: Maven builds it, its consumers can compile against it, and Karaf installs it. Each step has its own generator fragment. Missing one gives a module that compiles but never runs, or a bundle that fails to resolve at runtime.

## Practice

### Platform base

- The root `pom.xml`, the module poms and `karaf-features/src/main/feature/feature.xml` are generated with named fragment slots, among them root `extra-modules` and `extra-profiles`, per-module `extra-dependencies`, and the feature slots `extra-bundles` and `extra-repositories` ([available fragment extension points](../../agent-docs/deployment/build-process.md#available-fragment-extension-points)). How slots and the `application/generator-overrides/` folder work is covered in [[karaf-customization-via-fragments]].
- The root pom groups modules into profiles that a `-Dskip...` property turns off, for example `build-sdk` (`-DskipSDK`) and `build-docker` (`-DskipDocker`) ([build profiles](../../agent-docs/deployment/build-process.md#build-profiles)). *verify*: the docs list the profiles but do not say which profile the `extra-modules` slot sits in; in the observed template it sits inside `build-sdk`.

### Practice notes: the three-file checklist

For a module `<new-module>` with artifact id `<app>-application-<new-module>`:

```
application/
├── <new-module>/
│   ├── pom.xml                       parent = <app>-application, packaging = bundle
│   └── src/main/java/<root>/<new-module>/...
└── generator-overrides/
    ├── pom.xml.extra-modules.fragment.hbs                 1. <module><new-module></module>
    ├── app/pom.xml.extra-dependencies.fragment.hbs        2. dependency on the new artifact
    ├── interceptors/pom.xml.extra-dependencies.fragment.hbs   (only if interceptors use it)
    └── karaf-features/src/main/feature/
        └── feature.xml.extra-bundles.fragment.hbs         3. <bundle>mvn:<group>/<artifact>/${project.version}</bundle>
```

1. **Build it.** Add the module to the root `extra-modules` fragment. It then builds with the generated backend modules and is skipped together with them.
2. **Let consumers compile.** Add a dependency in the `extra-dependencies` fragment of each consumer module. Respect the module direction in [[structure-custom-module-dependency-direction]].
3. **Install it.** Add a `<bundle>` line to the `extra-bundles` fragment, plus any third-party bundles it imports and an inline `<config>` block if it has a configured component.
4. **Order bundle lines by dependency** and say why in a comment when the order matters (a repackaged library before its consumer, see [[structure-third-party-wrapper-bundle]]).
5. **Group by module** inside the `extra-bundles` fragment, one comment header per module (`<!-- Scheduler -->`), so a module's bundles and config blocks can be found and removed together.
6. **Regenerate and check the generated files**: the module appears in the root pom between the `extra-modules` markers, and the bundle appears in the generated `feature.xml`. Empty markers mean the fragment path is wrong.
7. **Non-bundle modules** (a Docker-image-only module) go into an `extra-profiles` fragment with their own profile, activated by the property of the stage they belong to, for example `!skipDocker` ([[structure-non-java-service-folders]]).

## Rationale

- All wiring sits in fragment files, so it survives regeneration and needs no `.generator-ignore` entry ([[generator-ignore-config-protection]]).
- The checklist matches the three failure modes: not built, not on the consumer classpath, not installed (the component never activates although the build is green).
- Cost: a module touches four or more files outside its own folder; a short note in the module's own documentation listing them helps the next change.

## Example

One application registers several extra backend modules (shared services, a SOAP client, a scheduler, a repackaged REST client library, a report library and an identity-provider admin client) in one `extra-modules` fragment. The `app` and `interceptors` poms get the shared-services and library artifacts through their `extra-dependencies` fragments. One `extra-bundles` fragment installs all of them, grouped by module, with a comment that the repackaged REST library must load before the identity client. One more module that only builds a Docker image is added through `extra-profiles` and activates only when Docker images are built.

## When to avoid

- The code fits an existing module's role: add a package, not a module.
- Only a third-party bundle is needed and no own code: add the `<bundle>` line alone, no module.

## Related

- [[karaf-customization-via-fragments]] — how fragment slots work, inline `<config>` blocks
- [[osgi-karaf-bundle-architecture]] — which extra modules applications add
- [[structure-custom-module-dependency-direction]] — which module may depend on the new one
- [[structure-third-party-wrapper-bundle]] — when the new module only repackages a library
- [[structure-non-java-service-folders]] — modules that build images, not bundles
