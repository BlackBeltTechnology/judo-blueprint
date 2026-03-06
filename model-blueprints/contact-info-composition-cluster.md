---
id: "contact-info-composition-cluster"
title: "Contact Info Composition Cluster (Email, Phone, Address)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A set of small, composable contact information entities that are owned by a parent entity through composition: EmailAddress (email, name, active), PhoneNumber (phone, name, active, isFax), and Address (streetName, city, postalCode, building, floor, door, fullAddress, active). Each contact entity carries an `active` boolean (default: true) and toggle operations: `toggleActive` (enable/disable) and `togglePrimary` (set as primary). The parent entity (Partner, CompanyData, or User) composes multiple instances of each (0..*) and maintains a separate "primary" association (0..1) pointing to the preferred instance. A derived `container` relation (0..1) provides back-navigation to the parent. This pattern allows entities to have multiple addresses, emails, and phones with one designated as primary.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Email%" } }) {
  items { fqn name
    attributes { items { name } }
    operations { items { name } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { like: "%Phone%" } }) {
  items { fqn name
    attributes { items { name } }
    operations { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "EmailAddress",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EmailAddress", name: "email"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EmailAddress", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::EmailAddress", name: "active"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::EmailAddress", name: "toggleActive",
  customImplementation: true, operationType: "INSTANCE",
  binding: "{{NAMESPACE}}::EmailAddress.toggleActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::EmailAddress", name: "togglePrimary",
  customImplementation: true, operationType: "INSTANCE",
  binding: "{{NAMESPACE}}::EmailAddress.togglePrimary"
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "PhoneNumber",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "phone"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "active"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "isFax"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "toggleActive",
  customImplementation: true, operationType: "INSTANCE",
  binding: "{{NAMESPACE}}::PhoneNumber.toggleActive"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::PhoneNumber", name: "togglePrimary",
  customImplementation: true, operationType: "INSTANCE",
  binding: "{{NAMESPACE}}::PhoneNumber.togglePrimary"
} }) { success fqn } }
```

## Examples

### rackinspect
Three parallel sets of contact entities exist for different parent types:

**For Partner:**
- `EmailAddress` -- email (req), name, active (default: true); ops: toggleActive, togglePrimaryContact, toggleEszamla
- `PhoneNumber` -- phone (req), name, active (default: true), isFax (default: false); ops: toggleActive, togglePrimary
- `Address` -- streetName (req), city (req), postalCode (req), building, floor, door, number, fullAddress (req), active (default: true), isBilling, isDelivery, isHeadquarters, isPostal; ops: toggleActive, toggleBilling, toggleDelivery, toggleHeadquarters, togglePostal
- `BankAccount` -- accountNumber (req), bankName, active (default: true), sapId; relation: currency (1..1 ASSOC); ops: togglePrimary, toggleActive

**For CompanyData:**
- `CompanyEmail` -- email (req), name, active (default: true); ops: toggleActive, togglePrimary
- `CompanyPhone` -- phone (req), name, active (default: true), fax (default: false); ops: toggleActive, togglePrimary
- `CompanyAddress` -- same fields as Address; ops: toggleActive, toggleBilling, toggleHeadquarters, togglePostal, togglePrimary
- `CompanyBankAccounts` -- iban (req), bankName (req), swiftCode, active (default: true); relation: currency (1..1 ASSOC); ops: toggleActive

**For User:**
- `UserEmail` -- email (req), name, active (default: true), notes; ops: toggleActive, togglePrimary
- `UserPhone` -- phone (req), name, active (default: true), notes, type (default: MOBIL); ops: toggleActive, togglePrimary
- `UserAddress` -- city (req), postalCode (req), addressInformation (req), fullAddress, active (default: true), notes; ops: toggleActive, togglePrimary
