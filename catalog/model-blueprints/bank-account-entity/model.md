## Examples

### doors-model
**Entity types (all in doors::entities package):**

- **Bank**: `doors::entities::Bank` (non-CRUD)
  - Attributes: name (req, identifier), giroCode (req, identifier)
  - Seeded via init data with Hungarian bank names and codes (e.g., "Raiffeisen Bank Zrt." with giroCode "120")
  - Managed by admin actor via Banks access point (full CRUD on admin::Bank TO)

- **BankAccount**: `doors::entities::BankAccount` (non-CRUD)
  - Attributes: accountNumber (req, identifier)
  - Relations:
    - bank [0..1] ASSOC Bank (one-way)
    - partner [0..1] ASSOC Partner (bidirectional, tracks partner ownership)
    - ownerCompany [0..1] ASSOC Company (bidirectional, tracks company ownership)
  - Operations: validateBankAccount (INSTANCE, model-defined) -- resolves bank from account number prefix: `this.bank = Bank!filter(b | b.giroCode == this.accountNumber!first(3))!any()`

- **Owned by Partner** (`doors::entities::Partner`):
  - bankAccounts [0..*] COMPOSITION BankAccount
  - mainBankAccount [0..1] ASSOCIATION BankAccount (bidirectional, rangeExpression: self.bankAccounts)

- **Owned by Company** (`doors::entities::Company`):
  - bankAccounts [0..*] COMPOSITION BankAccount
  - mainBankAccount [0..1] ASSOCIATION BankAccount (bidirectional, rangeExpression: self.bankAccounts)

- **Derived on Contract** (derived bank account access):
  - contractorBankAccount [0..1] DERIVED (getterExpression: self.contractor.mainBankAccount)
  - partnerBankAccount [0..1] DERIVED (getterExpression: self.partner.mainBankAccount)

**Transfer objects:**
- admin::BankAccount -- accountNumber + bank/partner/ownerCompany AGGREGATION relations
- admin::Bank -- name, giroCode
- employee::BankAccount -- accountNumber, bankName (DERIVED: self.bank.name) + bank AGGREGATION
- employee::Bank -- name, giroCode
- The admin actor manages Banks directly via a dedicated access point, while bank accounts are managed through Company and Partner detail views
