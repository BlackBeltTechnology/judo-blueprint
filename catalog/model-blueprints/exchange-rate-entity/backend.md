## Backend guidance

### Two write paths, one rule set

A rate is written in one of two ways: a manual operation for a person's entry, and a static operation that fetches rates from an external source. Both write the same row, so both must enforce the same rules: no future date, source and target currencies differ, rate unit is a positive whole number.

### Validate field errors with the attribute name

A field problem (a future date, the same currency on both sides, a zero rate unit) is a validation error with the attribute as its location. This lets the form show it under the field. Anything that is not about one field is a business fault with a code and a message. See the Part B pattern in the problems doc.

### External failures are business errors, not 500s

The automatic fetch depends on an external service. When that service is down, or returns no rate for a currency, do not let a raw runtime exception escape: the user would see a 500. Wrap the failure in the business fault declared on the operation, with a code such as `EXCHANGE_RATE_SOURCE_UNAVAILABLE`, and log the cause. Then the user gets a clear message and the transaction rolls back cleanly.

### Fetch only what is missing

Before the fetch, query the currencies that lack an automatic rate for the day. A currency with only a manual rate for the day still needs an automatic one, because the automatic row is the source of record. Write one automatic row per missing currency.

### Keep the fetch behind a service

Call the external source through a service interface, not directly in the operation. The operation then depends on the interface, and the client can be replaced in tests. See [[external-api-adapter-provider-pattern]].

### Project code, not platform API

The example project uses its own helpers for building validation results and business errors, and its own date utility. These are project code. Copy the pattern, not the names.

## Examples

### rackinspect

- The automatic fetch is a static operation with a custom implementation. It queries the currencies except the base currency, finds the ones without a current automatic rate, asks the external rate service for those, and writes the rates as automatic.
- The manual entry operation validates the date, the currency pair and the rate unit before it writes the row.
- A second operation delegates to the same implementation, so the same rule is reachable from another service context.
- Currencies and the initial rates are seeded during initialization.
