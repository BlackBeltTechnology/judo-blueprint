---
id: generator-ignore-app-theme
title: Generator-Ignore for App.tsx and Theme
description: "Protect hand-edited `src/App.tsx` and `src/theme/index.tsx` from regeneration by listing them in `.generator-ignore`, after checking that hooks, model palette and theme fragments are not enough."
aliases: [ignore App.tsx, ignore theme file]
keywords: [generator-ignore, App.tsx, theme, checksum, regeneration, checksum mismatch, theme fragments]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:rackinspect", "status:emerging"]
category: build
status: emerging
projects: [trivia, rackinspect]
evidence: ["trivia:unrecorded", "rackinspect:application/frontend-react/rackinspect__services__generic_user/.generator-ignore"]
alternatives: []
related: [complete-frontend-replacement, dark-theme-override, pwa-manifest-customization, generator-ignore-i18n-layout]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Keep a hand-edited app shell or theme file across builds. This is the last resort when no hook, model setting or override fragment can express the change.

## Practice

### Platform base

- The generator records a checksum for every generated file in `.generated-files__<actor_fqn>`. A file not listed in `.generator-ignore` is regenerated on build; if it was edited by hand (checksum mismatch) the build fails ([checksum protection](../../agent-docs/frontend/README.md)).
- `.generator-ignore` sits in the actor frontend module root and works like `.gitignore`: exact paths, wildcards, directories, patterns, `#` comments. Add the file, then edit it; your changes survive rebuilds ([.generator-ignore](../../agent-docs/frontend/README.md)).
- Platform guidance: hooks first, editing generated files only when no hook exists. For the theme, prefer a same-named override of one theme fragment (`index.ts.mui-<component>.fragment.hbs`, theme options, palette fragments) over ignoring all of `index.tsx`; app-wide colors come from the actor's palette in the model ([theme override fragments](../../agent-docs/frontend/theming.md)).

### Practice notes: ignore the shell and theme

When a frontend fully takes over the shell and theme, its `.generator-ignore` lists them:

```
.generator-ignore
.gitignore
src/App.tsx
src/theme/index.tsx
```

All other generated files keep regenerating. Ignore the narrowest file that works, and put related entries together.

- After a platform upgrade, diff each ignored file against a freshly generated copy and port new tokens or structure by hand.
- Do not copy this to actors that need no customization; an unmodified file should stay generated.

## Rationale

The ignore list is simple and leaves the rest of generation intact. The cost is that ignored files stop receiving generator fixes and can drift from the framework.

## Example

- A game frontend ignores `src/App.tsx`, `src/theme/index.tsx` and `public/manifest.json`; the admin frontend lists only `.generator-ignore` and `.gitignore` and stays fully generated.
- A frontend that keeps App.tsx and the theme generated: its customization goes through hooks and custom components; its ignore list covers the application customizer, layout config and three i18n files.

## When to avoid

- A hook, the actor palette or one theme fragment override is enough: use those, see [[dark-theme-override]].
- The file only fails the checksum because of formatting changes: the docs describe an ignore-checksums build option for that, instead of ignoring the file.

## Related

- [[complete-frontend-replacement]] — replacing the whole UI, which ignores many files
- [[dark-theme-override]] — the theme file takeover this protects
- [[pwa-manifest-customization]] — another file typically listed
- [[generator-ignore-i18n-layout]] — the same mechanism for i18n and layout files
