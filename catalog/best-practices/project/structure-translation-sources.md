---
id: structure-translation-sources
title: Translation Source Spreadsheets and Glossary Location
description: "Keep a business-owned translation spreadsheet under one stable path outside application/, extract it into a machine-readable glossary that scripts check the generated locale files against, and treat the locale JSON files as the runtime artifact."
aliases: [translation spreadsheet, translations.xlsx, terminology glossary, translation dictionary, i18n source files]
keywords: [translations, xlsx, glossary, dictionary, hu-HU, en-US, locale json, application_en-US.json, terminology, i18n scripts]
tags: ["domain:project", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:translations.xlsx", "rackinspect:scripts/i18n/ticketing-glossary.json", "rackinspect:openspec/specs/translation-dictionary/spec.md"]
alternatives: []
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Customers and translators often own the terminology in a spreadsheet, while the running frontend reads generated locale JSON files. Give the spreadsheet one stable home, turn it into a glossary that tools can read, and check the locale files against it, so the UI, the user guide and the business use the same words.

## Practice

### Platform base

The frontend reads flat translation files from `public/i18n/` in each frontend module: `application_<locale>.json` generated from the model labels and `system_<locale>.json` for platform texts ([i18n directory structure](../../agent-docs/frontend/i18n.md#directory-structure)). A hand-translated locale file must be listed in `.generator-ignore` to survive regeneration, see [[generator-ignore-i18n-layout]]. Backend messages use properties files per locale ([backend i18n](../../agent-docs/backend/internationalization-guide.md)). The platform has no spreadsheet import for translations; the spreadsheet is a project artifact.

### Practice notes: one source, one glossary, checked outputs

| Artifact | Location | Owner |
|---|---|---|
| Translation spreadsheet (terms per language, one sheet per UI area) | one stable path outside `application/`, for example `docs/i18n/translations.xlsx` | business or translators |
| Glossary extracted from it (JSON: term, language values, source key) | next to the scripts that use it, for example `scripts/i18n/` | developers |
| Locale files (`application_<locale>.json`, `system_<locale>.json`) | generated frontend `public/i18n/` | generator plus `.generator-ignore` |
| Backend message properties | the backend module resources | developers |

- Keep one spreadsheet under a fixed name and let git hold the versions. A second copy with a date and a reviewer suffix in the name splits the source of truth.
- Extract the spreadsheet into a glossary file once and grow the glossary when new terms appear; add a term to the glossary before using it in a locale file.
- Check the locale files with a script that asserts the glossary term appears in every matching key (see [[structure-scripts-folder]]).
- Keep all model labels in one language, so the generated default file is consistent; the other languages come from the locale files ([[hungarian-full-localization]], [[i18n-custom-translation-keys]]).
- Generate human-readable term lists (lexicon, UI text overview for the user guide) from the locale files or the glossary instead of maintaining them by hand.

## Rationale

- Translators keep their familiar tool; developers get a diffable, testable glossary.
- Terms stay consistent across UI, emails and user guide because every output is checked against one list.
- Cost: the spreadsheet-to-glossary extraction is a manual or scripted step that must be repeated when translators deliver a new spreadsheet.

## Example

- One project keeps a three-language spreadsheet with many terms on separate sheets for navigation, operations, entities, fields, enumerations, messages and other texts. For a long time the English UI did not use it; a later change extracted it into a dictionary artifact and filled `application_en-US.json` from it, protected by `.generator-ignore`. A glossary JSON in `scripts/i18n/` names the required stem per concept and is asserted against the locale files.
- Gaps in the same project: the spreadsheet sits at the root next to a dated copy with a reviewer suffix, and a Hungarian lexicon and a UI text list in `docs/` are hand-maintained copies of the locale files.

## When to avoid

- Single-language applications, or projects where model labels and a few `custom.*` keys cover all texts: the locale files alone are enough.
- Teams that use a translation management service: that service is the source; export into the locale files and skip the spreadsheet.

## Related

- [[hungarian-full-localization]] — maintaining full locale files with scripts
- [[generator-ignore-i18n-layout]] — protecting hand-translated locale files
- [[i18n-custom-translation-keys]] — project-specific keys and their defaults
- [[i18n-osgi-service]] — backend message translations
- [[structure-repository-root-layout]] — why the spreadsheet does not belong at the root
