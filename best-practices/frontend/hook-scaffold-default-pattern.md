---
id: "hook-scaffold-default-pattern"
title: "Hook Scaffold .ts.default Convention"
domain: "frontend"
category: "hook"
score: 70.4
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - itracker
  - workflow-poc
  - reserve-app
---
## Description

The JUDO generator creates hook scaffold files with `.ts.default` extension under `src/custom/hooks/`. These files contain the hook function signature, useful imports, and an empty return object. To activate a hook, the developer renames it from `.ts.default` to `.ts` and adds action implementations. This convention lets the generator produce starter code without overwriting active customizations.

## Structure

```
src/custom/hooks/
  pages/
    registerSomePageActionsHook.ts.default      # Scaffold (inactive)
    registerOtherPageActionsHook.ts             # Activated (renamed)
  containers/
    registerSomeContainerActionsHook.ts.default  # Scaffold
  dialogs/
    registerSomeDialogActionsHook.ts.default     # Scaffold
```

Scaffold file content:

```typescript
const HookImplementation = (data, editMode, storeDiff, refresh, submit) => {
  const { t } = useTranslation();
  const { navigate, back } = useJudoNavigation();
  const { getLatestViewData } = useViewData();
  const someService = new SomeServiceImpl(judoAxiosProvider);

  return {
    // implement actions here
  };
};
```

## Examples

### Trivia
Admin frontend has 24 `.ts.default` scaffolds: 9 page hooks, 11 container hooks, and 4 dialog hooks. None have been activated -- all return empty `{}`. Categories include: `registerActorsAdminAdminCategoriesAccessViewPageActionsHook.ts.default`, `registerActorsAdminTaskTask_FormActionsHook.ts.default`, etc.

### RackInspect
All scaffolds have been activated into working hooks. The `src/custom/` directory contains 87 active `.ts`/`.tsx` files (no `.ts.default` files remain). This shows the progression from scaffold to full customization: renaming, implementing action methods, and registering in `application-customizer.tsx`.

### itracker
60 total hook scaffolds across two actors (UserActor: 24 container + 8 dialog + 10 page; Admin: 9 container + 3 dialog + 6 page), all remaining as `.ts.default` inactive. Demonstrates a project that relies entirely on model-driven behavior without activating any hooks.

### workflow-poc
2 hook scaffolds generated (WorkflowVersion View_Edit custom implementations, guest page hook registration), both left as `.ts.default` inactive. Despite the complex workflow domain with operations and redirects, the project uses a generator override (HBS fragment) and OperationFlowManager instead of individual hook overrides.

### reserve-app
Scaffolds generated across 5 actor frontends. Only 1 scaffold activated in AdminActor: `registerServicesAdminActorStorageTypesAccessViewPageActionsHook.ts` (dialog hook for conditional field validation). All other scaffolds across all 5 actors remain as `.ts.default`. Demonstrates minimal activation in a multi-actor project.

## Trade-offs

- **Pros**: Ready-made starting points for customization; preserves generator capability to update scaffolds; clear naming convention for finding hook points
- **Cons**: Large number of scaffolds can be overwhelming; no documentation on which hooks are most useful; inactive hooks add directory clutter
- **When to use**: This is the standard JUDO pattern for all generated frontends -- hooks are automatically scaffolded

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [application-customizer-hub](application-customizer-hub.md)
