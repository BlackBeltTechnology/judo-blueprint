## Overview

The contact info entities (EmailAddress, PhoneNumber, Address, BankAccount) are managed through toggle custom operations and create interceptors that handle primary designation and parent validation after changes.

## Implementation Pattern

- Each contact entity has `ToggleActiveCustomImplementation` and `TogglePrimaryCustomImplementation` (or similar) as OSGi `@Component` classes that flip the corresponding boolean and update via DAO
- Toggle operations on child entities query the parent (Partner, CompanyData, User) via `dao.queryContainer()` and call `validate.accept(parent)` to re-run business rules after the flag change
- Create interceptors (`EmailAddressCreateInterceptor`, `CreatePhoneInterceptor`, `UserAddressCreateInterceptor`, etc.) run as `postCall` hooks on the parent's `_createInstance*` operations
- The create interceptor pattern: (1) extract the newly created child entity from the return payload, (2) check input flags like `isPrimaryContact` or `isPrimary`, (3) if true, set the primary association on the parent via `parentDao.setPrimary*(parent, child)`
- Three parallel sets of contact entities exist for different parent types (Partner, CompanyData, User), each with their own interceptors and toggle operations but following the same structural pattern

## Examples

### rackinspect
- Key files: `custom/.../emailaddress/ToggleActiveCustomImplementation.java`, `custom/.../phonenumber/ToggleActiveCustomImplementation.java`, `interceptors/partner/emailaddress/EmailAddressCreateInterceptor.java`, `interceptors/partner/phonenumber/CreatePhoneInterceptor.java`, `interceptors/user/useremail/UserEmailCreateInterceptor.java`, `interceptors/user/useraddress/UserAddressCreateInterceptor.java`, `interceptors/companydata/companyaddress/CompanyAddressCreateInterceptor.java`
- Pattern: Toggle operations reload by ID, flip boolean, update, then call `validate.accept(partner)` on the parent; create interceptors extract input flags and set primary associations in `postCall`
- Notable: `EmailAddressCreateInterceptor` handles two primary designations: `isPrimaryContact` and `isEszamla` (electronic invoice email), each setting a different association on Partner
- For User contact entities, the `UserCreateInterceptor` creates the initial primary address, phone, and email in a single `postCall`, then calls `recalculatePermissions`
- `CompanyAddressCreateInterceptor` handles four designations: primary, headquarters, billing, postal -- each setting a different association on CompanyData
