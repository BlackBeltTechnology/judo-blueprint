---
id: pwa-manifest-customization
title: PWA Manifest Customization
description: "Take over the generated public/manifest.json through .generator-ignore to set the installable web app name, display mode and colors; trivia uses it for a mobile-first player frontend."
aliases: [PWA manifest override, installable web app manifest]
keywords: [pwa, manifest.json, generator-ignore, standalone, display, theme color, background color, installable, mobile first, checksum]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: build
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [generator-ignore-app-theme, custom-public-assets]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Make a mobile-first frontend installable with its own name and look by owning `public/manifest.json` instead of the generated one.

## Practice

### Platform base

- The frontend module ships a generated `public/manifest.json` ([project structure](../../agent-docs/frontend/README.md)). Generated files are protected by a checksum: an edited generated file fails the build unless it is listed in `.generator-ignore`, which works like `.gitignore`; files not listed are regenerated on the next build ([checksum protection and .generator-ignore](../../agent-docs/frontend/README.md), [surviving regeneration](../../agent-docs/deployment/generator-plugins.md)).
- The platform docs do not describe the manifest content or PWA behaviour (service worker, install prompts); the content below is project practice.

### Project practice: own the manifest (trivia)

- Add `public/manifest.json` to `.generator-ignore`, then edit it. The edit is lost on regeneration if the entry is missing, and the build fails on the checksum before that.
- Set `name` and `short_name` (app launcher label), `display: standalone` (no browser chrome), `theme_color` and `background_color`.
- Keep the values in line with the real icons and the frontend theme; the file is now maintained by hand, so check it after generator upgrades for fields the template added.
- This file is usually the only `public/` file that needs ignoring; other assets are simply added ([[custom-public-assets]]).

## Rationale

An installable app needs its own name and colors. Ignoring the file is cheap, but its updates become manual.

## Example

trivia: the player frontend sets the app name to "JUDO Trivia", short name "Trivia", standalone display and a black theme color, and lists `public/manifest.json` in `.generator-ignore`, so the game can be installed on phones.

## When to avoid

- The application is used only in a desktop browser and the generated defaults are fine.
- You only need a theme change; the theme has its own override ([[generator-ignore-app-theme]]).

## Related

- [[generator-ignore-app-theme]] — the same ignore mechanism for the theme file
- [[custom-public-assets]] — other files in `public/`
