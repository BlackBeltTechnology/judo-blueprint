---
id: quote-lines-with-price-modifiers
title: Quote with Lines and Scoped Price Modifiers
description: A quote header that owns priced item lines and price modifier instances, where a modifier applies either to one line or to the whole quote, and the totals are derived from the lines.
aliases: [offer with items and discounts, order lines with surcharges, scoped price modifier]
keywords: [quote, offer, line, price, modifier, discount, surcharge, scope, total, derived]
tags: [domain:model, layer:model, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: []
related: [price-margin-calculation-utilities, registry-header-with-lines, draft-done-status-enum]
fragment: quote-lines-with-price-modifiers
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-09-24
last_updated: 2026-11-10
---
## Intent

Price a quote from its lines and let discounts and surcharges act at two levels. A line carries a quantity and a price. A price modifier can be attached to one line, or to the whole quote. The totals are derived, so they never drift from the lines.

### A modifier has a catalog definition and an applied instance

The modifier definition holds the name, the percentage, the kind (surcharge or discount) and the scope (line or quote). The applied instance points to a definition and carries the percentage used on this quote. A later change of the definition does not rewrite quotes that already used it.

### The scope says where an instance may sit

A modifier whose scope is line is attached to a line. A modifier whose scope is quote is attached to the quote itself. The scope enumeration is the rule that decides which owner is allowed.

## Structure

- **Quote** has a stored `status` (draft, done, accepted, rejected), a composition `lines` to many QuoteLine, a composition `modifiers` to many PriceModifierInstance, and a derived `total`.
- **QuoteLine** has an integer `quantity`, a numeric `basePrice`, a mandatory association `product` to Product, a composition `modifiers` to many PriceModifierInstance, and a derived `lineTotal` (quantity times base price).
- **PriceModifier** is the definition: `name`, `percent`, `modifierType` (surcharge or discount) and `scope` (line or quote).
- **PriceModifierInstance** has its own `percent` and a mandatory association `modifier` to the definition.
- **Product** is the reference record a line points to.

## Constraints

- Both owners compose the same instance entity. An instance belongs to exactly one owner, so the owner side is a derived back relation.
- The scope of the definition must match the owner of the instance. The model does not enforce this; check it in an interceptor on create or update.
- Derived totals are computed on read. If a stored copy of the price is needed (for example the price at the time of acceptance), add a stored attribute and fill it in an operation, because a derived value cannot be frozen.
- Apply line modifiers before quote modifiers, and state that order in the calculation so the result is the same everywhere.
- Rounding rules belong in one shared place; see [[price-margin-calculation-utilities]].

## Variations

- **Original and modified values.** Keep the first calculated price and quantity next to the current ones on the line, so a revision can show what changed.
- **Versioned quotes.** A quote can point to its previous version, so a revised quote keeps the history.
- **Item kinds.** A product type enumeration (material or service) lets modifiers and calculations treat the two kinds differently.

## When to use

- A quote or order has lines with quantities and prices.
- Discounts or surcharges apply both to single lines and to the whole document.
- Totals must always agree with the lines.

## When to avoid

- Prices are fixed and have no modifiers. A plain header with lines is enough; see [[registry-header-with-lines]].
- Modifiers apply to one level only. Drop the scope enumeration and the second composition.
- Totals have to stay unchanged after acceptance. Store the numbers in an operation instead of deriving them.

## Related

- [[price-margin-calculation-utilities]] — shared rounding and margin calculations for the totals
- [[registry-header-with-lines]] — the header and line aggregate without prices
- [[draft-done-status-enum]] — a small status enumeration like the quote status
