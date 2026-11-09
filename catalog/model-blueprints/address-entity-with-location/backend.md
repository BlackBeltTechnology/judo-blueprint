## Overview

The Address entity backend handles address creation and updates through interceptors and service classes, including computed fullAddress/addressInformation fields, flag-based designation management (headquarters, billing, postal), and parent validation after changes.

## Implementation Pattern

The `UpdateAddressCustomImplementation` delegates to a shared service which: (1) queries the linked Address via the association relation, (2) validates constraints (e.g., PostalCode-City combination), (3) computes `fullAddress` and `addressInformation` strings via a shared utility, and (4) either updates the existing Address or creates a new one linked to the parent. Address creation interceptors handle initial flag assignments (headquarters, billing, postal) by setting the corresponding association on the parent entity in a `postCall` hook. The computed `fullAddress` is built from country, postal code, city, and address information, while `addressInformation` is auto-computed from street name and optional components (building, staircase, floor, door, lot number) unless `manualAddressInformation` is set.

## Examples

### mlszksz-platform
- Key files: `custom/.../organizationadminpanel/UpdateAddressCustomImplementation.java`, `common/services/impl/OrganizationServiceImpl.java`, `common/utils/AddressUtils.java`
- Pattern: Custom operation delegates to `organizationService.updateAddress()` which implements create-or-update: queries existing address via `organizationAdminPanelDao.queryAddress()`, updates if present or creates via `organizationAdminPanelDao.createAddress()` if absent
- Validation: PostalCode-City cross-validation queries `entityPostalCodeDao.queryCities()` and checks if the selected city is in the linked list; throws INVALID_CITY_POSTAL_CODE on mismatch
- Computed fields: `AddressUtils.computeFullAddress()` and `computeAddressInformation()` build formatted strings from address components
- Notable: Registration flow (`RegistrationServiceImpl.buildAddress()`) also constructs addresses, with identifier stripping (`stripIdentifiers()`) when copying address from RegistrationRequest to Organization

### rackinspect
- Key files: `interceptors/partner/address/AddressCreateAndUpdateInterceptor.java`, `interceptors/partner/PartnerCreateInterceptor.java`, `common/services/AddressService.java`
- Pattern: `AddressCreateAndUpdateInterceptor` intercepts both create and update operations on Partner addresses; `postCall` sets headquarters/billing/postal associations on the parent Partner based on boolean flags, then delegates to `AddressService` for computed fields
- Computed fields: `AddressService.updateFullAddress()` builds `"country, postalCode city, addressInformation"` format; `autoUpdateAddressInformation()` concatenates streetName + optional components (publicPlaceCategory, number, building, staircase, floor, door, lotNumber) unless `manualAddressInformation` is true
- Notable: `PartnerCreateInterceptor.preCall()` extracts address fields from flat `form_*` attributes on the Partner input payload and restructures them into a nested Address payload before creation; `postCall` sets designation associations and calls `validate.accept(partner)`
- Three address variants (Address, CompanyAddress, UserAddress) each have separate create interceptors handling primary designation: `CompanyAddressCreateInterceptor`, `UserAddressCreateInterceptor`
