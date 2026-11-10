## Overview

Interceptors cover the built-in create and update of the partner and its contacts. The custom validate and toggle operations are not covered by interceptors (platform rule: interceptors fire only on built-in operations), so they carry their own rules. All class names below are example project code, not platform API.

## Implementation Pattern

- **Create interceptor (project practice).** `preCall` checks that a headquarters is given and turns flat form attributes into a nested address payload; `postCall` sets the headquarters, billing and postal associations on the created partner and calls an address helper service for computed fields. See [[form-field-flattening]] and [[interceptor-crud-lifecycle]].
- **Update interceptor.** Validates the update and recalculates computed address fields.
- **Child create interceptors.** Contact creation (e-mail, phone, bank account) sets the primary designation after the contact exists.
- **Validate custom operation.** Clears and rewrites the error rows, aligns the billing flag on every address with the billingAddress association, resets the validity flag and updates the partner. Because it is a custom operation, no interceptor runs around it; it is called explicitly from the toggle operations of the contacts.
- **Toggle custom operation.** Reload by id, flip the active flag, update; see [[toggle-operation-pattern]].
- **Faults.** A rule violation that should stop the operation is a modeled fault (HTTP 422) declared on the operation; field errors are validation exceptions (HTTP 400). The stored error rows are a separate project pattern for showing results after a refresh.

## Examples

### rackinspect (example project code, not platform API)
- Key files: `interceptors/partner/PartnerCreateInterceptor.java`, `PartnerUpdateInterceptor.java`, `custom/.../partner/ValidateCustomImplementation.java`, `ToggleActiveCustomImplementation.java`, `common/services/AddressService.java`
- Pattern: the create interceptor builds the nested address payload from flat form fields and sets the designations in `postCall`; the validate operation synchronizes the billing flags.
- Notable: the validate operation is the shared consistency check, called from the contact toggles and create interceptors.
