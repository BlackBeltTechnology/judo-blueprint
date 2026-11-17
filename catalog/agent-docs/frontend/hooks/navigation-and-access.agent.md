# navigation-and-access.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/navigation-and-access.md.

## Overview
- Covers routing, redirects, page-level access, hotkeys and navigation interception of the generated React frontend.

## Actor Accesses as Menu Items
- Sidebar menu = Actor accesses in the ESM model; each access → menu item (primary navigation).
- Menu built in `src/layout/Drawer/DrawerContent/Navigation/` from the application navigation controller.
- Boolean controls: `hiddenBy` (not rendered when true), `enabledBy` (disabled when false), `requiredBy` (field required when true).
- Backend interceptors set booleans on transfer objects; frontend reads them via `hiddenBy`/`enabledBy` expressions. Decide access on the backend.
- Scope: actor accesses (menu), relations (tabs, tables, links), attributes (form fields).

## RedirectServiceHook
- Generated `Redirect` page (`src/pages/Redirect.tsx`) calls the registered redirect service with URL search params.
- `REDIRECT_HOOK_INTERFACE_KEY = 'RedirectServiceHook'`; `type RedirectServiceHook = () => (searchParams: URLSearchParams) => Promise<void>`.
- Hook factory is a React hook (may call `useJudoNavigation`); returned function navigates itself. Throwing shows translated error `judo.pages.redirect.error`.
- Auth gate redirects unauthenticated users before this page; no own login redirect needed. Use `usePrincipal()` (`~/auth/principal-context`) when the target depends on user.
- Register: `context.registerService<RedirectServiceHook>(REDIRECT_HOOK_INTERFACE_KEY, ...)` in `application-customizer.tsx`.
- Examples: basic (missing `id` → throw), resolving target with a generated service, auth-aware redirect.

## Access Filtering
- Wraps the whole authenticated layout; can block or replace UI (e.g. "access denied" when principal lacks a modeled flag).
- Only one filter is used: the best-ranked registration. Not selected per page. Check no second filter is registered.
- `ACCESS_FILTER_COMPONENT_INTERFACE_KEY = 'AccessFilterComponent'`; props `AccessFilterComponentProps { principal: <Actor>Stored; children?: ReactNode }`.
- Exists only when the app has authentication. Layout renders `<AuthProxyComponent filter="(objectClass=AccessFilterComponent)" principal={principal}>`; with no service, children render unchanged.
- No `component` filter property, no extra props: page-level rules go inside component (e.g. `useLocation()`) or, better, into model `hiddenBy`/`enabledBy`.
- Time-based access example exists. Client-side filter is UX only; enforce authorization in backend.

## Hotkey Support
- Global hotkeys generated in `src/hotkeys.tsx` (`registerGlobalHotkeys`, uses `react-hotkeys-hook`). No `hotkeys` entry in application customizer.
- To add global hotkeys override `actor/src/hotkeys.tsx.imports.fragment.hbs` (imports) and `actor/src/hotkeys.tsx.body.fragment.hbs` (`useHotkeys(...)` calls) — Template Override Process.
- Generated function provides `t` and `[createDialog, closeDialog] = useDialog()`.
- Component-local shortcuts: `window.addEventListener('keydown', ...)` needs no override.
- Examples: context-aware hotkeys, hotkey help dialog.

## Navigation Interception
- `NAVIGATION_INTERCEPTOR_INTERFACE_KEY = 'JudoNavigationInterceptor'`; `NavigationInterceptorHook = ({ stringifyPath }) => NavigationInterceptor`.
- `NavigationInterceptor { decorateNavigation(to): string | Partial<Path>; onBeforeInitialLoad?(): void }`.
- Interceptor can only rewrite the target (e.g. sticky query params). No `beforeNavigate`; cannot cancel navigation.
- Unsaved-changes: use generated `useNavigationConfirmation` (`~/hooks`; see Extension Points); generated forms already use it.
- Session expiry: generated auth layer handles 401 (clears storage, reloads → identity provider). No custom session checks.

## Type-Safe Navigation
- `useJudoNavigation()` (from `~/components`) returns `{ navigate, clearNavigate, externalNavigate, navigateBackTo, back, isBackDisabled, setTitle }`.
- `navigate(to)` takes react-router `To` (string or `{ pathname, search }`) and applies registered navigation interceptor. Route helpers from `~/routes` (e.g. `routeToServiceEntityView(...)`).
- Breadcrumb stack, not browser history: `navigate` pushes; `back` pops; `navigateBackTo(item)` truncates; `clearNavigate(to)` empties and goes; `externalNavigate(url)` sets `window.location`.
- `isBackDisabled` when stack empty. `setTitle` sets page label (missing title logs warning). `back()` with empty stack goes to dashboard.
- Examples: query parameters, external navigation.

## Best Practices
- Clean up `keydown` listeners in `useEffect` return.
- Call `event.preventDefault()` for Ctrl+key shortcuts (else browser opens new window).
- Check auth state (`principal`) before rendering protected UI.
- Keep custom components under `src/custom`; generated hook files are not generated (only `.default` twin), no `.generator-ignore` entry needed.

## Complete Example
- Full combined example of hooks in one file.

## Troubleshooting
- Hotkeys not working: verify listener attached and cleaned up; log keys and ctrl state.
- Access filter not showing: verify `registerService` with `ACCESS_FILTER_COMPONENT_INTERFACE_KEY`.
- Navigation not redirecting: log path before `navigate`.

## Related Documentation
- Hook system overview, data hooks, action hooks, development workflow.
