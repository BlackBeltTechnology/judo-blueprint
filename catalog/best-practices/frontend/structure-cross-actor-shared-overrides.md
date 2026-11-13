---
id: structure-cross-actor-shared-overrides
title: Sharing Frontend Resources Across Actor Modules
description: Put resources that every actor frontend needs (template overrides, i18n fragments, icons) in the parent generator-overrides folder, keep TypeScript custom code per actor, and treat a shared custom-code module as an open question.
aliases: [shared generator overrides, cross-actor frontend sharing, common frontend module]
keywords: [generator-overrides, override-dir, actor module, shared code, common module, custom implementations, duplication, multi-actor]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/generator-overrides/ui-react/actor/public", "rackinspect:application/frontend-react/rackinspect__services__generic_user/pom.xml"]
alternatives: []
related: [structure-frontend-react-parent-layout, dual-actor-frontend-architecture, i18n-generator-override-extra-fragment, custom-public-assets, shared-service-helper-module, generator-override-extra-dependencies]
fragment: "none: frontend-only"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Several actor frontends of one application often need the same branding, translation keys or custom behaviour. Decide where each kind of shared resource lives so it is written once and every actor build picks it up.

## Practice

### Platform base

- Each actor module's `override-dir` defaults to `${project.parent.basedir}/generator-overrides`, so by default all actor modules read one override folder ([module properties](../../agent-docs/frontend/build-and-deployment.md)).
- A file in the override folder with the same name as a generator template replaces that template ([template name](../../agent-docs/frontend/README.md)); fragment overrides inject content into a template slot ([[i18n-generator-override-extra-fragment]]).
- Custom code under an actor's `src/custom/` is outside generator scope and belongs to that module only ([hook files and the custom folder](../../agent-docs/frontend/extension-points.md)). The agent-docs describe no mechanism that shares `src/custom/` code between actor modules.

### Shared at parent level: generator input only

```
application/frontend-react/generator-overrides/
  ui-react/actor/public/                         # applied to every actor build
    favicon.ico, apple-touch-icon.png, ...       # replace generated icons
    i18n/application_default_extra.fragment.hbs  # extra translation keys
```

- Put in the shared `generator-overrides/` only what the generator consumes: template overrides, fragment overrides and replacement files for generated assets.
- If one actor needs a different version, set that actor's `override-dir` to its own folder rather than adding actor checks to a shared template.
- Whether a file with a name the templates never produce (for example a new logo) is copied into the actor build is *verify*. Until checked, add new assets in each actor's `public/` ([[custom-public-assets]]).

### Per actor: TypeScript custom code

- Keep hooks, custom implementations and helper modules in each actor's `src/custom/`. Inside one actor, extract shared logic into helper modules ([[shared-service-helper-module]]).
- The Pandino registration names in hook files embed the actor's service paths, so registration files are rarely identical across actors even when the logic is.

### Open question: a common module for custom code

A developer asked whether custom implementations used by several actor frontends belong in a common module. No example in the catalog shows a working answer:

- Possible routes are a local package (workspace or `file:` dependency added through the `package.json` fragment of [[generator-override-extra-dependencies]]) or a shared source folder imported through a path alias. Both are *verify*: neither is documented in the agent-docs nor seen in an example.
- Until a route is proven, keep logic in pure, actor-independent helper files so that a later move into a shared module is a copy, not a rewrite.

## Rationale

The shared override folder is the one sharing point the platform wires up by default, and it acts at generation time, so every actor gets the same output without import tricks. TypeScript code is compiled per actor module with its own generated types and service paths; sharing it needs build setup that the platform does not provide out of the box.

## Example

- One app: `generator-overrides/ui-react/actor/public/` holds several icon files and `i18n/application_default_extra.fragment.hbs`, used through the default `override-dir` in the actor pom. The same folder also holds a logo file, which the actor module keeps a second copy of in its own `public/`.
- One app builds a single actor frontend, so all TypeScript custom code lives in that actor's `src/custom/`; it never had to share custom code between actors.

## When to avoid

- Only one actor frontend exists: keep everything in that module; a shared override folder is still the default location for template overrides.
- Actors need different branding or translations: use per-actor `override-dir` values instead of one shared folder.

## Related

- [[structure-frontend-react-parent-layout]] — what lives at the parent level
- [[dual-actor-frontend-architecture]] — why actors get separate modules
- [[i18n-generator-override-extra-fragment]] — the shared i18n fragment
- [[custom-public-assets]] — per-actor static assets
- [[shared-service-helper-module]] — helper modules inside one actor
- [[generator-override-extra-dependencies]] — how a shared package could be added to `package.json`
