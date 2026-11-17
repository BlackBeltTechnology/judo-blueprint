---
id: structure-frontend-react-parent-layout
title: Frontend-React Parent Folder Layout
description: Keep application/frontend-react as a thin aggregator (parent pom, shared UI model module, shared generator-overrides, one folder per built actor) and remove actor folders that the pom no longer builds.
aliases: [frontend-react layout, frontend parent module, actor module folders]
keywords: [frontend-react, parent pom, actor module, model module, generator-overrides, build-react profile, stale actor folder, README.adoc]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/pom.xml", "rackinspect:application/frontend-react/README.adoc", "rackinspect:application/frontend-react/rackinspect__services__ai_service__ai_service/.generator-ignore"]
alternatives: []
related: [dual-actor-frontend-architecture, structure-cross-actor-shared-overrides, custom-component-directory]
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Make the `application/frontend-react/` folder readable at a glance: what is shared by all actor frontends, what belongs to one actor, and which actor folders are actually built.

## Practice

### Platform base

- The platform generates one frontend module per modeled actor, named `<app>__<actor path>`, under `application/frontend-react/` ([[dual-actor-frontend-architecture]]).
- Each actor module's pom defines `actor`, `actor-name`, `node-install-dir` (default `${project.parent.basedir}/.nodejs`) and `override-dir` (default `${project.parent.basedir}/generator-overrides`), so Node.js and the override folder are shared by all actors unless an actor overrides the property ([module properties](../../agent-docs/frontend/build-and-deployment.md)).
- Generated actor files are tracked by checksum in a file in the actor module root ([checksum protection](../../agent-docs/frontend/README.md)).

### Practice notes: four kinds of children, nothing else

```
application/frontend-react/
  pom.xml                 # aggregator: profiles list the model module and the actor modules
  README.adoc             # build properties and profiles
  model/                  # shared UI model built from the ESM, used by every actor
  generator-overrides/    # shared template overrides and static assets (all actors)
  <app>__<ns>__<actor>/   # one folder per actor that the pom builds
  .nodejs/                # shared Node.js install (ignored)
```

- The parent pom lists the `model` module in one profile and the actor modules in another (`build-react`), so `skipFrontendModel` and `skipReact` can switch them off independently.
- Every actor folder under the parent must be a module in that profile. When an actor is removed from the model or from the build, delete its folder and its leftover checksum files, instead of leaving a stub.
- Code that serves one actor stays in that actor's `src/custom/` ([[custom-component-directory]]). Only resources that every actor needs go to the parent level, in `generator-overrides/` ([[structure-cross-actor-shared-overrides]]).
- Keep the parent `README.adoc` in step with the real actor list.

## Rationale

The parent folder is where a newcomer starts. If it holds only the aggregator, the shared model, the shared overrides and the built actors, the folder listing is the documentation. A stub folder for an actor that is not built looks like a second frontend, invites edits that never ship, and its `.generator-ignore` drifts from reality.

## Example

- One frontend: the parent pom builds `model` and one actor, `<app>__services__generic_user`. A second folder, `<app>__services__ai_service__ai_service`, holds only a `.generator-ignore` and is not a module, and the generic user module still carries an empty `.generated-files-aiservice` next to `.generated-files-genericuser`. The `README.adoc` names the actor as `<app>__services__genericuser`, which no longer matches the folder. These are the leftovers the practice avoids.
- One frontend: `generator-overrides/ui-react/actor/public/` holds favicons, the logo and an i18n fragment that every actor build picks up through the shared `override-dir`.

## When to avoid

- An actor folder is kept on purpose for an actor that is modeled but not yet built: then add it to the pom profile (even if fully generated) or document the reason in the parent README.
- The checksum file name differs between platform versions (`.generated-files__<actor>` in the docs, `.generated-files-<actor>` in one example): *verify* before deleting one.

## Related

- [[dual-actor-frontend-architecture]] — why there is one module per actor
- [[structure-cross-actor-shared-overrides]] — what may live at the parent level for all actors
- [[custom-component-directory]] — layout inside one actor's `src/custom/`
