---
title: Frontend UI Hooks
description: AppBar extra component, hero and logo props, footer text and menu customization hooks.
aliases: [customize appbar, change logo, footer text, add menu items, hero section customization, custom navigation menu, frontend hooks]
keywords: [CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY, AppBarExtraComponentsHook, CustomHeroPropsHook, CustomLogoPropsHook, FooterTextHook, MenuItemsCustomizerHook, NavItemType, MENU_ACTIONS_HOOK_INTERFACE_KEY, registerMenuActionsHook, spaceRequired]
tags: [domain:frontend, layer:frontend, status:platform]
---

# UI Hooks

## Overview

UI hooks allow you to customize the visual appearance and layout of the application. These hooks enable you to add custom components to the AppBar, customize the hero section, modify the logo, and change footer text.

### Field and View Display

There is no hook for the display of a single field or a whole view. The route is a model-level custom implementation: set `customImplementation` to `true` on the `DataField` (not on the `DataColumn`) and register a component for the generated element key, as described in [advanced-patterns.md → Component Replacement Hook](../advanced-patterns.md). The scaffold `src/custom/hooks/custom-implementations/register<Container>CustomImplementations.tsx.default` holds the register function and the key for each such element.

- The field stays in the mask, so the page still loads its value; the custom component receives it through its proxy props.
- To load a value but not show it, mark the `DataField` `customImplementation=true` and render nothing from the component.
- A `ui:Placeholder` marked `customImplementation` generates no scaffold and renders nothing; use a `DataField`.

## AppBar Extra Components

### Purpose

Add custom components to the application's AppBar (top navigation bar), such as notification bells, user menus, theme toggles, or quick action buttons.

### Basic Implementation

```typescript
// src/custom/components/NotificationBell.tsx
import { FC } from 'react';
import { IconButton, Badge } from '@mui/material';
import { Notifications as NotificationsIcon } from '@mui/icons-material';

export const NotificationBell: FC = () => {
  const notificationCount = 4; // Replace with actual logic

  const handleClick = () => {
    // Open notifications panel
    console.log('Open notifications');
  };

  return (
    <IconButton color="inherit" onClick={handleClick}>
      <Badge badgeContent={notificationCount} color="error">
        <NotificationsIcon />
      </Badge>
    </IconButton>
  );
};
```

### Registration

The AppBar accepts exactly one extra component, registered as a Pandino service under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` (value `'CustomVisualElement'`, exported from `~/custom`) with the service property `component: 'AppBarExtraComponents'`. The service is an `AppBarExtraComponentsHook` (from `~/layout/Header/HeaderContent`): a function returning `{ Component, spaceRequired? }`. `spaceRequired` (default 1) is the grid space the component claims in addition to the default header content.

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY } from '~/custom';
import type { AppBarExtraComponentsHook } from '~/layout/Header/HeaderContent';
import { NotificationBell } from './components/NotificationBell';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    context.registerService<AppBarExtraComponentsHook>(
      CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY,
      () => ({ Component: NotificationBell, spaceRequired: 1 }),
      { component: 'AppBarExtraComponents' },
    );
  }
}
```

### Placement

The extra component renders in two places, both from the same hook: in the drawer, below the logo and above the menu (children stack as a column, so a single button stretches over the full drawer width), and in the header grid, right-aligned before the settings and profile controls. Wrap several controls in one flex `Box` so they stay in a row at their natural width. The hook has no other slot, for example no separate top-right area for a language switch.

In the horizontal top bar the navigation takes `8 - spaceRequired` of the 12 grid columns and the right side takes `2 + spaceRequired`; `spaceRequired` defaults to 1. Set a larger `spaceRequired` when the extra component needs more width in the top bar.

### Stored layout configuration

The generated frontend keeps its layout configuration (for example drawer orientation and other `ConfigContext` state) in the browser `localStorage` under the key `<model>-config`. A stored config overrides a changed model or generated default, so users who already opened the app keep the old layout until that key is cleared (for example `localStorage.removeItem("<model>-config")`).

### Advanced Examples

#### User Profile Menu

