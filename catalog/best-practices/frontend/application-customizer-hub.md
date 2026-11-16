---
id: application-customizer-hub
title: Application Customizer as Central Hook Registration Hub
description: All Pandino service registrations of a frontend (hooks, visual elements, interceptors, flow managers) are made from the single customizer file, with one register function per hook file.
aliases: [customizer hub, central hook registration]
keywords: [application customizer, pandino, registerService, BundleContext, hook registration, custom folder]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:workflow-poc", "project:reserve-app", "project:park-here", "project:indamedia-adtrack", "status:established"]
category: config
status: established
projects: [rackinspect, workflow-poc, reserve-app, park-here, indamedia-adtrack]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/application-customizer.tsx", "workflow-poc:unrecorded", "reserve-app:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, hook-scaffold-default-pattern, generator-ignore-app-theme]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-11
---
## Intent

A JUDO frontend has many customization points. Calling every registration from one file makes it easy to audit what is customized, and keeps the individual hook files free of wiring.

## Practice

### Platform base

- All hooks register as Pandino services through `context.registerService<T>(INTERFACE_KEY, implementation, properties)`. Properties such as `{ component }` limit a hook to one page or container ([Pandino service registration](../../agent-docs/frontend/hooks/README.md)).
- `src/custom/application-customizer.tsx` is a plain generated file with an empty `customize(context)` method inside a class implementing `ApplicationCustomizer`. It is not a `.default` scaffold and is the place that calls your `register...Hook(context)` functions ([using .default scaffolds](../../agent-docs/frontend/hooks/README.md)).
- `application-customizer.tsx` is itself generated, so once you edit it, list it in `.generator-ignore`; your own hook files beside it are not generated and need no entry ([frontend guide](../../agent-docs/frontend/README.md), [hook files and the custom folder](../../agent-docs/frontend/extension-points.md)).
- The same file registers non-hook services too, for example an `OperationFlowManager` ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).

```typescript
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    registerMyPageActionsHook(context);           // one function per hook file
    registerMyTableRowHighlightingHook(context);
  }
}
```

### Practice notes: one customizer, one register function per hook

This layer is practice, not a platform feature:

- Keep the customizer a flat list of calls: dialog, page and container hooks, custom visual elements, row highlighting, the error interceptor, flow managers.
- Put each registration in its own `register...` function in a hook file, so the customizer stays readable even with many entries.
- Heavily customized projects have a long customizer; light projects have one call. Both use the same structure.

## Rationale

A single entry point makes customization auditable and the registration pattern uniform. The cost: the file grows with the project, is maintained by hand, and can cause merge conflicts when several developers add hooks.

## Example

- A heavily customized frontend: a long customizer registers over a hundred services: dialog hooks, custom visual elements, page hooks, form and view/edit hooks, row highlighting and an error interceptor.
- A workflow-focused frontend: a short customizer with three services: an operation flow manager for workflow results and two visual elements (a diagram and a code viewer).
- A frontend with one registration: a page hook for conditional field validation on one view; other actors keep the generated empty customizer.

## When to avoid

- No hook, interceptor or custom element is activated: leave the generated empty customizer as it is.

## Related

- [[pandino-action-hook-override]] — an action hook registered from this hub
- [[hook-scaffold-default-pattern]] — how scaffolds are activated before registering them
- [[generator-ignore-app-theme]] — other files that need `.generator-ignore` protection
