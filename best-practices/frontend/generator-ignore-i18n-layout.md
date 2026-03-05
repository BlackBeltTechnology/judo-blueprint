---
id: "generator-ignore-i18n-layout"
title: "Generator-Ignore for i18n Files and Layout Config"
domain: "frontend"
category: "build"
score: 10.8
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
---
## Description

Protect locale-specific translation files and layout configuration from being overwritten by the JUDO code generator. Unlike the app/theme ignore pattern, this pattern specifically targets i18n JSON files (e.g., `application_hu-HU.json`, `system_hu-HU.json`) and the layout config (`src/config/layout.ts`). This is essential for projects with full localization in a non-default language, where the translation files contain extensive manual translations that must not be regenerated.

## Structure

```
.generator-ignore:
  .generator-ignore
  .gitignore
  public/i18n/application_hu-HU.json    # ~3,310 lines of Hungarian translations
  public/i18n/system_hu-HU.json         # ~186 lines of system UI translations
  src/config/layout.ts                   # Layout constants (drawer width, theme mode, etc.)
  src/custom/application-customizer.tsx  # Central hook registration hub
```

## Examples

### RackInspect
`.generator-ignore` protects Hungarian locale files (3,310 + 186 lines), layout.ts (horizontal menu, light theme, 260px drawer width, responsive scaling 0.75-1.0), and `application-customizer.tsx` (100+ Pandino registrations). The project also uses Python utilities (`i18nCleaner.py`, `sort_json.py`, `update-localization.py`) to maintain the protected translation files.

## Trade-offs

- **Pros**: Full control over translations and layout; enables complete non-English localization; layout config stays stable
- **Cons**: Must manually add new generated translation keys when model changes; i18n files grow large; layout config may miss new framework options
- **When to use**: Any project requiring full localization in a non-default language, or custom layout configuration

## Related Patterns

- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [i18n-custom-translation-keys](i18n-custom-translation-keys.md)
- [application-customizer-hub](application-customizer-hub.md)
