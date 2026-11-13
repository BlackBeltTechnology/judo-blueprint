---
id: partner-with-contact-details
title: Partner/Customer Entity with Contact Details Cluster
description: A Partner (customer or vendor) entity that composes several addresses, bank accounts, e-mails, phones and ratings, with association shortcuts that mark the preferred contact of each kind.
aliases: [customer entity, vendor entity, business partner contacts]
keywords: [partner, customer, contact, address, bank account, primary, validation, rating]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: [contact-info-composition-cluster, partner-generalization-hierarchy]
fragment: partner-with-contact-details
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Represent an external business partner (customer or vendor) that has many contact points: several addresses, bank accounts, e-mails and phone numbers. One of each kind can be marked as the preferred one, so the rest of the model reads a single value without scanning the list.

### Contacts are composed, preferences are associations

Contact points belong to the partner and go with it when the partner is deleted. The preferred contact of each kind (headquarters, billing and postal address, primary bank account, e-mail and phone) is a separate optional association that points at one of the composed contacts.

### Validation results are data

A custom validate operation re-checks business rules and writes the findings as composed error rows, each with a field location and a message. The UI shows them next to the fields (see frontend.md). This is project practice, not a platform feature.

## Structure

- **Partner**: name (required), active flag (required, default true), VAT ids, notes, a validity flag (default true).
- **Composed, 0..\***: addresses, bankAccounts, emailAddresses, phoneNumbers, ratings and errors (PartnerError with a field location and a message).
- **Associations, 0..1**: headquarters, billingAddress, postalAddress (to an Address), primaryBankAccount, a primary e-mail contact, a primary phone contact, and the reference data paymentMethod, currency and language.
- **Rating**: result from the RatingResult enumeration (three grades: A, B and C).
- **Operations**: a toggle for the active flag and a validate operation (see backend.md).

## Constraints

- The preferred-contact associations must point at a contact composed by the same partner. The model does not narrow the choice by itself; a range on the relation or a rule in the operation must do it (project practice).
- Deleting the partner deletes its composed contacts, ratings and error rows. It does not delete the reference data (payment method, currency, language).
- Interceptors fire only on built-in operations (create, update, delete, reference operations). The custom toggle and validate operations are not intercepted, so each checks its own rules.
- Business rule violations are modeled faults (HTTP 422) and field errors are validation exceptions (HTTP 400). The error rows are a project data pattern on top of that.

## Variations

- **Smaller partner.** Keep only addresses and one primary e-mail; see [[contact-info-composition-cluster]].
- **Company data.** A second entity with the same contact cluster for the operator's own company.
- **Subtypes.** Split by legal form instead of one flat partner; see [[partner-generalization-hierarchy]].
- **Derived list.** Expose a derived collection, for example delivery addresses, instead of another stored flag.

## When to use

- A customer or vendor has several contacts of each kind and one preferred one.
- Business rules over the contacts must be re-checked after any change.

## When to avoid

- A single address and e-mail are enough. Use plain attributes.
- The partner types have different required data. Use [[partner-generalization-hierarchy]].

## Related

- [[contact-info-composition-cluster]] — the reusable e-mail, phone and address cluster
- [[partner-generalization-hierarchy]] — partners split by legal form
- [[bank-account-entity]] — the composed bank account
- [[address-entity-with-location]] — the composed address
- [[primary-selection-pattern]] — the preferred-contact association
- [[toggle-operation-pattern]] — the active toggle
- [[form-field-flattening]] — creating the first address from flat form fields
