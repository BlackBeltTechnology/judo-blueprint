---
id: "toggle-active-operation"
title: "Toggle Active Boolean Operation Pattern"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A pervasive pattern where entities carry an `active` boolean attribute (default: true) and a `toggleActive` instance operation with custom implementation that flips the flag. This provides soft-enable/disable semantics without deletion. The toggle operation is an INSTANCE-type custom operation. Many entities in the same model apply this identical pattern, making it a cross-cutting concern. Some entities extend the pattern with additional toggle operations (togglePrimary, toggleBilling, toggleHeadquarters, togglePostal, toggleDelivery) for multi-flag management.

## Detection Query

```graphql
{ esm { entitytypes(limit: 100) {
  items { fqn name
    attributes { items { name defaultExpression } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities that have an `active` attribute with default "true" and a `toggleActive` operation of type INSTANCE.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "active"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "toggleActive",
  customImplementation: true, operationType: "INSTANCE",
  binding: "{{NAMESPACE}}::{{ENTITY_NAME}}.toggleActive"
} }) { success fqn } }
```

## Examples

### rackinspect
Entities with the toggleActive pattern (15 entities):
- `rackinspect::entities::Address` -- active (default: true), toggleActive + toggleBilling + toggleDelivery + toggleHeadquarters + togglePostal
- `rackinspect::entities::BankAccount` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::CompanyAddress` -- active (default: true), toggleActive + toggleBilling + toggleHeadquarters + togglePostal + togglePrimary
- `rackinspect::entities::CompanyBankAccounts` -- active (default: true), toggleActive
- `rackinspect::entities::CompanyEmail` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::CompanyPhone` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::EmailAddress` -- active (default: true), toggleActive + togglePrimaryContact + toggleEszamla
- `rackinspect::entities::Partner` -- active (default: true), toggleActive + validate
- `rackinspect::entities::PaymentDeadline` -- active (default: true), toggleActive
- `rackinspect::entities::PaymentMethod` -- active (default: true), toggleActive
- `rackinspect::entities::PhoneNumber` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::Unit` -- active (default: true), toggleActive + toggleStandaloneStorable
- `rackinspect::entities::User` -- active (default: true), toggleActive + recalculatePermissions
- `rackinspect::entities::UserAddress` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::UserEmail` -- active (default: true), toggleActive + togglePrimary
- `rackinspect::entities::UserPhone` -- active (default: true), toggleActive + togglePrimary
