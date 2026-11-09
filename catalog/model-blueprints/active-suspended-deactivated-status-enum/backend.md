## Overview

The Active/Suspended/Deactivated tri-state lifecycle is enforced through custom operation classes on CompanyUser and OrganizationAdminPanel transfer objects, each delegating to UserService or OrganizationService for status validation and state transitions.

## Implementation Pattern

Each status transition (activate, suspend, deactivate) is a separate `@Component` custom operation class that injects a domain service via `@Reference`. The service layer re-queries the entity from the database, validates the current status is the expected precondition (e.g., must be SUSPENDED to activate), performs guard checks (cannot suspend the last PLATFORM_ADMIN, cannot deactivate the last COMPANY_ADMIN in an organization, cannot suspend admin organizations), sets the new status, and persists the update. All operations throw `BusinessErrorException` with i18n-sourced messages for invalid transitions. Each custom operation also logs an audit event with the previous status and user/organization context.

## Examples

### mlszksz-platform
- Key files: `custom/.../companyuser/ActivateCustomImplementation.java`, `DeactivateCustomImplementation.java`, `SuspendCustomImplementation.java`, `custom/.../organizationadminpanel/ActivateCustomImplementation.java`, `SuspendCustomImplementation.java`
- Pattern: CompanyUser operations delegate to `userService.activate()`/`suspend()`/`deactivate()`; OrganizationAdminPanel operations delegate to `organizationService.reactivate()`/`suspend()`
- Service layer: `UserServiceImpl` enforces SUSPENDED->ACTIVE (activate), ACTIVE->SUSPENDED (suspend), any->DEACTIVATED (deactivate) with "last admin" guards; `OrganizationServiceImpl` enforces ACTIVE->SUSPENDED and SUSPENDED->ACTIVE with admin-org protection
- Audit: Each operation logs via `auditLogService.log()` with action types like USER_REACTIVATED, USER_SUSPENDED, USER_DEACTIVATED, ORGANIZATION_SUSPENDED, ORGANIZATION_REACTIVATED
- Notable: Guard checks prevent platform lockout (last PLATFORM_ADMIN) and organization lockout (last COMPANY_ADMIN within an org)
