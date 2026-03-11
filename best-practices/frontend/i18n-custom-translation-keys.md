---
id: "i18n-custom-translation-keys"
title: "Custom Translation Keys with custom.* Prefix"
domain: "frontend"
category: "i18n"
score: 73.2
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
alternatives:
  - react-intl-flat-key-pattern
---
## Description

Add project-specific translation keys using a `custom.*` prefix convention in both the locale-specific JSON files (e.g., `application_hu-HU.json`) and the generator override extra fragment (for English defaults). Custom keys cover UI text for hand-built components that the generator does not produce translations for. The `defaultValue` parameter in `t()` calls provides a fallback when translation files are not loaded.

## Structure

Translation key prefixes:
- `custom.dimension.*` - Dimension parameter UI strings
- `custom.dialog.*` - Custom dialog titles and descriptions
- `custom.loading.*` - Loading state messages
- `custom.error.*` - Error messages for custom operations
- `extra.localization.operation.*` - Custom operation labels
- `judo.error.validation-failed.*` - Custom validation error messages

Usage in code:
```typescript
// Direct import (non-React)
import { t } from 'i18next';
t('custom.dimension.select-row', { defaultValue: 'Select row' });

// React hook
const { t } = useTranslation();
t('custom.dialog.row-selection.title', { groupLabel, defaultValue: `Select Row from "${groupLabel}"` });
```

## Examples

### RackInspect
15+ custom keys for dimension parameter UI (`custom.dimension.select-row`, `custom.dimension.add-new-row`, `custom.dimension.no-selection`), row selection dialog (`custom.dialog.row-selection.title` with `{{groupLabel}}` interpolation), loading states (`custom.loading.parameters`), and error messages (`custom.error.fetch-parameters-failed`). All have Hungarian translations in `application_hu-HU.json` and English defaults via the generator override fragment.

## Trade-offs

- **Pros**: Consistent key naming convention; generator does not conflict with custom.* prefix; defaultValue ensures fallback
- **Cons**: Two places to maintain (locale JSON + generator fragment); no automated key validation; can accumulate unused keys
- **When to use**: Any custom component that displays user-facing text

## Related Patterns

- [i18n-generator-override-extra-fragment](i18n-generator-override-extra-fragment.md)
- [react-intl-flat-key-pattern](react-intl-flat-key-pattern.md)
