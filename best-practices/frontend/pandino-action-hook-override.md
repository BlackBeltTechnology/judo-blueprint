---
id: "pandino-action-hook-override"
title: "Pandino Service Registry for Action Hook Overrides"
domain: "frontend"
category: "hook"
score: 70.4
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - reserve-app
---
## Description

The JUDO framework uses Pandino (an OSGi-like service registry for JavaScript) to enable runtime action hook injection in generated pages. Each page component queries the Pandino registry for a hook service matching its interface key. If found, the hook's returned actions are spread over the default actions, allowing selective overrides. This decouples customization from the generated page code.

## Structure

```typescript
// In a generated page component
const { service: customActionsHook } = useTrackService<ActionsHook>(
  `(${OBJECTCLASS}=${ACTIONS_HOOK_INTERFACE_KEY})`
);

const customActions = customActionsHook?.(data, editMode, storeDiff, refresh, submit);

const actions = {
  getPageTitle,
  backAction,
  refreshAction,
  updateAction,
  deleteAction,
  getMask,
  ...(customActions ?? {}),  // Custom overrides spread on top
};
```

Pages also support extended action types like `postRefreshAction`:

```typescript
type ActionsExtended = PageActions & {
  postRefreshAction?: (data, storeDiff, setValidation) => Promise<void>;
};
```

## Examples

### Trivia
Admin frontend's 2 custom page overrides (Categories AccessViewPage, Contest Categories RelationViewPage) both use `useTrackService` to query Pandino for action hooks. The corresponding `.ts.default` scaffolds in `src/custom/hooks/pages/` are ready for activation but currently return empty objects.

### RackInspect
Over 100 Pandino service registrations in `application-customizer.tsx` covering dialog hooks (48), page hooks (10), form action hooks (3), view/edit hooks (3), table row highlighting hooks (2), custom visual element implementations (13), and a form page action hook. All registered via `context.registerService<HookType>(INTERFACE_KEY, hookImpl, { component: COMPONENT_KEY })`.

### itracker
Pandino infrastructure is fully generated across all 15 pages and 11 dialogs. Each component uses `useTrackService` to query for hooks, but none are registered -- all 60 hook scaffolds remain as `.ts.default`. Demonstrates Pandino as a zero-overhead pattern when no customizations are needed.

### reserve-app
Single Pandino hook registration in AdminActor: `registerServicesAdminActorStorageTypesAccessViewPageActionsHook` registers against `SERVICES_ADMIN_ACTOR_STORAGE_TYPES_ACCESS_VIEW_PAGE_ACTIONS_HOOK_INTERFACE_KEY`. The hook overrides `isNameRequired` to make the name field conditionally required based on the `active` flag. Demonstrates the lightest possible Pandino usage -- one hook across 5 actor frontends.

## Trade-offs

- **Pros**: Non-invasive customization; generated page code remains untouched; hooks are resolved at runtime; supports partial overrides
- **Cons**: Pandino adds runtime complexity; hook registration requires understanding the service registry; debugging can be harder
- **When to use**: Standard JUDO pattern for customizing generated page actions without modifying generated code

## Related Patterns

- [hook-scaffold-default-pattern](hook-scaffold-default-pattern.md)
- [application-customizer-hub](application-customizer-hub.md)
