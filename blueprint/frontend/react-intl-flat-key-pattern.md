---
id: "react-intl-flat-key-pattern"
title: "React-Intl Flat Key Translation Pattern"
domain: "frontend"
category: "i18n"
score: 9.9
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
alternatives:
  - i18n-custom-translation-keys
---
## Description

Use `react-intl` (FormatJS) with flat dot-separated key strings in a single TypeScript locale file. Keys follow the convention `pages.{page}.{element}.{property}` for page-specific strings and `navigator.{item}` for navigation. Messages are defined as a plain object in a `.ts` file (not JSON), exported as `{ locale, messages }`. Each `intl.formatMessage()` call includes a `defaultMessage` fallback. This is simpler than the JSON-based i18next approach used in generator-produced frontends.

## Structure

```typescript
// src/i18n/en.ts
export const i18nEN = {
  locale: 'en',
  messages: {
    'navigator.Build': 'Build',
    'navigator.Storage': 'Storage',
    'pages.galaxies.table.Name': 'Name',
    'pages.galaxies.table.Real': 'Real',
    'pages.galaxies.table.Delete': 'Delete',
    'judo.const.Set filters': 'Set filters',
  },
};

// Usage in components
const intl = useIntl();
const label = intl.formatMessage({
  id: 'pages.galaxies.table.Name',
  defaultMessage: 'Name',
});
```

## Examples

### ActionGroupTestReact
Single `src/i18n/en.ts` file with flat key-value messages. Keys cover navigator labels, table column headers, table actions, and common UI constants. Used with `useIntl()` hook in column definitions and page headers. `defaultMessage` provides fallback if key is missing. IntlProvider wraps the entire app in `App.tsx`.

## Trade-offs

- **Pros**: Simple flat structure; TypeScript file provides type checking; defaultMessage ensures fallback; react-intl is well-maintained
- **Cons**: All translations in one file (no splitting by feature); no namespace separation; flat keys can get long; only one locale file shown
- **When to use**: Custom JUDO frontends with simple i18n needs and a single primary locale

## Related Patterns

- [i18n-custom-translation-keys](i18n-custom-translation-keys.md)
- [hungarian-full-localization](hungarian-full-localization.md)
