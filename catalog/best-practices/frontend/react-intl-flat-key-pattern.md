---
id: react-intl-flat-key-pattern
title: React-Intl Flat Key Translation Pattern
description: "In a hand-built JUDO frontend, keep UI strings as flat dot-separated keys in one TypeScript locale file used with react-intl, with a defaultMessage on every lookup; the generated frontend uses react-i18next JSON files instead."
aliases: [react-intl flat keys, FormatJS locale file]
keywords: [react-intl, formatjs, flat keys, translation, locale file, defaultMessage, useIntl, i18n, hand-built frontend, react-i18next]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: i18n
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: [i18n-custom-translation-keys]
related: [i18n-custom-translation-keys, hungarian-full-localization, complete-frontend-replacement]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Give a hand-built frontend a simple, typed translation setup that uses the same flat dot-notation key style as the generated one.

## Practice

### Platform base

- The generated frontend uses react-i18next with flat translation files in `public/i18n/` named `application_<locale>.json` (generated from the model) and `system_<locale>.json` (platform strings) ([i18n](../../agent-docs/frontend/i18n.md)).
- Generated keys are flat dot-notation strings, not nested objects, for example `entities.User.User_View_Edit.firstName`, `enumerations.StatusType.ACTIVE`, `menuTree.<label>`; the full key is passed to `t` ([key naming conventions and flat keys](../../agent-docs/frontend/i18n.md)).
- Do not use react-intl inside the generated frontend; this pattern is for a hand-built frontend that replaces it ([[complete-frontend-replacement]]). To add keys to the generated frontend, see [[i18n-custom-translation-keys]].

### Practice notes: react-intl with a TypeScript message file

- One `src/i18n/en.ts` exports `{ locale, messages }`, with messages as a plain object of flat keys (a `.ts` file, so keys are checked by the compiler, unlike JSON).
- Key convention: `pages.<page>.<element>.<property>` for page strings, `navigator.<item>` for navigation, and `judo.const.<text>` for common constants.
- Every lookup passes a `defaultMessage` to `intl.formatMessage`, so a missing key shows readable text.
- `IntlProvider` wraps the application once, in `App.tsx`.

```typescript
export const i18nEN = {
  locale: 'en',
  messages: { 'navigator.Home': 'Home', 'pages.orders.table.Name': 'Name' },
};
const intl = useIntl();
const label = intl.formatMessage({ id: 'pages.orders.table.Name', defaultMessage: 'Name' });
```

## Rationale

Flat keys are simple and the TypeScript file adds type checking. The cost is a single file for all strings, no namespaces, long keys, and one locale in the sample.

## Example

A hand-built app: `src/i18n/en.ts` holds navigator labels, table column headers, table actions and common constants; components read them with `useIntl()`, and the fallback text covers missing keys.

## When to avoid

- The generated frontend is used; extend its JSON translations instead.
- Several locales with feature-based splitting are needed; use a catalog-per-feature or the generated JSON structure.

## Related

- [[i18n-custom-translation-keys]] — extra keys in the generated frontend
- [[hungarian-full-localization]] — a second locale in the generated format
- [[complete-frontend-replacement]] — the hand-built frontend this applies to