```typescript
// src/custom/components/UserProfileMenu.tsx
import { FC, useState } from 'react';
import { IconButton, Menu, MenuItem, Avatar, Typography } from '@mui/material';
import { usePrincipal } from '~/auth/principal-context';

export const UserProfileMenu: FC = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const principal = usePrincipal();

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    // Implement logout logic
    handleClose();
  };

  return (
    <>
      <IconButton onClick={handleClick} color="inherit">
        <Avatar
          src={principal?.avatar}
          alt={principal?.name}
          sx={{ width: 32, height: 32 }}
        />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem disabled>
          <Typography variant="body2">
            {principal?.firstName} {principal?.lastName}
          </Typography>
        </MenuItem>
        <MenuItem onClick={() => { /* Navigate to profile */ }}>
          Profile
        </MenuItem>
        <MenuItem onClick={() => { /* Navigate to settings */ }}>
          Settings
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          Logout
        </MenuItem>
      </Menu>
    </>
  );
};
```

#### Theme Toggle

```typescript
// src/custom/components/ThemeToggle.tsx
import { FC, useState } from 'react';
import { IconButton } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';

export const ThemeToggle: FC = () => {
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
    // Implement theme switching logic
    // Update theme context or local storage
    localStorage.setItem('theme', darkMode ? 'light' : 'dark');
  };

  return (
    <IconButton onClick={toggleTheme} color="inherit">
      {darkMode ? <Brightness7 /> : <Brightness4 />}
    </IconButton>
  );
};
```

#### Quick Search

```typescript
// src/custom/components/QuickSearch.tsx
import { FC, useState } from 'react';
import {
  IconButton,
  Dialog,
  DialogContent,
  TextField,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';

export const QuickSearch: FC = () => {
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const searchResults = [
    // Replace with actual search logic
    { id: '1', title: 'Activity A', type: 'activity' },
    { id: '2', title: 'Event B', type: 'event' },
  ];

  return (
    <>
      <IconButton color="inherit" onClick={handleOpen}>
        <SearchIcon />
      </IconButton>
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            placeholder="Search activities, events..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <List>
            {searchResults.map(result => (
              <ListItem key={result.id} button>
                <ListItemText
                  primary={result.title}
                  secondary={result.type}
                />
              </ListItem>
            ))}
          </List>
        </DialogContent>
      </Dialog>
    </>
  );
};
```

#### Multiple AppBar Components

Only one `Component` can be registered, so compose several controls in one wrapper component and claim enough space:

```typescript
// src/custom/components/AppBarExtras.tsx
import { QuickSearch } from './QuickSearch';
import { NotificationBell } from './NotificationBell';
import { ThemeToggle } from './ThemeToggle';

export const AppBarExtras = () => (
  <>
    <QuickSearch />
    <NotificationBell />
    <ThemeToggle />
  </>
);

// registration: () => ({ Component: AppBarExtras, spaceRequired: 3 })
```

## Hero and Logo Customization

### Purpose

Customize the hero section (landing page banner) and application logo.

### Hero Customization

The hero (profile header) properties are customized with a `CustomHeroPropsHook` (`CUSTOM_HERO_PROPS_HOOK_INTERFACE_KEY` = `'CustomHeroPropsHook'`, defined in `~/hooks/useHeroProps`). It is a hook factory that returns a function mapping the defaults to new props. `UseHeroProps` has `imgSrc`, `actorName`, `preferredUsername?` and `email?`.

```typescript
context.registerService<CustomHeroPropsHook>(
  CUSTOM_HERO_PROPS_HOOK_INTERFACE_KEY,
  () => (defaults) => ({ ...defaults, imgSrc: '/images/custom-hero.png' }),
);
```

### Logo Customization

A `CustomLogoPropsHook` (`CUSTOM_LOGO_PROPS_HOOK_INTERFACE_KEY` = `'CustomLogoPropsHook'`, in `~/hooks/useLogoProps`) maps the default `UseLogoProps` (`subTitle`, `imgSrc`, `iconSrc`) to custom values. Image paths are relative to `public/`.

```typescript
context.registerService<CustomLogoPropsHook>(
  CUSTOM_LOGO_PROPS_HOOK_INTERFACE_KEY,
  () => (defaults) => ({ ...defaults, imgSrc: '/images/custom-logo.svg', subTitle: '[Your Application]' }),
);
```

The application logo and icon defaults come from the actor's `applicationLogo` in the model; prefer changing the model for a permanent change.

### Custom Hero Component

