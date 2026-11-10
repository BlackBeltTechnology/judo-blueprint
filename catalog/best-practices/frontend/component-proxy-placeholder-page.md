---
id: component-proxy-placeholder-page
title: ComponentProxy Placeholder Page for Custom Dashboard Entry Points
description: "A dashboard page component that renders a ComponentProxy with a minimal fallback heading, so a menu route works at once and the real dashboard UI is delivered later as a Pandino service."
aliases: [dashboard placeholder page, custom dashboard route]
keywords: [ComponentProxy, Pandino, dashboard, placeholder, routes.tsx, menu-items.tsx, MenuItemAccess, custom visual element]
tags: ["domain:frontend", "layer:frontend", "project:compsych-letter-demo", "status:single-project"]
category: page
status: single-project
projects: [compsych-letter-demo]
evidence: ["compsychletter:unrecorded"]
alternatives: [custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-05-13
last_updated: 2026-11-10
---
## Intent

A `MenuItemAccess` points at a dashboard transfer object, but the UI model gives that dashboard no layout (no view), so the generator produces no page component for it. The route still needs something to render. A small page component built on `ComponentProxy` fills the gap: it shows a minimal heading until a custom implementation is registered in the Pandino service registry, and it renders that implementation afterwards. Routing is decoupled from the dashboard content, which can arrive in a later change.

## Practice

### Platform base

- Custom UI is added as a Pandino service. A custom implementation of a model element is registered under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (from `~/custom`) with the service property `component` set to a per-element key, and the register function is called from `application-customizer.tsx` ([custom component replacement](../../agent-docs/frontend/advanced-patterns.md), [application customizer hub](../../agent-docs/frontend/hooks/AGENTS.md)).
- Files under `src/custom/` are never regenerated ([action hooks, keep custom hooks under src/custom](../../agent-docs/frontend/hooks/action-hooks.md)).
- Whether the generator really emits no page for a dashboard without a layout, and the exact `ComponentProxy` props, are *verify* items: check the generated sources of your version.

### Project practice: placeholder page per dashboard (compsychletter)

The agent-docs do not describe this page shape; it is project practice.

- One `default export function <Dashboard>Page()` per dashboard, rendering a `ComponentProxy`.
- The `filter` matches `OBJECTCLASS` = `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` and a `component` value equal to the page's own exported string constant (`<DASHBOARD>_PAGE_INTERFACE_KEY`). A later bundle imports that constant to register its implementation.
- The child of the proxy is the fallback: a plain heading with the dashboard label.
- The route is added to `routes.tsx` as a lazy-loaded route at the access path, and the menu entry to `menu-items.tsx`. In the project both files are listed in `.generator-ignore`, so they are edited by hand.

```tsx
// Example project code: src/pages/<Actor>/DocumentsDashboardPage/index.tsx
import { OBJECTCLASS } from '@pandino/pandino-api';
import { ComponentProxy } from '@pandino/react-hooks';
import { CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY } from '~/custom';

export const DOCUMENTS_DASHBOARD_PAGE_INTERFACE_KEY = 'DocumentsDashboardPage';

export default function DocumentsDashboardPage() {
  return (
    <ComponentProxy
      filter={`(&(${OBJECTCLASS}=${CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY})(component=${DOCUMENTS_DASHBOARD_PAGE_INTERFACE_KEY}))`}
    >
      <h1>Documents</h1>
    </ComponentProxy>
  );
}
```

```tsx
// routes.tsx (hand-edited)
const DocumentsDashboardPage = lazy(() => import('./pages/<Actor>/DocumentsDashboardPage'));
routes.push({ path: 'documents', exact: true, element: <Suspense><DocumentsDashboardPage /></Suspense> });

// menu-items.tsx (hand-edited)
{ id: 'documentsMenu', type: 'item', title: 'Documents', url: '/documents', icon: 'mdi:file-document-multiple-outline' }
```

## Rationale

- The route works before the dashboard UI exists, so navigation can ship first.
- The override mechanism is the normal Pandino one, so the real UI needs no edit of the placeholder.
- Cost: `routes.tsx` and `menu-items.tsx` are edited by hand, and the fallback heading is minimal (add a spinner or skeleton if needed).

## Example

In compsychletter, three placeholder pages were created for `DocumentsDashboard`, `AuthoringDashboard` and `DataDashboard` after `MenuItemAccess` entries were added to the `LetterUser` actor. Each exports its own `*_PAGE_INTERFACE_KEY`. All three were navigable at once; the real dashboards came later as separate Pandino bundles.

## When to avoid

- When the dashboard has a layout in the UI model: the generated page already exists.
- When the real component exists already: register it directly ([[custom-visual-element-override]]).

## Related

- [[access-paired-with-menu-item]] — the menu wiring that creates the need for a page
- [[panel-dashboard-transfer]] — the dashboard transfer object this page stands for
- [[application-customizer-hub]] — where the Pandino registration lives
- [[custom-visual-element-override]] — replacing a model element with a custom component
