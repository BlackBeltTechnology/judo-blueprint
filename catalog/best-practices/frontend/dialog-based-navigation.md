---
id: dialog-based-navigation
title: Dialog-Based Navigation with State Machine
description: Drive a single-screen custom frontend by a page-state variable and dialog-open flags instead of URL routes, for games, wizards and kiosks.
aliases: [state machine navigation, routeless navigation, page state navigation]
keywords: [navigation, state machine, dialog, page state, routing, kiosk, wizard, extra routes]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: navigation
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [complete-frontend-replacement, localstorage-session-persistence]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Some UIs (games, wizards, kiosks) are one continuous experience where URLs add nothing. A page-state variable plus dialog flags replaces routing for such a hand-written frontend.

## Practice

### Platform base

- The generated frontend is route-based: each actor access becomes a navigation entry and a page, and create and edit forms open as dialogs over those pages ([navigation controller and actor accesses](../../agent-docs/frontend/model-screen-layout.md)). Routing is part of that generation.
- Supported ways to add screens inside the generated app are extra React Router routes (`src/extra-routes.tsx`, prepended to the generated routes), the menu actions hook and custom visual elements ([extension points](../../agent-docs/frontend/extension-points.md), [custom component replacement](../../agent-docs/frontend/advanced-patterns.md)). Generated forms use the unsaved-changes confirmation hook `useNavigationConfirmation`; reuse it in custom editing components.
- The state-machine navigation below is not a platform feature. It only applies where the generated routing and pages are not used at all (a replaced frontend, see [[complete-frontend-replacement]]).

### Practice notes: page state plus dialog flags

```typescript
type PageType = 'list' | 'detail' | 'result' | 'none';

const [activePage, setActivePage] = useState<PageType>('list');
const [isRegistrationOpen, setRegistrationOpen] = useState(false);

return (
  <>
    {activePage === 'list' && <ItemList />}
    {activePage === 'detail' && <ItemDetail />}
    <RegistrationDialog open={isRegistrationOpen} />
    <BottomNavigation /> {/* fixed navigation for page switching */}
  </>
);
```

- One union type names every page; one boolean per dialog. Keep transitions in a small number of handlers so the flow stays readable.
- Persist the state the user would otherwise lose on reload, for example in local storage ([[localstorage-session-persistence]]).
- Accept the loss of deep links, browser back and URL sharing; if any of these matter, use routes (generated or extra routes) instead.

## Rationale

State transitions are explicit and dialogs give a natural modal flow without URL management. The cost: no deep linking, a non-functional back button, no sharing of states by URL and harder testing of a given state.

## Example

A game frontend: a five-value page state and five dialog flags drive the flow through a list, registration, activation, a detail view, a round, results and a ranking board, with a bottom navigation bar offering the list and a reset action.

## When to avoid

- The application uses the generated pages and menu: extend with extra routes or hooks instead.
- Users need bookmarks, back-button navigation or links from outside (e-mail, push notifications).

## Related

- [[complete-frontend-replacement]] — the setting where this navigation applies
- [[localstorage-session-persistence]] — keeping state across reloads
