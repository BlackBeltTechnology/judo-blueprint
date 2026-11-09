---
id: "partner-generalization-hierarchy"
title: "Partner Generalization Hierarchy (Multi-Type Business Partner)"
score: 32.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - doors-model
---
## Description

A Partner entity generalization hierarchy where a base Partner entity is extended by multiple concrete subtypes representing different legal forms of business partners. The base Partner entity holds shared attributes (name, email, phone) and shared relations (bankAccounts composition, mainBankAccount association, postalAddress composition to Address). Concrete subtypes add type-specific attributes and address relations.

The hierarchy typically includes:

- **Partner** (base) -- shared attributes: name (req), email, phone. Shared relations: bankAccounts [0..*] COMPOSITION BankAccount, mainBankAccount [0..1] ASSOCIATION BankAccount (range: self.bankAccounts), postalAddress [0..1] COMPOSITION Address. Has an init operation for seeding test data.
- **CompanylikePartner** (intermediate, extends Partner) -- adds taxNumber, euTaxNumber attributes and hqAddress [0..1] COMPOSITION Address for headquarters. Has a loadNavData operation for external data integration (e.g., fetching company data from a national company registry API).
- **OrganizationPartner** (extends CompanylikePartner) -- adds companyRegistrationNumber, representative, representativeTitle attributes and siteAddresses [0..*] COMPOSITION Address for multiple site locations.
- **SelfEmployedPartner** (extends CompanylikePartner) -- adds registrationNumber attribute.
- **PrivatePartner** (extends Partner directly) -- adds taxId, hisId (health insurance social ID) attributes and livingAddress [0..1] COMPOSITION Address.
- **OtherPartner** (extends Partner directly) -- adds registrationNumber attribute and address [0..1] COMPOSITION Address.

A PartnerType enumeration classifies partners at a higher level: FREELANCE, RESIDENT_ENTERPRISE, FOREIGN_ENTERPRISE, FOUNDATION, ORGANIZATION, GOVERMENT, OTHER.

Transfer objects mirror the generalization hierarchy, with each actor seeing appropriate partner projections: the admin actor manages companies/organizations, while the employee actor works with all partner types through specialized TOs with address management operations.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
