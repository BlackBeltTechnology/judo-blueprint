## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Partner%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Partner",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "vatId"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "active"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "logo"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "notes"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "addresses",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "bankAccounts",
  target: "{{NAMESPACE}}::BankAccount", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "emailAddresses",
  target: "{{NAMESPACE}}::EmailAddress", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "phoneNumbers",
  target: "{{NAMESPACE}}::PhoneNumber", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "headquarters",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "billingAddress",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "primaryBankAccount",
  target: "{{NAMESPACE}}::BankAccount", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "primaryContactEmail",
  target: "{{NAMESPACE}}::EmailAddress", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Partner", name: "primaryPhoneNumber",
  target: "{{NAMESPACE}}::PhoneNumber", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Partner", name: "toggleActive",
  customImplementation: true, operationType: "INSTANCE", binding: "{{NAMESPACE}}::Partner"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Partner", name: "validate",
  customImplementation: true, operationType: "INSTANCE", binding: "{{NAMESPACE}}::Partner"
} }) { success fqn } }
```

## Examples

### rackinspect
- **Entity**: `rackinspect::entities::Partner` (non-CRUD)
  - Attributes (13): name (req), active (default: true), vatId, vatIdEu, vatIdGroup, customerSAPCode, vendorSAPCode, isEszamla (default: false), notes, errorMessages, genericValid (default: true), serviceCalculationPeriod, logo
  - Composition relations (5): addresses (0..* Address), bankAccounts (0..* BankAccount), emailAddresses (0..* EmailAddress), phoneNumbers (0..* PhoneNumber), ratings (0..* Rating), partnerErrors (0..* PartnerError)
  - Association relations (8): billingAddress (0..1), headquarters (0..1), postalAddress (0..1), primaryBankAccount (0..1), primaryContactEmail (0..1), primaryEszamlaEmail (0..1), primaryPhoneNumber (0..1), paymentDeadline (0..1), paymentMethod (0..1), currency (0..1), language (0..1)
  - Derived: deliveryAddresses (0..*)
  - Operations: toggleActive, validate
- **CompanyData entity**: `rackinspect::entities::CompanyData` follows a similar pattern with companyAddresses, companyBankAccounts, companyEmails, companyPhones composed, plus headquarters, billingAddress, postalAddress, primaryAddress, primaryEmail, primaryPhone association shortcuts
