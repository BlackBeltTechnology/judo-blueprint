---
id: bank-account-entity
title: Bank Account Entity with Bank Reference
description: A BankAccount entity with an account number, an optional association to a reference Bank, and owned by a Partner through a composition with a main-account association.
aliases: [bank account, bank reference]
keywords: [bank, account, reference, composition, association]
tags: [domain:model, layer:model, project:doors-model, status:single-project]
category: pattern
status: single-project
projects: [doors-model]
evidence: ["doors-model:unrecorded"]
alternatives: []
fragment: bank-account-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Hold a financial account identified by its number, link it to a bank taken from a reference table, and let an owning party keep several accounts with one marked as main. The reference bank is shared; each account belongs to exactly one owner.

### Bank accounts have one owner

A BankAccount is held by a single owning entity through a composition. Only that owner can create and delete it. Several owner types can exist, but each account has one parent, so a composition never has two owners at once.

### The bank comes from a reference table

Bank is a reference entity with a name and a giro code. A BankAccount points to at most one Bank through an association. The association does not own the bank, so removing an account never removes a bank.

## Structure

The BankAccount entity has a required account number, which is its identifier. Bank has a required name and a required giro code, both identifiers. BankAccount has one optional association to Bank (0..1, association kind).

The owning entity, Partner in the fragment, holds the accounts as a composition (0..*) and designates one of them as its main account with an optional association (0..1). Other owner types (for example Company) follow the same pattern.

## Constraints

- A composition has exactly one owner. The platform validator rejects a bidirectional relation with a composition end: if the account must point back to its owner, make the owner end an aggregation and the back-pointer an association. The fragment uses a one-way composition, so it has no back-pointer.
- The main-account association should reference only the owner's own accounts. Range expressions belong to transfer-object relations, not to entity relations. Restrict the candidates with a range expression on the owner's transfer-object relation that exposes the main account, for example the owner's own accounts. Otherwise check it in the operation that sets the main account. This is common practice, not an entity-level platform rule.
- Account number, bank name and giro code are required.

## Variations

- **Owner-side main account.** The owner (an entity) holds the main account as a single association. This is the form in the fragment.
- **Bank lookup by number prefix.** An operation on BankAccount sets the bank by matching the first digits of the account number against the bank's giro code. This is application logic inside a model-defined instance operation, not a platform feature.
- **Derived bank access.** A derived member on a related entity reads the owner's main account, for example a contract that exposes its contractor's main account. The derived member is read-only.

## When to use

- A party (person or organization) keeps one or more bank accounts, and one is the default.
- Bank names and giro codes are maintained once and reused by many accounts.

## When to avoid

- An account must belong to several owners at once. A composition has one owner, so model a shared account with an association instead.
- The bank must be kept as a text value on the account. Use the reference-data pattern if bank data is managed as a list.

## Related

- [[reference-data-lookup-entity]]: the reference table pattern used for Bank
- [[contact-info-composition-cluster]]: other owned contact data held by the same owners
- [[partner-generalization-hierarchy]]: the partner hierarchy that owns bank accounts
- [[identity-account-organization-cluster]]: the organization side that also owns accounts
