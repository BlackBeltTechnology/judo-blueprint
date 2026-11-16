---
id: generator-ignore-config-protection
title: Generator-Ignore for Configuration Protection
description: "List hand-edited configuration files and custom code in .generator-ignore so that regeneration from the model neither overwrites them nor fails the build on a checksum mismatch."
aliases: [generator ignore, protect config from regeneration, generated file protection]
keywords: [generator-ignore, regeneration, checksum, judo.properties, judo-karaf.env, config, default template]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:itracker", "project:alba", "project:mlszksz-platform", "project:viterra_demo", "project:bhs-global-operation", "project:judo-demo-miniworkflow", "project:ubives", "project:park-here", "project:indamedia-adtrack", "project:InterfaceRegister", "project:judo-partner", "project:workflow-poc", "project:reserve-app", "status:established"]
category: config
status: established
projects: [trivia, rackinspect, itracker, alba, mlszksz-platform, viterra_demo, bhs-global-operation, judo-demo-miniworkflow, ubives, park-here, indamedia-adtrack, InterfaceRegister, judo-partner, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:application/app/.generator-ignore", "itracker:unrecorded", "alba:unrecorded", "mlszksz-platform:application/.generator-ignore", "viterra_demo:unrecorded", "bhs-global-operation:unrecorded", "judo-demo-miniworkflow:unrecorded", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded", "InterfaceRegister:unrecorded", "judo-partner:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Code generation from the model rewrites files in the application. Files that developers own (runtime configuration, secrets, hand-written operation classes) must be listed in `.generator-ignore`, or the next build either overwrites them or fails.

## Practice

### Platform behavior

The platform docs describe the mechanism ([code generation and checksum protection](../../agent-docs/backend/README.md)): generated files are tracked by checksum in `.generated-files`; files not listed in `.generator-ignore` are regenerated on build or generate; if a tracked file was edited by hand the build fails on the checksum mismatch. Editing a generated file is the last resort: prefer generator parameters (`generator-parameter.properties`) and the fragment extension points (files under `application/generator-overrides/`), and only then edit and add the path to `.generator-ignore`.

For custom operations the docs say: the generated `.default` file is a read-only blueprint that is regenerated on every build; create a new `.java` file with your logic and add the `.default` path to `.generator-ignore` ([understanding generated default implementations](../../agent-docs/backend/custom-operations.md)).

### Practice notes: the standard root list

The root `.generator-ignore` of a freshly generated application is a short file, and the examples keep this set:

```
.generator-ignore
judo.properties
judo-karaf.env
generator-parameter.properties
```

- The file lists itself so it is not overwritten.
- `judo.properties` holds runtime configuration; `judo-karaf.env` holds environment values and secrets (SMTP credentials, identifier signer secret, filestore settings; see [application config](../../agent-docs/deployment/application-config.md)); `generator-parameter.properties` holds generation parameters.
- Add further root files that the team edits (some applications add `judo.sh` or `.gitignore`).
- Application-level `.generator-ignore` files list `.default` paths of implemented operations, or edited build files such as a `pom.xml`. Frontend submodules keep their own `.generator-ignore`.
- Some applications keep custom operations in a separate `custom/` source directory instead, so no application-level entries are needed.
- Some examples list renamed `.java.default` files. That is observed in practice; the platform docs advise a new `.java` file next to the untouched `.default` blueprint.

## Rationale

- Secrets and local configuration survive regeneration, and the build does not fail on a checksum mismatch for files you own.
- The syntax is simple, similar to a gitignore.
- Cost: the list is maintained by hand. A file that is edited but not listed fails the next build or is overwritten. External secret management (a vault, orchestrator secrets) reduces what has to be protected.

## Example

- Most examples: the standard four-entry root list. Frontend submodules have their own files. An application with no custom operations keeps the standard list as the minimal baseline.
- Some examples: the standard list plus `judo.sh`. One also has application-level lists for custom operation templates and a `pom.xml`.
- One application: the standard list at the root and an application-level list of several entries.
- One example: standard list plus `.gitignore`, and a schema `pom.xml` entry.
- One example: only `judo.properties`, an early-stage minimum.

## When to avoid

- Do not list a file only to avoid fixing a generator parameter or a fragment extension point that already covers the change.
- Never list the `.default` blueprints in the expectation of editing them: write a new implementation file.

## Related

- [[osgi-karaf-bundle-architecture]] — the runtime configuration these files feed
