---
id: custom-component-directory
title: Custom Component Directory Outside Generator Scope
description: Keep hand-written React components in a dedicated directory such as src/custom, away from generated files, so regeneration never touches them.
aliases: [custom code folder, src/custom components]
keywords: [custom component, directory, src/custom, generator-ignore, gitignore, pandino component]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:rackinspect", "project:workflow-poc", "project:reserve-app", "status:established"]
category: component
status: established
projects: [trivia, rackinspect, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/application-customizer.tsx", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
related: [complete-frontend-replacement, glassmorphic-styled-components, application-customizer-hub]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Hand-written components (pages, dialogs, shared widgets) need a home that regeneration never overwrites and that is easy to tell apart from generated code.

## Practice

### Platform base

- Files you add in `src/custom/` are not generated, so they need no `.generator-ignore` entry (the folder is committed; only `.default` scaffolds are gitignored) ([hooks: using .default scaffolds](../../agent-docs/frontend/hooks/README.md), [frontend guide](../../agent-docs/frontend/README.md)).
- The generator creates hook scaffolds as `.default` files under `src/custom/hooks/` (`pages/`, `dialogs/`, `containers/`, `custom-implementations/`, `components/cards/`, `sub-themes/`). Custom components registered through Pandino (custom visual element implementations) live next to them ([extension points](../../agent-docs/frontend/extension-points.md)).
- Files outside `src/custom/` that the generator owns carry a generated header and are checksum-protected: editing them fails the build unless they are listed in `.generator-ignore`, which also stops generator updates for that file. Keeping hand-written code in a separate directory avoids that trade-off.
- `src/custom/application-customizer.tsx` is a plain generated file with an empty `customize(context)` method; register custom hooks and components from there.

### Practice notes: one custom root, subfolders by role

The layout below is a convention, not generated output:

```
src/custom/
  application-customizer.tsx     # registrations
  components/                    # reusable custom components and their register... files
  hooks/                         # scaffold copies: pages/, dialogs/, containers/, custom-implementations/
```

- Put every hand-written file under one root and import generated code through the `~/` alias; never put custom files into generated folders such as `pages/`, `containers/` or `services/`.
- Mirror the generator's subfolders (`hooks/dialogs`, `hooks/pages`) so scaffold copies stay discoverable.
- Some frontends use a different root, such as `src/<app>/`, for custom pages and dialogs. This also works because the generator does not produce files there; like `src/custom/`, the folder is committed to version control.

## Rationale

A single custom root makes the boundary between generated and hand-written code obvious, keeps upgrades free of merge work and keeps `.generator-ignore` short. Custom components cannot reuse generated page scaffolding and import across the boundary.

## Example

- A game frontend with a small set of custom files in `src/<app>/` (dialogs, game pages, shared styled components, utilities).
- A heavily customized frontend: a custom root with many files in `hooks/custom-implementations/`, `hooks/dialogs/`, `hooks/pages/`, form and view-edit action hook folders, table row highlighting hooks, plus `application-customizer.tsx` and an error handler registration.
- A workflow frontend: `src/custom/components/` with a diagram renderer and a code viewer, each with its Pandino registration file.
- A frontend with a single hook file in `src/custom/hooks/dialogs/` for one actor; the other four actor frontends have no custom files.

## When to avoid

- The whole frontend is replaced: see [[complete-frontend-replacement]].
- The frontend is fully generated and needs no custom code.

## Related

- [[complete-frontend-replacement]] — replacing the generated frontend instead of extending it
- [[glassmorphic-styled-components]] — styled components typically placed in such a directory
- [[application-customizer-hub]] — where custom components and hooks are registered
