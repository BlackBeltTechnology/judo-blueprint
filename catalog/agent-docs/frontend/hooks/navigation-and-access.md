---
title: Frontend Navigation and Access Hooks
description: Redirect service, access filter, hotkeys, navigation interceptor and navigation helpers of the generated React frontend.
aliases: [redirect deep link, access denied screen, keyboard shortcuts, navigation interceptor, sticky query parameters, route helpers, hide menu item, unsaved changes warning]
keywords: [REDIRECT_HOOK_INTERFACE_KEY, RedirectServiceHook, ACCESS_FILTER_COMPONENT_INTERFACE_KEY, AccessFilterComponentProps, NAVIGATION_INTERCEPTOR_INTERFACE_KEY, NavigationInterceptorHook, decorateNavigation, useJudoNavigation, useNavigationConfirmation, registerGlobalHotkeys, hiddenBy, enabledBy]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Navigation and Access Control Hooks

## Overview

Navigation and access control hooks manage routing, redirects, and page-level permissions. These hooks allow you to customize redirect behavior, filter access to pages, add keyboard shortcuts, and intercept navigation.

## Actor Accesses as Menu Items

**Important**: The sidebar menu structure is driven by **Actor accesses** defined in the ESM model. Each access on an Actor becomes a menu item. This is the primary navigation mechanism.

### How Menu Items are Generated

```
ESM Actor Definition:
  └── accesses (list)
        ├── access "Administration" → Menu item "Administration"
        ├── access "Reports" → Menu item "Reports"
        └── access "Settings" → Menu item "Settings"
```

The generated menu is in:
```
src/layout/Drawer/DrawerContent/Navigation/ (menu items are built from the application navigation controller)
```

### Access Control via Boolean Attributes

Each access, relation, and attribute can have visibility/enablement controlled by three boolean attributes:

| Attribute | Purpose | UI Effect |
|-----------|---------|-----------|
| `hiddenBy` | Visibility control | Element not rendered when `true` |
| `enabledBy` | Interactivity control | Element disabled when `false` |
| `requiredBy` | Validation control | Field required when `true` |

### Backend Interceptor Control

Interceptors can dynamically set boolean values on transfer objects to control frontend visibility:

```java
@Override
public AdministrationInfo preRead(AdministrationInfo input) {
    // Control what the user can see/access
    input.setCanManageUsers(userHasRole("ADMIN"));
    input.setCanViewReports(userHasPermission("reports:view"));
    return input;
}
```

The frontend then uses these values via `hiddenBy`/`enabledBy` expressions:

```xml
<!-- ESM: Relation hidden when canManageUsers is false -->
<relations name="users" target="_UserInfo"
  hiddenBy="not self.canManageUsers"/>
```

### Scope of Access Control

Access control applies to:

1. **Menu Items (Actor Accesses)**: Top-level navigation entries
2. **Relations**: Tabs, tables, and links between transfer objects
3. **Attributes**: Individual form fields/widgets

```xml
<!-- Menu access controlled -->
<accesses name="Administration" hiddenBy="not self.isAdmin"/>

<!-- Relation tab controlled -->
<relations name="sensitiveData" hiddenBy="not self.hasSecurityClearance"/>

<!-- Field widget controlled -->
<attributes name="salary" hiddenBy="not self.canViewSalary" enabledBy="self.canEditSalary"/>
```

### Profile and Bottom Menu Entries

The generated profile and bottom-menu entries are inconsistent:

- The Profile item is generated whenever `application.authentication` is set, but it is wired only to `openProfilePage`, which is passed only when `application.profilePage` is also set. Configure a profile page.
- The logout button exists only inside the `application.profilePage` block of the drawer profile. Applications with authentication but no profile page get no logout button there.
- `doLogout` is defined in the mobile profile popover but never rendered, so the popover offers no logout.
- When the profile page is not opened in a dialog, the drawer profile action calls `routeTo<Page>()`, but only `calculateNavigationRoute` is imported from `~/routes`.
- The "Other" popover opens with items from index 3 (`handleOtherPopupOpen`), but `itemOther()` starts at index 4, so the two splits disagree.

