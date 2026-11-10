---
id: address-field-auto-composition
title: Address Field Auto-Composition from Components
description: "A frontend-only pattern that fills a summary address field from the individual address parts on blur, and lets the user switch the automatic fill off with a manual override flag."
aliases: [address summary field, address line auto fill, composed address text]
keywords: [address, summary, auto composition, blur, manual override, form]
tags: [domain:frontend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [address-entity-with-location]
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Keep a human-readable address line in step with the individual address parts, without asking the user to type it twice. The line is recomputed when a part loses focus. A manual override lets the user keep their own text.

### The summary follows the parts

The summary field is written from the parts only when the user has not taken manual control. Each part that changes triggers a recomputation of the summary.

### Manual override wins

A flag on the address records that the user edited the summary by hand. While the flag is set, the automatic fill does not write to the summary, so the user's text is kept.

## Structure

This is a frontend pattern with no model shape. The address entity holds the parts as attributes (street name, public place category, number, building, staircase, floor, door, lot number), a summary text attribute, and a boolean manual override flag. The UI computes the summary from the parts when a part loses focus. The model is the same as in [[address-entity-with-location]] or in any address entity that has these attributes.

## Constraints

- The summary is computed in the UI. It is not a derived attribute on the model, so the backend does not recompute it unless its own code does.
- When the manual override flag is set, the summary is not recomputed.
- Empty parts are skipped, so the summary has no doubled separators.
- The computation runs on blur, not on each keystroke. A blur handler exists on the generated container hook only for a UI field whose blur option is switched on in the UI model, so each address part field needs that option.

## Variations

- **Blur on every part.** Each part has its own blur handler that calls the same shared function. This is the reference form.
- **Recompute on save.** The summary is computed once when the form is saved. This is simpler, but the user does not see the line while editing.
- **No override.** The summary is always computed and no flag is shown. Use this when the line must never differ from the parts.

## When to use

- A form has several address parts and a single summary line is shown or stored.
- The summary is usually the parts joined, but sometimes the user must write it by hand.
- The same summary appears in forms and in view-edit sections.

## When to avoid

- The summary must be stored and searched by the server. Compute it in the backend or as a derived attribute.
- The address has only one free-text field. There is nothing to compose.
- The parts are edited in different systems with no shared form.

## Related

- [[address-entity-with-location]] — the address entity whose parts this pattern composes
- [[organization-entity]] — an owner with an address shown in forms
