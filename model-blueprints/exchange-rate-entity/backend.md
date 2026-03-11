## Overview

The ExchangeRate entity has two backend entry points: an automatic `updateExchangeRates` static operation that fetches rates from the Hungarian National Bank (MNB) API, and a manual `createExchangeRate` operation that validates and persists user-entered rates.

## Implementation Pattern

- `UpdateExchangeRatesCustomImplementation` is an OSGi `@Component` implementing the `UpdateExchangeRates` static operation interface
- It injects `CurrencyDao`, `ExchangeRateDao`, and an `ExchangeRateService` (external API client for MNB web services)
- The auto-fetch flow: (1) query all currencies except HUF, (2) check which currencies lack today's AUTO rate (or only have a MANUAL rate), (3) call `exchangeRateService.getCurrentCurrencyRates()` for absent currencies, (4) create `ExchangeRateForCreate` entries with `ExchangeRateRecordingMethod.AUTO` and source `"MNB"`
- `CreateExchangeRateCustomImplementation` handles manual entry with validation: future dates are rejected, source and target currencies must differ, rateUnit must be a positive natural number, and rate/rateRepeat must match (double-entry confirmation)
- A service-level delegate `UpdateExchangeRatesCustomImplementation` in the partner_service package simply injects and calls the entity-level implementation
- Validation uses `ExceptionUtils.createValidationResult()` to build field-level error lists, thrown as a batch via `ExceptionUtils.createValidationException()`

## Examples

### rackinspect
- Key files: `custom/.../_default_transferobjecttypes/entities/exchangerate/UpdateExchangeRatesCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/user/CreateExchangeRateCustomImplementation.java`, `custom/.../partner_service/exchangerate/UpdateExchangeRatesCustomImplementation.java`
- Pattern: Auto-fetch via MNB `ExchangeRateService` OSGi service; manual creation with multi-field validation (future date check, currency equality check, rate unit check, double-entry rate confirmation)
- Notable: Uses `TemporalUtils.dateNow()` for consistent date handling; the partner_service version is a thin delegate to the entity-level implementation to expose the same operation from a different service context
- Currency and initial exchange rate data are seeded by the `ExcelDataImporter` during initialization
