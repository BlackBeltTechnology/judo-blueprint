## Model shape

The shape is a Partner entity with six composed collections, nine optional associations and a rating enumeration.

- **Partner** has name (required), isActive (required, default true), vatId, vatIdEu, vatIdGroup, notes and isValid (default true).
- **Composed collections (0..*)**: addresses, bankAccounts, emailAddresses, phoneNumbers, ratings and errors. They are owned by the partner and deleted with it.
- **Preferred contacts (association, 0..1)**: headquarters, billingAddress and postalAddress to an Address; primaryBankAccount; primaryEmail; primaryPhone.
- **Reference data (association, 0..1)**: paymentMethod, currency and language. They outlive the partner.
- **Rating** holds a RatingResult (EXCELLENT, ACCEPTABLE, NOT_ACCEPTABLE).
- **PartnerError** holds a field location and a message, written by the validate operation.

Generated UI pages follow from the entities: View, Form and Table pages for Partner and for each contact. Keep the generated Form for the partner and embed the contact tables; customize it only for the validation display (see frontend.md).

## Structure diagram

<!-- mermaid:generated fragment=partner-with-contact-details cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class Address {
    <<Entity>>
    +String city
    +String streetName
  }
  class BankAccount {
    <<Entity>>
    +String accountNumber
  }
  class Currency {
    <<Entity>>
    +String name [1]
  }
  class EmailAddress {
    <<Entity>>
    +String email [1]
  }
  class Language {
    <<Entity>>
    +String name [1]
  }
  class Partner {
    <<Entity>>
    +String name [1]
    +Boolean isActive [1]
    +String vatId
    +String vatIdEu
    +String vatIdGroup
    +Text notes
    +Boolean isValid
  }
  class PartnerError {
    <<Entity>>
    +String location
    +String errorMessage
  }
  class PaymentMethod {
    <<Entity>>
    +String name [1]
  }
  class PhoneNumber {
    <<Entity>>
    +String number [1]
  }
  class Rating {
    <<Entity>>
    +RatingResult result [1]
  }
  class RatingResult {
    <<Enumeration>>
    EXCELLENT
    ACCEPTABLE
    NOT_ACCEPTABLE
  }
  Partner *-- "*" Address : addresses
  Partner *-- "*" BankAccount : bankAccounts
  Partner *-- "*" EmailAddress : emailAddresses
  Partner *-- "*" PartnerError : errors
  Partner *-- "*" PhoneNumber : phoneNumbers
  Partner *-- "*" Rating : ratings
  Partner --> "0..1" Address : billingAddress
  Partner --> "0..1" Address : headquarters
  Partner --> "0..1" Address : postalAddress
  Partner --> "0..1" BankAccount : primaryBankAccount
  Partner --> "0..1" Currency : currency
  Partner --> "0..1" EmailAddress : primaryEmail
  Partner --> "0..1" Language : language
  Partner --> "0..1" PaymentMethod : paymentMethod
  Partner --> "0..1" PhoneNumber : primaryPhone
  Rating ..> RatingResult : result
```
<!-- /mermaid:generated -->
