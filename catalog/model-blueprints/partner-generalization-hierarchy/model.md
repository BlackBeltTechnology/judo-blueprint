## Examples

### doors-model
**Entity types (all in doors::entities package):**

- **Partner**: `doors::entities::Partner` (non-CRUD, base entity)
  - Attributes: name (req), email, phone
  - Relations: bankAccounts [0..*] COMPOSITION BankAccount, mainBankAccount [0..1] ASSOC BankAccount (bidirectional, range: self.bankAccounts), postalAddress [0..1] COMPOSITION Address
  - Operations: init (STATIC, model-defined -- seeds test OrganizationPartner instances with addresses and bank accounts)

- **CompanylikePartner**: `doors::entities::CompanylikePartner` (non-CRUD, extends Partner)
  - Additional attributes: taxNumber, euTaxNumber
  - Additional relations: hqAddress [0..1] COMPOSITION Address
  - Operations: loadNavData (INSTANCE, custom -- integrates with external company registry API, returns LoadNavDataResult TO with title and message)

- **OrganizationPartner**: `doors::entities::OrganizationPartner` (non-CRUD, extends CompanylikePartner)
  - Additional attributes: companyRegistrationNumber, representative, representativeTitle
  - Additional relations: siteAddresses [0..*] COMPOSITION Address

- **SelfEmployedPartner**: `doors::entities::SelfEmployedPartner` (non-CRUD, extends CompanylikePartner)
  - Additional attributes: registrationNumber

- **PrivatePartner**: `doors::entities::PrivatePartner` (non-CRUD, extends Partner directly)
  - Additional attributes: taxId, hisId
  - Additional relations: livingAddress [0..1] COMPOSITION Address

- **OtherPartner**: `doors::entities::OtherPartner` (non-CRUD, extends Partner directly)
  - Additional attributes: registrationNumber
  - Additional relations: address [0..1] COMPOSITION Address

**Generalization hierarchy:**
```
Partner (base)
  +-- CompanylikePartner (intermediate)
  |     +-- OrganizationPartner
  |     +-- SelfEmployedPartner
  +-- PrivatePartner
  +-- OtherPartner
```

**Enumeration:**
- `PartnerType`: FREELANCE(1), RESIDENT_ENTERPRISE(2), FOREIGN_ENTERPRISE(3), FOUNDATION(4), ORGANIZATION(5), GOVERMENT(6), OTHER(7)

**Transfer objects (in doors::actors::employee package):**
- PrivatePartner TO -- maps PrivatePartner, exposes: name (req), email, phone, taxId, hisId, partnerType, livingAddress (AGGREGATION), postalAddress (AGGREGATION), bankAccounts (AGGREGATION), mainBankAccount (AGGREGATION). Operations: createPartner (STATIC), create/delete living/postal address, add/remove bank accounts
- OrganizationPartner TO -- maps OrganizationPartner, exposes: name (req), email, phone, companyRegistrationNumber, taxNumber, euTaxNumber, representative, representativeTitle, partnerType, hqAddress (AGGREGATION), postalAddress (AGGREGATION), siteAddresses (AGGREGATION), bankAccounts (AGGREGATION), mainBankAccount (AGGREGATION). Operations: createPartner (STATIC), loadNavData, manage addresses and bank accounts
- SelfEmployedPartner TO -- maps SelfEmployedPartner, similar structure with registrationNumber
- OtherPartner TO -- maps OtherPartner, similar structure with registrationNumber
- PartnerSelect TO -- simplified view for partner selection in contract forms, exposing only name and phone
