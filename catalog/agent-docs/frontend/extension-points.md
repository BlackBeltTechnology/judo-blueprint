---
title: Frontend Extension Points
description: Extra routes, guest page, sub-theme hooks, menu actions hook, application switcher, navigation confirmation and table state persistence in the generated React frontend.
aliases: [custom routes, guest login page, custom theme hook, menu customization, table state storage, switch application]
keywords: [extraRoutes, GUEST_PAGE_INTERFACE_KEY, SUB_THEME_HOOK_INTERFACE_KEY, registerMenuActionsHook, MENU_ACTIONS_HOOK_INTERFACE_KEY, useApplicationSelector, useNavigationConfirmation, LazyTable, sessionStorage, uniqueId, generateActionsHook]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Frontend Extension Points

Supported extension points of the generated React frontend that are not hooks of a specific page.

## Extra Routes

`src/extra-routes.tsx` exports `extraRoutes: Array<{ path: string; element: ReactElement; exact?: boolean }>`. It is generated empty, and the generated `routes.tsx` prepends these routes to the generated ones. Add custom React Router routes there instead of editing generated routing files (protect the file in `.generator-ignore`).

## Guest Page

With `supportGuestAccess` enabled on the application, an unauthenticated user is not redirected to `signinRedirect`. The auth gate renders a guest page instead. If no `GuestPage` service is registered, the gate shows the application name and a `Login / Register` button that calls `signinRedirect()`. Register your own component as a service under `GUEST_PAGE_INTERFACE_KEY` (the value `'GuestPage'`, imported from `~/auth/Auth`):

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

## Dashboard Page

A page whose container is an empty dashboard (no layout) renders a `ComponentProxy` for the custom visual element key `DashboardPage` (`DASHBOARD_PAGE_INTERFACE_KEY`, exported from the generated `src/pages/index.tsx`) and shows `Hello!` when no service matches. Register an `FC` under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (from `~/custom`) with the service property `component` set to `'DashboardPage'` to replace that page:

```typescript
context.registerService<FC<any>>(CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY, MyDashboard, { component: 'DashboardPage' });
```

## Cards Configuration Hook

Card containers can be configured through a registration generated at `src/custom/hooks/components/cards/register<Component>ConfigurationHook.tsx.default`.

The registration function is `register<Component>CardsContainerConfig(context)`. It registers a hook under the service key `<COMPONENT>_CARDS_CONTAINER_CONFIG_HOOK_INTERFACE_KEY`. The hook takes no arguments (it may call React hooks) and returns this object, with every member optional:

```typescript
{
  layout?: 'horizontal' | 'vertical';
  showPagination?: boolean;
  ToolbarElement?: FC<ToolbarElementProps<Row>>;   // filter bar above the cards
  ActionbarElement?: FC<ActionbarElementProps<Row>>;
  CardElement?: FC<CardProps<Row, RowActionDefinitions>>; // one card per row
}
```

A custom `CardElement` should render a `<Grid size={ { sm: 12, md: 6, lg: 4, xl: 4 } }>` as its root so cards line up on all devices.

The cards container renders no create button of its own. `ActionbarElement` is the place for one: it renders above the cards when set, and without it the container shows no action bar.

The cards container also renders no row operation buttons. Its generated template passes row actions only as row-click handlers (`onRowClick`) and never builds the `tableRowActions` that the table container uses, so table operations such as `<Operation>` must be added in a custom `CardElement`.

A cards container on a relation needs a refresh action on that relation table. The generated cards container calls `fetch` unconditionally when it loads, and the generated page passes `fetch` only when the table has a refresh action, so without one the load fails with `fetch is not a function`.

## Multi-Application Switcher

When the model has alternative applications, the profile popup shows an application switcher (`useApplicationSelector()`). `changeApplication(key)` clears the security storage and navigates the whole page to `origin + '/' + key`. `generateAlternativeApplications` builds the key-to-name map from translation keys `applications.<simpleName>`.

## Unsaved-Changes Navigation Confirmation

The generated hook `src/hooks/useNavigationConfirmation.ts` gates navigation away from edited state. Reuse it in custom components that edit data to get the same unsaved-changes confirmation as generated forms.

## Table State Persistence

`LazyTable` and `EagerTable` persist grid state in `sessionStorage` under keys built from the table `uniqueId`: `${uniqueId}-sortModel`, `${uniqueId}-filterModel`, `${uniqueId}-filters`, `${uniqueId}-rowsPerPage` and, with a licensed MUI plan, `${uniqueId}-columnState`. The keys depend only on `uniqueId`, so it must be unique per table; two tables with the same id read and write each other's state.

## Event Bus

The generated app wraps the page tree in an `EventBusProvider`. Custom components read it with `useEventBus()` (from `~/hooks`), which returns `{ publish, subscribe }`. It must run inside the provider, otherwise it throws.

- `publish(topic: string, ...args)` calls every handler registered for `topic`, synchronously, in registration order.
- `subscribe(topic: string, handler)` registers the handler and returns an unsubscribe function. Call it in a `useEffect` cleanup.
- Topics are plain strings. Generated pages use two formats, where `<pageXmiId>` is the page's XMI id from the UI model:
  - `refresh:<pageXmiId>` asks the page to reload its data. Operation actions publish it for the root page after they finish.
  - `<pageXmiId>:refreshed` is published with the fresh data after a page's refresh action succeeds.
- The XMI ids change with the model, so read them from the generated page file (the `<Page>XMIID` constant in `pages/types.ts`) instead of hard-coding them.

## Hook Files and the Custom Folder

Hook scaffolds are generated only when the corresponding hook flag is set in the model (for example `generateActionsHook`). Hook scaffolds are generated as `.default` files under `src/custom/` (the frontend `.gitignore` ignores `*.ts.default` / `*.tsx.default`). A copy without `.default`, and any file you add yourself, is outside generator scope and needs no `.generator-ignore` entry. `src/custom/` itself is **not** gitignored: commit your custom code. The generator does write four files there without `.default` (`application-customizer.tsx`, `index.tsx`, `custom-element-types.ts`, `interfaces.ts`); if you hand-edit one of those, list it in `.generator-ignore`.

### Typeahead Option Getters

A string input with the typeahead flag renders `TextWithTypeAhead`, an autocomplete with `freeSolo` enabled (free text is allowed). The page's custom hooks can provide the suggestions through a getter named `get<AttributeName>Options`, where `<AttributeName>` is the input's attribute name with its first letter upper-cased (for example `getForm_<field>Options` for the attribute `form_<field>`):

```ts
get<AttributeName>Options?: (
  searchText: string,
  data: <Data>,
  editMode: boolean,
  validation: Map<keyof <Data>, string>
) => Promise<string[]>;
```

The getter is optional and returns the list of suggestion strings.
