---
id: "dual-actor-frontend-architecture"
title: "Dual-Actor Frontend Architecture (Custom + Generated)"
domain: "frontend"
category: "framework"
score: 42.0
usage_count: 4
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - itracker
  - reserve-app
  - doors-model
alternatives:
  - single-actor-heavy-customization
---
## Description

A JUDO project can generate separate frontend applications for different actors (roles), each with its own customization level. One actor frontend may be completely custom-built while another uses the standard generated JUDO UI. Both share the same backend model and services but present entirely different user experiences. Each actor frontend is deployed at its own context path (`/{model}/{actor}`). In some projects, both actors use the generated UI with no customizations. The pattern extends to three or more actors when the domain requires distinct role-based interfaces.

## Structure

```
application/frontend-react/
  model/                          # Shared UI model artifacts
  {model}__{actor1}/              # Actor 1 frontend (custom or generated)
    .generator-ignore             # Extensive or minimal ignore list
    src/App.tsx                   # Custom or generated root
    src/custom-app/               # Hand-built components (if custom)
  {model}__{actor2}/              # Actor 2 frontend (generated)
    .generator-ignore             # Minimal ignore list
    src/custom/hooks/             # Hook scaffolds (.ts.default)
    src/pages/                    # Generated pages
```

Deployment paths:
- Actor 1: `/{model-name}/{actor1-name}` (e.g., `/trivia/Player`)
- Actor 2: `/{model-name}/{actor2-name}` (e.g., `/trivia/Admin`)

## Examples

### Trivia
Two actor frontends: **Player** (`trivia__actors__player__player`) is a completely custom quiz game SPA with glassmorphic design, dialog-based navigation, and localStorage sessions. **Admin** (`trivia__actors__admin__admin`) is a standard generated JUDO CRUD app with default theme and 24 inactive hook scaffolds. Same backend, completely different UX.

### itracker
Two actor frontends: **UserActor** (initiative tracking with approval workflow, 9 pages, 8 dialogs, 42 hook scaffolds) and **Admin** (reference data CRUD with 6 pages, 3 dialogs, 18 hook scaffolds). Both are 100% generated with zero code customizations. Shared Howmet Aerospace branding via model-defined colors and `logo.svg`.

### SkillMatrix (Flutter)
Three actor frontends: **Admin** (5 pages, user management), **HR Employee** (65 pages, full skill matrix management with reports and search), **Professional** (28 pages, self-service profile + manager subordinate/training management). All 100% generated Flutter/Dart with identical theming. Extends the pattern to 3 actors with a dual-namespace Professional actor (self-service + manager).

### kozut-eugyfel-client (Flutter)
Three actor frontends: **Munkatars** (~75 pages, employee task and report management), **Admin** (~40 pages, user/org/county management), **E-Ugyfel Alkalmazas** (~3 pages, public citizen portal with anonymous access). Extends to 3 actors with different authentication levels -- OAuth required for workers/admin, anonymous access for citizens. All generated with shared template overrides.

### reserve-app
Five actor frontends: **AdminActor** (13 access points, full CRUD management with 1 custom hook), **PartnerActor** (2 access points, reservation management), **LogisticianActor** (dashboard only), **DoormanActor** (dashboard only), **Readonly** (dashboard only). Extends the multi-actor pattern to 5 roles with 3 dashboard-only placeholder actors. Partner uses restricted "ForPartner" transfer objects with fewer attributes.

### doors-model
ESM model defines 2 actors: **Admin** (simple CRUD for 5 master data entities -- companies, employees, divisions, positions, banks) and **Employee** (complex contract lifecycle management with 19 access points, 4 menu groups, and workflow-driven approval/signing/close operations). No frontend generated yet -- model-only project using older ESM XML format.

### ams-frontend
Two Flutter actor frontends: **Admin** (250 Dart files, manages applications/campaigns/users with Open/Close/Load campaign operations and custom Excel download) and **Manager** (411 Dart files, approval workflow with bulk approve-all and subordinate management). Both fully generated with shared Handlebars template overrides. Distinct navigation menus per role.

## Trade-offs

- **Pros**: Right tool for each user role; admin gets fast generated CRUD; public users get polished custom UX; shared backend
- **Cons**: Maintaining two frontend approaches increases complexity; custom frontend does not benefit from generator updates
- **When to use**: When different user roles have fundamentally different UX needs (e.g., admin CRUD vs. public-facing experience), or when the domain naturally separates into end-user vs. admin workflows

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [admin-default-generated-ui](admin-default-generated-ui.md)
- [single-actor-heavy-customization](single-actor-heavy-customization.md)
