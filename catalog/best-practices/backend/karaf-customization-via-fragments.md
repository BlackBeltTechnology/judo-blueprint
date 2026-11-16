---
id: karaf-customization-via-fragments
title: Karaf Customization via Generator Fragment Overrides
description: "Extra Karaf bundles, repositories, Maven plugins or dependencies and OSGi config PIDs are added through the generator's named fragment slots, so they survive regeneration without editing generated files."
aliases: [feature.xml fragment, generator-overrides, extra-bundles fragment, inline config]
keywords: [fragment, feature.xml, extra-bundles, generator-overrides, karaf-features, config PID, env substitution, generator-ignore]
tags: ["domain:backend", "layer:backend", "project:compsych-letter-demo", "project:rackinspect", "project:indamedia-adtrack", "status:emerging"]
category: config
status: emerging
projects: [compsych-letter-demo, rackinspect, indamedia-adtrack]
evidence: ["compsych-letter-demo:unrecorded", "rackinspect:application/generator-overrides/karaf-features/src/main/feature/feature.xml.extra-bundles.fragment.hbs", "indamedia-adtrack:unrecorded"]
alternatives: []
fragment: "none: infrastructure"
first_seen: 2026-05-12
last_updated: 2026-11-11
---
## Intent

Customize the `karaf-features` module and other generated Maven modules (extra bundles, extra repositories, extra plugins or dependencies, OSGi configuration) without editing the generated `feature.xml` or `pom.xml`. The generator emits those files with named override slots; a fragment file you create is spliced in at the matching marker, so the change survives regeneration. This is the backend analog of the frontend patterns [[generator-override-extra-dependencies]], [[handlebars-generator-template-override]] and [[i18n-generator-override-extra-fragment]].

## Practice

### Platform base

