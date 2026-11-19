---
id: dual-actor-frontend-architecture
title: Dual-Actor Frontend Architecture (Custom + Generated)
description: Give each actor its own generated frontend module with its own customization level, so a customer-facing actor can be custom-built while an admin actor stays fully generated.
aliases: [one frontend per actor, multi-actor frontend, mixed customization frontends]
keywords: [actor, frontend, multi-actor, customization level, generator-ignore, role-based UI, keycloak client]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:itracker", "project:reserve-app", "project:doors-model", "status:established"]
category: framework
status: established
projects: [trivia, itracker, reserve-app, doors-model]
evidence: ["trivia:unrecorded", "itracker:unrecorded", "reserve-app:unrecorded", "doors-model:unrecorded"]
alternatives: [single-actor-heavy-customization]
related: [complete-frontend-replacement, admin-default-generated-ui, single-actor-heavy-customization]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Different roles need different experiences: back-office users want fast generated CRUD, customers or participants want a tailored UI. The platform generates one frontend module per actor, so each can be customized to a different degree on top of one shared backend.

## Practice

### Platform base

- A frontend module is generated per modeled actor, named `<app>__<actor path>` (for example `<app>__service__admin`) under `application/frontend-react/`, next to a shared `model/` folder that holds the generated UI model. Each module has its own `.generator-ignore`, `src/custom/` folder and hook scaffolds ([frontend guide](../../agent-docs/frontend/README.md)).
- Each actor also gets its own generated Playwright e2e project, with its own `node_modules`, so tests and helpers are split per actor and each project points at its own actor's frontend ([E2E troubleshooting](../../agent-docs/e2e-testing/troubleshooting.md)).
- What an actor sees is defined by its accesses and menu in the model; each access becomes a navigation entry and page of that actor's frontend ([navigation controller and actor accesses](../../agent-docs/frontend/model-screen-layout.md)).
- The backend resolves the actor from the token's `azp` claim (dashes become dots, the result must equal an actor FQN). A frontend client with another name needs the `JUDO_PLATFORM_ACCEPTABLE_CLIENTS` whitelist; each actor exposes `~meta` and `~principal` endpoints that a custom frontend uses to obtain a token ([authentication guide: several Keycloak clients in one realm](../../agent-docs/backend/authentication-guide.md)).
- Customization options per module, from least to most: leave scaffolds inactive; activate hooks from `src/custom/`; sub-themes and custom visual elements; extra routes ([hooks overview](../../agent-docs/frontend/hooks/README.md), [extension points](../../agent-docs/frontend/extension-points.md)).

### Practice notes: pick a customization level per actor

- Admin or reference-data actors: keep fully generated ([[admin-default-generated-ui]]) and improve the experience in the model.
- Customer-facing actors: customize deliberately: hooks first ([[single-actor-heavy-customization]]), full replacement only when the generated layout cannot serve ([[complete-frontend-replacement]]). A replaced frontend gets no generator updates.
- Restrict what each actor sees with its own accesses and, where fields must differ, separate transfer objects per role rather than frontend hiding.
- Two actors are the tested shape; they can differ in authentication (for example an anonymous public actor next to authenticated staff actors). A third actor can break the generated frontend build with duplicate type imports, because actors are processed in model file order and a later actor can rebind an earlier actor's operation actions (known issue, see [build process](../../agent-docs/deployment/build-process.md)). Adding the new actor first in the model file avoided it in a tested model; check the generated sources after adding an actor.
- Keep `.generator-ignore` minimal for the generated actors and larger only for the customized one.

## Rationale

Each audience gets the fitting tool: generated CRUD costs nothing to maintain, a custom UI is built only where it pays. The cost is maintaining two approaches, and customized modules do not benefit from generator updates.

## Example

- A completely custom participant SPA next to an admin actor that is a generated CRUD app with inactive scaffolds.
- Two actors (document tracking with an approval workflow, reference data CRUD), both fully generated, with shared branding from model colors and the logo.
- A multi-actor app: one actor with full CRUD and a single hook, one for booking management with restricted transfer objects, and dashboard-only actors.
- Two Flutter apps: one mixes authenticated staff actors with an anonymous public portal.
- A model-only example: two actors (simple master-data admin, complex order lifecycle employee) with no frontend generated yet.

## When to avoid

- All users share the same experience: one actor is enough.
- The actors differ only in permissions: use access and transfer object differences in the model, not separate frontends.

## Related

- [[complete-frontend-replacement]] — replacing one actor's frontend entirely
- [[admin-default-generated-ui]] — the fully generated side
- [[single-actor-heavy-customization]] — heavy hook customization of one actor
