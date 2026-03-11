## Overview

The toggleActive operation (and its siblings togglePrimary, toggleBilling, etc.) is implemented as custom operation classes on each entity, each flipping the corresponding boolean flag via the entity DAO and optionally triggering validation on the parent.

## Implementation Pattern

- Each `ToggleActiveCustomImplementation` class is an OSGi `@Component` implementing the generated `ToggleActive` interface for the specific entity
- The implementation follows a consistent three-step pattern: (1) reload the entity by ID, (2) flip the boolean via `setActive(!getActive())`, (3) update via DAO
- For child entities (Address, PhoneNumber, EmailAddress), the toggle additionally queries the parent (Partner) via `dao.queryContainer()` and calls `validate.accept(partner)` to re-run business rules
- Additional toggle operations (togglePrimary, toggleBilling, toggleHeadquarters, togglePostal, toggleDelivery) follow the same pattern but flip different flags
- A shared `Validate` custom operation is injected via `@Reference` when parent validation is needed after toggling
- Variant: User.toggleActive includes a safety check preventing deactivation of the current user (via `VariableResolver` to resolve the actor email) and validates that at least one user with ROLES and USERS permission remains active

## Examples

### mlszksz-platform
- Key files: `custom/.../admin/capability/ActivateToggleCustomImplementation.java`, `custom/.../admin/city/ActivateToggleCustomImplementation.java`, `common/services/MasterDataService.java`
- Pattern: Thin custom operation delegates to `MasterDataService.toggleCapabilityActive()` / `MasterDataService.toggleCityActive()`; service queries entity, flips `isActive`, calls `dao.update()`
- Notable: Both City and Capability share the same `MasterDataService` and follow an identical toggle pattern; the operation name `activateToggle` (TO-level) maps to `isActive` (entity-level)

### rackinspect
- Key files: `custom/.../_default_transferobjecttypes/entities/address/ToggleActiveCustomImplementation.java`, `custom/.../partner/ToggleActiveCustomImplementation.java`, `custom/.../user/ToggleActiveCustomImplementation.java`, and 13+ more across address, bankaccount, emailaddress, phonenumber, unit, paymentdeadline, paymentmethod, companyaddress, companyemail, companyphone, useraddress, useremail, userphone packages
- Pattern: Each entity has its own `ToggleActiveCustomImplementation` -- reload by ID, flip `active`, update via DAO with mask; child entities also call `validate.accept(partner)` on the parent
- Notable: 15+ entities implement `toggleActive` plus additional toggles: `togglePrimary`, `toggleBilling`, `toggleDelivery`, `toggleHeadquarters`, `togglePostal`, `toggleEszamla`, `toggleStandaloneStorable`
- Safety: `User.toggleActive` uses `VariableResolver` to prevent self-deactivation and `RoleAndUserValidationDao` to ensure at least one user retains ROLES and USERS permissions
