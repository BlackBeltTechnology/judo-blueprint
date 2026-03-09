---
id: "exchange-rate-entity"
title: "Exchange Rate Entity with Source/Target Currency"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

An ExchangeRate entity that records currency conversion rates between a source and target Currency. It stores the rate value, rateUnit (how many units of source currency, typically 1), the date the rate applies to, and metadata about how the rate was recorded: recordingMethod (MANUAL or AUTO enum), sourceOfRecording (external API or manual entry), and timestampOfRecording (default: now()). Denormalized sourceCode/sourceString and targetCode/targetString provide quick display without joining to Currency. A static `updateExchangeRates` operation with custom implementation fetches rates from an external source. The Currency entity is a reference table with code, name, scale, and formattedString attributes.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
