---
id: structure-generator-ignore-scope
title: Keep the Actor .generator-ignore to Hand-Edited Generated Files
description: List only generated files that you edited in place in an actor module's .generator-ignore, grouped by area with a one-line reason, and never use it as a register of custom files or tests.
aliases: [generator-ignore hygiene, generator-ignore noise, frontend generator-ignore layout]
keywords: [generator-ignore, actor module, src/custom, __tests__, custom files, noise, checksum, regeneration]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/.generator-ignore"]
alternatives: []
related: [generator-ignore-i18n-layout, generator-ignore-app-theme, custom-component-directory, hook-scaffold-default-pattern]
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

An actor module's `.generator-ignore` should tell a reader exactly which generated files the project has taken over. Entries for files the generator never writes hide those few real take-overs.

## Practice

### Platform base

- `.generator-ignore` has one purpose: stop the generator from re-emitting a file you edited in place. It is not a "this file is custom" marker and is not needed for files the generator never produces ([One Rule](../../agent-docs/frontend/README.md)).
- Copies of `.default` hook scaffolds and new files under `src/custom/` are outside generator scope and need no entry; adding them is noise ([hooks One Rule](../../agent-docs/frontend/hooks/README.md)).
- The generator does write `application-customizer.tsx`, `index.tsx`, `custom-element-types.ts` and `interfaces.ts` in `src/custom/` without `.default`; an edited one needs an entry ([hook files and the custom folder](../../agent-docs/frontend/extension-points.md)).

### Practice notes: short file, grouped by area

```
# version control
.generator-ignore
.gitignore

# hand-translated locales (generated, edited in place)
public/i18n/application_hu-HU.json
public/i18n/system_hu-HU.json

# layout constants
src/config/layout.ts

# hook registrations
src/custom/application-customizer.tsx
```

- Before adding a line, check that the path appears in the module's checksum file (`.generated-files…`). If it does not, the generator does not own the file and the line is not needed.
- One group per area (version control, locales, theme, layout, customizer), each with a comment that says why the file is taken over.
- Do not list custom helpers, custom components, test files or planned files. Track those in version control and in a module README, not in `.generator-ignore`.
- Review the file when upgrading the platform: every entry is a generated file that no longer receives template fixes.

## Rationale

Each real entry costs upgrade work, because that file stops following the templates. A short list keeps that cost visible. Noise entries do no harm to the build, but they make the list look longer than the real take-over, and readers start to treat `.generator-ignore` as the place where new files must be registered.

## Example

- One frontend's `.generator-ignore` holds the entries above plus `public/i18n/application_en-US.json`, then many more paths grouped under change-ticket comments: helpers in `src/custom/hooks/utils/`, components in `src/custom/hooks/custom-implementations/`, tests in `src/__tests__/`, and `src/custom/type-augmentations.d.ts`, which does not exist. None of these, nor the `en-US` file, are in the module's checksum file, so they are noise.

## When to avoid

- A platform version emits files in a folder you also use for custom code: then an entry for the colliding path is a real take-over and belongs in the list.

## Related

- [[generator-ignore-i18n-layout]] — the locale and layout entries
- [[generator-ignore-app-theme]] — theme files taken over in place
- [[custom-component-directory]] — custom files need no entry
- [[hook-scaffold-default-pattern]] — `.default` copies need no entry