The hero has no component-level hook, only the props hook above. Replacing the hero component requires a template override (see [Template Override Process](../README.md#template-override-process)).

## Footer Text

### Purpose

Customize the footer text displayed at the bottom of the application.

### Basic Implementation

The footer text is provided by a `FooterTextHook` (`FOOTER_TEXT_HOOK_INTERFACE_KEY` = `'FooterTextHook'`, exported from `~/layout/Footer`): a hook factory returning a function that returns a plain string. The string is rendered as text, not HTML, so links are not possible this way. The default is the application title and the current year.

```typescript
import { FOOTER_TEXT_HOOK_INTERFACE_KEY, type FooterTextHook } from '~/layout/Footer';

context.registerService<FooterTextHook>(
  FOOTER_TEXT_HOOK_INTERFACE_KEY,
  () => () => `© ${new Date().getFullYear()} [Your Application Name]`,
);
```

A footer with links or other markup needs a template override of `actor/src/layout/Footer.tsx`.

## Menu Manipulation

### Purpose

Modify the generated navigation menu structure.

### Adding Menu Items

Menu item `id` values of generated entries are the model element ids with `@` removed (long strings), so ids such as `dashboard` or `entities` in the examples below are placeholders: match on `title` (the model `label`, when set) or on a suffix of the real id, and log `menuItems` once to see them. Valid `type` values are `'group'`, `'collapse'` and `'item'`. A top-level entry with children is a `group`; a nested entry with children is a `collapse`; a leaf is an `item`. The drawer renders top-level entries only as `group` or `item`, so a top-level custom entry typed `collapse` renders wrongly. Group and item titles are translated with `t('menuTree.<title>', { defaultValue: title })`. The generator emits `menuTree.<label>` keys only for model navigation labels, so a group title created in a hook has no key and shows its English title in other locales. Known issue; workaround: add `"menuTree.<Group title>": "<translation>"` to each locale's application translation file for every title that a hook creates.

```typescript
// src/custom/hooks/menuCustomizer.tsx
import type { MenuItemsCustomizerHook } from '~/layout/Drawer/DrawerContent/Navigation';
import type { NavItemType } from '~/layout/Drawer/DrawerContent/Navigation/NavItem';

export const customMenuHook: MenuItemsCustomizerHook = () => (menuItems) => {
  // Add custom menu item
  // NavItemType: { id, type: 'group' | 'collapse' | 'item', title?, url?, onClick?, icon?, disabled?, hiddenBy?, children? }
  const reportsItem: NavItemType = {
    id: 'reports',
    type: 'group',
    title: 'Reports',
    icon: 'chart-bar',
    children: [
      { id: 'entity-report', type: 'item', title: 'Entity Report', url: '/reports/entity' },
      { id: 'item-report', type: 'item', title: 'Item Report', url: '/reports/item' },
      { id: 'performance-report', type: 'item', title: 'Performance Report', url: '/reports/performance' },
    ]
  };

  // Insert after specific item
  const insertIndex = menuItems.findIndex(item => item.id === 'entities');

  return [
    ...menuItems.slice(0, insertIndex + 1),
    reportsItem,
    ...menuItems.slice(insertIndex + 1)
  ];
};
```

### Removing Menu Items

```typescript
export const customMenuHook: MenuItemsCustomizerHook = () => (menuItems) => {
  // Remove specific items
  return menuItems.filter(item =>
    item.id !== 'debug' && item.id !== 'admin'
  );
};
```

### Reordering Menu Items

```typescript
export const customMenuHook: MenuItemsCustomizerHook = () => (menuItems) => {
  // Define custom order
  // Generated ids are long model ids, so order by title (the model label)
  const order = ['Dashboard', 'Entities', 'Items', 'Reports', 'Settings'];

  // Copy before sorting: sort() mutates the array owned by the framework
  return [...menuItems].sort((a, b) => {
    const aIndex = order.indexOf(a.title ?? '');
    const bIndex = order.indexOf(b.title ?? '');

    if (aIndex === -1) return 1;
    if (bIndex === -1) return -1;

    return aIndex - bIndex;
  });
};
```

### Role-Based Menu

```typescript
import { usePrincipal } from '~/auth/principal-context';

export const customMenuHook: MenuItemsCustomizerHook = () => (menuItems) => {
  const principal = usePrincipal();

  // Filter menu based on roles
  return menuItems.filter(item => {
    // Admin-only items
    if (item.id === 'users' || item.id === 'settings') {
      return principal?.roles?.includes('ADMIN');
    }

    // Manager-only items
    if (item.id === 'reports') {
      return principal?.roles?.includes('MANAGER') ||
             principal?.roles?.includes('ADMIN');
    }

    // Default: show item
    return true;
  });
};
```

### Registration

```typescript
// src/custom/application-customizer.tsx
import { MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY, type MenuItemsCustomizerHook } from '~/layout/Drawer/DrawerContent/Navigation';
import { customMenuHook } from './hooks/menuCustomizer';

context.registerService<MenuItemsCustomizerHook>(
  MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY,
  customMenuHook
);
```

### Menu Operation Actions

Menu entries that call model operations are handled by a separate hook, registered with `registerMenuActionsHook(context)` (scaffold `src/custom/hooks/registerMenuActionsHook.ts.default`, generated only when the application has menu operations). It registers a `MenuActionsHook` under `MENU_ACTIONS_HOOK_INTERFACE_KEY` from `~/layout/Drawer/DrawerContent/Navigation/menuCustomization`. Gotcha: its value is `'MENU_ACTIONS_HOOK'`, without the `Hook` suffix of the other keys. The returned `MenuPageActions` object has an optional handler per navigation controller action (and `post<Action>` handlers for actions without input).

## Best Practices

### 1. Keep Components Small

```typescript
// ✅ Good - Small, focused component
export const NotificationBell: FC = () => {
  return <IconButton><Badge>...</Badge></IconButton>;
};

// ❌ Bad - Too much logic in one component
export const MegaComponent: FC = () => {
  // 200 lines of code
};
```

### 2. Use Consistent Styling

```typescript
// ✅ Good - Use theme colors
<IconButton color="inherit">

// ❌ Bad - Hardcoded colors
<IconButton sx={{ color: '#ffffff' }}>
```

### 3. Handle Loading States

```typescript
// ✅ Good
export const UserMenu: FC = () => {
  const principal = usePrincipal();

  if (!principal) {
    return <CircularProgress size={24} />;
  }

  return <Avatar src={principal.avatar} />;
};
```

### 4. Protect Custom Components

```bash
# Apply the One Rule (see hooks/README.md → Understanding .generator-ignore).
# NotificationBell.tsx and UserProfileMenu.tsx are brand-new hand-written
# components (case 3); the generator never emits these paths. NO
# .generator-ignore entry needed.
```

### 5. Test Responsiveness

```typescript
// Use Material-UI breakpoints
import { useMediaQuery, useTheme } from '@mui/material';

export const ResponsiveMenu: FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return isMobile ? <MobileMenu /> : <DesktopMenu />;
};
```

## Complete Example

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY } from '~/custom';
import type { AppBarExtraComponentsHook } from '~/layout/Header/HeaderContent';
import { FOOTER_TEXT_HOOK_INTERFACE_KEY, type FooterTextHook } from '~/layout/Footer';
import { MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY, type MenuItemsCustomizerHook } from '~/layout/Drawer/DrawerContent/Navigation';
import { AppBarExtras } from './components/AppBarExtras';
import { customMenuHook } from './hooks/menuCustomizer';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    context.registerService<AppBarExtraComponentsHook>(
      CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY,
      () => ({ Component: AppBarExtras, spaceRequired: 3 }),
      { component: 'AppBarExtraComponents' },
    );

    context.registerService<MenuItemsCustomizerHook>(
      MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY,
      customMenuHook,
    );

    context.registerService<FooterTextHook>(
      FOOTER_TEXT_HOOK_INTERFACE_KEY,
      () => () => `© ${new Date().getFullYear()} [Your Application Name]`,
    );
  }
}
```

## Troubleshooting

### "AppBar component not showing"

**Verify registration:**
```typescript
// Check application-customizer.tsx: the service property must be exactly
{ component: 'AppBarExtraComponents' }
```

**Check import:**
```typescript
import { NotificationBell } from './components/NotificationBell';
```

### "Logo not displaying"

**Verify file path:**
```bash
ls -la public/images/logo.svg
# File should exist
```

**Check configuration:**
```typescript
// CustomLogoPropsHook result
{ ...defaults, imgSrc: '/images/logo.svg' }  // Path relative to public/
```

### "Menu changes not applying"

**Verify hook registration:**
```typescript
context.registerService<MenuItemsCustomizerHook>(
  MENU_ITEMS_CUSTOMIZER_HOOK_INTERFACE_KEY,
  customMenuHook
);
```

## Related Documentation

- [Hook System Overview](./README.md)
- [Data Hooks](./data-hooks.md)
- [Table Hooks](./table-hooks.md)
- [Theming](../theming.md)
- [Development Workflow](../development-workflow.md)
