---
id: price-margin-calculation-utilities
title: Price/Margin Calculation Utility Library
description: A frontend-only library of pure functions that convert between cost price, selling price and gross margin, shared by form hooks that fill dependent price fields.
aliases: [margin calculator, gross margin helpers]
keywords: [price, margin, gross margin, calculation, utility, library, selling price]
tags: [domain:frontend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/utils/priceCalculationHelper.ts"]
alternatives: []
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Keep the price arithmetic in one tested place. A cost price, a selling price and a gross margin depend on each other, so a change to one field must update the others. Pure functions with no UI dependency make the rule the same wherever it is used.

### Gross margin, not markup

The selling price is computed as cost divided by one minus the margin, so the margin is a share of the selling price. The inverse functions use the same rule, so the two directions agree.

### Invalid input gives no result

A margin of 100 percent or more, a zero divisor, or a missing input returns no value instead of a number. Callers then leave the dependent field empty rather than show a wrong price.

## Structure

The library is a set of pure functions in one module. It covers three conversions: cost price and margin to selling price; cost price and selling price to margin; and a time-based standard selling price, from standard minutes and an hourly rate. Results are rounded to two decimal places by default. The module has no framework import, so it can be unit tested without rendering.

## Constraints

- A margin of 100 percent or more, a zero or missing divisor, and a null or undefined input return no value.
- Each function rounds its result to a configurable number of decimal places, two by default.
- The forward and inverse functions must agree: feeding one result into the other returns the original input within floating-point tolerance.
- The library is frontend-only. The backend does not compute these values, so a backend rule that depends on them must recompute the price itself.

## Variations

- **Pure module shared by hooks.** Hooks import the functions and write results into dependent fields. This is the layout used here.
- **Backend calculation.** The same formulas run in a backend operation, so the stored price is authoritative. Use this when the price must not depend on the client.
- **Rule in the model.** The price is a derived attribute on the entity (a model expression evaluated by the platform). Use this when every reader needs the same value without a hook.

## When to use

- Several forms must keep a cost price, selling price and margin in step.
- The formulas must be tested in isolation.
- The margin definition is a gross margin, the share of the selling price.

## When to avoid

- The value must be stored and trusted by the server. Compute it in a backend operation as well.
- The rule is a markup over cost rather than a margin on selling price. Write a separate function, since the inverse differs.
- The calculation needs external data such as exchange rates. Keep that lookup in the caller.

## Related

- [[shared-service-helper-module]] — the same pattern of shared pure helpers used by custom code
- [[platform-configuration-singleton]] — a source of configurable rates when margins are stored centrally
