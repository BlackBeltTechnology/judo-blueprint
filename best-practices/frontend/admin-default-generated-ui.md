---
id: "admin-default-generated-ui"
title: "Admin Frontend with Default Generated JUDO UI"
domain: "frontend"
category: "page"
score: 91.9
usage_count: 6
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - itracker
  - skillmatrix-frontend
  - reserve-app
  - doors-model
  - ams-frontend
---
## Description

Use the JUDO-generated frontend as-is for administrative CRUD operations, with minimal or zero customizations. The generated UI provides access table pages (list views), access view pages (detail views), relation table/view pages (sub-entity navigation), standard forms, and a complete routing/navigation system. Hook scaffolds are generated but left as `.ts.default` (inactive) in React, or have no hook mechanism in Flutter. This approach is viable when the admin experience does not require special UX.

## Structure

```
src/
  pages/Actors/Admin/
    Entity1/AccessTablePage/     # Generated list view
    Entity1/AccessViewPage/      # Generated detail view
    Entity2/AccessTablePage/
    Entity2/AccessViewPage/
    Entity1/Entity2/RelationTablePage/   # Sub-entity list
    Entity1/Entity2/RelationViewPage/    # Sub-entity detail
  custom/hooks/
    pages/*.ts.default           # Inactive page hook scaffolds
    containers/*.ts.default      # Inactive container hook scaffolds
    dialogs/*.ts.default         # Inactive dialog hook scaffolds
  theme/                         # Default generated theme
```

`.generator-ignore` contains only `.generator-ignore` and `.gitignore`.

## Examples

### Trivia
Admin frontend manages 10+ entity types (Categories, Contests, Questions, Tasks, Standings, Tests, Users, Uploads, Admins, PersonalBests) with 100% generated pages, tables, and forms. 24 hook scaffolds remain inactive (`.ts.default`). Only 2 page overrides exist (Categories AccessViewPage, Contest Categories RelationViewPage) but contain no custom logic beyond generated patterns.

### itracker
Admin frontend manages 3 entity types (Users, Categories, Regions) with 6 pages, 3 dialog forms, and 18 inactive hook scaffolds (9 container + 3 dialog + 6 page). Full CRUD for all entities. `.generator-ignore` protects only itself and `.gitignore`. Dashboard lands on Users table.

### SkillMatrix (Flutter)
Admin actor manages user accounts with 5 pages (Dashboard, Users Table/Create/View/Update) plus 3 generic pages (Settings, Error, Blank). Single menu item ("Users"). Special features: "Delete User" with conditional confirmation ("The user has skills. Are you sure?"), "Create Test Data" unbound operation, and role assignment switches conditionally enabled via `actorIsAdmin` flag. Zero customizations beyond model definition.

### reserve-app
AdminActor manages 13 entity types (Companies, Gates, LoadingTimes, LoadingTypes, ManagedUsers, Partners, ProductCategories, Projects, Spots, StorageTypes, Units, VehicleTypes, Profile) with 13 access points, 18 dialogs, and 10 relation pages. Nearly all generated -- only 1 hook activated (StorageTypes conditional validation). Most entities follow an identical `name`+`active` pattern with Table + Form + View_Edit containers.

### doors-model
Admin actor model defines simple CRUD for 5 master data entities: Companies (5 columns), Employees (5 columns), Divisions (2 columns), Positions (2 columns), and Banks. Each entity has a table, create form, and detail view with consistent layout. Flat 5-item menu using Material Design icons (domain, account_group_outline, family_tree, arrow_decision, bank). Model-only -- would generate standard Admin CRUD frontend.

### ams-frontend
Admin Flutter actor manages 3 entity types (Applications, Campaigns, Users) with 3 navigation menu items. All page structure is 100% generated. The only customizations are cross-cutting Handlebars template overrides (Excel download function, widget rendering tweaks) -- no per-page hooks or code modifications. `.generator-ignore` protects only the REST client file, not pages or theme.

## Trade-offs

- **Pros**: Zero custom code to maintain; automatic updates from generator; consistent UX across all entities; rapid development
- **Cons**: Limited UX flexibility; all entities look and behave the same; no custom business logic in frontend
- **When to use**: Internal admin dashboards, back-office tools, or when admin UX is not a priority

## Related Patterns

- [dual-actor-frontend-architecture](dual-actor-frontend-architecture.md)
- [hook-scaffold-default-pattern](hook-scaffold-default-pattern.md)
