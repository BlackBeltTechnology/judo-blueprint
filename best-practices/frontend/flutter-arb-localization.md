---
id: "flutter-arb-localization"
title: "Flutter ARB-Based Localization"
domain: "frontend"
category: "i18n"
score: 61.8
usage_count: 4
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
alternatives:
  - hungarian-full-localization
---
## Description

The JUDO Flutter frontend uses Flutter's standard `intl` package with ARB (Application Resource Bundle) files for localization. Translation keys use a numeric encoding scheme for special characters (space=32, period=46, underscore=95). Lookup is via `AppLocalizations.of(context).lookUpValue(context, 'key')` which resolves to a giant switch/case method. Supported locales include English (en) and Hungarian (hu). This contrasts with the React frontend's i18next JSON-based approach.

## Structure

```
lib/actor_name/l10n/
  app_localizations.dart        # Generated lookup class
  arb/intl_messages.arb         # Translation resources
  dart/messages_all.dart        # Generated message loader
  dart/messages_messages.dart   # Generated message implementations
```

Translation key encoding:
```dart
// "First Name" -> "_First32Name" (32 = space)
// "ACCESS_DENIED" -> "_ACCESS95DENIED" (95 = underscore)
```

Coverage: domain terms, actions, role labels, enum values, error messages, filter operations, and UI labels (~100+ keys per actor).

## Examples

### SkillMatrix
All three actors include English and Hungarian ARB files covering entity names, CRUD actions, role labels (Admin/HR/Professional), enum values (BEGINNER/CONVERSATIONAL/FLUENT/NATIVE), JUDO platform error codes, filter operations, and UI chrome. Keys use numeric encoding (e.g., `_Skill32Levels` for "Skill Levels").

### kozut-eugyfel-client
All three actors include Hungarian (primary) and English ARB files with 150+ keys per actor. Covers navigation items (Sajat feladatok, Aktiv bejelentesek), entity attributes (Azonosito, Targy, Helyszin), action labels, enum values (AKTIV, LEZART, TOVABBITAS), and parameterized error messages. Hungarian character encoding in method names (e.g., `_Saj195t116feladatok` for "Sajat feladatok").

### kozut-eugyfel-model-test
Model defines Hungarian domain terms (Bejelentes, Felhasznalo, Megye, Esemeny, Ertesites) and 7 enumerations with Hungarian values. Labels use Hungarian even in "English" locale for domain terms -- only framework UI strings (Add, Edit, Delete) are English.

### ams-frontend
Admin actor has ~80 translation keys and Manager has a similar set. Both support English (default) and Hungarian locales. Key categories: domain terms (Applications, Campaigns, Users), field labels, actions (Create, Delete, Open, Close, Load, Download), enum values (APPROVED, REJECTED, PENDING, OPEN, CLOSED), and filter operations.

## Trade-offs

- **Pros**: Standard Flutter i18n pattern; compile-time key validation; built-in pluralization support; generated from model
- **Cons**: Numeric encoding makes keys hard to read; giant switch/case is less efficient than hash maps; ARB tooling less mature than i18next
- **When to use**: Standard JUDO Flutter localization -- automatically generated from model

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
- [hungarian-full-localization](hungarian-full-localization.md)
- [i18n-custom-translation-keys](i18n-custom-translation-keys.md)
