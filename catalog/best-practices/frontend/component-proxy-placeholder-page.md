---
id: "component-proxy-placeholder-page"
title: "ComponentProxy Placeholder Page for Custom Dashboard Entry Points"
domain: "frontend"
category: "page"
score: 72.0
usage_count: 1
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - compsychletter
---
## Description

Dashboard transfer objects without an explicit `<view>` UI layout in the ESM model do not get generated page components. When a `MenuItemAccess` entry is wired to such a dashboard, the corresponding route needs a page component. The canonical placeholder uses `ComponentProxy` from `@pandino/react-hooks`: it renders a custom implementation if one is registered in the Pandino service registry, or falls back to a minimal heading. This decouples routing from implementation — the route works immediately, and the real dashboard UI is delivered later via a Pandino bundle without touching the generated file.

## Structure

- One `default export function XxxPage()` per dashboard, rendering a `ComponentProxy`
- `filter` attribute targets `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` + a component-specific string key
- Fallback child is a minimal `<h1>Label</h1>` (visible until Pandino override is registered)
- Exports a unique `XXX_PAGE_INTERFACE_KEY` string constant — downstream bundles import this to register their implementation
- Lives in `src/pages/LetterUser/<XxxDashboard>Page/index.tsx`
- Registered in `routes.tsx` as a lazy-loaded route at the access path (e.g. `/documents`, `/authoring`, `/data`)

## Code Shape

```tsx
// src/pages/LetterUser/DocumentsDashboardPage/index.tsx
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

Route registration in `routes.tsx` (generator-ignored — edit manually):

```tsx
const DocumentsDashboardPage = lazy(() => import('./pages/LetterUser/DocumentsDashboardPage'));

// ...

routes.push({ path: 'documents', exact: true, element: <Suspense><DocumentsDashboardPage /></Suspense> });
```

Menu entry in `menu-items.tsx` (also generator-ignored — edit manually):

```tsx
{
  id: 'documentsMenu',
  type: 'item',
  title: 'Documents',
  url: '/documents',        // or use exported routeToDocumentsDashboard()
  icon: 'mdi:file-document-multiple-outline',
}
```

## Examples

### CompSychLetter
Three placeholder pages created for `DocumentsDashboard`, `AuthoringDashboard`, `DataDashboard` after adding `MenuItemAccess` entries to `LetterUser`. Each exports a unique `*_PAGE_INTERFACE_KEY` constant. All three immediately navigable in the browser; real dashboard content delivered via separate Pandino bundles in follow-on changes.

## Trade-offs

- Pros: Route works before the full implementation exists; Pandino override mechanism decouples routing from content; consistent with the generated `DashboardPage` pattern
- Cons: Requires manual edits to `routes.tsx` and `menu-items.tsx` (both generator-ignored); fallback heading is minimal — add a loading spinner or skeleton if needed
- Prefer when: Dashboard TO has no `<view>` model layout, navigation needs to be available immediately, dashboard implementation will arrive via a separate change or Pandino bundle

## Related Patterns

- [access-paired-with-menu-item](../model/access-paired-with-menu-item.md) — menu item wiring that triggers need for this pattern
- [panel-dashboard-transfer](../model/panel-dashboard-transfer.md) — the dashboard TO this page component represents
- [application-customizer-hub](application-customizer-hub.md) — Pandino registration point
