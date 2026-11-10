---
id: hook-scaffold-default-pattern
title: Hook Scaffold .ts.default Convention
description: "The generator emits inactive `.default` hook scaffolds under `src/custom/hooks/`; activate one by copying it to a normal file, implementing it and registering it in the application customizer."
aliases: [.default scaffold, hook scaffold activation]
keywords: [hook scaffold, .default, src/custom/hooks, application-customizer, generateActionsHook, activation, regeneration]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:rackinspect", "project:itracker", "project:workflow-poc", "project:reserve-app", "status:established"]
category: hook
status: established
projects: [trivia, rackinspect, itracker, workflow-poc, reserve-app]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "itracker:unrecorded", "workflow-poc:unrecorded", "reserve-app:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, application-customizer-hub]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Start every frontend customization from the generated scaffold of the hook, so the signature and imports are right and the hook point is easy to find.

## Practice

### Platform base

- The generator creates `.default` scaffold files for hook registrations under `src/custom/hooks/`: error handler interceptor, `pages/`, `dialogs/`, `containers/`, `custom-implementations/`, `components/cards/`, `sub-themes/`, `registerMenuActionsHook.ts.default` and the guest page registration. A scaffold exists only when the hook is enabled in the model (for example `generateActionsHook`) ([scaffold files](../../agent-docs/frontend/hooks/README.md), [hook files](../../agent-docs/frontend/extension-points.md)).
- `src/custom/application-customizer.tsx` is a plain generated file with an empty `customize(context)`; it is where `register...Hook(context)` calls go. It is not a `.default` file.
- A `.default` file is not compiled. Copy it to the same name without `.default`, implement it, and register it. Do not edit the `.default` file: it is regenerated on every build. The copy is not generated (the frontend `.gitignore` ignores only the `.default` files), so it survives regeneration and needs no `.generator-ignore` entry ([activating a scaffold](../../agent-docs/frontend/hooks/README.md)).

### Project practice: leave the scaffolds, activate on demand

```
src/custom/hooks/
  pages/
    registerSomePageActionsHook.ts.default   # scaffold, inactive
    registerOtherPageActionsHook.ts          # activated copy
  containers/ ...
  dialogs/ ...
```

The scaffold body is the hook function with its generated arguments and an empty return, to which you add the action handlers:

```typescript
const HookImplementation = (data, editMode, storeDiff, refresh, submit) => {
  const { t } = useTranslation();
  const someService = new SomeServiceImpl(judoAxiosProvider);
  return {
    // implement actions here
  };
};
```

- Activate only the hooks you need; leave the others as scaffolds. An unused scaffold costs nothing at runtime.
- Name hooks by the generated scaffold name, so the hook point can be found from the page it belongs to.
- Old notes of this pattern speak of renaming; the docs say copy, which leaves the regenerated `.default` for comparison after model changes.

## Rationale

Scaffolds give correct signatures and imports for every hook point the model enables. Because the `.default` files are gitignored and copied rather than edited, the generator can keep updating the originals.

## Example

- trivia admin: 24 scaffolds (page, container, dialog), none activated.
- itracker: about 60 scaffolds over two actors, none activated; behavior comes from the model.
- workflow-poc: 2 scaffolds, left inactive; it uses a generator fragment override and `OperationFlowManager` instead.
- reserve-app: one activated (a dialog hook for conditional field validation) among scaffolds for five actors.
- rackinspect: all scaffolds activated into about 87 working files under `src/custom/`.

## When to avoid

- The model setting or a built-in widget already gives the behavior; do not add a hook by habit.
- For a hook type with no scaffold, enable the hook flag in the model first instead of writing registration code from scratch.

## Related

- [[pandino-action-hook-override]] — how an activated hook is registered
- [[application-customizer-hub]] — the file where registrations are collected