Workaround: configure a profile page and customise the bottom menu or drawer where needed.

## RedirectServiceHook

### Purpose

The generated `Redirect` page (`src/pages/Redirect.tsx`) calls a registered redirect service with the URL search parameters. Use it for deep links that must resolve at runtime (for example redirect to an entity found by an external id).

Real shape (from `~/pages/Redirect`): `REDIRECT_HOOK_INTERFACE_KEY = 'RedirectServiceHook'` and `type RedirectServiceHook = () => (searchParams: URLSearchParams) => Promise<void>`. The hook factory is called as a React hook, the returned function receives the search parameters and navigates itself. If it throws, the page shows the translated error `judo.pages.redirect.error`.

### Basic Implementation

```typescript
// src/custom/hooks/redirectService.tsx
import { useJudoNavigation } from '~/components';
import type { RedirectServiceHook } from '~/pages/Redirect';

export const redirectServiceHook: RedirectServiceHook = () => {
  const { navigate } = useJudoNavigation();

  return async (searchParams) => {
    const id = searchParams.get('id');
    if (!id) {
      throw new Error('Missing id');
    }
    navigate(`/some/route/${id}`);
  };
};
```

### Registration

```typescript
// src/custom/application-customizer.tsx
import { REDIRECT_HOOK_INTERFACE_KEY, type RedirectServiceHook } from '~/pages/Redirect';
import { redirectServiceHook } from './hooks/redirectService';

context.registerService<RedirectServiceHook>(REDIRECT_HOOK_INTERFACE_KEY, redirectServiceHook);
```

### Advanced Examples

#### Resolving a Target with a Generated Service

```typescript
export const redirectServiceHook: RedirectServiceHook = () => {
  const { navigate } = useJudoNavigation();

  return async (searchParams) => {
    const externalId = searchParams.get('externalId');
    // Use a generated service (new XServiceImpl(judoAxiosProvider)) or a modeled
    // operation to resolve the target; do not use raw fetch().
    const target = await resolveTarget(externalId);
    navigate(`/orders/${target.__identifier}`);
  };
};
```

#### Authentication-Aware Redirect

Unauthenticated users are sent to the identity provider by the auth gate before the redirect page renders, so the hook does not need its own login redirect. Read the principal with `usePrincipal()` from `~/auth/principal-context` when the target depends on the user.

## Access Filtering

### Purpose

Wrap the whole authenticated layout with a component that can block or replace the UI, for example to show an "access denied" screen when the principal lacks a modeled flag. Only one filter is used (the best matching service); it is not selected per page.

Real shape (from `~/auth`): `ACCESS_FILTER_COMPONENT_INTERFACE_KEY = 'AccessFilterComponent'` and `AccessFilterComponentProps { principal: <Actor>Stored; children?: ReactNode }`. It exists only when the application has authentication. The layout renders `<AuthProxyComponent filter="(objectClass=AccessFilterComponent)" principal={principal}>`; without a registered service the children render unchanged.

### Basic Implementation

```typescript
// src/custom/components/AccessFilter.tsx
import type { FC } from 'react';
import { Alert, Container } from '@mui/material';
import type { AccessFilterComponentProps } from '~/auth';

export const AdminAccessFilter: FC<AccessFilterComponentProps> = ({ principal, children }) => {
  // isAdmin is an attribute modeled on the principal transfer object
  if (!principal?.isAdmin) {
    return (
      <Container>
        <Alert severity="error">Access Denied: Administrator privileges required</Alert>
      </Container>
    );
  }

  return <>{children}</>;
};
```

### Registration

