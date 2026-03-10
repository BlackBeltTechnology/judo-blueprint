---
id: "hungarian-full-localization"
title: "Full Hungarian Localization with Python i18n Utilities"
domain: "frontend"
category: "i18n"
score: 66.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - doors-model
---
## Description

Provide complete Hungarian (hu-HU) localization for a JUDO frontend application, including both application-specific translations (entity fields, menu items, enumerations) and system-level translations (login, actions, dialogs, errors). The locale files are protected via `.generator-ignore` and maintained with Python utility scripts for cleaning, sorting, and updating translation keys. The default language in layout.ts remains `'en'`, but the Hungarian translation files override all visible strings. In Flutter variants, Hungarian is the primary locale set directly in the ARB files and AppLocalizations delegate. In model-only projects, Hungarian labels are embedded directly in the ESM model XML and would drive generated i18n files.

## Structure

```
public/i18n/
  application_hu-HU.json    # ~3,310 lines - domain translations
  system_hu-HU.json          # ~186 lines - framework UI strings
  i18nCleaner.py             # Removes unused keys
  sort_json.py               # Sorts keys alphabetically
  update-localization.py     # Syncs generated + manual keys
```

Translation key categories:
- `services.*` (~3,159 entries) - Entity fields and views
- `menuTree.*` (29 entries) - Navigation menu labels
- `enumerations.*` (~70 entries) - Enum value labels (including `_null`)
- `custom.*` (~15 entries) - Custom component strings
- `judo.security.*`, `judo.action.*`, etc. - System strings

## Examples

### RackInspect
3,310-line `application_hu-HU.json` covers 29 menu items, 16 enumeration types with Hungarian labels (e.g., `Zold`, `Piros`, `Sarga` for error types), and all entity field labels. 186-line `system_hu-HU.json` covers system UI (e.g., `judo.security.login` = "Belepes", `judo.action.save` = "Mentes"). Three Python scripts maintain the files: `i18nCleaner.py` removes stale keys, `sort_json.py` ensures consistent ordering.

### kozut-eugyfel-client (Flutter)
Hungarian as primary language in ARB-based Flutter localization. 150+ translation keys per actor covering navigation (Sajat feladatok, Aktiv bejelentesek, Lezart bejelentesek), entities (Bejelentes, Felhasznalo, Megye), actions (Bejelentes letrehozasa, Bejelentes lezarasa), and enum values (AKTIV, LEZART, MEGNYITAS). English as secondary fallback. No Python scripts needed -- ARB files are generated directly.

### doors-model
ESM XML model embeds Hungarian labels directly on all UI elements: menu items (Feladataim, Szerzodeseim, Partnerek), table columns (Letrehozas datuma, Nyilvantartasi szam), form fields (Dokumentum statusza), and buttons (Jovahagyas, Elutasitas, Alairas, Lezaras). A few labels remain in English (Divisions, Positions, Banks, In progress). Labels would generate i18n translation keys when the frontend is produced.

### ams-frontend
Both Admin and Manager actors support English (default) and Hungarian locales via ARB-based Flutter localization. ~80 keys per actor covering domain terms (Applications, Campaigns, Users, Approval List, Subordinates), field labels, enum values (OPEN/CLOSED, PENDING/APPROVED/REJECTED, ACCESS/REVOKE/CONFIRMATION), and action labels (Open, Close, Load, Download, Approve All).

## Trade-offs

- **Pros**: Complete user experience in target language; professional localization; Python utilities reduce maintenance burden
- **Cons**: Large files require careful management; model changes add new keys that must be manually translated; no runtime language switching
- **When to use**: Enterprise applications deployed in a specific locale where full localization is required

## Related Patterns

- [generator-ignore-i18n-layout](generator-ignore-i18n-layout.md)
- [i18n-custom-translation-keys](i18n-custom-translation-keys.md)
- [i18n-generator-override-extra-fragment](i18n-generator-override-extra-fragment.md)
- [flutter-arb-localization](flutter-arb-localization.md)
