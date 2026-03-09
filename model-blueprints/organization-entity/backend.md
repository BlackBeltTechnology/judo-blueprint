## Overview

The Organization entity is managed through an `OrganizationService` OSGi service that handles creation (with admin user provisioning), data updates, address management, and status transitions (suspend/reactivate). Organization creation also provisions a Keycloak user for the initial admin.

## Implementation Pattern

- `OrganizationServiceImpl` is an OSGi `@Component` injecting `OrganizationDao`, `UserDao`, `UserService`, `AddressDao`, `OrganizationAdminPanelDao`, and i18n services
- `createOrganization()` validates uniqueness of organization name and user email, creates the Organization with ACTIVE status, then delegates user creation to `UserService.createUser()` which also provisions a Keycloak account
- `updateCompanyData()` updates profile fields from an unmapped `OrganizationDataUpdate` TO, handles capability relation management (remove all then add new), and restricts organization renaming to PLATFORM_ADMIN role
- `updateAddress()` creates or updates the composed Address entity, validates PostalCode-City combinations against the reference data hierarchy, and computes `fullAddress` and `addressInformation` strings using `AddressUtils`
- `suspend()` validates the organization is ACTIVE and not the admin organization before setting SUSPENDED status
- `reactivate()` validates the organization is SUSPENDED before restoring ACTIVE status
- Custom operations: `CreateOrganizationCustomImplementation` (AdminDashboard), `UpdateComapnyDataCustomImplementation`, `UpdateAddressCustomImplementation`, `SuspendCustomImplementation`, `ActivateCustomImplementation` (OrganizationAdminPanel)

## Examples

### mlszksz-platform
- Key files: `common/services/OrganizationService.java`, `common/services/impl/OrganizationServiceImpl.java`, `custom/.../admindashboard/CreateOrganizationCustomImplementation.java`, `custom/.../organizationadminpanel/UpdateAddressCustomImplementation.java`
- Pattern: Service layer handles creation + Keycloak provisioning + address composition; address update validates PostalCode-City relationships; status transitions enforce state machine rules
- Notable: Organization creation is a compound operation (creates Organization + User + Keycloak account); address computation uses shared `AddressUtils` for consistent Hungarian-format addresses across registration and update flows
