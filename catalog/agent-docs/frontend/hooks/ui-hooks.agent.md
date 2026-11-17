# ui-hooks.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/ui-hooks.md.

## Overview

- UI hooks customize look and layout: AppBar extra component, hero, logo, footer text, menu.
- No hook for a single field or whole view. Use model-level `customImplementation`: set `customImplementation=true` on the `DataField` (not the `DataColumn`) and register a component for the generated element key. See `../advanced-patterns.md` (Component Replacement Hook). Scaffold `src/custom/hooks/custom-implementations/register<Container>CustomImplementations.tsx.default`.
- Field stays in the mask; the component gets the value via proxy props.
- To load but not show: `customImplementation=true` and render nothing.
- `ui:Placeholder` with `customImplementation` generates no scaffold and renders nothing; use a `DataField`.

## AppBar Extra Components

- Purpose: notification bell, user menu, theme toggle, quick actions.
- Exactly ONE extra component. Register as Pandino service under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (value `'CustomVisualElement'`, from `~/custom`) with property `{ component: 'AppBarExtraComponents' }`.
- Service type `AppBarExtraComponentsHook` (from `~/layout/Header/HeaderContent`): `() => ({ Component, spaceRequired? })`. `spaceRequired` default 1: grid space claimed beyond default header.
- Placement: rendered in the drawer (below logo, above menu; single button stretches full width) and in the header grid right-aligned before settings and profile. Wrap several controls in one flex `Box` to keep them in a row. No other slot (e.g. no top-right language switch).
- Multiple controls: compose in one wrapper component and set `spaceRequired` to match (e.g. 3).
- Stored layout: `ConfigContext` (drawer orientation etc.) is in `localStorage` under `<model>-config`. A stored config overrides model changes; clear with `localStorage.removeItem("<model>-config")`.
- Examples: user profile menu (`usePrincipal()`), theme toggle, quick search dialog. Illustrative.

## Hero and Logo Customization

- Hero props: `CustomHeroPropsHook` (`CUSTOM_HERO_PROPS_HOOK_INTERFACE_KEY` = `'CustomHeroPropsHook'`, from `~/hooks/useHeroProps`). Factory returning `(defaults) => newProps`. `UseHeroProps`: `imgSrc`, `actorName`, `preferredUsername?`, `email?`.
- Logo: `CustomLogoPropsHook` (`CUSTOM_LOGO_PROPS_HOOK_INTERFACE_KEY` = `'CustomLogoPropsHook'`, from `~/hooks/useLogoProps`). Maps `UseLogoProps` (`subTitle`, `imgSrc`, `iconSrc`). Image paths relative to `public/`.
- Logo/icon defaults come from actor `applicationLogo` in the model; prefer model change for permanent change.
- Hero has no component-level hook; replacing it needs a template override (see `../README.md#template-override-process`).

## Footer Text

- `FooterTextHook` (`FOOTER_TEXT_HOOK_INTERFACE_KEY` = `'FooterTextHook'`, from `~/layout/Footer`): factory returning `() => string`. Rendered as text, not HTML; no links.
- Default: application title and current year.
- Links or markup need a template override of `actor/src/layout/Footer.tsx`.

## Menu Manipulation

- Hook: `MenuItemsCustomizerHook` (`MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY`, from `~/layout/Drawer/DrawerContent/Navigation`). Factory `() => (menuItems) => newItems`.
- Generated item `id` = model element id with `@` removed (long). Match on `title` (model `label`) or id suffix; log `menuItems` to see them.
- `NavItemType`: `{ id, type: 'group' | 'collapse' | 'item', title?, url?, onClick?, icon?, disabled?, hiddenBy?, children? }`.
- Type rules: top-level with children = `group`; nested with children = `collapse`; leaf = `item`. Drawer renders top-level only as `group` or `item`; a top-level `collapse` renders wrongly.
- Add: splice into array at an index. Remove: `filter`. Reorder: copy first (`[...menuItems]`) because `sort()` mutates framework-owned array; order by `title`; unknown titles to the end.
- Role-based: `usePrincipal()` roles (`ADMIN`, `MANAGER`) filter by item id.
- Icon names are strings (e.g. `chart-bar`).
- Menu operation actions: separate hook via `registerMenuActionsHook(context)` (scaffold `src/custom/hooks/registerMenuActionsHook.ts.default`, generated only when the app has menu operations). Key `MENU_ACTIONS_HOOK_INTERFACE_KEY` from `~/layout/Drawer/DrawerContent/Navigation/menuCustomization`; value is `'MENU_ACTIONS_HOOK'` (no `Hook` suffix, unlike others). Returns `MenuPageActions`: optional handler per navigation controller action, plus `post<Action>` for actions without input.

## Best Practices

- Keep components small and focused.
- Use theme colors (`color="inherit"`), not hardcoded `sx` colors.
- Handle loading: show `CircularProgress` while `usePrincipal()` is null.
- Protect custom components: brand-new hand-written files (e.g. `NotificationBell.tsx`) are outside generator scope; no `.generator-ignore` entry. See `hooks/README.md` → Understanding `.generator-ignore`.
- Responsive: `useMediaQuery(theme.breakpoints.down('sm'))`.

## Complete Example

- `application-customizer.tsx` `customize(context)` registers: AppBar extra (`spaceRequired: 3`), menu customizer, footer text.

## Troubleshooting

- AppBar component not showing: check service property is exactly `{ component: 'AppBarExtraComponents' }`; check import.
- Logo not displaying: file must exist under `public/`; `imgSrc` relative to `public/` (e.g. `/images/logo.svg`).
- Menu changes not applying: verify `MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY` registration.

## Related Documentation

- [Hook System Overview](./README.md)
- [Data Hooks](./data-hooks.md)
- [Table Hooks](./table-hooks.md)
- [Theming](../theming.md)
- [Development Workflow](../development-workflow.md)
