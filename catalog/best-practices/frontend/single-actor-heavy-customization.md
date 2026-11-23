---
id: single-actor-heavy-customization
title: Single-Actor Frontend with Heavy Hook Customization
description: "Keep every page of a single-actor frontend generated and put the behaviour in hooks, custom visual element implementations and registrations in application-customizer.tsx; one app has about a hundred registrations and changes no generated page."
aliases: [heavily hooked generated frontend, hook-only customization]
keywords: [single actor, heavy customization, hooks, application-customizer, custom visual element, scaffold, src/custom, generated pages, generator upgrades]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: framework
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/application-customizer.tsx"]
alternatives: [dual-actor-frontend-architecture, zero-customization-generated-frontend]
related: [dual-actor-frontend-architecture, application-customizer-hub, pandino-action-hook-override, zero-customization-generated-frontend, complete-frontend-replacement]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Get a tailored UX in an enterprise CRUD application without editing generated pages, so every generator upgrade still flows in.

## Practice

### Platform base

- Hooks register as Pandino services from `src/custom/application-customizer.tsx`, normally by copying the generated `.default` scaffolds under `src/custom/hooks/` to names without `.default` and calling their `register...(context)` functions ([hooks: using .default scaffolds](../../agent-docs/frontend/hooks/README.md)). A copied scaffold is never removed by `generate`: when the model element behind it goes, delete your copy too, or the frontend build fails on the missing imports.
- Hook code you add in `src/custom/` is not generated and survives regeneration without `.generator-ignore` entries; the generated `application-customizer.tsx` needs an entry once you edit it ([frontend guide](../../agent-docs/frontend/README.md)).
- Model elements that the generator exposes as extension points can be replaced by custom visual element implementations registered under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` ([custom component replacement](../../agent-docs/frontend/advanced-patterns.md)). Container, page and dialog hooks have generated, per-container names; always take the names from the generated scaffolds ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).

### Practice notes: all customization in hooks

This is a choice about how far to go with the platform's mechanisms:

- Leave generated `pages/`, `containers/` and `services/` untouched. When a UI need cannot be met by a hook, use a custom visual element implementation rather than editing generated code.
- Group the code under `src/custom/hooks/` by kind: custom implementations, dialog action hooks, page action hooks, form blur hooks, view/edit hooks, table row highlighting hooks, shared utilities.
- Keep `application-customizer.tsx` as the one registration hub ([[application-customizer-hub]]); it can grow to over a hundred registrations, so keep the hook files themselves free of wiring.
- `.generator-ignore` is used only for the few generated files that are truly taken over (translations, layout configuration).

```
src/custom/
  application-customizer.tsx   # registration hub
  hooks/
    custom-implementations/  dialogs/  pages/
    FormActionsHooks/  ViewEditActionHooks/  TableRowHighlightingHooks/  utils/
```

## Rationale

All generated pages stay current with the generator and look consistent; the customization is non-invasive and in one codebase. The cost: hooks cannot express every UI (some need a visual element), many hooks are hard to navigate, and the customizer grows large.

## Example

One app: a single actor with a large `src/custom` tree (including scaffolds), many registrations and many menu items, with no generated page edited. Customizations include a configurable-parameter component (a custom visual element), a masked identifier input, address auto-composition, table row highlighting, PDF preview and mask optimizations.

## When to avoid

- The UX diverges from page-per-access CRUD; see [[complete-frontend-replacement]].
- The actor needs no behaviour beyond the generated one; see [[zero-customization-generated-frontend]].
- Several actors with different needs; see [[dual-actor-frontend-architecture]].

## Related

- [[dual-actor-frontend-architecture]] — one customized and one generated actor
- [[application-customizer-hub]] — the registration file
- [[pandino-action-hook-override]] — how hooks are registered
- [[zero-customization-generated-frontend]] — the opposite end
- [[complete-frontend-replacement]] — when hooks are not enough
