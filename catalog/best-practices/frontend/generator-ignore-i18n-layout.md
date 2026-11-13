---
id: generator-ignore-i18n-layout
title: Generator-Ignore for i18n Files and Layout Config
description: "Protect hand-translated locale JSON files and the layout config from regeneration by listing them in `.generator-ignore`."
aliases: [ignore i18n files, ignore layout config]
keywords: [generator-ignore, i18n, application_hu-HU.json, system_hu-HU.json, layout.ts, localization, regeneration]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: build
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/.generator-ignore", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/config/layout.ts"]
alternatives: []
related: [generator-ignore-app-theme, i18n-custom-translation-keys, application-customizer-hub]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A frontend with extensive manual translations or tuned layout constants must keep those files across builds.

## Practice

### Platform base

- Translation files are generated flat in `public/i18n/` as `application_<locale>.json` (from the model: entities, enumerations, menu, services) and `system_<locale>.json` (platform UI texts); `*_default.json` is the fallback ([directory structure](../../agent-docs/frontend/i18n.md)).
- Generated files not in `.generator-ignore` are regenerated and a hand-edited one fails the checksum check; `.generator-ignore` is the documented protection ([checksum protection](../../agent-docs/frontend/README.md)).
- Platform docs describe adding a language by copying the default files and translating them, and finding missing keys by diffing against the default ([adding languages](../../agent-docs/frontend/i18n.md)).

### Practice notes: ignore locale and layout files

A frontend that keeps its translations and layout constants lists them:

```
.generator-ignore
.gitignore
public/i18n/application_hu-HU.json
public/i18n/system_hu-HU.json
src/config/layout.ts
src/custom/application-customizer.tsx
```

- Ignored locale files are no longer updated when the model adds entities or attributes; add the new generated keys by hand (diff against `application_default.json`).
- `src/config/layout.ts` (drawer width, theme mode, menu orientation) is code from this example, not documented platform behavior; verify it exists in your generated frontend.
- For only a few extra keys, a `custom.*` prefix plus an override fragment avoids ignoring the whole file, see [[i18n-custom-translation-keys]].

## Rationale

Manual translation lines and tuned layout values must not be overwritten. The price is manual key maintenance and a layout file that can miss new framework options.

## Example

One frontend protects its Hungarian locale files, its layout config (horizontal menu, light theme, drawer width) and the application customizer with many hook registrations. It maintains the translation files with its own scripts (cleaner, sorter, updater).

## When to avoid

- Only a handful of project keys is needed: use [[i18n-custom-translation-keys]].
- English-only apps with the generated texts: leave the files generated.

## Related

- [[generator-ignore-app-theme]] — the same mechanism for shell and theme
- [[i18n-custom-translation-keys]] — extra keys without ignoring files
- [[application-customizer-hub]] — the customizer file also listed here
