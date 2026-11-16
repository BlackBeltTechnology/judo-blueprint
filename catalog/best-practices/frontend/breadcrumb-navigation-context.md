---
id: breadcrumb-navigation-context
title: Breadcrumb Navigation Context Provider
description: Navigation goes through one context hook that keeps a breadcrumb stack, giving forward, back and reset semantics independent of browser history, plus a visual breadcrumb trail.
aliases: [BreadcrumbProvider, useJudoNavigation breadcrumb]
keywords: [breadcrumb, navigation, useJudoNavigation, back, clearNavigate, history, provider, title]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: navigation
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: [dialog-based-navigation]
related: [dialog-based-navigation, complete-frontend-replacement]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Deep entity hierarchies (for example customer, order, line item) make the browser back button an unreliable way to go up one level. A navigation hook that records a breadcrumb stack gives consistent back behavior and a visible trail.

## Practice

### Platform base

- The generated React frontend exports `useJudoNavigation()` from `~/components`. It returns `{ navigate, clearNavigate, externalNavigate, navigateBackTo, back, isBackDisabled, setTitle }`; `navigate` takes a path string or `{ pathname, search }` and applies the registered navigation interceptor ([type-safe navigation](../../agent-docs/frontend/hooks/navigation-and-access.md)).
- A navigation interceptor (`NAVIGATION_INTERCEPTOR_INTERFACE_KEY`) can only rewrite the target of a navigation, for example to add sticky query parameters. It has no before-navigate veto, so it cannot implement a breadcrumb stack ([navigation interceptor](../../agent-docs/frontend/hooks/navigation-and-access.md)).
- Custom routes are added in `src/extra-routes.tsx` ([extra routes](../../agent-docs/frontend/extension-points.md)). Generated forms with unsaved changes use the generated `useNavigationConfirmation` hook; custom navigation that leaves an edited form should reuse it.

### Practice notes: a breadcrumb provider behind the same hook API

This layer is practice, not a platform feature. A custom replacement frontend implements the provider; with the generated frontend, check what `useJudoNavigation` already provides before writing another one:

- A provider wraps the routes and holds a stack of visited locations with their titles.
- `navigate` pushes the current location and title, then goes forward; `back` pops and returns; `clearNavigate` empties the stack and goes to a root route, used by sidebar entries; `isBackDisabled` is true when the stack is empty.
- A breadcrumb component in the header renders the trail, limited to the last few items.
- Pages set their title through `setTitle`.

```tsx
// Example code
<BreadcrumbProvider>
  <Outlet />
</BreadcrumbProvider>

const { navigate, back, clearNavigate, isBackDisabled, setTitle } = useJudoNavigation();
navigate(`/orders/${row.__signedIdentifier}`); // push breadcrumb, go forward
back();                                        // pop breadcrumb, go back
clearNavigate('/orders');                       // reset the stack
```

## Rationale

Back navigation stays consistent through deep chains, the trail is visible, and each page owns its title. The cost: the stack runs parallel to browser history and can drift from it, it is lost on page refresh, and sidebar navigation must reset it.

## Example

One app keeps the provider and the trail component in one components file. `navigate` stores the current location and title, `back` pops and navigates to the previous entry, the header shows at most two crumbs, and its back button is disabled when no history exists.

## When to avoid

- Navigation is shallow, or the browser history is enough.
- The application navigates through dialogs only; see [[dialog-based-navigation]].
- The generated navigation hook already gives the behavior you need.

## Related

- [[dialog-based-navigation]] — navigation by state machine instead of a stack
- [[complete-frontend-replacement]] — the replacement frontend that carries this provider
