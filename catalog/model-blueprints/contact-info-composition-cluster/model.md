## Examples

### rackinspect
Three parallel sets of contact entities exist for different parent types:

**For Partner:**
- `EmailAddress` -- email (req), name, active (default: true); ops: toggleActive, togglePrimaryContact, toggleEszamla
- `PhoneNumber` -- phone (req), name, active (default: true), isFax (default: false); ops: toggleActive, togglePrimary
- `Address` -- streetName (req), city (req), postalCode (req), building, floor, door, number, fullAddress (req), active (default: true), isBilling, isDelivery, isHeadquarters, isPostal; ops: toggleActive, toggleBilling, toggleDelivery, toggleHeadquarters, togglePostal
- `BankAccount` -- accountNumber (req), bankName, active (default: true), sapId; relation: currency (1..1 ASSOC); ops: togglePrimary, toggleActive

**For CompanyData:**
- `CompanyEmail` -- email (req), name, active (default: true); ops: toggleActive, togglePrimary
- `CompanyPhone` -- phone (req), name, active (default: true), fax (default: false); ops: toggleActive, togglePrimary
- `CompanyAddress` -- same fields as Address; ops: toggleActive, toggleBilling, toggleHeadquarters, togglePostal, togglePrimary
- `CompanyBankAccounts` -- iban (req), bankName (req), swiftCode, active (default: true); relation: currency (1..1 ASSOC); ops: toggleActive

**For User:**
- `UserEmail` -- email (req), name, active (default: true), notes; ops: toggleActive, togglePrimary
- `UserPhone` -- phone (req), name, active (default: true), notes, type (default: MOBIL); ops: toggleActive, togglePrimary
- `UserAddress` -- city (req), postalCode (req), addressInformation (req), fullAddress, active (default: true), notes; ops: toggleActive, togglePrimary
