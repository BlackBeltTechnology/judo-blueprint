---
id: i18n-generator-override-extra-fragment
title: i18n Generator Override Extra Fragment for Custom Keys
description: "Inject custom translation keys into the generated default English translation file (`application_default.json`) using a Handlebars template fragment."
aliases: []
keywords: [i18n, generator, override, extra, fragment, custom keys, application_default.json, translation]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:park-here", "status:emerging"]
category: i18n
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:application/frontend-react/generator-overrides/ui-react/actor/public/i18n/application_default_extra.fragment.hbs"]
alternatives: []
related: [i18n-custom-translation-keys, generator-override-extra-dependencies, generator-ignore-i18n-layout]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Custom UI code (hand-written components, custom operations, project fault messages) needs translation keys that the model does not produce. This practice gives those keys English defaults in the generated `application_default.json` without editing the generated file, so they survive regeneration.

## Practice

### Platform base

- `public/i18n/application_*.json` files are generated from the model and are overwritten on regeneration (or fail the checksum check) unless listed in `.generator-ignore`; keys follow flat dot notation inside a `translation` object ([i18n](../../agent-docs/frontend/i18n.md)).
- The generator supports fragment overrides: a file with the same relative path and name as a template's fragment, placed in the override directory, is picked up on every generation and needs no `.generator-ignore` entry ([fragment overrides](../../agent-docs/deployment/build-process.md)).
- The platform key patterns include `extra.localization.operation.<operationName>` for custom operation labels and `faults.<app>...` for fault messages ([i18n](../../agent-docs/frontend/i18n.md)).

### Practice notes: a fragment for `application_default.json`

The agent-docs describe fragment overrides for `pom.xml` and `feature.xml`; the i18n slot below is practice from one example and is not covered by the agent-docs, so check the generated output after adding it.

- Place `application_default_extra.fragment.hbs` under the frontend override directory at `ui-react/actor/public/i18n/`.
- The UI template includes this partial as `actor/public/i18n/application_default_extra.fragment.hbs` inside `application_default.json`, after a placeholder line (`"__extra": "Placeholder for additional translations",`), so the override file keeps that relative path and the content is key-value lines that continue the object.
- The content is JSON key-value pairs without wrapping braces; the generator merges it into the `translation` object of `application_default.json`.
- Use a `custom.*` prefix for project keys so they never collide with generated keys ([[i18n-custom-translation-keys]]).
- Other locales (for example Hungarian) are maintained separately in a locale file protected by `.generator-ignore`.

```
"extra.localization.operation.createOrderOperation": "Create Order",
"custom.dialog.row-selection.title": "Select row from \"{{groupLabel}}\" group",
"custom.parameter.no-selection": "-- None --",
"judo.error.validation-failed.CUSTOM_ERROR": "Custom error message",
```

The fragment is itself a Handlebars template, so a literal i18next placeholder written with double braces may need escaping to reach the output unchanged; verify in the generated file.

## Rationale

The generated default file stays fully model-driven while custom keys still get English fallbacks. A missing default makes the UI show the raw key for any locale without its own file. The cost is one more file to keep in step with the locale files.

## Example

One app injects a set of keys: operation labels, configurable-parameter UI text, row-selection dialog strings with a `groupLabel` placeholder, a record creation label and a custom validation error message. Translations for other locales live in a separate ignored locale file.

## When to avoid

- The frontend hand-maintains all locale files under `.generator-ignore` anyway ([[generator-ignore-i18n-layout]]).
- No custom component needs its own keys.

## Related

- [[i18n-custom-translation-keys]] — the `custom.*` key convention these defaults carry
- [[generator-override-extra-dependencies]] — same fragment mechanism for npm dependencies
- [[generator-ignore-i18n-layout]] — the alternative of ignoring the generated locale files
