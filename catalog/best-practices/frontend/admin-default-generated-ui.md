---
id: admin-default-generated-ui
title: Admin Frontend with Default Generated JUDO UI
description: Use the generated frontend unchanged for administrative CRUD actors, leaving hook scaffolds inactive, when the admin experience needs no special UX.
aliases: [default generated admin UI, zero-customization frontend]
keywords: [admin, frontend, default, generated, access table, access view, hook scaffold, generator-ignore]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:itracker", "project:reserve-app", "project:doors-model", "status:established"]
category: page
status: established
projects: [trivia, itracker, reserve-app, doors-model]
evidence: ["trivia:unrecorded", "itracker:unrecorded", "reserve-app:unrecorded", "doors-model:unrecorded"]
alternatives: []
related: [dual-actor-frontend-architecture, hook-scaffold-default-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

For back-office actors that only need CRUD over master data, the generated frontend is enough. The model decides what the UI contains, so the admin frontend stays free of hand-written code.

## Practice

### Platform base

- Each access of the actor determines a generated page: a table access becomes a table page, a view access a view page, with create and edit forms as dialogs; relations get their own table and view pages ([UI model to frontend mapping](../../agent-docs/frontend/model-screen-layout.md)). Menu items come from the actor's menu entries ([navigation elements](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)).
- Layout gaps are model problems: an access whose target has no table or view cannot get a page from the generator, so complete the UI in the model first ([UI authoring guide](../../agent-docs/model/ui-authoring-guide.md)).
- Hook scaffolds are generated as `.default` files under `src/custom/hooks/`. A `.default` file is not compiled; it only takes effect when copied to a name without `.default` and registered from `application-customizer.tsx` ([hooks: using .default scaffolds](../../agent-docs/frontend/hooks/README.md)).
- `src/custom/` is gitignored in the frontend module, so nothing there needs a `.generator-ignore` entry ([frontend guide](../../agent-docs/frontend/README.md)).

### Project practice: leave the admin UI alone

This layer is project practice, not a platform feature:

- Do not activate scaffolds, override pages or theme for the admin actor; keep customization out of its pages entirely. The `.generator-ignore` then protects only itself and `.gitignore`.
- Improve the admin UX in the model (labels, table columns, layout, menu order), not in the frontend.
- When a single hook is needed (for example conditional validation on one form), activate just that scaffold and keep the rest inactive.

## Rationale

No custom code means nothing to maintain across generator upgrades, and every entity looks and behaves the same. The cost is limited UX flexibility and no frontend-only business logic.

## Example

- trivia: ten-plus entity types with fully generated tables and forms; dozens of scaffolds stay inactive.
- itracker: three entity types (users, categories, regions), full CRUD, landing on the users table.
- reserve-app: thirteen master-data entities with a uniform name-plus-active shape; one hook activated for conditional validation on one entity.
- doors-model: five master-data entities with a flat menu and consistent table, create form and detail layout.

## When to avoid

- Users need a tailored experience, custom navigation or frontend-side business logic.
- The actor is customer-facing rather than internal; see [[dual-actor-frontend-architecture]].

## Related

- [[dual-actor-frontend-architecture]] — an admin actor kept generated next to a customized actor
- [[hook-scaffold-default-pattern]] — how the inactive scaffolds work
