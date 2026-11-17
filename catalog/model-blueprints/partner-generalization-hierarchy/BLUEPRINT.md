---
id: partner-generalization-hierarchy
title: Partner Generalization Hierarchy (Multi-Type Business Partner)
description: An abstract Partner base entity extended by concrete subtypes for different legal forms of business partner, each with its own tax data and address relations.
aliases: [business partner hierarchy, multi-type partner, legal form subtypes]
keywords: [partner, generalization, hierarchy, subtype, abstract, legal form, address, bank account]
tags: ["domain:model", "layer:model", "project:doors-model", "status:single-project"]
category: pattern
status: single-project
projects: [doors-model]
evidence: ["doors-model:unrecorded"]
alternatives: [credential-generalization-hierarchy, post-generalization-hierarchy, partner-with-contact-details]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model business partners of different legal forms (company, self-employed person, private person, other) as one family. What every partner has is held once on a base entity. What differs by legal form is held only on the subtype that needs it.

### The base type is abstract and shared

Partner holds the shared attributes (name, email, phone, partner type) and the shared relations (bank accounts, a main bank account, a postal address). It is never created on its own. Other entities and transfer objects can refer to a partner without knowing the legal form.

### Legal-form data lives in subtypes

An intermediate type groups the company-like forms and adds tax data and a headquarters address. Concrete subtypes add what only they need, such as representative data or several site addresses.

## Structure

- **Partner** (abstract): name (required), email, phone, partnerType (PartnerType enumeration). Relations: bankAccounts (composition, 0..*), mainBankAccount (association, 0..1, chosen from the partner's own bank accounts) and postalAddress (composition, 0..1).
- **CompanyPartner** (intermediate, extends Partner): taxNumber, euTaxNumber, hqAddress (composition, 0..1).
- **OrganizationPartner** (extends CompanyPartner): registrationNumber, representative, representativeTitle, siteAddresses (composition, 0..*).
- **SelfEmployedPartner** (extends CompanyPartner): registrationNumber.
- **IndividualPartner** (extends Partner): taxId, healthInsuranceId, livingAddress (composition, 0..1).
- **OtherPartner** (extends Partner): registrationNumber, address (composition, 0..1).
- **PartnerType** enumeration: FREELANCE, RESIDENT_ENTERPRISE, FOREIGN_ENTERPRISE, FOUNDATION, ORGANIZATION, GOVERNMENT, OTHER.
- **Address** and **BankAccount** are entities owned by the partner (see [[address-entity-with-location]] and [[bank-account-entity]]).

## Constraints

- A subtype inherits every attribute and relation of its supertypes. An abstract entity cannot be used as a field type; it can only be inherited, so persisted data always sits in a concrete subtype.
- Addresses and bank accounts are composed: deleting a partner deletes them. The main bank account only points to one of the partner's own bank accounts; the model does not narrow the choice by itself, so a range expression on the relation or a rule in the operation must keep it inside the partner's own accounts.
- The partner type enumeration and the subtype are two separate facts. The model does not tie them together; creating operations must set them consistently (project practice).
- Where a transfer object maps the abstract base and is reached through an access, the platform's generated Create action offers the concrete subtypes. Otherwise each subtype gets its own transfer object, as the source project did for each actor.

## Variations

- **Per-actor transfer objects.** One transfer object per concrete subtype exposes the fields and address operations that actor needs. A small partner-select transfer object shows only name and phone for pickers.
- **External registry lookup.** The company-like type can carry a custom operation that loads company data from a national registry. Interceptors do not run for custom operations, so that operation checks its own rules.
- **Single address.** Replace the per-subtype address relations by one postal address on the base when the forms do not need separate addresses.
- **Flat alternative.** One Partner entity with a type value and optional fields, when the forms share nearly all fields.

## When to use

- Partners come in several legal forms with different required data.
- Shared data such as bank accounts and postal address must be modeled once.
- Other parts of the model must refer to any partner polymorphically.

## When to avoid

- Only one legal form exists, or the forms differ only by a label. Use a single entity with an enumeration.
- Contact details are the main concern and the partner is a flat record. See [[partner-with-contact-details]].

## Related

- [[partner-with-contact-details]] — a flat partner with composed contact data
- [[credential-generalization-hierarchy]] — another abstract base with per-kind subtypes
- [[post-generalization-hierarchy]] — a content generalization with shared base fields
- [[address-entity-with-location]] — the address entity the partner composes
- [[bank-account-entity]] — the bank account entity the partner composes
- [[generalization-base-entity]] — the underlying best practice
