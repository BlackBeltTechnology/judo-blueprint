---
id: complete-frontend-replacement
title: Complete Frontend Replacement with Generated Service Layer
description: Replace all generated pages, routing, layout and theme with a hand-built app while still consuming the generated service layer and transfer object types, for UX that diverges from CRUD or for reference apps.
aliases: [custom SPA over generated services, hand-built frontend]
keywords: [frontend replacement, generator-ignore, App.tsx, service layer, custom app, generated services, SPA]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:actiongroup-test-react", "status:emerging"]
category: page
status: emerging
projects: [trivia, actiongroup-test-react]
evidence: ["trivia:unrecorded", "actiongroup-test-react:unrecorded"]
alternatives: [zero-customization-generated-frontend]
related: [generated-service-layer-reuse, generator-ignore-app-theme, custom-component-directory, dialog-based-navigation, zero-customization-generated-frontend]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some UX requirements fundamentally diverge from the generated CRUD pages: games, immersive mobile apps, real-time views. This practice builds the whole UI by hand and keeps only what the generator does well: the typed service layer that talks to the backend.

## Practice

### Platform base

- The generator produces data-access services (`data-axios` templates, one service implementation per page and relation, with `refresh`, `update`, `delete` and operation calls) and transfer object types ([service generation](../../agent-docs/frontend/model-screen-layout.md)). These are independent of the generated pages.
- Generated files are tracked by checksum. A manually edited generated file fails the build unless it is listed in `.generator-ignore`, which works like `.gitignore` ([code generation and checksum protection](../../agent-docs/frontend/README.md)).
- Your own code under `src/custom/` is not generated, so it survives regeneration without `.generator-ignore` entries (`src/custom/` is committed, not gitignored). Extra routes can be added in `src/extra-routes.tsx` ([extension points](../../agent-docs/frontend/extension-points.md)). Prefer these supported extension points and hooks when they are enough.
- The generated frontend authenticates, applies access control and registers hooks; a replacement must handle sign-in and the signed identifiers of instances itself (they change after every update of an entity, see [signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).

### Project practice: hand-built app over generated services

This layer is project practice (trivia, actiongroup-test-react), not a platform feature. Two variants exist:

- Partial replacement (trivia): protect the app root and theme files in `.generator-ignore`, put the custom components in a directory the generator does not know, and construct generated service classes directly in the custom root. Generated pages, routes and containers are still produced but unused.
- Full replacement (actiongroup-test-react): no generator-managed UI at all; all pages, layout, theme, dialogs and utilities are hand-written, and generated Axios services and types are imported from a generated folder.
- Implement navigation, state, error handling and localization yourself; none of the generated hook mechanisms apply to custom pages.

## Rationale

You get full UI freedom and no constraint from generated page patterns. The cost: no generated pages, tables or forms, all UI maintained by hand, and manual migration when the frontend framework or generator changes.

## Example

- trivia: the player frontend is a quiz-game single-page app. The root component acts as a state-machine controller that renders custom contest and dialog components and calls generated player services directly.
- actiongroup-test-react: a hand-built reference app with more than twenty pages that demonstrates action group routes, CRUD, many-aggregation and single-access entity patterns.

## When to avoid

- The UX is CRUD-like: use the generated frontend, see [[zero-customization-generated-frontend]].
- Hooks, sub-themes and extra routes can cover the differences.
- The team cannot maintain a full UI.

## Related

- [[generated-service-layer-reuse]] — consuming the generated services
- [[generator-ignore-app-theme]] — protecting the app root and theme
- [[custom-component-directory]] — where custom components live
- [[dialog-based-navigation]] — navigation without generated routes
- [[zero-customization-generated-frontend]] — the opposite approach
