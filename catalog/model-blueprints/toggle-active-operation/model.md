## Detection Query

```graphql
{ esm { entitytypes(limit: 100) {
  items { fqn name
    attributes { items { name defaultExpression } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities that have an `active` or `isActive` attribute with default "true" and a `toggleActive` or `activateToggle` operation of type INSTANCE.

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

### mlszksz-platform
Transfer objects with the activateToggle pattern (TO-level variant):
- `MLSZKSZPlatform::services::admin::City` -- isActive attribute on entity `MLSZKSZPlatform::entities::City` (req, default: true); activateToggle INSTANCE operation on the admin City TO
- `MLSZKSZPlatform::services::admin::Capability` -- isActive attribute on entity `MLSZKSZPlatform::entities::Capability` (req, default: true); activateToggle INSTANCE operation on the admin Capability TO

This project uses `isActive` (entity-level attribute) and `activateToggle` (TO-level operation) instead of `active` and `toggleActive`. The toggle operation is defined on the transfer object in the admin service package rather than on the entity itself, and is not marked as customImplementation, indicating it uses model-defined behavior to flip the isActive flag.
