---
id: cards-container-configuration-hook
title: Cards Container Configuration Hook (Custom Card Layout)
description: A frontend pattern for replacing a cards container's row rendering with custom card components through the container's generated configuration hook, keeping paging and data loading.
aliases: [custom card layout, cards container hook]
keywords: [cards, container, configuration, hook, custom, card, layout, responsive]
tags: [domain:model, layer:frontend, project:park-here, status:single-project]
category: pattern
status: single-project
projects: [park-here]
evidence: ["park-here:unrecorded"]
alternatives: [address-field-auto-composition]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Show relation data as visually rich cards instead of table rows, with icons, timelines, images and action buttons. The container keeps its paging, filtering and data loading, so only the look of each item changes.

### Only the row rendering changes

The hook replaces the card element and leaves the rest of the container alone. Paging and filtering keep working because the data still comes from the same container.

### Each container has its own generated hook

The hook interface and its key are generated for each container (platform behaviour, see the agent-docs on container hook registration). The generator also emits a scaffold `register<Component>ConfigurationHook.tsx.default` under `src/custom/hooks/components/cards/`. A project copies it without `.default`, fills it in and calls its register function from `application-customizer.tsx`. The copy is not generated, so it survives regeneration.

## Structure

The pattern is a frontend layer. A customizer registers a configuration hook for one container. The hook returns a required card element and optional toolbar, action bar, layout and pagination overrides. The card element receives a row, the column definitions, a row-click handler and the container's actions. Each card sits in a responsive grid item and calls the actions it needs.

## Constraints

- The hook key is generated per container. Take it from the container's generated `customization` module, not from a typed-in string. There is no `~/generated` barrel.
- A `.default` scaffold is not compiled. Activate it by copying it, never by editing the `.default` file, which is regenerated on every build.
- The agent-docs only state that cards containers are configured through the generated scaffold. The exact hook return shape (card element required, optional toolbar, action bar, layout, pagination) comes from the evidence of one project. Check it against the generated types of your container.
- Each card must sit in a responsive grid item, or the container lays cards out in a single column.
- Actions a row does not allow must not be rendered. The server still enforces the rule.

## Variations

- **Different card per relation.** Each container gets its own card for the same entity, when the active and past views need different layouts.
- **Toolbar for filters.** A toolbar element adds a search or filter control above the cards.
- **No pagination.** Turn off the container's pagination when a short list is shown as a fixed set of cards.

## When to use

- A relation's rows need a richer presentation than a grid can give.
- Each row has an action set that depends on the row's state.
- Time-bounded or image-based data reads better as cards.

## When to avoid

- The data is a dense list that users scan and sort. A table is better.
- The whole view must be custom, not just the rows. Use a full custom component hook instead.
- The card needs data the container does not load. Load it in the container's query instead.

## Related

- [[address-field-auto-composition]]: another per-page hook registration pattern in the frontend
- [[inline-pdf-preview-post-action]]: a post-action hook that opens a file from a container action
- [[capability-lookup-entity]]: shows the generated hook-key rule for a lookup entity's frontend
