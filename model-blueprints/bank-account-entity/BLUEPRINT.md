---
id: "bank-account-entity"
title: "Bank Account Entity with Bank Reference"
score: 32.0
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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
