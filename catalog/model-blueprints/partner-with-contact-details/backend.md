## Overview

The Partner entity's backend manages creation through interceptors that handle initial address setup with flag designations, validation through a custom `Validate` operation that synchronizes billing address flags, and toggle operations for the active status.

## Implementation Pattern

- `PartnerCreateInterceptor` handles Partner creation in two phases: `preCall` validates that headquarters is set and restructures flat `form_*` attributes into a nested Address payload; `postCall` sets headquarters/billing/postal associations on the created Partner and delegates to `AddressService` for computed fields
- `ValidateCustomImplementation` clears and recalculates partner errors: it synchronizes the `isBilling` flag across all addresses to match the current `billingAddress` association, resets `genericValid` to true, and updates the partner
- `ToggleActiveCustomImplementation` follows the standard toggle pattern: reload by ID, flip `active`, update
- `PartnerUpdateInterceptor` handles updates with validation and address field recalculation
- The `AddressService` (common module) provides `updateFullAddress()` and `autoUpdateAddressInformation()` for computed address fields
- Create interceptors for child contact entities (EmailAddress, PhoneNumber, BankAccount) handle primary designation after creation
- The `Validate` operation is referenced from toggle operations on child entities (Address, EmailAddress, PhoneNumber) to re-run partner-level business rules after any contact info change

## Examples

### rackinspect
- Key files: `interceptors/partner/PartnerCreateInterceptor.java`, `interceptors/partner/PartnerUpdateInterceptor.java`, `custom/.../partner/ValidateCustomImplementation.java`, `custom/.../partner/ToggleActiveCustomImplementation.java`, `interceptors/partner/address/AddressCreateAndUpdateInterceptor.java`, `interceptors/partner/emailaddress/EmailAddressCreateInterceptor.java`, `interceptors/partner/phonenumber/CreatePhoneInterceptor.java`, `common/services/AddressService.java`
- Pattern: Partner creation interceptor validates headquarters requirement, builds nested Address payload from flat form fields, sets designation associations in `postCall`; Validate operation synchronizes `isBilling` flags across all addresses to match the `billingAddress` association
- Notable: `PartnerCreateInterceptor.preCall()` transforms flat `form_*` attributes (form_city, form_streetName, etc.) into a structured `addresses` payload with Address fields -- this is the JUDO pattern for converting form-optimized TOs into entity composition structure
- The `Validate` operation acts as a cross-cutting concern: called from address toggle, email toggle, phone toggle, and create interceptors to ensure partner-level consistency after any contact info change
