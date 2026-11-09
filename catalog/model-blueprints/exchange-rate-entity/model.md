## Examples

### rackinspect
- **ExchangeRate entity**: `rackinspect::entities::ExchangeRate` (non-CRUD)
  - Attributes (10): date (req), rate (req), rateUnit (req, default: 1), recordingMethod (req), sourceOfRecording (req), timestampOfRecording (req, default: now()), sourceCode, sourceString, targetCode, targetString
  - Relations: source (1..1 ASSOC to Currency), target (1..1 ASSOC to Currency)
  - Operations: updateExchangeRates (STATIC, custom) -- fetches rates from external API
- **Currency entity**: `rackinspect::entities::Currency` (non-CRUD)
  - Attributes: code (req), name, formattedString, scale, paymentMethodForSap
- **ExchangeRateRecordingMethod enum**: `rackinspect::entities::ExchangeRateRecordingMethod` -- MANUAL(1), AUTO(2)
- User entity has operations: createExchangeRate, updateExchangeRateForDateInterval
