---
id: bank-account-entity
title: "Bank Account Entity with Bank Reference"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - doors-model
---

## Description

A BankAccount entity representing a financial bank account with an accountNumber attribute and a reference to a Bank entity. The Bank entity serves as a lookup/reference data table with name and giroCode (bank identifier code). BankAccounts are composed by both Company and Partner entities, with a designated mainBankAccount association pointing to the primary account. The BankAccount has a validateBankAccount operation that auto-resolves the bank reference by matching the first 3 digits of the account number against the bank's giroCode.

Key structural patterns:
- BankAccount is owned via COMPOSITION by both Partner and Company entities (dual ownership)
- A mainBankAccount [0..1] ASSOCIATION with rangeExpression "self.bankAccounts" constrains selection to owned accounts
- The partner/ownerCompany bidirectional relations on BankAccount track which entity owns each account
- Bank is a simple lookup entity (name + giroCode) referenced by BankAccount via [0..1] ASSOCIATION
- The validateBankAccount operation provides auto-lookup of the Bank from the account number prefix

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%BankAccount%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
    operations { items { name } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Bank" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

Look for a BankAccount entity with an accountNumber attribute and a bank relation, alongside a Bank entity with name and giroCode.

## Creation Mutations

### Bank entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Bank",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Bank", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Bank", name: "giroCode"
} }) { success fqn } }
```

### BankAccount entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "BankAccount",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::BankAccount", name: "accountNumber"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::BankAccount", name: "bank",
  target: "{{NAMESPACE}}::Bank", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Composition from parent entities

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "bankAccounts",
  target: "{{NAMESPACE}}::BankAccount", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::{{PARENT_ENTITY}}", name: "mainBankAccount",
  target: "{{NAMESPACE}}::BankAccount", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Validate operation

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::BankAccount", name: "validateBankAccount",
  operationType: INSTANCE
} }) { success fqn } }
```

## Examples

### doors-model
**Entity types (all in doors::entities package):**

- **Bank**: `doors::entities::Bank` (non-CRUD)
  - Attributes: name (req, identifier), giroCode (req, identifier)
  - Seeded via init data with Hungarian bank names and codes (e.g., "Raiffeisen Bank Zrt." with giroCode "120")
  - Managed by admin actor via Banks access point (full CRUD on admin::Bank TO)

- **BankAccount**: `doors::entities::BankAccount` (non-CRUD)
  - Attributes: accountNumber (req, identifier)
  - Relations:
    - bank [0..1] ASSOC Bank (one-way)
    - partner [0..1] ASSOC Partner (bidirectional, tracks partner ownership)
    - ownerCompany [0..1] ASSOC Company (bidirectional, tracks company ownership)
  - Operations: validateBankAccount (INSTANCE, model-defined) -- resolves bank from account number prefix: `this.bank = Bank!filter(b | b.giroCode == this.accountNumber!first(3))!any()`

- **Owned by Partner** (`doors::entities::Partner`):
  - bankAccounts [0..*] COMPOSITION BankAccount
  - mainBankAccount [0..1] ASSOCIATION BankAccount (bidirectional, rangeExpression: self.bankAccounts)

- **Owned by Company** (`doors::entities::Company`):
  - bankAccounts [0..*] COMPOSITION BankAccount
  - mainBankAccount [0..1] ASSOCIATION BankAccount (bidirectional, rangeExpression: self.bankAccounts)

- **Derived on Contract** (derived bank account access):
  - contractorBankAccount [0..1] DERIVED (getterExpression: self.contractor.mainBankAccount)
  - partnerBankAccount [0..1] DERIVED (getterExpression: self.partner.mainBankAccount)

**Transfer objects:**
- admin::BankAccount -- accountNumber + bank/partner/ownerCompany AGGREGATION relations
- admin::Bank -- name, giroCode
- employee::BankAccount -- accountNumber, bankName (DERIVED: self.bank.name) + bank AGGREGATION
- employee::Bank -- name, giroCode
- The admin actor manages Banks directly via a dedicated access point, while bank accounts are managed through Company and Partner detail views
