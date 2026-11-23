---
id: i18n-custom-translation-keys
title: "Custom Translation Keys with custom.* Prefix"
description: "Name project-specific translation keys with a `custom.*` prefix, give English defaults through the generator override fragment and other locales in the locale files."
aliases: [custom.* keys, project translation keys]
keywords: [custom translation keys, custom.* prefix, defaultValue, i18next, application_default.json, extra fragment, locale files]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: i18n
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/custom-implementations/DimensionParametersViewComponent.tsx", "rackinspect:application/frontend-react/rackinspect__services__generic_user/public/i18n/application_hu-HU.json"]
alternatives: [react-intl-flat-key-pattern]
related: [i18n-generator-override-extra-fragment, react-intl-flat-key-pattern]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Hand-built components need translated texts that the model does not produce. A fixed prefix keeps them apart from generated keys.

## Practice

### Platform base

- Translation files are flat dot-notation keys under a `translation` root; `t()` takes the full key ([flat keys](../../agent-docs/frontend/i18n.md)).
- The platform's own key patterns are `entities.*`, `enumerations.*`, `menuTree.*`, `services.*`, `faults.<prefix>.*` and `extra.localization.operation.<name>` for custom operation labels ([key conventions](../../agent-docs/frontend/i18n.md)).
- `application_<locale>.json` files are generated and regenerate unless listed in `.generator-ignore`; keep a `_default` fallback ([best practices](../../agent-docs/frontend/i18n.md)).

### Practice notes: `custom.*` plus defaults

The convention puts every non-generated string under `custom.*`, grouped by area:

- `custom.parameter.*` for a feature's UI strings, `custom.dialog.*` for dialog titles and texts, `custom.loading.*`, `custom.error.*`.
- English defaults go into the generator override extra fragment ([[i18n-generator-override-extra-fragment]]); other locales go into the locale file, protected as in [[generator-ignore-i18n-layout]].
- Always pass a `defaultValue` so the text still shows when a key is missing.

```typescript
import { t } from 'i18next';            // outside React
t('custom.parameter.select-row', { defaultValue: 'Select row' });

const { t } = useTranslation();         // inside a component
t('custom.dialog.row-selection.title', { groupLabel, defaultValue: `Select Row from "${groupLabel}"` });
```

- Check periodically for unused custom keys; nothing validates them automatically.
- Two files must be updated per new key (fragment and locale file).

## Rationale

The prefix cannot clash with generated keys, so regeneration and model changes do not touch them, and a reader sees at once which texts are hand-written.

## Example

One app: keys under one `custom.<area>.*` prefix for a configurable-parameter UI (select row, add new row, no selection), a row-selection dialog with a `groupLabel` placeholder, loading states and fetch-error messages. English defaults come from the override fragment; Hungarian ones from `application_hu-HU.json`.

## When to avoid

- The text belongs to a model element: set the label in the model and let the generator emit the key.
- Custom operation labels already fit `extra.localization.operation.<name>`.

## Related

- [[i18n-generator-override-extra-fragment]] — the English defaults mechanism
- [[react-intl-flat-key-pattern]] — flat key usage in components
- [[generator-ignore-i18n-layout]] — protecting locale files