- Generated files such as `pom.xml` and `feature.xml` carry paired marker comments, for example `<!-- To define create 'app/pom.xml.extra-dependencies.fragment.hbs' file -->` and `<!-- End of ... -->`. By default the fragment is an empty stub from the template jar; a file with the same relative path and name in the override directory replaces it ([extending generated files via fragment overrides](../../agent-docs/deployment/build-process.md#extending-generated-files-via-fragment-overrides)).
- Override directory: `application/generator-overrides/`, wired into the generator invocation of the root `pom.xml`. A second root `generator-overrides/` serves the root-level generator step.
- A fragment survives regeneration and needs no `.generator-ignore` entry. The docs say to prefer fragments over `.generator-ignore`: a fragment keeps the file under generator control, an ignore entry freezes it and lets it drift from the template ([available extension points](../../agent-docs/deployment/build-process.md#available-fragment-extension-points)).
- Documented slots: root `pom.xml` (project-definition, properties-definition, model-properties-definition, judo-properties-definition, extra-dependency-management, extra-plugin-management, extra-plugins, extra-modules, extra-profiles, release-profiles, distribution-management, repository-definition); per module pom (`app`, `karaf-features`, e2e, and others) project-definition, properties-definition, extra-plugin-management, extra-plugins, extra-dependencies; and for `karaf-features/src/main/feature/feature.xml` the slots `extra-repositories`, `extra-bundles`, `model-bundles`.
- Hand-edits to a generated file are protected by checksums; `.generator-ignore` is the only way to keep an edited generated file ([generated files you edit](../../agent-docs/backend/README.md)). Forcing regeneration with the ignore-checksum flag overwrites drifted files and drops hand-edits.
- Configuration values for the app are normally `JUDO_PLATFORM_*` environment variables, from `judo-karaf.env` locally ([application config](../../agent-docs/deployment/application-config.md)). The docs do not describe inline `<config>` blocks in `feature.xml`; the config guidance below is a convention, *verify*.

### Practice notes: slots, layout and OSGi config

Observed in two example applications, not documented platform behaviour:

- Fragment path mirrors the generated file: `application/generator-overrides/karaf-features/src/main/feature/feature.xml.<slot>.fragment.hbs`, `application/generator-overrides/<module>/pom.xml.<slot>.fragment.hbs`, and `application/generator-overrides/pom.xml.<slot>.fragment.hbs` for the root. The layout sits beside the frontend `generator-overrides/ui-react/...` tree.
- The slot name must match the path in the marker comment exactly; a typo is silently ignored. After adding a fragment, regenerate and compare the generated file: if the markers are still empty, the path is wrong.
- Use `extra-bundles` for `<bundle>` lines, `<feature>` dependencies and inline `<config>` blocks; `extra-repositories` for extra feature repositories (needed when a feature lives outside the platform feature repository); `extra-dependencies` for compile dependencies of a module; `properties-definition` to pin a Maven property such as a CXF version; `extra-modules` on the root pom for extra sub-modules.
- Configuring an OSGi component that reads `@Component(configurationPid = ...)`, three ways, in preference order:
  1. **Inline `<config name="pid">` in the `extra-bundles` fragment**, with `${env:VAR:-default}` values. Reasons given: env substitution at install time (the local launcher feeds the env file), defaults let a fresh checkout boot, the PID is registered so components can use `configurationPolicy = REQUIRE`, and the PID sits next to its consumer.
  2. **`karaf-features/etc/<pid>.cfg`**, only for values env substitution cannot express (a multi-line certificate) and only if the application's offline assembly packages that directory. If it does not, the file never reaches Config Admin and `REQUIRE` components stay inactive silently.
  3. **`.generator-ignore` plus a direct edit**, only when no slot exposes the location ([[generator-ignore-config-protection]]).
- Customizing the `karaf-offline` assembly: it is typically not regenerated after first scaffold, so check for fragment markers and edit directly if there are none.

```xml
<!-- Example fragment: feature.xml.extra-bundles.fragment.hbs -->
<bundle>mvn:org.apache.cxf/cxf-rt-rs-sse/3.5.6</bundle>
<config name="hu.example.MyComponent">
    endpoint=${env:MY_ENDPOINT:-https://localhost:8443}
    timeoutMs=${env:MY_TIMEOUT_MS:-5000}
</config>
```

## Rationale

- Customizations survive regeneration, the generated XML stays authoritative so diffs review cleanly, and per-environment overrides become an env-file edit instead of a rebuild.
- Limits: only emitted slots exist, and a misspelled fragment name fails silently, so the marker text is the source of truth.
- Forcing regeneration after the checksum errors silently drops hand-edits to non-ignored files: move changes into a fragment or an ignore entry first.
- Fallback when no slot exists (the `internal` module pom had no dependency slot in the observed template): `.generator-ignore`, accepting manual merges.

## Example

### One application

One centralized `extra-bundles` fragment shows the techniques together: extra platform features (export, report, Epsilon runtime), a scheduler bundle with the Karaf scheduler core, and several inline `<config>` blocks: a Keycloak admin client (five env-driven values, consumer with `REQUIRE`), bootstrap admin users (env only, empty default), Quartz cron schedules (literal values, see [[quartz-scheduled-job]]), and servlet path plus base URL composed from one env variable into two PIDs. It also uses properties and extra-dependency fragments in several modules and a root extra-modules fragment registering application sub-modules (common, report, scheduler, keycloak client and others).

### Another application

1. An `extra-bundles` fragment with one `cxf-rt-rs-sse` bundle line for an SSE endpoint, because the platform JAX-RS feature ships the frontend but not the SSE provider ([[custom-jaxrs-sse-endpoint]]). Rejected: editing `feature.xml`, a non-existent Karaf feature, upgrading the vendored CXF.
2. Document-converter and external provider PIDs as `karaf-features/etc/*.cfg`: miswired, because the offline assembly did not package that directory. The consumers compensate with `configurationPolicy = OPTIONAL` and component property defaults. Remediation: move both PIDs to inline `<config>` blocks and drop the workaround.
3. Hand-edited dependencies in the `internal` module pom, protected with a `.generator-ignore` entry (the same file already protected another pom).

[[magic-link-authentication]] and [[email-service-integration]] are `REQUIRE` consumers that rely on the PID being registered at feature install.

## When to avoid

- The value fits the documented `JUDO_PLATFORM_*` environment variables: use those, no fragment.
- You need to change content at a place with no slot: use `.generator-ignore` and accept the merge cost.

## Related

- [[osgi-karaf-bundle-architecture]] — context for the `karaf-features` and `karaf-offline` modules
- [[generator-ignore-config-protection]] — escape hatch when no fragment slot exists
- [[generator-override-extra-dependencies]] — frontend twin for `package.json`
- [[handlebars-generator-template-override]] — broader generator override discussion
- [[i18n-generator-override-extra-fragment]] — frontend fragment for translations
- [[quartz-scheduled-job]] — uses inline config blocks for cron settings
- [[custom-jaxrs-sse-endpoint]] — adds a bundle through this mechanism
- [[magic-link-authentication]] — `REQUIRE` config consumer
- [[email-service-integration]] — `REQUIRE` config consumer
