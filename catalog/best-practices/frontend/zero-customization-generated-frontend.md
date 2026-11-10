---
id: zero-customization-generated-frontend
title: Zero-Customization Fully Generated Frontend
description: "A frontend where the whole UI comes from the model: no activated hooks, no overridden generated files, and UI richness achieved by model configuration alone."
aliases: [fully generated UI, model-driven frontend]
keywords: [generated frontend, zero customization, generator-ignore, hook scaffolds, model-driven, ui model, flutter, react]
tags: ["domain:frontend", "layer:frontend", "project:itracker", "project:reserve-app", "status:emerging"]
category: framework
status: emerging
projects: [itracker, reserve-app]
evidence: ["itracker:unrecorded", "reserve-app:unrecorded"]
alternatives: [single-actor-heavy-customization, complete-frontend-replacement]
related: [admin-default-generated-ui, model-defined-color-palette, hook-scaffold-default-pattern, single-actor-heavy-customization, complete-frontend-replacement]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Ship the frontend as generated: design the model, generate, deploy. Every layout, visibility rule, action button, column width and colour is a model setting, and nothing is written by hand in the frontend module.

## Practice

### Platform base

- Generated React frontend files are protected by a checksum; a changed generated file fails the build unless listed in `.generator-ignore` ([frontend guide](../../agent-docs/frontend/README.md)). A fully generated frontend never edits them.
- Hook scaffolds (`*.ts.default` under `src/custom/hooks/`) are generated only for elements whose hook flag (for example `generateActionsHook`) is set in the model, and stay inactive until copied. `src/custom/` is gitignored in the frontend module, so even activated hooks need no `.generator-ignore` entry ([extension points](../../agent-docs/frontend/extension-points.md), [hook system](../../agent-docs/frontend/hooks/README.md)).
- The UI model decides what a page looks like: grid layout (`col`, `row`), hidden-by, enabled-by and required-by rules, column width, sortable and default sort, rows per page, dialog opening and so on ([ESM to UI mappings](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)).

### Project practice: stay inside the model

This layer is project practice (itracker, reserve-app):

- Keep `.generator-ignore` to its default content (itself and `.gitignore`); no theme, layout or i18n files are overridden.
- Do not activate any hook scaffold; the generated `src/custom/application-customizer.tsx` stays unmodified.
- Get the richer behaviour from the model: a split column layout for a view, button visibility from derived booleans on the transfer object, explicit column widths and sort orders, a fixed page size for long tables, opening sub-resource views in a dialog with auto close on save, and brand colours as actor properties.
- Static branding such as a logo in `public/` is the only accepted addition.
- Flutter frontends follow the same rule; the observed Flutter projects add only Handlebars template overrides for cross-cutting features such as download or upload buttons and theme palette, with no hand-written Dart ([template override process](../../agent-docs/frontend/README.md)).

```
frontend/<app>__<actor>/
  .generator-ignore        only itself and .gitignore
  public/logo.svg          the one custom asset
  src/custom/              scaffolds unmodified, all hook files inactive
  src/pages, containers, dialogs, theme, layout, services   generated
```

## Rationale

There is no frontend code to maintain: upgrades come from the generator, there are no merge conflicts on generated files, and the model remains the single source of truth. The cost is that the UI is limited to what the model can express: standard look and feel, no custom frontend business logic, and no advanced interaction patterns such as masking, auto-scroll or inline PDF preview.

## Example

- itracker: two actor frontends, both without hand-written code; the richness comes from model configuration as listed above.
- reserve-app: four of five actor frontends have untouched `.generator-ignore` files; three are dashboard-only actors with no access points, and the fourth has two access points and no hooks.
- Flutter projects in the portfolio (skill matrix, a citizen portal client) apply the same rule with Handlebars overrides only.

## When to avoid

- When the product needs behaviour the model cannot express; use [[single-actor-heavy-customization]] for one actor, or [[complete-frontend-replacement]] when the generated UI does not fit at all.
- Do not treat "zero customization" as a rule that forbids a single hook: an activated hook under `src/custom/` costs little, see [[hook-scaffold-default-pattern]].

## Related

- [[admin-default-generated-ui]] — a generated admin UI as default
- [[model-defined-color-palette]] — colours from the model, the usual last piece
- [[hook-scaffold-default-pattern]] — the inactive scaffolds this practice leaves alone
- [[single-actor-heavy-customization]] — the opposite end for one actor
- [[complete-frontend-replacement]] — replacing the generated frontend altogether
