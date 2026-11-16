---
id: custom-public-assets
title: "Custom Public Assets (Logos, Images, Icons)"
description: Add custom static assets (logos, backgrounds, QR codes) to the frontend public directory under unique names, and protect only the generator-owned files you override.
aliases: [branding assets, custom logo, static images]
keywords: [public, assets, logo, images, favicon, generator-ignore, applicationLogo, flutter assets]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:itracker", "project:workflow-poc", "project:indamedia-adtrack", "status:established"]
category: customization
status: established
projects: [trivia, itracker, workflow-poc, indamedia-adtrack]
evidence: ["trivia:unrecorded", "itracker:unrecorded", "workflow-poc:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: []
related: [pwa-manifest-customization, generator-ignore-app-theme]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-11
---
## Intent

Branding and static media (logos, background images, QR codes, icons) belong in the frontend `public/` directory. This entry says how to add them without fighting the generator.

## Practice

### Platform base

- `public/` of the React frontend holds static files served as-is; it also holds `i18n/` and `manifest.json` ([frontend guide: project layout](../../agent-docs/frontend/README.md)).
- Logo and icon defaults come from the actor's `applicationLogo` in the model; prefer changing the model for a permanent change. A `CustomLogoPropsHook` can instead map the default logo props (`subTitle`, `imgSrc`, `iconSrc`) to custom values, with image paths relative to `public/` ([UI hooks: logo customization](../../agent-docs/frontend/hooks/ui-hooks.md)).
- A generated file you edit by hand fails the checksum check on the next build unless it is listed in `.generator-ignore`, which stops the generator from writing it at all. `.generator-checksum-ignore` is the alternative: such files skip validation but are always regenerated ([build and deployment: checksum handling](../../agent-docs/frontend/build-and-deployment.md), [.generator-ignore](../../agent-docs/frontend/README.md)).
- Files you add to `public/` are normal tracked files; only the generated i18n and asset files there are overwritten on regeneration.

### Practice notes: unique names, ignore only overrides

- Add new assets under file names the generator does not produce (for example a background image or a QR code); these need no `.generator-ignore` entry.
- When an asset replaces a generator-produced file (a customized `manifest.json`, a replaced `logo.svg`), list that file in `.generator-ignore`. Whether a given file is generator-produced is not stated in the agent-docs: check the generated header (`G E N E R A T E D   S O U R C E`) of the file.
- Reference assets with root-relative paths (`/background.png`) from custom components or the logo hook.
- Keep image weight low; assets in `public/` are not bundled but still cost load time.
- Flutter frontends are a variant: some copy assets into each actor app through a copy rule in the generator override configuration (`flutter.yaml`) with overwrite disabled, and declare them in the Flutter asset list. The agent-docs do not cover this.

## Rationale

Unique names make the assets invisible to the generator, so nothing needs protecting; the few overridden files are explicit in `.generator-ignore`. The cost is manual management and, for overridden files, the loss of generator updates for them.

## Example

- One app: three custom assets (a sharing QR code, a full-screen dark background, a white logo variant) plus a customized, generator-ignored `manifest.json`.
- Two actor frontends use a custom `public/logo.svg` for the drawer header.
- One app has a background image in a format the generator does not produce, so no ignore entry.
- Flutter frontends: organization logos copied to every actor app via a generator-override copy rule.

## When to avoid

- A logo change that can live in the model (`applicationLogo`): change the model instead.
- Assets that must be versioned with content hashes: import them from `src/custom/` so the bundler fingerprints them.

## Related

- [[pwa-manifest-customization]] — the one `public/` file usually generator-ignored
- [[generator-ignore-app-theme]] — which generated files to protect
