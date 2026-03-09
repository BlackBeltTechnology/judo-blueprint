---
id: "partner-with-contact-details"
title: "Partner/Customer Entity with Contact Details Cluster"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A Partner (or Customer) entity representing an external business entity with comprehensive contact information. The partner composes multiple sub-entities for multi-valued contact data: addresses (0..*), bankAccounts (0..*), emailAddresses (0..*), phoneNumbers (0..*). Special "primary" associations point to the preferred instance of each contact type (primaryBankAccount, primaryContactEmail, primaryPhoneNumber, headquarters, billingAddress, postalAddress). The partner also carries business attributes: name, vatId, vatIdEu, active flag, logo, notes, SAP codes, and associations to payment method, payment deadline, currency, and language. A validate operation performs business rule checks. Ratings (0..*) are composed for vendor evaluation.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
