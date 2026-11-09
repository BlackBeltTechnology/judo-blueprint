## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%ExchangeRate%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name memberType } }
    operations { items { name operationType } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ExchangeRateRecordingMethod"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ExchangeRateRecordingMethod", name: "MANUAL", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ExchangeRateRecordingMethod", name: "AUTO", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Currency",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Currency", name: "code"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Currency", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "ExchangeRate",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "rate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "rateUnit"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "recordingMethod"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "timestampOfRecording"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "source",
  target: "{{NAMESPACE}}::Currency", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "target",
  target: "{{NAMESPACE}}::Currency", lower: 1, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::ExchangeRate", name: "updateExchangeRates",
  customImplementation: true, operationType: "STATIC", binding: "{{NAMESPACE}}::ExchangeRate.updateExchangeRates"
} }) { success fqn } }
```

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
