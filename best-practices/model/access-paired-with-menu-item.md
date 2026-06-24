---
id: "access-paired-with-menu-item"
title: "Every UI-Reachable Access Must Be Paired with a MenuItemAccess"
domain: "model"
category: "access"
score: 90.0
usage_count: 8
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - judo-demo-miniworkflow
  - mlszksz-platform
  - rackinspect
  - park-here
  - reserveapp
  - ams-frontend
  - indamedia-adtrack
  - compsychletter
---
## Description

An `Access` on an `ActorType` defines a REST/data surface only — it does **not** add anything to the navigation menu. The JUDO frontend generator drives the navigation drawer (`menu-items.tsx`) and routing (`routes.tsx`) **exclusively** from `ActorType.menuItems`. An actor with N accesses and zero menu items renders an empty sidebar; the dashboards are reachable by URL/REST but invisible to end users.

**Rule:** every `Access` intended to be UI-reachable MUST be paired with a `MenuItemAccess` (directly under `ActorType.menuItems`, or nested in a `MenuItemGroup`). Create the menu item in the same authoring stage as the access. API-only accesses (intentionally hidden from the menu) are the documented exception — flag them in the model with documentation/annotation.

## Structure

- `Access` carries data semantics (target TO, cardinality, getter, CRUD flags). It has **no** `icon`, `label`, or `showInMenu` field.
- `MenuItemAccess` carries navigation chrome: `label` (display name), `iconName` (e.g. MDI icon), optional `hidden`/`hiddenBy` for visibility guards, optional `subTheme`. It references one `Access` via its `access` field.
- `MenuItemGroup` is a container for nested menu items; use when more than ~5 top-level entries or when section grouping is meaningful.
- `menuOrientation` on the actor (`VERTICAL` / `HORIZONTAL`) controls drawer layout.
- Authoring order: `Access` first, `MenuItemAccess` after (the `MenuItemAccess.access` reference resolves by xmi:id on the just-created access). EList append-only ordering applies — plan top-to-bottom menu order before issuing creates.

## Examples

### judo-demo-miniworkflow
`GenericActor` declares accesses (`myDocuments`, `waitingForApproval`, `users`, …) and a parallel set of `MenuItemAccess` entries with MDI icons. Menu visibility on admin entries is gated via `hiddenBy: GenericUser.isNotAdmin`, demonstrating that hidden menu items still need a `MenuItemAccess` — `hidden`/`hiddenBy` is on the menu item, not the access.

### MLSZKSZPlatform (AdminActor)
13 access points → 13 menu items, each with icon and label ("5 menu items for entity management" in the admin domain). One-to-one access ↔ menu-item correspondence.

### ReserveApp (AdminActor)
13 access points described in the catalog as "13 access points (menu item accesses)" — phrasing reflects the lockstep pairing: every access has a corresponding `MenuItemAccess`. Actors with no accesses yet (Logistician, Doorman, Readonly) have no menu items.

### AMS-Frontend
Manager actor has 3 accesses, 3 menu items (people / done_all / done icons). Admin actor has 3 accesses, 3 menu items (people / apps / done_all icons). Lockstep pairing.

### CompSychLetter (anti-example — Phase-0 gap)
`LetterUser` declares 3 DERIVED accesses (`documents → DocumentsDashboard`, `authoring → AuthoringDashboard`, `data → DataDashboard`) but `menuItems.totalCount = 0`. Generated `menu-items.tsx` is `return []` and `routes.tsx` has only `/`. The user logs in, principal resolves, but the sidebar is blank. Phase-1 of the project is expected to add the three matching `MenuItemAccess` entries. The pattern is well-formed; the menu-pairing step was simply not run yet.

## Trade-offs

- Pros: Single rule "create access → create menu item" eliminates the most common cause of blank-menu post-deployment surprises. Keeps data and UI concerns cleanly separated (`Access` = REST, `MenuItemAccess` = chrome).
- Cons: Two model elements per dashboard entry; ordering matters (EList append-only).
- Prefer when: Any access is intended to be user-facing (almost always). Skip only when an access is explicitly API-only (programmatic/internal) — and document the exception.

## Anti-Patterns

- **Access without MenuItemAccess** — produces blank sidebar; users cannot reach the dashboard except by direct URL. Verify with `judo_cli graphql '{ esm { actortypes { items { name menuItems(limit:1){totalCount} accesses(limit:1){totalCount} } } } }'` — any actor with `accesses > 0` and `menuItems = 0` is suspect.
- **Putting `iconName` on Access** — `ESM_Access` has no such field; menu chrome lives only on `MenuItemAccess`.
- **Relying on a fallback** — there is no "accesses-as-menu" fallback in the React generator. `useMenus()` reads `menuItems` and only `menuItems`.
- **Expecting `build -f` alone to populate `menu-items.tsx` and `routes.tsx`** — both files are typically in `.generator-ignore` and are never overwritten by the generator. Adding `MenuItemAccess` to the model and rebuilding does NOT auto-populate them. Manual edits to `menu-items.tsx` (add `NavItemType` entries) and `routes.tsx` (add lazy route entries) are always required. `extra-routes.tsx` is NOT generator-ignored and is overwritten every build — do not put custom routes there.
- **Running `build -f` without `-i` after `transform --load`** — `transform --load` poisons the frontend checksum file. The next `build -f` fails with "There are manual changes in the generated files". Always run `build -f -i` after `transform --load`.

## Verification

```bash
judo_cli graphql '{
  esm { actortypes(limit:10) {
    items {
      fqn
      accesses(limit:1) { totalCount }
      menuItems(limit:1) { totalCount }
    }
  } }
}'
```

Any actor where `accesses.totalCount > 0 && menuItems.totalCount == 0` is missing its menu wiring (unless every access is intentionally API-only — document the reason).

## Related Patterns

- [panel-dashboard-transfer](panel-dashboard-transfer.md) — the Dashboard TO pattern these accesses target
- [self-access-point](self-access-point.md) — `self`-getter accesses (still need MenuItemAccess)
- [derived-access-filtering](derived-access-filtering.md) — derived accesses with `hiddenBy` on menu items
