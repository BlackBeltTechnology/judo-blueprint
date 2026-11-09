## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Partner%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
    generalizations { items { fqn } }
  }
} } }
```

Look for a Partner entity with subtypes that have generalizations pointing to it, and a PartnerType enum.

## Creation Mutations

### Partner base entity

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
  container: "{{NAMESPACE}}::Partner", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Partner", name: "phone"
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
  container: "{{NAMESPACE}}::Partner", name: "postalAddress",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### CompanylikePartner (intermediate subtype)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "CompanylikePartner",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::CompanylikePartner",
  target: "{{NAMESPACE}}::Partner"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::CompanylikePartner", name: "taxNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::CompanylikePartner", name: "euTaxNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::CompanylikePartner", name: "hqAddress",
  target: "{{NAMESPACE}}::Address", lower: 0, upper: 1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### OrganizationPartner (extends CompanylikePartner)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "OrganizationPartner",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::OrganizationPartner",
  target: "{{NAMESPACE}}::CompanylikePartner"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationPartner", name: "companyRegistrationNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::OrganizationPartner", name: "representative"
} }) { success fqn } }
```

### PrivatePartner (extends Partner)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "PrivatePartner",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::PrivatePartner",
  target: "{{NAMESPACE}}::Partner"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PrivatePartner", name: "taxId"
} }) { success fqn } }
```

### PartnerType enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "PartnerType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PartnerType", name: "FREELANCE", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PartnerType", name: "RESIDENT_ENTERPRISE", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::PartnerType", name: "FOREIGN_ENTERPRISE", ordinal: 3
} }) { success fqn } }
```

## Examples

### doors-model
**Entity types (all in doors::entities package):**

- **Partner**: `doors::entities::Partner` (non-CRUD, base entity)
  - Attributes: name (req), email, phone
  - Relations: bankAccounts [0..*] COMPOSITION BankAccount, mainBankAccount [0..1] ASSOC BankAccount (bidirectional, range: self.bankAccounts), postalAddress [0..1] COMPOSITION Address
  - Operations: init (STATIC, model-defined -- seeds test OrganizationPartner instances with addresses and bank accounts)

- **CompanylikePartner**: `doors::entities::CompanylikePartner` (non-CRUD, extends Partner)
  - Additional attributes: taxNumber, euTaxNumber
  - Additional relations: hqAddress [0..1] COMPOSITION Address
  - Operations: loadNavData (INSTANCE, custom -- integrates with external company registry API, returns LoadNavDataResult TO with title and message)

- **OrganizationPartner**: `doors::entities::OrganizationPartner` (non-CRUD, extends CompanylikePartner)
  - Additional attributes: companyRegistrationNumber, representative, representativeTitle
  - Additional relations: siteAddresses [0..*] COMPOSITION Address

- **SelfEmployedPartner**: `doors::entities::SelfEmployedPartner` (non-CRUD, extends CompanylikePartner)
  - Additional attributes: registrationNumber

- **PrivatePartner**: `doors::entities::PrivatePartner` (non-CRUD, extends Partner directly)
  - Additional attributes: taxId, hisId
  - Additional relations: livingAddress [0..1] COMPOSITION Address

- **OtherPartner**: `doors::entities::OtherPartner` (non-CRUD, extends Partner directly)
  - Additional attributes: registrationNumber
  - Additional relations: address [0..1] COMPOSITION Address

**Generalization hierarchy:**
```
Partner (base)
  +-- CompanylikePartner (intermediate)
  |     +-- OrganizationPartner
  |     +-- SelfEmployedPartner
  +-- PrivatePartner
  +-- OtherPartner
```

**Enumeration:**
- `PartnerType`: FREELANCE(1), RESIDENT_ENTERPRISE(2), FOREIGN_ENTERPRISE(3), FOUNDATION(4), ORGANIZATION(5), GOVERMENT(6), OTHER(7)

**Transfer objects (in doors::actors::employee package):**
- PrivatePartner TO -- maps PrivatePartner, exposes: name (req), email, phone, taxId, hisId, partnerType, livingAddress (AGGREGATION), postalAddress (AGGREGATION), bankAccounts (AGGREGATION), mainBankAccount (AGGREGATION). Operations: createPartner (STATIC), create/delete living/postal address, add/remove bank accounts
- OrganizationPartner TO -- maps OrganizationPartner, exposes: name (req), email, phone, companyRegistrationNumber, taxNumber, euTaxNumber, representative, representativeTitle, partnerType, hqAddress (AGGREGATION), postalAddress (AGGREGATION), siteAddresses (AGGREGATION), bankAccounts (AGGREGATION), mainBankAccount (AGGREGATION). Operations: createPartner (STATIC), loadNavData, manage addresses and bank accounts
- SelfEmployedPartner TO -- maps SelfEmployedPartner, similar structure with registrationNumber
- OtherPartner TO -- maps OtherPartner, similar structure with registrationNumber
- PartnerSelect TO -- simplified view for partner selection in contract forms, exposing only name and phone
