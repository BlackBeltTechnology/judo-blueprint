---
id: exchange-rate-entity
title: Exchange Rate Entity with Source/Target Currency
description: "A non-CRUD ExchangeRate entity that records a conversion rate between a source and a target Currency for a date, with the recording method (manual or automatic) and the time it was recorded."
aliases: [currency rate entity, conversion rate entity]
keywords: [exchange, rate, source, target, currency, recording method, conversion]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: exchange-rate-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Keep a dated history of conversion rates between currencies, so that amounts can be converted at the rate that applied on a given day. Each rate records how it was obtained, so a manual entry and an automatically fetched rate can be told apart.

### Rates are records, not edits

The rate entity is not createable, updateable or deleteable, so the generated pages offer no create, edit or delete action. A rate is written by a dedicated custom operation (backend code can still write the entity), either a manual entry or an automatic fetch.

### Recording metadata is part of the row

Each rate stores its recording method (manual or automatic), the source it came from, and the time it was recorded. These let a reviewer see where a number came from.

## Structure

The ExchangeRate entity has a date, a rate value, a rate unit (how many units of the source currency the rate covers, default 1), a recording method, a source-of-recording text and a recording timestamp. It has two required associations to Currency: the source currency and the target currency. The Currency entity is a reference table with a code (identifier) and a name.

## Constraints

- Createable, updateable and deleteable are all false on the rate and the currency entities.
- The date, rate, rate unit, recording method, source of recording and recording timestamp are required.
- The rate unit defaults to 1.
- The recording method is one of the two enumeration values (manual or automatic).
- The source and the target currency are both required. Their code is the identifier of the currency.

## Variations

- **Automatic fetch.** A static operation fetches the current rates from an external source and writes one automatic rate per currency that lacks a rate for the day. See [[external-api-adapter-provider-pattern]] for isolating the external source behind an adapter.
- **Manual entry with confirmation.** A manual operation validates the entry and requires the rate to be typed twice. See [[sensitive-field-double-entry-verification]].
- **Denormalized currency codes.** Store the source and target currency codes and names on the rate for quick display, without a join. Keep them in step with the Currency reference.

## When to use

- Amounts in one currency must be converted at a dated rate.
- A reviewer must see whether a rate was entered by a person or fetched by a system.
- Rates for a day are fixed once recorded and a correction is a new row.

## When to avoid

- A single fixed rate that never changes. Use a constant.
- Real-time conversion for a trading system. Use a rate service with its own caching.
- Users must edit a recorded rate in place. Write a new row instead.

## Related

- [[external-api-adapter-provider-pattern]] — isolating an external rate source behind an adapter
- [[sensitive-field-double-entry-verification]] — the double-entry confirmation used for manual rates
- [[active-inactive-status-enum]] — a small fixed enumeration of the same kind as the recording method
