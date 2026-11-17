---
id: hungarian-full-localization
title: Full Hungarian Localization with Python i18n Utilities
description: "Provide complete Hungarian (hu-HU) translations for a JUDO frontend: application keys from the model plus system keys, kept in sync with project scripts."
aliases: [hu-HU localization, full translation, locale file maintenance]
keywords: [hu-HU, localization, application_hu-HU.json, system_hu-HU.json, translation scripts, generator-ignore, enumerations _null, menuTree]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:doors-model", "status:emerging"]
category: i18n
status: emerging
projects: [rackinspect, doors-model]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/public/i18n/application_hu-HU.json", "doors-model:unrecorded"]
alternatives: []
related: [generator-ignore-i18n-layout, i18n-custom-translation-keys, i18n-generator-override-extra-fragment]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Deliver the whole UI in Hungarian: entity labels, menus and enumerations (application texts) as well as login, actions, dialogs and errors (system texts).

## Practice

### Platform base

- Translations are flat files in `public/i18n/`: `application_<locale>.json` (generated from the model) and `system_<locale>.json` (platform UI), plus `*_default.json` fallbacks. Keys are flat dot-notation under a `translation` root ([directory structure](../../agent-docs/frontend/i18n.md)).
- Generated key patterns: `entities.<Entity>.<Component>.<field>`, `enumerations.<Type>.<VALUE>` and `enumerations.<Type>._null`, `menuTree.<label>`, `services.<service>...`, `faults.<prefix>.<object>.<attribute>`, `extra.localization.operation.<name>` ([key conventions](../../agent-docs/frontend/i18n.md)).
- The generator writes `application_default.json` from the model. The generated `sync-translations.py` merges it into `application_<defaultLanguage>.json`: it adds new model keys, keeps existing values, and drops keys no longer in the source. Other locale files, such as a script-written `application_hu-HU.json`, are not written by the generator and survive regeneration; `.generator-ignore` protects any file the generator does write, and once ignored it no longer follows the model ([best practices](../../agent-docs/frontend/i18n.md), see [[generator-ignore-i18n-layout]]).
- Adding a language: copy the default files, translate, update the language selector. Users switch language at runtime through i18n `changeLanguage` and a registered language dropdown ([adding languages](../../agent-docs/frontend/i18n.md)).
- Labels set on the UI model elements become the generated translation keys, so Hungarian can also be provided in the model.

### Practice notes: ignored locale files plus scripts

```
public/i18n/
  application_hu-HU.json    # model-derived translations
  system_hu-HU.json         # framework UI strings
  i18nCleaner.py            # remove unused keys
  sort_json.py              # sort keys
  update-localization.py    # merge newly generated keys with manual ones
```

The scripts are custom tools, not platform features. This setup keeps `application_hu-HU.json` and `system_hu-HU.json` in `.generator-ignore` and runs them after model changes.

- Translate enumerations including `_null`, menu labels and every entity field.
- Diff the key set against `application_default.json` to find untranslated keys after each model change.
- Keep project-specific strings under a `custom.*` prefix, see [[i18n-custom-translation-keys]].
- The layout default language can stay `en`; the Hungarian files supply all visible strings.

## Rationale

Users get one language throughout. The cost is maintenance: ignored files miss new generated keys until synced, so scripted syncing prevents untranslated gaps.

## Example

- One frontend: a large application file (menu items, enumerations, all field labels) and a short system file (login, save and similar), maintained with a cleaner and a sorter script.
- Another app puts Hungarian labels on the UI model elements (menu items, table columns, form fields, buttons); a few labels stay English. The keys are generated when the frontend is built.
- Flutter variants use ARB files, which is outside the React docs here.

## When to avoid

- The default texts are enough or only a few strings differ: use [[i18n-custom-translation-keys]].
- Labels can be set in the model itself: translate there and let the generator produce the keys, without ignored files.

## Related

- [[generator-ignore-i18n-layout]] — protecting the locale files
- [[i18n-custom-translation-keys]] — project keys with a `custom.*` prefix
- [[i18n-generator-override-extra-fragment]] — adding default keys via an override fragment
