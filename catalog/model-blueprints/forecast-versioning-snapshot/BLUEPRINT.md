---
id: "forecast-versioning-snapshot"
title: "Forecast Versioning with Monthly Snapshot Composition"
score: 38.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - itracker
---
## Description

A versioning pattern for periodic financial forecasts where a parent entity (e.g., Initiative) maintains both current monthly forecasts and archived forecast versions. The structure has three levels:

1. **Parent entity** (e.g., Initiative) -- composes both:
   - `monthlyForecasts` (0..* COMPOSITION) -- the current/active monthly breakdown
   - `forecastVersions` (0..* COMPOSITION) -- archived snapshots of previous forecast states

2. **MonthlyForecast entity** -- represents a single month's forecast data with:
   - `month` (required) -- month identifier or label
   - `savingPotential` (required) -- projected value
   - `saving` -- actual realized value
   - `date` -- specific date reference

3. **ForecastVersion entity** -- a timestamped snapshot that captures:
   - `timestamp` (required) -- when the snapshot was taken
   - `sumOfSavingPotential` (required) -- aggregated total of projected values
   - `sumOfSaving` (required) -- aggregated total of actual values
   - `monthlyForecasts` (0..* COMPOSITION to MonthlyForecastVersion) -- the frozen monthly breakdown

4. **MonthlyForecastVersion entity** -- an immutable copy of monthly data within a version:
   - Same fields as MonthlyForecast (date, savingPotential, saving)
   - Composed by ForecastVersion, not directly by the parent

An `archiveForecast` instance operation on the parent entity triggers the snapshot: it copies the current monthly forecasts into a new ForecastVersion with their aggregated sums and a timestamp.

This pattern enables tracking how forecasts evolve over time -- comparing what was projected at different points against actual outcomes. It differs from simple entity-change-history-snapshot by maintaining structured monthly granularity within each version rather than flat attribute snapshots.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
