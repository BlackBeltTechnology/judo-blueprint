---
title: Frontend Extension Points
description: Extra routes, guest page, sub-theme hooks, menu actions hook, application switcher, navigation confirmation and table state persistence in the generated React frontend.
---

# Frontend Extension Points

Supported extension points of the generated React frontend that are not hooks of a specific page.

## Extra Routes

`src/extra-routes.tsx` exports `extraRoutes: Array<{ path: string; element: ReactElement; exact?: boolean }>`. It is generated empty, and the generated `routes.tsx` prepends these routes to the generated ones. Add custom React Router routes there instead of editing generated routing files (protect the file in `.generator-ignore`).

## Guest Page

With `supportGuestAccess` enabled on the application, an unauthenticated user is not redirected to `signinRedirect`. The auth gate renders a guest page instead. Register your own component as a service under `GUEST_PAGE_INTERFACE_KEY` (the value `'GuestPage'`, imported from `~/auth/Auth`):

```typescript
context.registerService<FC<any>>(GUEST_PAGE_INTERFACE_KEY, GuestPage);
```

The scaffold `src/custom/hooks/default-guest-page-hook-registration.tsx.default` contains `registerGuestPage(context)`. The default page shows a Login / Register button (i18n key `judo.guest-page.login-register`) that calls `signinRedirect()`.

## Sub-Theme Hooks

A named sub-theme is registered by `register<SubTheme>SubThemeHook(context)` (scaffold `src/custom/hooks/sub-themes/register<Name>SubThemeHook.tsx.default`):

```typescript
context.registerService<SubThemeHook>(SUB_THEME_HOOK_INTERFACE_KEY, mySubTheme, { name: '<safeCamelCaseName>' });
```

`SUB_THEME_HOOK_INTERFACE_KEY` and `SubThemeHook` come from `~/theme/SubThemeWrapper`. The function receives `(parentTheme: Theme, data?: any)` and returns `{ components: { ... } }` MUI overrides. The generated sample overrides `MuiPaper.styleOverrides.root`.

## Menu Actions Hook

The menu actions hook is registered with `registerMenuActionsHook` (scaffold `src/custom/hooks/registerMenuActionsHook.ts.default`) using `MENU_ACTIONS_HOOK_INTERFACE_KEY` from `~/layout/Drawer/DrawerContent/Navigation/menuCustomization`. Gotcha: the key's value is `'MENU_ACTIONS_HOOK'`, without the `Hook` suffix used by the other hook keys (`MenuItemsCustomizerHook`, `CustomHeroPropsHook`, `CustomLogoPropsHook`, `FooterTextHook`). Registered handlers return a `MenuPageActions` object with an optional handler per navigation action. The menu items customizer key lives in the Navigation `index.tsx` (value `'MenuItemsCustomizerHook'`).

## Cards Configuration Hook

Card containers can be configured through a registration generated at `src/custom/hooks/components/cards/register<Component>ConfigurationHook.tsx.default`.

## Multi-Application Switcher

When the model has alternative applications, the profile popup shows an application switcher (`useApplicationSelector()`). `changeApplication(key)` clears the security storage and navigates the whole page to `origin + '/' + key`. `generateAlternativeApplications` builds the key-to-name map from translation keys `applications.<simpleName>`.

## Unsaved-Changes Navigation Confirmation

The generated hook `src/hooks/useNavigationConfirmation.ts` gates navigation away from edited state. Reuse it in custom components that edit data to get the same unsaved-changes confirmation as generated forms.

## Table State Persistence

`LazyTable` and `EagerTable` persist grid state in `sessionStorage` under keys built from the table `uniqueId`: `${uniqueId}-sortModel`, `${uniqueId}-filterModel`, `${uniqueId}-filters`, `${uniqueId}-rowsPerPage` and, with a licensed MUI plan, `${uniqueId}-columnState`. The keys depend only on `uniqueId`, so it must be unique per table; two tables with the same id read and write each other's state.

## Hook Files and the Custom Folder

Hook scaffolds are generated only when the corresponding hook flag is set in the model (for example `generateActionsHook`). Hook scaffolds are generated as `.default` files under `src/custom/` (the frontend `.gitignore` ignores `*.ts.default` / `*.tsx.default`). A copy without `.default`, and any file you add yourself, is outside generator scope and needs no `.generator-ignore` entry. `src/custom/` itself is **not** gitignored: commit your custom code. The generator does write four files there without `.default` (`application-customizer.tsx`, `index.tsx`, `custom-element-types.ts`, `interfaces.ts`); if you hand-edit one of those, list it in `.generator-ignore`.
