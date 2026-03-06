---
id: "application-customizer-hub"
title: "Application Customizer as Central Hook Registration Hub"
domain: "frontend"
category: "hook"
score: 56.3
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - workflow-poc
  - reserve-app
---
## Description

The `src/custom/application-customizer.tsx` file serves as the central hub for all Pandino service registrations in a JUDO frontend. It uses the `BundleContext` to register action hooks, custom visual element implementations, table row highlighting hooks, and error interceptors. This file is listed in `.generator-ignore` because the generator produces a skeleton version, but the developer extends it with all custom registrations.

## Structure

```typescript
// src/custom/application-customizer.tsx
import { BundleContext } from '@anthropic/pandino';

export function registerCustomizations(context: BundleContext) {
  // Action hooks for pages
  context.registerService(PAGE_ACTIONS_HOOK_KEY, pageHookImpl, { component: COMP_KEY });

  // Action hooks for dialogs
  context.registerService(DIALOG_ACTIONS_HOOK_KEY, dialogHookImpl, { component: COMP_KEY });

  // Custom visual element overrides
  context.registerService(CUSTOM_VISUAL_ELEMENT_KEY, customComponent, { component: COMP_KEY });

  // Table row highlighting
  context.registerService(TABLE_ROW_HIGHLIGHTING_KEY, highlightHookImpl, { component: COMP_KEY });

  // Error handler interceptor
  context.registerService(ERROR_HANDLER_KEY, errorInterceptor);
}
```

Must be in `.generator-ignore` to prevent overwriting:
```
src/custom/application-customizer.tsx
```

## Examples

### RackInspect
`application-customizer.tsx` (~270 lines) registers 100+ hooks: 48 dialog hooks, 13 custom visual element implementations, 10 page hooks, 3 form action hooks, 3 view/edit hooks, 2 table row highlighting hooks, 1 form page action hook, and 1 error handler interceptor. Each import and registration follows a consistent pattern.

### workflow-poc
`application-customizer.tsx` (~47 lines) registers 3 services: an `OperationFlowManager` (custom redirect handler for workflow operation results), a Mermaid diagram visual element, and a CodeViewer syntax highlighting visual element. Demonstrates a lightweight customizer focused on domain visualization rather than hook overrides.

### reserve-app
`application-customizer.tsx` in AdminActor registers a single hook: `registerServicesAdminActorStorageTypesAccessViewPageActionsHook` for conditional field validation on StorageTypes. The other 4 actor frontends use unmodified generated customizer skeletons. Demonstrates the simplest possible customizer with just one registration call.

## Trade-offs

- **Pros**: Single entry point for all customizations; easy to audit what is customized; clear registration pattern
- **Cons**: File grows large in heavily customized projects; must be manually maintained; merge conflicts if multiple developers add hooks simultaneously
- **When to use**: Every JUDO frontend that activates hook scaffolds needs to register them here

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [hook-scaffold-default-pattern](hook-scaffold-default-pattern.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
