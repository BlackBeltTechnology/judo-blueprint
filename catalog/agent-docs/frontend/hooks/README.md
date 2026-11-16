---
title: Frontend Hook System Overview
description: Pandino-based hook system of the generated React frontend: hook categories, .default scaffolds, registration patterns and .generator-ignore guidance.
---

# Hook System Overview

## Introduction

The JUDO frontend uses a **hook-based customization system** that allows you to extend and modify generated behavior without editing generated code. Hooks are registered from the central `src/custom/application-customizer.tsx` file and use the **Pandino** dependency injection framework.

## Core Concepts

### What Are Hooks?

Hooks are **customization points** in the generated code where you can inject your own logic. They allow you to:

- Modify component behavior
- Add custom UI elements
- Filter and transform data
- Control navigation
- Customize validation
- Override default operations

### Why Hooks?

**Benefits:**
- ✅ **No generated code edits** - All customizations in `src/custom/`
- ✅ **Upgrade-safe** - Regeneration doesn't break customizations
- ✅ **Type-safe** - Full TypeScript support
- ✅ **Modular** - Each hook handles specific functionality
- ✅ **Maintainable** - Clear separation of concerns

**Alternative (Not Recommended):**
- ❌ Edit generated files → Build fails on checksum mismatch
- ❌ Add a `.default` stub or a brand-new file to `.generator-ignore` → Lose generator updates / pointless noise. See One Rule below.
- ❌ Template overrides → Complex to maintain

## Hook Architecture

### Pandino Service Registration

All hooks register through the **Pandino** dependency injection framework:

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import {
  type TableRowHighlightingHook,
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
} from '~/theme/table-row-highlighting';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    // Register hook with interface key
    context.registerService<TableRowHighlightingHook>(
      TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
      myHighlightingHook,
      { component: 'ServiceCanvassingEventsTable' }
    );
  }
}
```

### Key Components

**Interface Keys:**
- String identifiers for each customizable feature
- Example: `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY`
- Exported from the module that owns the hook (for example `~/theme/table-row-highlighting`, `~/layout/Footer`) or from the generated `~/containers/<path>/customization` module for container hooks; there is no `~/generated` barrel

**Service Properties:**
- Configuration objects: `{ component, column, page }`
- Filter which components the hook applies to
- Example: `{ component: 'ServiceActivityForm', column: 'name' }`

**Hook Implementation:**
- Must be React hooks for DI support
- Follow TypeScript interfaces
- Return functions or configuration objects

**Precedence:**
- Page-level hooks override container-level hooks
- More specific hooks override general hooks

## Available Hook Categories

### 1. Data Hooks
Access and manage application data:
- `usePrincipal` - Current user information
- `useViewData` - Page/dialog data access

[Learn more →](./data-hooks.md)

### 2. UI Hooks
Customize visual components (also guest page, sub-theme hooks and menu actions, see [Extension Points](../extension-points.md)):
- AppBar extra components
- Hero and logo customization
- Footer text
- Menu manipulation

[Learn more →](./ui-hooks.md)

### 3. Table Hooks
Enhance table functionality:
- Row highlighting
- Custom columns
- Sidekick components (above-table UI)
- Column customization

[Learn more →](./table-hooks.md)

### 4. Action Hooks
Control operations and flows:
- Container actions (form/table operations)
- Page actions (custom button handlers)
- Operation flow management
- Post-operation navigation

[Learn more →](./action-hooks.md)

### 5. Navigation and Access
Manage routing and permissions:
- Redirect service
- Access filtering
- Hotkey support
- Navigation interception

[Learn more →](./navigation-and-access.md)

### 6. Validation Hooks
Customize input validation:
- Date/DateTime validation
- Field-specific rules
- Custom error messages

[Learn more →](./validation-hooks.md)

## Using .default Scaffold Files

The generator creates `.default` scaffold files for hook registrations under `src/custom/hooks/` (error handler interceptor, `pages/`, `dialogs/`, `containers/`, `custom-implementations/`, `components/cards/`, `sub-themes/`, `registerMenuActionsHook.ts.default`, `default-guest-page-hook-registration.tsx.default`). Only hooks enabled in the model get a scaffold (for example `generateActionsHook`).

`src/custom/application-customizer.tsx` is **not** a `.default` file: it is a plain generated file with an empty `customize(context)` method, and it is where you call your `register...Hook(context)` functions. Because the generator writes it, add it to `.generator-ignore` the first time you edit it (case 1 of the One Rule below); otherwise the build's checksum check fails on the hand edit or the next run regenerates it.

### Activating a Scaffold

A `.default` file is not compiled. To use it, copy it to the same name without `.default`, implement it and call its register function from `application-customizer.tsx`:

```bash
cd src/custom/hooks/pages
cp registerServiceUsersViewPageActionsHook.ts.default registerServiceUsersViewPageActionsHook.ts
```

The copy without `.default` is not generated, so regeneration does not touch it and it needs no `.generator-ignore` entry. Do not edit the `.default` file itself; it is regenerated on every build. (`src/custom/` is not gitignored; only the `.default` files are.)

### Example Registration

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { registerServiceUsersViewPageActionsHook } from './hooks/pages/registerServiceUsersViewPageActionsHook';
import {
  type TableRowHighlightingHook,
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
} from '~/theme/table-row-highlighting';
import { canvassingEventHighlighting } from './hooks/tableRowHighlighting';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    registerServiceUsersViewPageActionsHook(context);

    context.registerService<TableRowHighlightingHook<any>>(
      TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
      canvassingEventHighlighting,
      { component: 'ServiceCanvassingEventsTable' },
    );
  }
}
```

