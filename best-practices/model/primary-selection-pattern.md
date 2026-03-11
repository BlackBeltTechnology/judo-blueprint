---
id: "primary-selection-pattern"
title: "Primary Selection Pattern for Collection Items"
domain: "model"
category: "operation"
score: 73.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - judo-partner
---
## Description

When an entity owns a collection of child items (e.g., addresses, phone numbers, email addresses), one item can be designated as the "primary" or default entry. The parent entity holds an association reference to the primary item (e.g., `Partner.primaryBankAccount`), and the child entity exposes a `togglePrimary` or `setAsPrimary` operation that updates the parent reference. This enforces single-primary semantics.

## Structure

- Parent entity has a collection composition: `children -> ChildType [0..*]`
- Parent entity has a single association: `primaryChild -> ChildType [0..1]` (or a derived relation filtering by `isPrimary`)
- Child entity has a `togglePrimary` or `setAsPrimary` instance operation
- The operation sets the parent's primary reference to `this` (or clears it)
- Only one item in the collection can be primary at a time
- Variant: Child entity stores an `isPrimary: Boolean` flag, and the parent has a derived relation filtering by `isPrimary`

## Examples

### RackInspect
`Partner` has `bankAccounts [0..*]` (composition) and `primaryBankAccount [0..1]` (association). `BankAccount.togglePrimary` updates the partner's reference. Same pattern for: `Partner.primaryContactEmail`/`primaryEszamlaEmail`/`primaryPhoneNumber`, `User.primaryUserAddress`/`primaryUserEmail`/`primaryUserPhone`, `CompanyData.primaryAddress`/`primaryEmail`/`primaryPhone`.

### judo-partner
`Partner.addresses [0..*]` (composition) with `Partner.primaryAddress [0..1]` (derived). `Address.isPrimary: Boolean` flag with `Address.setAsPrimary` operation. Same for contacts: `Partner.contacts [0..*]` with `Partner.primaryContact [0..1]` (derived) and `Contact.isPrimary` + `Contact.setAsPrimary`. The derived relations filter the collection by the `isPrimary` flag.

## Trade-offs

- Pros: Clean single-primary enforcement, parent always knows its default item, toggle operation handles mutual exclusivity
- Cons: Requires both a collection and a single reference on the parent, toggle logic must clear previous primary
- Prefer when: A collection of contact information or addresses needs a designated default entry

## Related Patterns

- [toggle-operation-pattern](toggle-operation-pattern.md)
- [composition-ownership](composition-ownership.md)
