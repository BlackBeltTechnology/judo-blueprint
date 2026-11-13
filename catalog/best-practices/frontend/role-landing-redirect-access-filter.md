---
id: role-landing-redirect-access-filter
title: Role Landing Redirect via Access Filter Component
description: "A registered AccessFilterComponent sends each signed-in role from the home route to its own first visible menu entry, derived from the generated menu tree instead of a role-to-URL map."
aliases: [post-login landing page, role home redirect, landing redirect]
keywords: [AccessFilterComponent, landing page, redirect, role, hiddenBy, menu, useMenus, home route]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: navigation
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/components/LandingRedirect.tsx", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/application-customizer.tsx"]
alternatives: [operation-flow-redirect-pattern]
related: [operation-flow-redirect-pattern, post-operation-navigation-hook, access-paired-with-menu-item]
fragment: "none: frontend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

An application with several roles has one home route, but not every role may open the page behind it. The generated page for a role that is not allowed to see it fails to load and the app then shows the not-found page. A small component mounted as the access filter looks at the signed-in principal and the menu the principal can see, and moves roles that cannot use the home page to their first visible menu entry.

## Practice

### Platform base

- Register one service under `ACCESS_FILTER_COMPONENT_INTERFACE_KEY` from `application-customizer.tsx`. It receives `{ principal, children }`, is rendered around the authenticated layout, and without a registered service the children render unchanged ([access filtering](../../agent-docs/frontend/hooks/navigation-and-access.md#access-filtering)).
- Only one filter is used, and it is not selected per page, so page-level rules are decided inside the component, for example with `useLocation()` (same section).
- Visibility of menu entries is modeled with `hiddenBy` on the actor accesses, so the backend decides what each role sees ([access flags](../../agent-docs/frontend/hooks/navigation-and-access.md)).
- A client-side filter is a UX layer only. Real authorization stays in the backend.

### Practice notes: the landing redirect

This layer is practice, not a platform feature:

- **Derive, do not map.** Read the generated menu tree with the generated `useMenus()` hook and compute the target from it. A hard-coded role-to-URL table drifts out of sync with the model.
- **Visible leaves.** Walk the tree depth first and keep the leaf items the principal may see. An item or group is hidden when its `hiddenBy` flag is true on the principal, and a hidden group removes its whole subtree, exactly as the sidebar does. The check repeats the generated navigation predicate, so keep the two in step. If a menu customizer hook is ever registered for the sidebar, apply it here too (*verify* against the generated navigation code).
- **Pure target function.** Put the decision in an exported function `landingTarget(menus, principal)`. It returns `'stay'` when a visible leaf has the empty url (the home page itself), otherwise the first visible url, otherwise `null`. Return `null` rather than guess, so the failure is to stay put.
- **Never return the home url.** A returned url is never empty, so the redirect cannot loop.
- **Act on the home route only.** Compute the target only when the pathname is `/`. This covers every arrival at the home route, including the breadcrumb link and a back button, not just the sign-in landing.
- **Render nothing while redirecting.** Navigate with `replace: true` in an effect and return `null` instead of `children`, so the home page never mounts for a role that cannot load it. Otherwise render `children` unchanged.

```tsx
// Example code: useMenus and the principal type are generated for the application
export const LandingRedirect: FC<AccessFilterComponentProps> = ({ principal, children }) => {
  const menus = useMenus();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const target = pathname === '/' ? landingTarget(menus, principal) : null;
  const redirecting = target !== null && target !== 'stay';

  useEffect(() => {
    if (redirecting) navigate(`/${target}`, { replace: true });
  }, [navigate, redirecting, target]);

  return redirecting ? null : <>{children}</>;
};
```

## Rationale

- The menu tree already encodes which roles see what, so the redirect cannot disagree with the sidebar.
- The principal is always resolved inside the layout, so there is no window in which an unresolved principal passes through.
- A pure function is unit-testable against the real generated menu, so a model change to a `hiddenBy` gate shows up as a failing test.

## Example

In one app, several provider-side roles see a task dashboard on the home route and stay there. Several operator-side roles are sent to their own page and an external role to a separate panel, all by their first visible menu entry. A unit test renders the component for an external, an operator and a reviewer principal and for a principal that sees nothing, using the real menu tree.

## When to avoid

- Every role may open the home page: no redirect is needed.
- The target depends on something the menu does not show (a last-visited page, a data condition): use [[operation-flow-redirect-pattern]] or a navigation hook instead.
- The redirect would only work around a page that fails for some roles: model the home access so that it is hidden for them.

## Related

- [[operation-flow-redirect-pattern]] — backend-driven redirect after an operation, not after sign-in
- [[post-operation-navigation-hook]] — per-operation navigation handlers
- [[access-paired-with-menu-item]] — the modeled menu entries and `hiddenBy` gates the redirect reads