```typescript
// src/custom/application-customizer.tsx
import type { FC } from 'react';
import { ACCESS_FILTER_COMPONENT_INTERFACE_KEY, type AccessFilterComponentProps } from '~/auth';
import { AdminAccessFilter } from './components/AccessFilter';

context.registerService<FC<AccessFilterComponentProps>>(
  ACCESS_FILTER_COMPONENT_INTERFACE_KEY,
  AdminAccessFilter,
);
```

### Advanced Examples

#### Per-Page and Per-Role Rules

The filter has no `component` filter property and no extra props, so page-level rules must be decided inside the component (for example with `useLocation()`), or, better, modeled: use `hiddenBy`/`enabledBy` on the actor accesses, relations and attributes (see the top of this document) so the backend decides.

```typescript
import { useLocation } from 'react-router-dom';

export const RouteAccessFilter: FC<AccessFilterComponentProps> = ({ principal, children }) => {
  const { pathname } = useLocation();
  const blocked = pathname.startsWith('/admin') && !principal?.isAdmin;
  return blocked ? <Alert severity="error">Access denied</Alert> : <>{children}</>;
};
```

#### Time-Based Access

```typescript
export const BusinessHoursFilter: FC<AccessFilterComponentProps> = ({ children }) => {
  const hour = new Date().getHours();
  if (hour < 9 || hour >= 17) {
    return <Alert severity="warning">The application is available 9 AM - 5 PM.</Alert>;
  }
  return <>{children}</>;
};
```

A client-side filter is only a UX layer. Enforce real authorization in the backend (interceptors and model access rules).

## Hotkey Support

### Purpose

Add keyboard shortcuts for quick navigation and actions.

### Basic Implementation

```typescript
// src/custom/hooks/hotkeySupport.tsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const useHotkeys = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      // Ctrl+N: New activity
      if (event.ctrlKey && event.key === 'n') {
        event.preventDefault();
        navigate('/activities/create');
      }

      // Ctrl+Shift+S: Search
      if (event.ctrlKey && event.shiftKey && event.key === 's') {
        event.preventDefault();
        openSearchDialog();
      }

      // Ctrl+H: Home
      if (event.ctrlKey && event.key === 'h') {
        event.preventDefault();
        navigate('/');
      }
    };

    window.addEventListener('keydown', handleKeyPress);

    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [navigate]);
};
```

### Registration

