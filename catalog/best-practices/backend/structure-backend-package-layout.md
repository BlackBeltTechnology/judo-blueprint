---
id: structure-backend-package-layout
title: Package Layout Inside Custom Backend Modules
description: Practice for Java package names inside app, interceptors, common, scheduler and client modules, keyed by module and business area, with a separate osgi package for components and short notes files next to the code.
aliases: [java package naming, backend package structure, interceptor package layout]
keywords: [package, naming, layout, interceptors, common, services, impl, osgi, utils, i18n, AGENTS.md, structure, module]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/interceptors/src/main/java", "rackinspect:application/common/src/main/java", "rackinspect:application/keycloak-client/src/main/java", "rackinspect:application/INTERCEPTORS.md", "rackinspect:application/CUSTOM-OPERATIONS.md"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Generated code fixes its own packages; hand-written modules do not. Use one naming scheme across modules, so a class's package tells which bundle it is in, which business area it serves and whether it is a component, and so package exports stay narrow.

## Practice

### Platform base

- Custom operation implementations go into the package of their generated `.default` twin, `<generated-root-package>.<app>.custom...`; an invented package breaks the wiring ([generator-emitted package convention](../../agent-docs/backend/custom-operations.md#generator-emitted-package-convention), [[custom-operation-osgi-component]]). That rule covers `app`; everything below is a convention for the other modules.

### Practice notes: `<root>.<module>.<area>`

| Module | Package scheme | Notes |
|---|---|---|
| `app` | generator package for operations; `<root>.<area>` for anything else | keep non-operation code out of the `custom` tree |
| `interceptors` | `<root>.interceptors.<area>[.<sub-area>]` | area = entity or business area; access guards split by CRUD kind: `access.create`, `access.update`, `access.delete` |
| `common` | `<root>.common.<capability>`, plus one `services` package and `common.utils` | service interfaces in `services`, implementations in `services.impl`; i18n bundles under `src/main/resources/<root path>/common/.../i18n` |
| `scheduler` | `<root>.scheduler[.<capability>]` | one sub-package per job family that needs its own configuration |
| library (`report`) | `<root>.report.<leg>.{context,helper,support}` | no component packages at all |
| client | `<root>.<client>` for plain code, `<root>.<client>.osgi` for components and the exported API | a WSDL-generated client may keep the vendor namespace and add `.osgi` |

Rules:

- **One root per application** (`<root>` = Maven group id path), then the module name. A class name search then tells you the bundle.
- **Split by business area, not by technical kind.** `interceptors.account`, not `interceptors.create`. The exception is a set of uniform guards (create/update/delete access checks), where the CRUD kind is the clearer key.
- **Components in `osgi`, plain code beside it** in client modules; export only the `osgi` (API) package ([[soap-client-integration]]).
- **Helper classes in one place.** Static helpers that more than one module uses belong to `common.utils`, not to a `utils` package of `interceptors` that `app` then imports ([[structure-custom-module-dependency-direction]]).
- **A short `AGENTS.md` or README next to a non-trivial package** (an interceptor area, an operation area, a module root) with its purpose, invariants and dependency direction. It moves with the code and is read by whoever edits that package.

### Notes files: prefer local over central inventories

A central inventory (one long document listing every operation or interceptor by category and by entity, with file locations and counts) is useful as an overview but goes stale: counts and paths change with every move. If you keep one, generate it or limit it to links into the local notes files; do not hand-maintain file locations in it.

## Rationale

- Package names that encode module and area keep `Export-Package` narrow and make OSGi wiring problems easy to locate.
- Area packages keep related interceptors and operations together, which is how changes arrive (one feature at a time).
- Local notes stay correct longer than a central inventory because the edit and the note sit in the same diff.

## Example

One application groups interceptors as `interceptors.account`, `interceptors.user.roles`, `interceptors.user.management`, `interceptors.audit.header` and `interceptors.access.{create,update,delete}`, each larger area with its own `AGENTS.md`. `common` holds `common.utils` (exception, sequence, number helpers), `common.utils.services` (service interfaces) with `common.utils.services.impl` (their components), and capability packages for media, requests and user management. The identity-provider client keeps factory and retry helpers in `<root>.keycloak` and its components in `<root>.keycloak.osgi`. The application also has two hand-written inventory files for custom operations and interceptors at the `application/` root; the interceptor inventory still points the helper classes to `interceptors/utils/` after they moved to `common.utils`, the drift described above. A second, older `common.services` package holds concrete component classes without interfaces next to the interface-based one; two schemes in one module is what the single `services` / `services.impl` rule avoids.

## When to avoid

- A module with a handful of classes needs no area sub-packages.
- Do not rename packages of generated code, or move a custom operation out of its generated package, to fit this scheme.

## Related

- [[custom-operation-osgi-component]] — package and registration of operation implementations
- [[structure-custom-module-dependency-direction]] — which module owns shared helpers
- [[soap-client-integration]] — `osgi` API package of a client module
- [[osgi-karaf-bundle-architecture]] — the modules these packages live in
