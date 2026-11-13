---
id: model-defined-color-palette
title: Model-Defined Color Palette via ESM Actor Properties
description: Define the application color palette directly in the ESM model on actor types rather than overriding theme files in code.
aliases: []
keywords: [color palette, actor, primaryColor, theme, branding, model-driven theme]
tags: ["domain:frontend", "layer:frontend", "project:itracker", "status:single-project"]
category: theme
status: single-project
projects: [itracker]
evidence: ["itracker:unrecorded"]
alternatives: [dark-theme-override]
related: [dark-theme-override, generator-ignore-app-theme]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Set the application's brand colors in the model, on the actor, instead of editing theme files. The theme files stay fully generated, are never protected with `.generator-ignore`, and follow generator updates.

## Practice

### Platform base

- An actor type carries seven color attributes: `primaryColor`, `secondaryColor`, `textPrimaryColor`, `textSecondaryColor`, `backgroundColor`, `subtitleColor` and `paperBackgroundColor`, written as `#rrggbbaa` ([actor type attributes](../../agent-docs/model/esm_metamodel/accesspoint.md)).
- The generator renders them into the generated palette file `src/theme/palette.ts` (React). To change the app-wide brand palette, change the actor in the model rather than the file ([theming](../../agent-docs/frontend/theming.md)).
- Everything finer than the seven slots (typography, component overrides, per-card colors) is the second theming layer: sub-theme hooks and theme override fragments ([theming](../../agent-docs/frontend/theming.md), [extension points](../../agent-docs/frontend/extension-points.md)).
- Code under `src/custom/` is not generated and needs no ignore entry; a file in the generated theme folder does.

### Practice notes: palette in the model only

This is practice, not an extra platform feature.

- Give each human actor the same brand palette (same seven values) so every client looks alike.
- Leave all theme files generated. Add no theme entry to `.generator-ignore`.
- Treat the seven slots as the limit. Reach for [[generator-ignore-app-theme]] or [[dark-theme-override]] only when branding needs more than they offer.
- Because the palette is data in the model, a rebrand is one model change plus regeneration.

## Rationale

One source of truth: the model. Nothing to merge on generator upgrades, and no stale copy of a theme file. The cost is the fixed set of seven colors: no component-level overrides, no custom CSS variables and no dark-mode toggle from the model alone.

## Example

Two actors in one app share the same palette: dark navy primary, orange-red secondary, near-black text and an off-white background; all theme files remain generated. Another app does the same for its admin and manager actors, and a Flutter client shares one palette across its actors, which the generator encodes into the Flutter theme.

## When to avoid

- Branding needs typography, spacing, per-component styling or a dark theme: use sub-themes or a protected theme file ([[generator-ignore-app-theme]], [[dark-theme-override]]).
- Different actors need different palettes only for single widgets: use sub-themes.

## Related

- [[dark-theme-override]] — a dark palette that the seven model colors cannot express
- [[generator-ignore-app-theme]] — protecting a hand-edited theme file instead