Global hotkeys are generated in `src/hotkeys.tsx` (`registerGlobalHotkeys`, built on `react-hotkeys-hook`). There is no `hotkeys` entry in the application customizer. To add global hotkeys, override the two fragments (see [Template Override Process](../README.md#template-override-process)):

- `actor/src/hotkeys.tsx.imports.fragment.hbs` for imports
- `actor/src/hotkeys.tsx.body.fragment.hbs` for the `useHotkeys(...)` calls

The generated function already provides `t` and the dialog helpers `[createDialog, closeDialog] = useDialog()`:

```typescript
// body fragment
useHotkeys('ctrl+shift+e', () => {
  // open your dialog or navigate
}, { preventDefault: true });
```

The `window.addEventListener('keydown', ...)` hooks below work for component-local shortcuts and need no override.

### Advanced Examples

#### Context-Aware Hotkeys

```typescript
export const useContextualHotkeys = (context: string) => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (context === 'entity-list') {
        // N: New entity (when on entity list)
        if (event.key === 'n' && !event.ctrlKey) {
          event.preventDefault();
          navigate('/entities/create');
        }

        // E: Export (when on entity list)
        if (event.key === 'e' && !event.ctrlKey) {
          event.preventDefault();
          exportEntities();
        }
      }

      if (context === 'entity-view') {
        // E: Edit entity (when viewing entity)
        if (event.key === 'e' && !event.ctrlKey) {
          event.preventDefault();
          navigate('edit');
        }

        // D: Delete entity
        if (event.key === 'd' && !event.ctrlKey) {
          event.preventDefault();
          deleteEntity();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [context, navigate]);
};

// Usage in component
export const EntityList: FC = () => {
  useContextualHotkeys('entity-list');
  return <div>...</div>;
};
```

#### Hotkey Help Dialog

```typescript
import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText,
  Chip
} from '@mui/material';

export const HotkeyHelp: FC = () => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      // ?: Show hotkey help
      if (event.key === '?' && !event.ctrlKey) {
        event.preventDefault();
        setOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  const hotkeys = [
    { key: 'Ctrl+N', description: 'Create new entity' },
    { key: 'Ctrl+Shift+S', description: 'Search' },
    { key: 'Ctrl+H', description: 'Go to home' },
    { key: '?', description: 'Show this help' },
  ];

  return (
    <Dialog open={open} onClose={() => setOpen(false)}>
      <DialogTitle>Keyboard Shortcuts</DialogTitle>
      <DialogContent>
        <List>
          {hotkeys.map(({ key, description }) => (
            <ListItem key={key}>
              <Chip label={key} size="small" sx={{ mr: 2 \}} />
              <ListItemText primary={description} />
            </ListItem>
          ))}
        </List>
      </DialogContent>
    </Dialog>
  );
};
```

## Navigation Interception

### Purpose

Intercept navigation to add custom behavior, such as sticky parameters or confirmation dialogs.

### Basic Implementation

Real shape (from `~/components`): `NAVIGATION_INTERCEPTOR_INTERFACE_KEY = 'JudoNavigationInterceptor'`; `NavigationInterceptorHook = ({ stringifyPath }) => NavigationInterceptor` with `NavigationInterceptor { decorateNavigation(to): string | Partial<Path>; onBeforeInitialLoad?(): void }`. There is no `beforeNavigate`; the interceptor can only rewrite the target (for example add sticky query parameters).

```typescript
// src/custom/hooks/navigationInterceptor.tsx
import {
  NAVIGATION_INTERCEPTOR_INTERFACE_KEY,
  type NavigationInterceptorHook,
} from '~/components';

export const navigationHook: NavigationInterceptorHook = ({ stringifyPath }) => ({
  decorateNavigation: (to) => {
    const currentActivity = localStorage.getItem('selectedActivity');

    if (currentActivity && typeof to === 'string') {
      return `${to}?activity=${currentActivity}`;
    }

    return to;
  },

  onBeforeInitialLoad: () => {
    const activity = new URLSearchParams(window.location.search).get('activity');
    if (activity) {
      localStorage.setItem('selectedActivity', activity);
    }
  },
});

// registration
// context.registerService<NavigationInterceptorHook>(NAVIGATION_INTERCEPTOR_INTERFACE_KEY, navigationHook);
```

### Advanced Examples

#### Unsaved Changes Warning

Interceptors cannot cancel navigation. For unsaved-changes confirmation use the generated `useNavigationConfirmation` hook (`~/hooks`, see [Extension Points](../extension-points.md)), which generated forms already use.

#### Session Handling

Session expiry is handled by the generated auth layer: a 401 response clears the security storage and reloads the page, which redirects to the identity provider. Do not implement custom session checks in the interceptor.

## Type-Safe Navigation

### Purpose

Use generated navigation helpers for type-safe routing.

### Basic Usage

`useJudoNavigation()` is exported from `~/components`. It returns `{ navigate, clearNavigate, externalNavigate, navigateBackTo, back, isBackDisabled, setTitle }`. `navigate(to)` takes a react-router `To` (a path string or `{ pathname, search }`) and applies the registered navigation interceptor; the generated route helpers from `~/routes` (for example `routeToServiceEntityView(...)`) build the paths.

`useJudoNavigation()` keeps a breadcrumb stack, not the browser history. `navigate(to)` pushes the current page onto the stack, `back()` pops it, `navigateBackTo(item)` truncates the stack to an item, `clearNavigate(to)` empties the stack and goes to `to`, and `externalNavigate(url)` sets `window.location`. `isBackDisabled` is true when the stack is empty, and `setTitle(title)` sets the label of the current page (a missing title logs a warning). With an empty stack, `back()` goes to the dashboard.

```typescript
import { useJudoNavigation } from '~/components';

export const QuickActions: FC = () => {
  const { navigate, back } = useJudoNavigation();

  return (
    <Box>
      <Button onClick={() => navigate('/service/activities/create')}>New Activity</Button>
      <Button onClick={back}>Back</Button>
    </Box>
  );
};
```

### Advanced Examples

#### Query Parameters

```typescript
const { navigate } = useJudoNavigation();

navigate({ pathname: '/service/items', search: `?entityId=${entity.__identifier}` });
```

#### External Navigation

```typescript
const { externalNavigate } = useJudoNavigation();
externalNavigate('https://example.com/docs');
```

## Best Practices

### 1. Clean Up Event Listeners

```typescript
// ✅ Good
useEffect(() => {
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, []);

// ❌ Bad
useEffect(() => {
  window.addEventListener('keydown', handleKeyPress);
}, []); // No cleanup
```

### 2. Prevent Default Browser Behavior

```typescript
// ✅ Good
if (event.ctrlKey && event.key === 'n') {
  event.preventDefault(); // Prevent browser's "new window"
  navigate('/activities/create');
}

// ❌ Bad
if (event.ctrlKey && event.key === 'n') {
  navigate('/activities/create'); // Browser still opens new window
}
```

### 3. Check Authentication State

```typescript
// ✅ Good
if (!principal) {
  return <Alert>Please log in</Alert>;
}

// ❌ Bad
// Assume user is always logged in
```

### 4. Keep Custom Components Under src/custom

```bash
# Nothing to do: your hook file is not generated (only its .default twin is), no .generator-ignore entry is needed
```

## Complete Example

```typescript
// src/custom/application-customizer.tsx
import type { FC } from 'react';
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { ACCESS_FILTER_COMPONENT_INTERFACE_KEY, type AccessFilterComponentProps } from '~/auth';
import { REDIRECT_HOOK_INTERFACE_KEY, type RedirectServiceHook } from '~/pages/Redirect';
import { NAVIGATION_INTERCEPTOR_INTERFACE_KEY, type NavigationInterceptorHook } from '~/components';
import { redirectServiceHook } from './hooks/redirectService';
import { navigationHook } from './hooks/navigationInterceptor';
import { AdminAccessFilter } from './components/AccessFilter';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    context.registerService<RedirectServiceHook>(REDIRECT_HOOK_INTERFACE_KEY, redirectServiceHook);
    context.registerService<NavigationInterceptorHook>(NAVIGATION_INTERCEPTOR_INTERFACE_KEY, navigationHook);
    context.registerService<FC<AccessFilterComponentProps>>(ACCESS_FILTER_COMPONENT_INTERFACE_KEY, AdminAccessFilter);
  }
}
```

## Troubleshooting

### "Hotkeys not working"

#### Check event listener
```typescript
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    console.log('Key pressed:', e.key, 'Ctrl:', e.ctrlKey);
  };
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, []);
```

### "Access filter not showing"

#### Verify registration
```typescript
context.registerService<FC<AccessFilterComponentProps>>(
  ACCESS_FILTER_COMPONENT_INTERFACE_KEY,
  AdminAccessFilter,
);
// Only the best-ranked registration is used; check that no second filter is registered
```

### "Navigation not redirecting"

#### Check navigate call
```typescript
const navigate = useNavigate();
console.log('Navigating to:', path);
navigate(path);
```

## Related Documentation

- [Hook System Overview](./README.md)
- [Data Hooks](./data-hooks.md)
- [Action Hooks](./action-hooks.md)
- [Development Workflow](../development-workflow.md)