## Common Template Patterns

| Pattern | Purpose | Recommendation |
|---------|---------|----------------|
| `src/custom/hooks/pages/register<Page>ActionsHook.ts.default` | Page-level action hook registrations | Copy without `.default` |
| `src/custom/hooks/containers/register<Container>ActionsHook.ts.default` | Container action hooks | Copy without `.default` |
| `src/custom/hooks/dialogs/register<Dialog>ActionsHook.ts.default` | Dialog action hooks | Copy without `.default` |
| `src/custom/hooks/sub-themes/register<Name>SubThemeHook.tsx.default` | Sub-theme hooks | Copy without `.default` |
| `src/theme/*.ts` (palette, typography, table-row-highlighting) | Plain generated theme files | Edit only with a `.generator-ignore` entry |

## Complete Workflow Example

### Scenario: Add Table Row Highlighting

```bash
# Step 1: Check generated templates
find src/custom -name "*.default"

# Step 2: application-customizer.tsx is a plain file, edited in step 4

# Step 3: Create custom hook
mkdir -p src/custom/hooks
cat > src/custom/hooks/tableRowHighlighting.tsx << 'EOF'
import type { TableRowHighlightingHook } from '~/theme/table-row-highlighting';
import type { ServiceCanvassingEventStored } from '~/services/data-api/model/ServiceCanvassingEvent';

export const canvassingEventHighlighting: TableRowHighlightingHook<ServiceCanvassingEventStored> = () => {
  return () => ([
    {
      name: 'overdue',
      label: 'Overdue Events',
      backgroundColor: '#ffebee',
      condition: (params) => {
        const deadline = new Date(params.row.eventDate);
        return deadline < new Date() && !params.row.completed;
      }
    }
  ]);
};
EOF

# Step 4: Register in customizer
# Edit src/custom/application-customizer.tsx to add the registration

# Step 5: Test (a hand-written file under src/custom/ is not generated, no .generator-ignore entry needed)
cd application/frontend-react/<app>__[actor_fqn]
pnpm run dev
```

## Hook Registration Patterns

### Single Hook Registration

```typescript
export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    context.registerService<TableRowHighlightingHook>(
      TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
      myHighlightingHook,
      { component: 'ServiceActivitiesTable' }
    );
  }
}
```

### Multiple Hooks

```typescript
export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    // Row highlighting
    context.registerService<TableRowHighlightingHook>(
      TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
      activityHighlighting,
      { component: 'ServiceActivitiesTable' }
    );

    // Custom column
    context.registerService<ColumnCustomizerHook>(
      TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY,
      statusColumn,
      { component: 'ServiceActivitiesTable', column: 'status' }
    );

    // Sidekick component
    context.registerService<FC>(
      SIDEKICK_COMPONENT_INTERFACE_KEY,
      ActivityChartSidekick,
      { component: 'ServiceActivitiesTable' }
    );
  }
}
```

### Conditional Registration

```typescript
export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    // Only register in production
    if (process.env.NODE_ENV === 'production') {
      context.registerService<AnalyticsHook>(
        ANALYTICS_HOOK_INTERFACE_KEY,
        analyticsHook
      );
    }

    // Feature flag based registration
    if (localStorage.getItem('betaFeatures') === 'true') {
      context.registerService<BetaFeatureHook>(
        BETA_FEATURE_HOOK_INTERFACE_KEY,
        betaFeatureHook
      );
    }
  }
}
```

## Understanding .generator-ignore

### One Rule

`.generator-ignore` uses `.gitignore`-style matching, scoped to generator output. Single purpose: stop the generator from re-emitting a file at path X because you hand-edited that exact generated file in place. It is **not** a "this file is custom" marker, and it is **not** needed for files the generator never produces.

Three cases:

1. **Generator emits file at path X, you hand-edit X in place.** → Add `X` to `.generator-ignore`. The only legitimate case. Examples: generator-emitted stub `src/custom/application-customizer.tsx`, generator-emitted `src/theme/palette.ts`, or a directly-edited file under `src/generated/`.
2. **`.default` rename pattern.** Generator emits `X.default`. Rename to `X` once and fill in the body. The generator re-emits `X.default` next round as a reference; it never touches `X`. → `X` is OUTSIDE generator scope. **No entry needed.** Do NOT add `X.default` either — you want it to keep regenerating as a reference.
3. **Brand-new hand-written file the generator never emits at that path** (new custom hook file, new component under `src/custom/components/`). → OUTSIDE generator scope. **No entry needed.**

Adding purely-custom files to `.generator-ignore` is noise; remove such entries.

### When to Use

**Add to .generator-ignore:**
- ✅ Generated files outside `src/custom/` that you **edited directly** (not preferred): theme files such as `src/theme/palette.ts`, generated containers
- ✅ Custom files you add outside `src/custom/` that collide with generated paths

**Don't add to .generator-ignore:**
- ❌ Your own files under `src/custom/` (not generated; only `application-customizer.tsx`, `index.tsx`, `custom-element-types.ts` and `interfaces.ts` there are generated)
- ❌ `.default` scaffolds and generated files you have not modified

### Example .generator-ignore

```
# Theme customizations edited by hand
src/theme/palette.ts
src/theme/typography.ts

# Directly edited generated files (not recommended)
# src/containers/Service/Users/Users_View_Edit/ServiceUsersView.tsx
```

### Verify Protection

```bash
# Check if file is protected
grep "application-customizer.tsx" .generator-ignore

# List all protected files
cat .generator-ignore

# Test regeneration
mvn clean install
git diff src/custom/
# Should show no unwanted changes
```

## Best Practices

### 1. Prefer Hooks Over Direct Edits

```typescript
// ✅ Good - Use hook
context.registerService<TableRowHighlightingHook>(
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
  myHook,
  { component: 'ServiceActivitiesTable' }
);

// ❌ Bad - Edit generated file
// Editing src/containers/.../ActivitiesTable.tsx
```

### 2. Activate Scaffolds by Copying

```bash
# ✅ Copy the scaffold to the same name without .default (src/custom/ is not regenerated)
cp src/custom/hooks/pages/registerFooPageActionsHook.ts.default src/custom/hooks/pages/registerFooPageActionsHook.ts

# ❌ Do not edit the .default file in place
```

### 3. Organize Custom Code

```
src/custom/
├── application-customizer.tsx
├── hooks/
│   ├── tableRowHighlighting.tsx
│   ├── usePrincipal.tsx
│   └── validation.tsx
├── components/
│   ├── ActivityChart.tsx
│   └── NotificationBell.tsx
└── utils/
    └── helpers.ts
```

### 4. Document Customizations

```typescript
/**
 * Highlights overdue canvassing events in red.
 *
 * Applied to: ServiceCanvassingEventsTable
 * Updated: 2024-12-15
 */
export const canvassingEventHighlighting: TableRowHighlightingHook = () => {
  return () => ([...]);
};
```

### 5. Test After Regeneration

```bash
# Always test after mvn clean install
mvn clean install
pnpm run dev
# Verify all customizations still work
```

## Troubleshooting

### "Hook not executing"

**Check registration:**
```typescript
// Verify in application-customizer.tsx
console.log('Registering hook');
context.registerService<TableRowHighlightingHook>(
  TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY,
  myHook,
  { component: 'ServiceActivitiesTable' }
);
```

**Verify component name:**
```bash
# Find correct component name in generated code
grep -rn "component=" src/containers | head   # component names used in hook service filters
```

### "File overwritten after build"

**Diagnose first — do NOT blindly add to `.generator-ignore`:**
- If `src/custom/hooks/myHook.tsx` is a brand-new file you wrote and the generator never emits at that path → case 3, no entry needed. The "overwrite" suggests something else (build output, formatter, git). Investigate.
- If the generator DOES emit a stub at that path and you hand-edited it → case 1:
  ```bash
  echo "src/custom/hooks/myHook.tsx" >> .generator-ignore
  ```
- If a `.default` stub exists (`myHook.tsx.default`), use the rename pattern — no entry needed (case 2).

### "Type errors with hook interface"

**Import correct types:**
```typescript
// ✅ Correct: import from the module that defines the hook
import type { TableRowHighlightingHook } from '~/theme/table-row-highlighting';

// ❌ Wrong: there is no ~/generated barrel
import { TableRowHighlightingHook } from '~/generated';
```

## Related Documentation

- [Data Hooks](./data-hooks.md) - usePrincipal, useViewData
- [UI Hooks](./ui-hooks.md) - AppBar, Hero, Logo, Footer
- [Table Hooks](./table-hooks.md) - Row highlighting, custom columns
- [Action Hooks](./action-hooks.md) - Container actions, operations
- [Navigation and Access](./navigation-and-access.md) - Redirects, access control
- [Validation Hooks](./validation-hooks.md) - Date/DateTime validation
- [Main README](../README.md) - Overview and architecture
