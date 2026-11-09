## Examples

### rackinspect
- **Entity**: `rackinspect::entities::Partner` (non-CRUD)
  - Attributes (13): name (req), active (default: true), vatId, vatIdEu, vatIdGroup, customerSAPCode, vendorSAPCode, isEszamla (default: false), notes, errorMessages, genericValid (default: true), serviceCalculationPeriod, logo
  - Composition relations (5): addresses (0..* Address), bankAccounts (0..* BankAccount), emailAddresses (0..* EmailAddress), phoneNumbers (0..* PhoneNumber), ratings (0..* Rating), partnerErrors (0..* PartnerError)
  - Association relations (8): billingAddress (0..1), headquarters (0..1), postalAddress (0..1), primaryBankAccount (0..1), primaryContactEmail (0..1), primaryEszamlaEmail (0..1), primaryPhoneNumber (0..1), paymentDeadline (0..1), paymentMethod (0..1), currency (0..1), language (0..1)
  - Derived: deliveryAddresses (0..*)
  - Operations: toggleActive, validate
- **CompanyData entity**: `rackinspect::entities::CompanyData` follows a similar pattern with companyAddresses, companyBankAccounts, companyEmails, companyPhones composed, plus headquarters, billingAddress, postalAddress, primaryAddress, primaryEmail, primaryPhone association shortcuts
