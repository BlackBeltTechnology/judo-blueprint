## Overview

The invitation with recipients pattern manifests in the React frontend through a dialog-level action hook that filters the available UserRole options in the invite user form based on the current user's role and organization context.

## Implementation Pattern

- **Dialog actions hook**: A Pandino-registered hook on the InviteUser input form dialog provides `filterRoleOptions` callback. The hook fetches `userRole` and `isAdminOrganization` from the OrganizationAdminPanel owner data, then filters the UserRole enum dropdown options.
- **Role-based invitation rules**: The hook implements a role-to-invitable-roles mapping: COMPANY_ADMIN can invite COMPANY_ADMIN/COMPANY_READER; PLATFORM_ADMIN on admin org can invite PLATFORM_ADMIN/ASSOCIATION_LEADERSHIP; PLATFORM_ADMIN on non-admin org can invite COMPANY_ADMIN/COMPANY_READER; ASSOCIATION_LEADERSHIP can invite ASSOCIATION_LEADERSHIP.
- **Container actions hook**: A secondary container-level hook is registered for the UserInvitationRequestInput form, though the actual filtering logic has been moved to the dialog-level hook which has access to ownerData.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesCompanyadminOrganizationAdminPanelOrganizationAdminPanel_View_EditInviteUserInputFormActionsHook.ts`, `custom/hooks/containers/registerServicesCompanyadminUserInvitationRequestInputContainerActionsHook.tsx`
- Pattern: The dialog hook fetches the OrganizationAdminPanel with `_mask: '{userRole,isAdminOrganization}'`, then returns a `filterRoleOptions` function that filters `EnumOption[]` based on the `INVITABLE_ROLES_BY_ROLE` mapping and the `isAdminOrganization` flag.
- Notable: The hook distinguishes between a PLATFORM_ADMIN viewing their own admin organization (can invite platform-level roles) versus viewing another company's panel (can only invite company-level roles).
