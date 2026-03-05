---
id: "pwa-manifest-customization"
title: "PWA Manifest Customization"
domain: "frontend"
category: "build"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

Customize the `public/manifest.json` file for Progressive Web App (PWA) capabilities by listing it in `.generator-ignore`. This enables setting a custom app name, display mode (standalone), theme color, and background color for the installable web app experience. Particularly useful for mobile-first applications.

## Structure

```json
{
  "short_name": "AppName",
  "name": "Full Application Name",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

Add to `.generator-ignore`:
```
public/manifest.json
```

## Examples

### Trivia
Player frontend customizes `manifest.json` with `"name": "JUDO Trivia"`, `"short_name": "Trivia"`, `"display": "standalone"`, `"theme_color": "#000000"`. Listed in `.generator-ignore` to prevent overwriting. Enables the trivia game to be installed as a PWA on mobile devices.

## Trade-offs

- **Pros**: Enables installable PWA experience; custom branding in app launcher; standalone display removes browser chrome
- **Cons**: Requires managing manifest updates manually; must coordinate with actual icons and theme colors
- **When to use**: Mobile-first applications or any app intended to be installed as a PWA

## Related Patterns

- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [custom-public-assets](custom-public-assets.md)
